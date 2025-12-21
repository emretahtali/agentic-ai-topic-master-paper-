from fastmcp import FastMCP

mcp = FastMCP(name="MCPTestServer")


@mcp.tool
def get_account_balance() -> str:
    """
    Tool: get_account_balance
    Description: Retrieves the current account balance.
    Parameters: None
    Returns:
        str: A string showing the account balance
             (e.g., "Hesap bakiyeniz: 12.500 TL").
    """
    return "Hesap bakiyeniz: 12.500 TL"


@mcp.tool
def make_money_transaction(recipient: str, amount: str) -> str:
    """
    Tool: make_money_transaction
    Description: Sends money to a specified recipient.
    Parameters:
        recipient (str): The recipient of the money (e.g., "Ayşe").
        amount (str): The amount to send (e.g., "500 TL").
    Returns:
        str: A confirmation string of the transaction
             (e.g., "Ayşe kişisine 500 TL gönderildi.").
    """
    return f"{recipient} kişisine {amount} gönderildi."


@mcp.tool
def get_credit_card_debt() -> str:
    """
    Tool: get_credit_card_debt
    Description: Retrieves the current outstanding credit card debt.
    Parameters: None
    Returns:
        str: A string showing the credit card debt
             (e.g., "Kredi kartı borcunuz: 3.200 TL").
    """
    return "Kredi kartı borcunuz: 3.200 TL"


if __name__ == "__main__":
    print("Server başladı")
    mcp.run(
        transport="stdio",
        host="0.0.0.0",
        port=8000
    )
