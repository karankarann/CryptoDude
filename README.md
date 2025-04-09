# CryptoDude
Crypto Dude is a real-time, AI-powered trading assistant for crypto and forex markets. Built with GPT-4, LangChain, and Streamlit, it answers market questions, fetches live data, computes indicators like RSI, and summarizes news — all in natural language. Designed for traders, researchers, and finance enthusiasts. Not financial advice 🚀.

# 🤖 Crypto Dude – Your AI-Powered Trading Assistant

Crypto Dude is a GenAI-based trading chatbot that gives you real-time insights on cryptocurrencies and forex markets using natural language. Ask it about live prices, technical indicators like RSI, or even the latest news — and it responds with intelligent, contextual answers.

![Crypto Dude Screenshot](screenshot.png) <!-- Optional: Add a screenshot later -->

---

## 🚀 Features

- 💬 Conversational interface (Streamlit + GPT-4)
- 📈 Real-time crypto & forex prices (CoinGecko, Alpha Vantage)
- 📊 Built-in technical indicators (e.g., RSI calculator)
- 📰 Market news summaries
- 🧠 Memory-enabled LLM with LangChain agent
- ⚙️ Easily extensible tools (plug in new APIs, models, or indicators)

---

## 🧱 Tech Stack

- [OpenAI GPT-4](https://platform.openai.com/)
- [LangChain](https://www.langchain.com/)
- [Streamlit](https://streamlit.io/)
- [CoinGecko API](https://www.coingecko.com/en/api)
- [Alpha Vantage API](https://www.alphavantage.co/)

---

## 🛠️ Setup Instructions

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/crypto-dude.git
   cd crypto-dude

2. **Install dependences**
   ```bash
   pip install -r requirements.txt

3. **Set your API keys**
   Edit config.py with yout actual keys
   - OpenAI API key (for GPT4 or GPT3.5)
   - Alpha Vantage API key (for forex and indicators)
   - CoinGecko (optional – free tier works without a key)
  
4. Run the App
   ```bash
   streamlit run app.py

6. Start chatting Ask questions like:
  - "What’s the price of Bitcoin?"
  - "Get me the RSI for ETH"
  - "Any news on the US Dollar?"

**🧪Example Queries**

"What is the current price of ETH in EUR?"

"Give me the 14-day RSI for BTC"

"Convert 1 ETH to USD"

"What's the latest Bitcoin news?"

**⚠️ Disclaimer**
This tool is for educational purposes only and does not constitute financial advice. Always do your own research before making trading decisions.
