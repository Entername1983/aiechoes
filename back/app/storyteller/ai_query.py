import google.generativeai as genai
import replicate
import replicate.client
from anthropic import AsyncAnthropic
from dependencies.settings import get_settings
from mistralai import Mistral, UserMessage
from openai import (
    AsyncOpenAI,
)

from app.exceptions.CallAiExceptions import CallAiExceptions

settings = get_settings()


class AiQuery:
    def __init__(self, llm: str, prompt: str):
        self.llm: str = llm
        self.prompt: str = prompt
        self.settings = settings.ai

    async def query(self) -> str:
        if self.llm == "gemini":
            return await self.query_gemini()
        if self.llm == "claude":
            return await self.query_claude()
        if self.llm == "gpt":
            return await self.query_gpt()
        if self.llm == "mistral":
            return await self.query_mistral()
        if self.llm == "llama":
            return await self.query_llama()
        raise CallAiExceptions.InvalidLlmError("Invalid llm")

    async def query_gpt(self) -> str:
        openai = AsyncOpenAI(api_key=self.settings.open_ai.openai_api_key)
        response = await openai.chat.completions.create(
            model=self.settings.open_ai.main_model,
            messages=[
                {
                    "role": "system",
                    "content": "You are playing a game of exquisite corpse",
                },
                {"role": "assistant", "content": self.prompt},
            ],
            max_tokens=self.settings.open_ai.max_tokens,
            top_p=self.settings.temperature,
            frequency_penalty=self.settings.frequency_penalty,
            presence_penalty=self.settings.presence_penalty,
        )
        response = response.choices[0].message.content
        if response is None:
            raise CallAiExceptions.NoResponseError("OpenAI call Response is None")
        return response

    async def query_gemini(self) -> str:
        genai.configure(api_key=self.settings.gemini.gemini_api_key)
        model = genai.GenerativeModel(self.settings.gemini.main_model)
        response = model.generate_content(self.prompt)
        return response.text

    async def query_claude(self) -> str:
        anthropic = AsyncAnthropic(
            api_key=self.settings.anthropic.anthropic_api_key,
        )
        completion = anthropic.messages.create(
            temperature=self.settings.temperature,
            model=self.settings.anthropic.main_model,
            max_tokens=self.settings.anthropic.max_tokens,
            messages=[
                {"role": "user", "content": self.prompt},
            ],
        )
        response = await completion
        response.content[0]
        return response.content[0].text

    async def query_mistral(self) -> str:
        client = Mistral(api_key=self.settings.mistral.mistral_api_key)
        user_message = UserMessage(role="user", content=self.prompt)
        messages = [user_message]
        chat_response = await client.chat.complete_async(
            model=self.settings.mistral.main_model,
            messages=messages,
        )
        if chat_response is None or chat_response.choices is None:
            raise CallAiExceptions.NoResponseError("Mistral call Response is None")
        content = chat_response.choices[0].message.content
        if isinstance(content, str):
            return content
        raise CallAiExceptions.InvalidResponseError(
            "Mistral call Response is not a string",
        )

    async def query_llama(self) -> str:
        client = replicate.Client(api_token=self.settings.llama.replicate_api_key)
        input_to_llm = {
            "top_p": self.settings.top_p,
            "prompt": self.prompt,
            "min_tokens": self.settings.llama.min_tokens,
            "temperature": self.settings.temperature,
            # "prompt_template": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nYou
            # are a helpful assistant<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{prompt}
            # <|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",
            "presence_penalty": self.settings.presence_penalty,
        }

        output = client.run(f"meta/{self.settings.llama.main_model}", input=input_to_llm)

        return "".join(output)
