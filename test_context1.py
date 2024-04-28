import openai
import json
import time 

openai.api_key = ""

class SocraticGPT:
    def __init__(self, role, n_round=10, model="gpt-4-turbo-2024-04-09"):
        self.role = role
        self.model = model
        self.n_round = n_round
        self.history = []
        
        if self.role == "Socrates":
            self.other_role = "Theaetetus"
        elif self.role == "Theaetetus":
            self.other_role = "Socrates"
        
        self.history = []
        
    def set_question(self, question):
        if self.role == "Socrates":
            self.history.append({
                "role": "system",
                 "content": f"Socrates and Theaetetus are two AI assistants to solve challenging problems. The problem statement is as follows: \"{question}\".\n\nSocrates and Theaetetus will engage in multi-round dialogue to solve the problem together. They must select an answer. Try to resolve it quickly as possible. Their discussion should follow a structured problem-solving approach, such as formalizing the problem, breaking down the question into steps, developing high-level strategies for solving the problem, critically evaluating each other's reasoning, avoiding arithmetic and logical errors, and effectively communicating their ideas.\n\nTheir ultimate objective is to come to a correct solution through reasoned discussion.\nTheir final answer should be just the number chosen. \n\nIt should begin with the phrase: \"Here is our @final answer:\".\n\nNow, suppose that you are {self.role}. Please discuss the problem with {self.other_role}!"}
            )
            self.history.append({
                "role": "assistant",
                "content": f"Hi Theaetetus, let's solve this problem together."
            })
        elif self.role == "Theaetetus":
            self.history.append({
                "role": "system",
                 "content": f"Socrates and Theaetetus are two AI assistants to solve challenging problems. The problem statement is as follows: \"{question}\".\n\nSocrates and Theaetetus will engage in multi-round dialogue to solve the problem together. They must select an answer. Try to resolve it quickly as possible. Their discussion should follow a structured problem-solving approach, such as formalizing the problem, breaking down the question into steps, developing high-level strategies for solving the problem, critically evaluating each other's reasoning, avoiding arithmetic and logical errors, and effectively communicating their ideas.\n\nTheir ultimate objective is to come to a correct solution through reasoned discussion.\nTheir final answer should be just the number chosen. \n\nIt should begin with the phrase: \"Here is our @final answer:\".\n\nNow, suppose that you are {self.role}. Please discuss the problem with {self.other_role}!"}
            )
            self.history.append({
                "role": "user",
                "content": f"Hi Theaetetus, let's solve this problem together."
            })

    def get_response(self, temperature=None):
        try:
            if temperature:
                res = openai.ChatCompletion.create(
                    model=self.model,
                    messages=self.history,
                    temperature=temperature
                )
            else:
                res = openai.ChatCompletion.create(
                model=self.model,
                messages=self.history
            )
            msg = res.get("choices")[0]["message"]["content"]
            # self.history.append({"role": "assistant", "content": msg})
            return msg
        except openai.error.RateLimitError:
            print("Rate limit exceeded, moving to the next question...")
          
            return None  # Indicator to move to the next question
        except Exception as e:
            print(f"An error occurred: {str(e)}")
       
            return None  # Treat other exceptions similarly
    
    def update_history(self, message):
        label = f"{self.other_role}'s Last Response:"
        newHistory = self.history
        newHistory.append({
            "role": "user",
            "content": f"{label} {message}"
        })

    def add_python_feedback(self, msg):
        self.history.append({
            "role": "system",
            "content": f"Excuting the Python script. It returns \"{msg}\""
        })
        


def process_questions(input_file_path, output_file_path):
    with open(input_file_path, 'r') as file:
        questions_data = json.load(file)

    responses_data = {}
    
    socrates = SocraticGPT("Socrates")
    theaetetus = SocraticGPT("Theaetetus")
    try:  # Try block to catch exceptions
        for i, entry in enumerate(questions_data, start=1):
            
            if i > 20:  # Limit processing to the first 100 questions
                break

            question = entry["question"]

            # Reset history at the start of each new question
            theaetetus.history = []
            socrates.history = []

            socrates.set_question(question)
            theaetetus.set_question(question)
            
            # print("Original question" + question + "\n")
            
            for _ in range(12):  # Simulate dialogue with a set number of turns
                # print("Socrates' history: " + str(socrates.history) + "\n")
                socrates_response = socrates.get_response()
                # print("Socrates response" + socrates_response + "\n")
                if socrates_response is None:  # Error encountered, skip to saving
                    raise Exception(f"Error encountered at question {i}.")
                if "@final" in socrates_response:
                    responses_data[f"answer_{i}"] = socrates_response
                    print(socrates_response)
                    break
                theaetetus.update_history(socrates_response)
                # print("Thaetetus history:" + str(theaetetus.history)+"\n")
                
                theaetetus_response = theaetetus.get_response()

                # print("Thaetetus response" + theaetetus_response + "\n")
                if theaetetus_response is None:  # Error encountered, skip to saving
                    raise Exception(f"Error encountered at question {i}.")
                if "@final" in theaetetus_response:
                    responses_data[f"answer_{i}"] = theaetetus_response
                    print(theaetetus_response)
                    break
                socrates.update_history(theaetetus_response)
    
    except Exception as e:
        print(e)  # Print the error message including the question number
        
    finally:  # Finally block ensures this code runs whether an exception occurred or not
        # Save the responses data to the JSON file before terminating
        with open(output_file_path, 'w') as outfile:
            json.dump(responses_data, outfile, indent=2)
        if 'e' in locals():  # Check if an exception was caught
            print("Terminating due to an error.")
            return  # End the function prematurely


if __name__ == "__main__":
    input_file_path = '/Users/tzvikifortgang/Downloads/JP/socratic/SocraticAI/processed_data.json'  # Update this path
    output_file_path = '/Users/tzvikifortgang/Downloads/JP/socratic/SocraticAI/354.json'  # Update this path
    process_questions(input_file_path, output_file_path)

