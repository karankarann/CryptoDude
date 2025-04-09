```python
# tools.py

import requests
import datetime
import math
import config

# Utility: small mapping for common crypto symbols to CoinGecko IDs
_SYMBOL_TO_COINGECKO_ID = {
    "btc": "bitcoin",
    "eth": "ethereum",
    "ada": "cardano",
    "xrp": "ripple",
    "ltc": "litecoin",
    "doge": "dogecoin",
    # add more as needed
}

def get_crypto_price(query: str) -> str:
    """
    Fetch the current price of a cryptocurrency in a specified currency (default USD).
    query: a string like "BTC" or "BTC,EUR" or "bitcoin usd".
    """
    try:
        # Parse input for coin and currency
        query = query.strip()
        if not query:
            return "Error: No cryptocurrency specified."
        # Allow formats: "COIN SYMBOL, CURRENCY" or "COIN SYMBOL CURRENCY"
        if "," in query:
            parts = [p.strip() for p in query.split(",", 1)]
        else:
            parts = query.split()
        coin_input = parts[0]
        currency = (parts[1] if len(parts) > 1 else config.DEFAULT_CRYPTO_CURRENCY)
        coin_input = coin_input.strip().lower()
        currency = currency.strip().lower()

        # Convert coin input to CoinGecko ID if necessary
        coin_id = _SYMBOL_TO_COINGECKO_ID.get(coin_input, coin_input.lower())
        # Construct API URL
        url = (f"https://api.coingecko.com/api/v3/simple/price"
               f"?ids={coin_id}&vs_currencies={currency}")
        if config.COINGECKO_API_KEY:
            # If API key is provided, include it (for CoinGecko Pro, if applicable)
            url += f"&x_cg_pro_api_key={config.COINGECKO_API_KEY}"
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return f"Error: Failed to fetch price for {coin_input.upper()}."
        data = response.json()
        if coin_id not in data or currency not in data[coin_id]:
            return f"Sorry, I couldn't find price data for '{coin_input}'."
        price = data[coin_id][currency]
        # Format the price with appropriate formatting (no too many decimals for large numbers)
        if price is None:
            return f"Price data for {coin_input.upper()} is not available."
        price_str = f"{price:,.4f}" if price < 1 else f"{price:,.2f}"
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"The current price of {coin_input.capitalize()} is {price_str} {currency.upper()} (as of {timestamp})."
    except Exception as e:
        return f"Error retrieving crypto price: {e}"

def get_forex_rate(query: str) -> str:
    """
    Fetch the current exchange rate for a forex pair.
    query: string like "EUR/USD" or "EUR USD" or "EUR,USD".
    """
    try:
        # Parse input to get base and quote currency
        query = query.strip().upper()
        if not query:
            return "Error: No currency pair specified."
        base = ""
        quote = ""
        if "/" in query:
            base, quote = query.split("/", 1)
        elif "," in query:
            base, quote = [p.strip() for p in query.split(",", 1)]
        elif " " in query:
            parts = query.split()
            base, quote = parts[0], parts[1] if len(parts) > 1 else ""
        else:
            return "Please provide a currency pair (e.g. EUR/USD)."
        base = base.strip()
        quote = quote.strip()
        if not base or not quote:
            return "Please provide both currencies for the forex pair."

        # Call Alpha Vantage currency exchange rate API
        url = (f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE"
               f"&from_currency={base}&to_currency={quote}&apikey={config.ALPHA_VANTAGE_API_KEY}")
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return "Error: Failed to fetch forex rate."
        data = response.json()
        if "Realtime Currency Exchange Rate" not in data:
            # Handle error messages or empty responses
            if "Note" in data:
                # Rate limit or other note from API
                return "API limit reached or service unavailable. Please try again later."
            else:
                return f"Could not retrieve exchange rate for {base}/{quote}."
        rate_info = data["Realtime Currency Exchange Rate"]
        rate = rate_info.get("5. Exchange Rate")
        last_update = rate_info.get("6. Last Refreshed")
        if not rate:
            return f"Exchange rate for {base}/{quote} not found."
        try:
            rate_val = float(rate)
            rate_str = f"{rate_val:,.6f}"  # format to 6 decimal places
        except:
            rate_str = rate
        if last_update:
            # last_update is typically in format "2023-12-01 14:30:00"
            return f"1 {base} = {rate_str} {quote} (Last updated: {last_update} UTC)."
        else:
            return f"1 {base} = {rate_str} {quote} (Realtime from Alpha Vantage)."
    except Exception as e:
        return f"Error retrieving forex rate: {e}"

def get_rsi(query: str) -> str:
    """
    Calculate the RSI (Relative Strength Index) for a given asset (crypto or forex).
    query: e.g. "BTC" or "BTC,14" or "EUR/USD,14" – asset and optional period (default 14).
    """
    try:
        query = query.strip()
        if not query:
            return "Error: No asset provided for RSI calculation."
        # Default period
        period = config.DEFAULT_RSI_PERIOD
        asset = query
        # If the query includes a comma or space, it might have a period or pair
        if "," in query:
            parts = [p.strip() for p in query.split(",", 1)]
            asset = parts[0]
            if len(parts) > 1:
                try:
                    period = int(parts[1])
                } except:
                    # If not an integer, ignore and use default
                    period = config.DEFAULT_RSI_PERIOD
        elif " " in query:
            parts = query.split()
            # If last part is a number, assume it's the period
            if parts and parts[-1].isdigit():
                asset = " ".join(parts[:-1])
                period = int(parts[-1])
            else:
                asset = query
        
        asset = asset.strip()
        if not asset:
            return "Error: Asset symbol or pair is required for RSI."
        asset_upper = asset.upper()
        # Determine if this is a crypto or a forex pair
        if "/" in asset:
            # Forex pair (e.g. "EUR/USD")
            base, quote = asset_upper.split("/", 1)
            # Fetch daily FX prices from Alpha Vantage
            url = (f"https://www.alphavantage.co/query?function=FX_DAILY"
                   f"&from_symbol={base}&to_symbol={quote}&outputsize=compact"
                   f"&apikey={config.ALPHA_VANTAGE_API_KEY}")
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                return "Error: Failed to fetch historical FX data."
            data = response.json()
            if "Time Series FX (Daily)" not in data:
                return f"Could not retrieve historical prices for {base}/{quote}."
            timeseries = data["Time Series FX (Daily)"]
            # Extract the most recent `period+1` closing prices
            dates = sorted(timeseries.keys())[-(period+1):]  # last period+1 days
            prices = [float(timeseries[date]["4. close"]) for date in dates]
            symbol_label = f"{base}/{quote}"
        else:
            # Crypto (asset could be symbol or name)
            coin = asset.lower()
            vs_cur = "usd"
            # If asset was given like "BTC/USD", handle that too:
            if " " in asset:  # e.g. "BTC USD"
                parts = asset.split()
                coin = parts[0].lower()
                vs_cur = parts[1].lower() if len(parts) > 1 else "usd"
            # Convert to CoinGecko ID if needed
            coin_id = _SYMBOL_TO_COINGECKO_ID.get(coin, coin)
            # Fetch historical market data for the past period+1 days
            days = period + 1
            url = (f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
                   f"?vs_currency={vs_cur}&days={days}&interval=daily")
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                return f"Error: Failed to fetch historical data for {asset_upper}."
            data = response.json()
            if "prices" not in data or len(data["prices"]) < period+1:
                return f"Not enough data to calculate {period}-day RSI for {asset_upper}."
            # `prices` is a list of [timestamp, price] entries (probably daily if interval=daily).
            # Extract the price values:
            prices = [p[1] for p in data["prices"][-(period+1):]]
            symbol_label = asset_upper
        
        # Compute RSI from price series
        if len(prices) < period+1:
            return f"Not enough data to compute {period}-day RSI for {symbol_label}."
        # Calculate average gains and losses
        gains = 0.0
        losses = 0.0
        for i in range(1, len(prices)):
            delta = prices[i] - prices[i-1]
            if delta >= 0:
                gains += delta
            else:
                losses += -delta
        avg_gain = gains / period
        avg_loss = losses / period
        if avg_loss == 0:
            rsi = 100.0
        elif avg_gain == 0:
            rsi = 0.0
        else:
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
        rsi_val = round(rsi, 2)
        # Determine basic interpretation
        interpretation = ""
        if rsi_val >= 70:
            interpretation = " (overbought)"
        elif rsi_val <= 30:
            interpretation = " (oversold)"
        else:
            interpretation = " (neutral)"
        return f"The {period}-day RSI for {symbol_label} is {rsi_val}{interpretation}."
    except Exception as e:
        return f"Error calculating RSI: {e}"

def get_news(query: str) -> str:
    """
    Fetch the latest news headlines related to the given asset or topic using Alpha Vantage News API.
    query: e.g. "BTC" or "Bitcoin" or "EUR/USD".
    """
    try:
        query = query.strip()
        if not query:
            return "Error: No topic provided for news."
        # Determine the tickers parameter for Alpha Vantage
        q_upper = query.upper()
        tickers_param = ""
        if "/" in q_upper or " " in q_upper:
            # If it's a pair like "EUR/USD" or "EUR USD", split into components
            parts = [p for p in re.split(r"[ /]+", q_upper) if p]
            if len(parts) >= 2:
                # assume it's a forex pair if both are known currency codes
                tickers_param = "FOREX:" + parts[0] + ",FOREX:" + parts[1]
            else:
                tickers_param = "FOREX:" + parts[0]
        else:
            # Single token like "BTC" or "AAPL" or "BITCOIN"
            # If it's a known fiat currency code, use FOREX: prefix (to get news about that currency)
            fiat_codes = {"USD","EUR","JPY","GBP","AUD","CAD","CHF","CNY","HKD"}
            if q_upper in fiat_codes:
                tickers_param = f"FOREX:{q_upper}"
            elif len(q_upper) <= 5 and q_upper.isalpha():
                # likely a stock or crypto symbol
                if q_upper in _SYMBOL_TO_COINGECKO_ID or q_upper in {"BTC","ETH","XRP","LTC","DOGE"}:
                    tickers_param = f"CRYPTO:{q_upper}"
                else:
                    # treat it as a stock ticker if not recognized as crypto
                    tickers_param = q_upper  
            else:
                # If it's a longer word (like "BITCOIN"), try to map common names to symbols
                name = q_upper
                if name == "BITCOIN":
                    tickers_param = "CRYPTO:BTC"
                elif name == "ETHEREUM":
                    tickers_param = "CRYPTO:ETH"
                else:
                    # default to keywords search if possible (Alpha Vantage might not support arbitrary keywords directly)
                    tickers_param = name

        # Call Alpha Vantage News & Sentiment API
        url = (f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT"
               f"&tickers={tickers_param}&limit=5&apikey={config.ALPHA_VANTAGE_API_KEY}")
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return "Error: Failed to retrieve news."
        data = response.json()
        # Alpha Vantage returns news in 'feed' or 'items'
        articles = []
        if "feed" in data:
            articles = data["feed"]
        elif "items" in data:
            articles = data["items"]
        else:
            if "Note" in data:
                return "News API limit reached. Please try again later."
            return "No news found for the given query."
        if not articles:
            return "No recent news for that topic."
        # Compile up to 3 latest headlines
        headlines = []
        for item in articles[:3]:
            title = item.get("title") or "No title"
            source = item.get("source") or item.get("source_title") or ""
            date_str = item.get("time_published", "")[:10]  # YYYY-MM-DD
            if source:
                headlines.append(f"{title} - {source} ({date_str})")
            else:
                headlines.append(f"{title} ({date_str})")
        result = "Latest news:\n" + "\n".join(f"{i+1}. {hl}" for i, hl in enumerate(headlines))
        return result
    except Exception as e:
        return f"Error fetching news: {e}"
