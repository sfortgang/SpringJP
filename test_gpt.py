import json
import openai
import time  # Import the time module

# Set your OpenAI API key here
openai.api_key = ''

def ask_chatgpt(question, model="gpt-4-turbo-2024-04-09"):
    try:
        # Instructing the model to output only the number of the correct answer
       
        full_prompt = f"{question}"
        
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "Your task is to read the following question and output the answer. Please just output the numeric answer as just the number alone."},
                {"role": "user", "content": full_prompt}
            ]
        )
        # Assuming the model's response will be a number or a phrase including a number
        # and stripping to clean up the response
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"

def process_questions_and_generate_responses(input_file_path, output_file_path):
    with open(input_file_path, 'r') as file:
        questions_data = json.load(file)
    
    responses_data = {}
    
    k = 0
    for i, entry in enumerate(questions_data, 1):
        if i > 100:
            break
        question = entry["question"]
        response = ask_chatgpt(question)
        print(response)
        responses_data[f"answer_{i}"] = response
        
        # Wait for 3 seconds before processing the next question
        k = k + 1
    
    with open(output_file_path, 'w') as outfile:
        json.dump(responses_data, outfile, indent=2)

# Adjust these file paths as necessary
input_file_path = '/Users/tzvikifortgang/Downloads/JP/socratic/SocraticAI/processed_data.json'
output_file_path = '/Users/tzvikifortgang/Downloads/JP/socratic/SocraticAI/35.json'

if __name__ == "__main__":
    process_questions_and_generate_responses(input_file_path, output_file_path)
