"""handlers for openai"""
import os
import json
from typing import List
from asyncio import run
from openai import AsyncOpenAI
from schemas.Prompt import Prompt
from functions.crowd_density import get_crowd_density
from handlers.functions_handler import get_crowd_management_suggestions

client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])


function_map = {
    "get_crowd_management_suggestions": {
        "function": get_crowd_management_suggestions,
        "function_input_format": {
            "type": "function",
            "function": {
                "name": "get_crowd_management_suggestions",
                "description": "Takes in a prompt on how to handle and manage crowds and generates a well-thought out solution",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "problem": {
                            "type": "string",
                            "description": "a succint, but accurate description of the problem",
                        },
                    },
                    "required": ["problem"],
                },
            }, }},
    "get_crowd_density":
        {"function": get_crowd_density,
         "function_input_format":  {
             "type": "function",
             "function": {
                 "name": "get_crowd_density",
                 "description": "gets crowd density on all stations for a particular line",
                 "parameters": {
                     "type": "object",
                     "properties": {
                         "station": {
                             "type": "string",
                             "enum": ["CIRCLE_LINE",
                                      "CIRCLE_LINE_EXT",
                                      "CHANGI_EXT",
                                      "DOWNTOWN_LINE",
                                      "EAST_WEST_LINE",
                                      "NORTH_EAST_LINE",
                                      "NORTH_SOUTH_LINE",
                                      "BUKIT_PANJANG_LRT",
                                      "SENGKANG_LRT",
                                      "PUNGGOL_LRT"],
                             "description": "The city and state, e.g. San Francisco, CA",
                         },
                     },
                     "required": ["station"],
                 },
             },
         }}
}


async def get_completion(messages: List[Prompt], params: object = {}) -> Prompt:
    """gets completion from open ai model"""
    messages = format_role_content(messages)
    tools = [function["function_input_format"]
             for _, function in function_map.items()]
    chat_completion = await client.chat.completions.create(
        messages=messages,
        tools=tools,
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
        function_response = await function_map[function_name]["function"](
            **function_args)
        return Prompt(**{"role": "function", "content": json.dumps(function_response), "name": function_name})
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
