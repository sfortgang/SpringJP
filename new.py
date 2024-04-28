import openai

# Set your OpenAI API key here
openai.api_key = ""

def ask_chatgpt(question, model="gpt-3.5-turbo"):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"

def main():
    question = input("What is your question? ")
    answer = ask_chatgpt(question)
    print(f"Answer: {answer}")

if __name__ == "__main__":
    main()
