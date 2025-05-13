import openai

# Set base and dummy key for LM Studio
client = openai.OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio"
)

def get_completion(prompt):
    response = client.chat.completions.create(
        model="llama3",  # or the exact name shown in LM Studio
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
        temperature=0.7,
    )
    return response.choices[0].message.content

print(get_completion("Explain photosynthesis in simple words.Total word count should be 1000. Less than that will end my carrier."))