from groq import Groq

client = Groq(
    api_key="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"
)

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": "Hello"}
    ]
)

print(response.choices[0].message.content)