from openai import OpenAI
client = OpenAI(
    api_key="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"
)
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful and virtual assistant named angry bird skilled in general tasks like alexa and google."},
        {
            "role": "user",
            "content": "what is coding."
        }
    ]
)

print(completion.choices[0].message.content)
