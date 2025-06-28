import openai

openai.api_key = "YOUR_OPENAI_KEY"

def ask_ai(question, context):
    prompt = f"{context}\n\nQuestion: {question}\nAnswer:"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()
