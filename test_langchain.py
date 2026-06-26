from langchain_groq import ChatGroq

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key="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"
)

response = llm.invoke("Say hello")
print(response.content)