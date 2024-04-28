import json

def convert_json_format(input_filename, output_filename):
    # Read the original JSON file
    with open(input_filename, 'r') as file:
        data_list = json.load(file)
    
    # Process each item in the list if it's a list of dictionaries
    new_data_list = []
    for data in data_list:
        new_data = {
            "question": data["question"],
            "answer": data["answer"].split("#### ")[1].strip()
        }
        new_data_list.append(new_data)
    
    # Write the new data to a JSON file
    with open(output_filename, 'w') as file:
        json.dump(new_data_list, file, indent=2)

# Example usage
convert_json_format('/Users/tzvikifortgang/Downloads/JP/socratic/SocraticAI/gsmprevious.json', '/Users/tzvikifortgang/Downloads/JP/socratic/SocraticAI/output.json')
