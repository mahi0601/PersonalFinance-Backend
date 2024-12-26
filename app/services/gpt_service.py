# import openai

# class GPTService:
#     def __init__(self, api_key: str):
#         openai.api_key = api_key

#     def generate_response(self, prompt: str, max_tokens: int = 100, temperature: float = 0.7) -> str:
#         try:
#             response = openai.Completion.create(
#                 engine="text-davinci-003",
#                 prompt=prompt,
#                 max_tokens=max_tokens,
#                 temperature=temperature
#             )
#             return response.choices[0].text.strip()
#         except Exception as e:
#             raise RuntimeError(f"Error generating GPT response: {str(e)}")
import openai

class GPTService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = self.api_key

    def generate_response(self, prompt: str, max_tokens: int, temperature: float):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Use a model compatible with the new API
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            raise ValueError(f"Error generating GPT response: {e}")
