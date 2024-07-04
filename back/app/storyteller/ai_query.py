import pathlib
import textwrap

import google.generativeai as genai
import replicate
import replicate.client
from anthropic import AI_PROMPT, HUMAN_PROMPT, AsyncAnthropic
from dependencies.settings import get_settings
from mistralai.async_client import MistralAsyncClient
from mistralai.models.chat_completion import ChatMessage
from openai import (
    APITimeoutError,
    AsyncOpenAI,
    InternalServerError,
    OpenAI,
    RateLimitError,
)
from utils.log_decorators import log_deco

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
        else:
            raise ValueError("Invalid llm")

    async def query_gpt(self) -> str:
        print(f"Calling GPT with prompt: {self.prompt}")
        openai = AsyncOpenAI(api_key=self.settings.openai_api_key)
        response = await openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are playing a game of exquisite corpse",
                },
                {"role": "assistant", "content": self.prompt},
            ],
            max_tokens=4095,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        response = response.choices[0].message.content
        print("response", response)
        if response is None:
            raise ValueError("OpenAI call Response is None")
        return response

    async def query_gemini(self) -> str:
        print(f"Calling Gemini with prompt: {self.prompt}")
        genai.configure(api_key=self.settings.gemini_api_key)
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(self.prompt)
        print("response", response)
        return response.text

    async def query_claude(self) -> str:
        print(f"Calling Claude with prompt: {self.prompt}")
        anthropic = AsyncAnthropic(
            api_key=self.settings.anthropic_api_key,
        )
        completion = anthropic.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=2000,
            messages=[
                {"role": "user", "content": self.prompt},
            ],
        )
        response = await completion
        response.content[0]
        return response.content[0].text

    async def query_mistral(self) -> str:
        client = MistralAsyncClient(api_key=self.settings.mistral_api_key)
        model = "mistral-large-latest"
        messages = [ChatMessage(role="user", content=self.prompt)]
        chat_response = await client.chat(
            model=model,
            messages=messages,
        )
        print(chat_response.choices[0].message.content)
        return chat_response.choices[0].message.content

    async def query_llama(self) -> str:
        print(f"Calling Llama with prompt: {self.prompt}")
        client = replicate.Client(api_token=self.settings.replicate_api_key)
        input = {
            "top_p": 0.9,
            "prompt": self.prompt,
            "min_tokens": 0,
            "temperature": 0.6,
            # "prompt_template": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nYou are a helpful assistant<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",
            "presence_penalty": 1.15,
        }

        output = client.run("meta/meta-llama-3-70b-instruct", input=input)

        joined_output = "".join(output)
        print("llama output", joined_output)
        print(type(joined_output))
        return joined_output
