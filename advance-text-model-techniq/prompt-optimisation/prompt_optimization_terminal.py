import pandas as pd

# Load the responses.csv file:
df = pd.read_csv("responses.csv")

# Shuffle the DataFrame
df = df.sample(frac=1).reset_index(drop=True)

# Add a new column to store feedback
df["feedback"] = pd.Series(dtype="str")

response_index = 0

def update_response():
    if response_index < len(df):
        new_response = df.iloc[response_index]["response"]
        print("\nResponse:")
        print(new_response if pd.notna(new_response) else "No response")
        print(f"Response: {response_index + 1} / {len(df)}")
    else:
        print("\nAll responses have been reviewed.")

def save_results():
    # Save the feedback to a CSV file
    df.to_csv("results.csv", index=False)
    print("\nA/B testing completed. Results saved to 'results.csv'.")
    # Calculate score for each variant and count the number of rows per variant
    summary_df = (
        df.groupby("variant")
        .agg(count=("feedback", "count"), score=("feedback", "mean"))
        .reset_index()
    )
    print("\nSummary:")
    print(summary_df)

while response_index < len(df):
    update_response()
    user_input = input("Provide feedback (1 for positive, 0 for negative, or 'q' to quit): ").strip()
    if user_input == "1":
        df.at[response_index, "feedback"] = 1
        response_index += 1
    elif user_input == "0":
        df.at[response_index, "feedback"] = 0
        response_index += 1
    elif user_input.lower() == "q":
        print("Exiting...")
        break
    else:
        print("Invalid input. Please enter 1, 0, or 'q'.")

if response_index >= len(df):
    save_results()