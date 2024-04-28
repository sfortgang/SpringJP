import json
import re

def compare_answers(dialogue_file, processed_data_file):
    # Load the dialogue responses
    with open(dialogue_file, 'r') as f:
        dialogue_data = json.load(f)

    # Load the processed data
    with open(processed_data_file, 'r') as f:
        processed_data = json.load(f)

    # Compile regex pattern to extract the final answer number
    pattern = re.compile(r"Here is our @final answer: (\d+)")

    correct_count = 0
    for i, entry in enumerate(processed_data, start=1):
        if i > 100:
         break
        answer_key = f"answer_{i}"
        if answer_key in dialogue_data:
            # Extract the final answer number from the dialogue response
            match = pattern.search(dialogue_data[answer_key])
            if match:
                final_answer = match.group(1)
                correct_answer = entry["answer"]

                if final_answer == correct_answer:
                    print(f"Question {i}: Correct (Found: {final_answer}, Expected: {correct_answer})")
                    correct_count += 1
                else:
                    print(f"Question {i}: Incorrect (Found: {final_answer}, Expected: {correct_answer})")
            else:
                print(f"Question {i}: No final answer found in dialogue.")
        else:
            print(f"Question {i}: No dialogue answer available.")

    print(f"\nTotal Correct: {correct_count} out of 100")

# Assuming the files are named dialogue_responses.json and processed_data.json
compare_answers('352.json', 'processed_data.json')