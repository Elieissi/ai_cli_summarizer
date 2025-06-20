from openai import OpenAI
from openai import OpenAIError

class Summarizer:
    def __init__(self, key):
        self.client = OpenAI(api_key=key)
        try:
            self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a summarizer."},
                    {"role": "user", "content": "Ping"}
                ],
                max_tokens=1
            )
        except OpenAIError as e:
            raise ValueError(f"Invalid API key: {e}")

    def summarize(self, text):
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You summarize text."},
                    {"role": "user", "content": f"Summarize this:\n\n{text}"}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except OpenAIError as e:
            return f"Error during summarization: {e}"
