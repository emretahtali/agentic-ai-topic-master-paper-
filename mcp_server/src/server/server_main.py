import os
import multiprocessing
from dotenv import load_dotenv, find_dotenv
from loguru import logger

from server.mcp_server import MCPServer
from tools import AppointmentTools

load_dotenv(find_dotenv())


def start_appointment_mcp():
    load_dotenv(find_dotenv())

    SERVER_NAME = "appointment_server"
    port = int(os.getenv(f"{SERVER_NAME.upper()}_PORT", 8081))
    host = "0.0.0.0"

    logger.info(f"Running Appointment MCP Server (Port: {port}, host:{host})")
    server = MCPServer(SERVER_NAME)
    server.register_tools(tool_instances=[AppointmentTools()])
    server.run(transport="sse", host=host, port=port)


def start_diagnosis_mcp():
    load_dotenv(find_dotenv())

    SERVER_NAME = "diagnosis_server"
    port = int(os.getenv(f"{SERVER_NAME.upper()}_PORT", 8080))
    host = "0.0.0.0"

    logger.info(f"Running Diagnosis MCP Server (Port: {port}, host:{host})")
    server = MCPServer(SERVER_NAME)
    # TODO: Tools class will be given
    server.register_tools(tool_instances=[])
    server.run(transport="sse", host=host, port=port)

def main():
    p1 = multiprocessing.Process(target=start_appointment_mcp)
    p2 = multiprocessing.Process(target=start_diagnosis_mcp)

    p1.start()
    p2.start()


if __name__ == "__main__":
    main()