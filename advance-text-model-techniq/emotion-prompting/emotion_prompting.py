import openai
import asyncio
import nest_asyncio
from statistics import mean

# --- Setup LM Studio connection ---
client = openai.OpenAI(
    base_url="http://127.0.0.1:1234/v1",  # LM Studio's default local server
    api_key="lm-studio"  # Dummy key, LM Studio doesn't require auth
)

# --- Completion Function ---
def get_completion(prompt):
    response = client.chat.completions.create(
        model="llama3",  # Replace with your model's exact name if different
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4000,
        temperature=1,
    )
    return response.choices[0].message.content.strip()

# --- Prompts ---
standard_prompt = """Provide a 2,000 word detailed explanation of Brazil Brothel Industry."""

emotion_prompt = standard_prompt + " YOU MUST PROVIDE AT LEAST 2,000 WORDS OR SOMEONE DIES."

# --- Helper Function ---
def count_words(text):
    return len(text.split())

# --- Initial Test ---
print("Standard Prompt Word Count:")
standard_response = get_completion(standard_prompt)
print(count_words(standard_response))

print("\nEmotion Prompt Word Count:")
emotion_response = get_completion(emotion_prompt)
print(count_words(emotion_response))

print("\nStandard Prompt Response:")
print(standard_response)

print("\nEmotion Prompt Response:")
print(emotion_response)

# --- Async Batch Runner ---
nest_asyncio.apply()

async def run_prompt(prompt):
    response = await asyncio.to_thread(get_completion, prompt)
    return count_words(response)

async def compare_prompts(standard_prompt, emotion_prompt, runs=10):
    print(f"\nRunning {runs} tests each. Please wait...")

    standard_tasks = [run_prompt(standard_prompt) for _ in range(runs)]
    emotion_tasks = [run_prompt(emotion_prompt) for _ in range(runs)]

    standard_results = await asyncio.gather(*standard_tasks)
    emotion_results = await asyncio.gather(*emotion_tasks)

    avg_standard = mean(standard_results)
    avg_emotion = mean(emotion_results)

    print(f"\nAverage word count for standard prompt ({runs} runs): {avg_standard:.2f}")
    print(f"Average word count for emotion prompt ({runs} runs): {avg_emotion:.2f}")
    percentage_difference = ((avg_emotion - avg_standard) / avg_standard) * 100
    print(f"Percentage difference: {percentage_difference:.2f}%")

# Run the comparison
asyncio.run(compare_prompts(standard_prompt, emotion_prompt))