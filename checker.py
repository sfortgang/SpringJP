import json

# Function to compare responses directly
def compare_answers_directly(processed_data_file, gpt_responses_file):
    with open(processed_data_file, 'r') as pd_file:
        processed_data = json.load(pd_file)
    
    with open(gpt_responses_file, 'r') as gr_file:
        gpt_responses = json.load(gr_file)
    
    # Initialize a counter for correct matches
    correct_matches = 0
    k = 0

    for i, question_and_answer in enumerate(processed_data, start=1):
        if k == 100:
            break
        model_answer_text = gpt_responses.get(f"answer_{i}")
        
        # Assuming the correct answer is just the number, extracting the model's chosen answer number
        model_answer_number = ''.join(filter(str.isdigit, model_answer_text))
        
        # Get the correct answer number as a string
        correct_answer = question_and_answer.get("answer")

        # Compare directly
        is_correct = (correct_answer == model_answer_number)
        if is_correct:
            correct_matches += 1

        print(f"Question {i}: Model's choice - {model_answer_number}, Marked correct answer - {correct_answer}. Direct Validation: {'Yes' if is_correct else 'No'}")
        k = k + 1
    
    print(f"\nTotal correct matches: {correct_matches} out of 100")

if __name__ == "__main__":
    processed_data_file = '/Users/tzvikifortgang/Downloads/JP/socratic/SocraticAI/processed_data.json'   # Update this path
    gpt_responses_file = '/Users/tzvikifortgang/Downloads/JP/socratic/SocraticAI/second.json'  # Update this path
    compare_answers_directly(processed_data_file, gpt_responses_file)
