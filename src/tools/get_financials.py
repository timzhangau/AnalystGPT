# src/tools/get_financials.py
# A tool function that returns fundamentals for a given ticker from a mock dictionary.

# Mock data
COMPANY_DATA = {
    "AAPL": {
        "overview": (
            "Apple Inc. is an American multinational technology company "
            "specializing in consumer electronics, software, and online services."
        ),
        "fundamentals": {
            "EPS": 6.05,
            "PE": 28.4,
            "revenue": 394.3,
            "revenue_unit": "USD (billions)",
        },
    }
    # Add more mock tickers as you like
}


def get_financials(input_ticker: str) -> str:
    """
    Get financial data for a given stock ticker (mock).
    This function can be recognized as a tool by the ReAct agent.
    """
    ticker = input_ticker.strip(" '\"").upper()
    data = COMPANY_DATA.get(ticker)
    if not data:
        return f"No data found for ticker '{ticker}'."

    f = data["fundamentals"]
    overview = data["overview"]
    return (
        f"**Company:** {ticker}\n"
        f"**Overview:** {overview}\n\n"
        f"**EPS:** {f['EPS']}\n"
        f"**P/E Ratio:** {f['PE']}\n"
        f"**Revenue:** {f['revenue']} {f['revenue_unit']}\n"
    )
