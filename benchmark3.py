import json
import re

def compare_answers_directly(processed_data_file, gpt_responses_file):
    with open(processed_data_file, 'r') as pd_file:
        processed_data = json.load(pd_file)

    with open(gpt_responses_file, 'r') as gr_file:
        gpt_responses = json.load(gr_file)

    # Initialize a counter for correct matches
    correct_matches = 0

    # Regular expression to find the first number after "@final"
    pattern = re.compile(r"@final\D*(\d+)")

    k = 0

    for i, question_and_answer in enumerate(processed_data, start=1):
        if k == 100:
          break

        model_answer_text = gpt_responses.get(f"answer_{i}", "")

        # Using regular expression to extract the first number following "@final"
        match = pattern.search(model_answer_text)
        model_answer_number = match.group(1) if match else "Not found"

        # Get the correct answer number as a string
        correct_answer = question_and_answer["answer"]

        # Compare directly
        is_correct = (correct_answer == model_answer_number)
        if is_correct:
            correct_matches += 1

        k = k + 1

        print(f"Question {i}: Model's choice - {model_answer_number}, Correct answer - {correct_answer}. Direct Validation: {'Correct' if is_correct else 'Incorrect'}")

    print(f"\nTotal correct matches: {correct_matches} out of {len(processed_data)}")

if __name__ == "__main__":
    processed_data_file = 'processed_data.json'  # Update this path
    gpt_responses_file = '35.json'  # Update this path
    compare_answers_directly(processed_data_file, gpt_responses_file)