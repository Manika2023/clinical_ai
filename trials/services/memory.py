from langchain_community.memory import ConversationBufferMemory
# from langchain_community.memory import M

memory = ConversationBufferMemory(
    return_messages=True,
    memory_key="chat_history"
)
