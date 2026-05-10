import yfinance as yf

def get_stock_data(symbol, period="1mo"):
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period=period)

        if data.empty:
            return None

        info = stock.info
        current_price = info.get("currentPrice", "N/A")
        name = info.get("longName", "N/A")

        return {
            "data": data,
            "price": current_price,
            "name": name
        }

    except Exception:
        return None
    