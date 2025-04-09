```python
# agent.py

from langchain.agents import Tool, initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
import config
import tools

# Initialize the language model (LLM)
# Here we use OpenAI's GPT-4 model via the API.
# You could swap this with ChatOpenAI(model="gpt-3.5-turbo") for cost savings,
# or configure another provider's model similarly.
llm = ChatOpenAI(model="gpt-4", temperature=0, openai_api_key=config.OPENAI_API_KEY)

# Define the tools for the agent, wrapping our functions.
tool_list = [
    Tool(
        name="get_crypto_price",
        func=tools.get_crypto_price,
        description=(
            "Fetch the current price of a cryptocurrency. "
            "Input format: '<COIN> [,<CURRENCY>]' for example 'BTC' or 'ETH,EUR'. "
            "By default, uses USD as the currency."
        )
    ),
    Tool(
        name="get_forex_rate",
        func=tools.get_forex_rate,
        description=(
            "Get the exchange rate for a currency pair. "
            "Input format: 'BASE/QUOTE', e.g. 'EUR/USD' to get the rate of 1 EUR in USD."
        )
    ),
    Tool(
        name="get_rsi",
        func=tools.get_rsi,
        description=(
            "Calculate the Relative Strength Index for an asset. "
            "Input format: '<ASSET> [,<PERIOD>]' where ASSET can be a crypto symbol or forex pair. "
            "Examples: 'BTC' (14-day RSI for Bitcoin/USD) or 'EUR/USD,14' for 14-day RSI on EUR/USD."
        )
    ),
    Tool(
        name="get_news",
        func=tools.get_news,
        description=(
            "Fetch recent news headlines related to a given asset or topic. "
            "Input: an asset symbol or name (e.g. 'BTC' or 'Bitcoin' or 'EUR/USD'). "
            "Returns a brief list of latest news headlines."
        )
    )
]

# Set up memory to retain conversation context (so the agent can remember previous Q&A)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Initialize the agent with tools and the LLM
agent_chain = initialize_agent(
    tool_list, 
    llm, 
    agent=AgentType.OPENAI_FUNCTIONS, 
    memory=memory, 
    verbose=False
)

# (We set verbose=False to avoid debug logs. For development, True can be useful to see the agent's thought process.)
