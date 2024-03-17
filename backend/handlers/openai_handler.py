"""handlers for openai"""
import os
import json
from typing import List
from asyncio import run
from openai import AsyncOpenAI
from schemas.Prompt import Prompt
from dotenv import load_dotenv

# dotenv_path = os.path.join(os.path.dirname(__file__), '..', '', '.env') 
# load_dotenv(dotenv_path)
# client =  os.getenv('OPENAI_API_KEY')

client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])


function_map = {
}


async def get_completion(messages: List[Prompt], params: object = {}) -> Prompt:
    """gets completion from open ai model"""
    messages = format_role_content(messages)
    chat_completion = await client.chat.completions.create(
        messages=messages,
        **params
    )
    llm_message = chat_completion.choices[0].message
    role = llm_message.role
    content = llm_message.content
    tool_calls = llm_message.tool_calls
    print(tool_calls)
    if tool_calls:
        function_name = tool_calls[0].function.name
        function_args = json.loads(tool_calls[0].function.arguments)
        function_response = function_map[function_name](**function_args)
        return Prompt(**{"role": "function", "content": function_response, "name": function_name})
    return Prompt(**{"role": role, "content": content})


def format_role_content(messages: object) -> List[Prompt]:
    """formats to role and content"""
    formatted_messages = []
    for message in messages:
        curr_prompt = {}
        curr_prompt["role"] = message["role"]
        curr_prompt["content"] = message["content"]
        if "name" in message:
            curr_prompt["name"] = message["name"]
        formatted_messages.append(curr_prompt)
    return formatted_messages


if __name__ == "__main__":
    run(get_completion([{"role": "user", "content": "hello there"}]))
