
import openai


class OpenAi:
    def text(self, question):
        OPENAI_API = "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"
        openai.api_key = OPENAI_API
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Q: {question}\nA:",
            temperature=0,
            max_tokens=500,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )
        return response.choices[0].text

    def photo(self, question):
        openai.api_key = OPENAI_API
        response = openai.Image.create(prompt=question, n=1, size="1024x")
        return response["data"][0]["url"]

