import json
import re

def read_json_data(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def extract_last_number(answer):
    # Find all numbers, possibly including commas and decimals
    numbers = re.findall(r'[0-9,]+\.?[0-9]*', answer.replace(',', ''))
    if numbers:
        # Return the last found number, remove commas if any, to handle numbers like '1,000'
        return numbers[-1].replace(',', '').strip()
    return None  # Return None if no number is found

def process_answers_35(data):
    # Extracts the last numerical answer from each entry in 35.json
    answers = {}
    for key, value in data.items():
        numeric_key = key.split('_')[1]  # Extract the numeric identifier from keys like "answer_1"
        last_number = extract_last_number(value)
        answers[numeric_key] = last_number
    return answers

def process_answers_output(data):
    # Prepare the answers from output.json for comparison by index
    answers = {}
    for index, item in enumerate(data):
        # The index starts at 0, but we need it to start at 1 to match 35.json entries
        answers[str(index + 1)] = item['answer']
    return answers

def compare_answers(answers_from_35, answers_from_output):
    correct_count = 0
    for key, answer in answers_from_35.items():
        if key in answers_from_output and answer == answers_from_output[key]:
            correct_count += 1
            print("correct with key " + key)
    return correct_count

def main():
    filename_35 = '352.json'
    filename_output = 'output.json'

    data_35 = read_json_data(filename_35)
    data_output = read_json_data(filename_output)

    answers_from_35 = process_answers_35(data_35)
    answers_from_output = process_answers_output(data_output)

    result = compare_answers(answers_from_35, answers_from_output)

    print(f"Number of matching answers: {result}")

if __name__ == "__main__":
    main()