import os
from langchain_openai import ChatOpenAI
# from langchain.agents import create_tool_calling_agent, AgentExecuto

from langchain_classic.agents import AgentExecutor
from langchain_classic.agents import create_tool_calling_agent

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from .tools import search_trials_db, search_trial_docs
# from .memory import memory   # should return chat messages list

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder




# LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY")
)

# Tools
tools = [search_trials_db, search_trial_docs]

# Prompt (NO chat_history)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a clinical research AI assistant."),
        ("human", "{input}"),
        # This is where tool calls, tool results, and reasoning steps store
        # Required for agents that use tools
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

# Agent
agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

# Executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)

# Runner
def run_agent(query: str):
    response = agent_executor.invoke(
        {"input": query}
    )
    return response["output"]
