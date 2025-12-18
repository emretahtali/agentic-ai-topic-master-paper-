from typing import Optional
from fastapi import FastAPI, WebSocket, Depends, Header, HTTPException
from .assistant_service import AssistantService
from .invoke_body import InvokeBody


class APIServer:
    """
    Wraps FastAPI and wires routes to a provided AssistantService.
    """

    def __init__(self, *, service: AssistantService, api_key: str):
        self._service = service
        self._api_key = api_key
        self._app = FastAPI()

        # Lifecycle hooks
        self._app.add_event_handler("startup", self._on_startup)

        # Routes
        self._define_routes()

    # Expose FastAPI app
    @property
    def app(self) -> FastAPI:
        return self._app

    # ----- lifecycle -----

    async def _on_startup(self) -> None:
        await self._service.startup()

    # ----- auth dependency -----

    async def _auth(self, authorization: Optional[str] = Header(None)) -> None:
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(401, "Missing/invalid Authorization header")

        token = authorization.split("Bearer ", 1)[1]
        if token != self._api_key:
            raise HTTPException(403, f"Authorization failed, invalid API key: {token}")

    # ----- routes -----

    def _define_routes(self) -> None:
        app = self._app
        service = self._service
        auth_dep = Depends(self._auth)

        @app.get("/healthz")
        def healthz():
            return {"ok": True}

        @app.post("/invoke")
        async def invoke(body: InvokeBody, _=auth_dep):
            """
            Conventional, non-streaming turn:
            - send only the new user message
            - include thread_id and client_turn_id
            """
            return await service.invoke(
                thread_id=body.thread_id,
                input_payload=body.input,
                client_turn_id=body.client_turn_id,
            )

        @app.websocket("/stream")
        async def stream(websocket: WebSocket):
            """
            Streaming:
              - Client connects with ?token=API_KEY
              - First frame: {"thread_id":"...", "input":{"message":"..."}}
            """
            await websocket.accept()
            if websocket.query_params.get("token") != self._api_key:
                await websocket.close(code=4403, reason="Authorization failed, invalid API key")
                return

            try:
                first = await websocket.receive_json()
                thread_id = first.get("thread_id")
                user_text = (first.get("input") or {}).get("message")
                if not thread_id or not user_text:
                    await websocket.close(code=4400, reason="Missing thread_id or input.message")
                    return

                async for event in service.stream(thread_id=thread_id, user_text=user_text):
                    await websocket.send_json(event)

                await websocket.send_json({"event": "complete"})

            except Exception as e:
                await websocket.send_json({"event": "error", "message": str(e)})

            finally:
                await websocket.close()
