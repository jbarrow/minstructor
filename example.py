import openai


client = openai.OpenAI()


if __name__ == "__main__":
    response = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": "What is the meaning of life?"
        }],
        model="gpt-3.5-turbo"
    )


    print(response)