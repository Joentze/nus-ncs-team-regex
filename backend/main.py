import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import ValidationError
from beanie.exceptions import DocumentNotFound
from schemas.Conversation import Conversation, ConversationFull, ConversationList
from schemas.Prompt import Prompt
from schemas.requests import ConversationPUT
from schemas.responses import CreatedResponse
from handlers.mongo_handler import add_to_message_history, add_token_count
from handlers.openai_handler import get_completion
from anon.anonymiser import encrypt_prompt, decrypt_prompt
from beanie import init_beanie

app = FastAPI()

# CORS middleware
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Constants
STATUS_404 = {"code": 404, "message": "Specified resource(s) was not found"}
STATUS_500 = {"code": 500, "message": "Internal Server Error"}
STATUS_422 = {"code": 422, "message": "Unable to create resource"}
STATUS_400 = {"code": 400, "message": "Invalid Parameters Provided"}

# MongoDB initialization


@app.on_event("startup")
async def init():
    """connects to mongodb"""
    client = AsyncIOMotorClient(os.environ["MONGODB_ROUTE"])
    await init_beanie(database=client.db_name, document_models=[ConversationFull])

# Conversation Endpoints


@app.post("/conversations", response_model=CreatedResponse, status_code=201)
async def create_conversation(convo: Conversation):
    """creates a new conversation"""
    try:
        convo_full = ConversationFull(**convo.to_json(), messages=[])
        obj = await convo_full.insert()
        return {"id": obj.to_json()["id"]}
    except Exception as e:
        print(e)
        return JSONResponse(content=STATUS_500, status_code=500)


@app.get("/conversations", response_model=ConversationList)
async def get_conversations():
    """gets all existing conversations"""
    try:
        data = {"data": await ConversationFull.find_all().to_list()}
        return data
    except Exception as e:
        print(e)
        return JSONResponse(content=STATUS_500, status_code=500)


@app.put("/conversations/{id}", status_code=204)
async def updates_conversation(id: str, convo: ConversationPUT):
    """updates an existing conversations name, parameters"""
    try:
        doc = await ConversationFull.get(id)
        await doc.set({ConversationFull.name: convo.name, ConversationFull.params: convo.params})
    except DocumentNotFound:
        return JSONResponse(content=STATUS_404, status_code=404)
    except Exception as e:
        print(e)
        return JSONResponse(content=STATUS_500, status_code=500)


@app.get("/conversations/{id}", response_model=ConversationFull, status_code=200)
async def get_conversation_history(id: str):
    """gets the full conversation history of a existing conversation"""
    try:
        doc = await ConversationFull.get(id)
        doc_decrypt_messages = ConversationFull(
            _id=id,
            name=doc.name,
            params=doc.params,
            tokens=doc.tokens,
            messages=[decrypt_prompt(message.dict())
                      for message in doc.messages]
        )
        return doc_decrypt_messages
    except DocumentNotFound:
        return JSONResponse(content=STATUS_404, status_code=404)
    except Exception as e:
        print(e)
        return JSONResponse(content=STATUS_500, status_code=500)


@app.delete("/conversations/{id}", status_code=204)
async def delete_conversation(id: str):
    """deletes an existing conversations"""
    try:
        convo = await ConversationFull.get(id)
        await convo.delete()
    except DocumentNotFound:
        return JSONResponse(content=STATUS_404, status_code=404)
    except Exception as e:
        print(e)
        return JSONResponse(content=STATUS_500, status_code=500)

# Query Endpoint


@app.post("/queries", response_model=CreatedResponse, status_code=201)
async def send_prompt_query(id: str, prompt: Prompt):
    """sends prompt to OpenAI LLM"""
    try:
        role, content = prompt.role, prompt.content
        doc = await ConversationFull.get(id)
        params = doc.params
        message_history = [decrypt_prompt(message.dict())
                           for message in doc.messages]
        encrypted_prompt = encrypt_prompt(prompt)
        await add_token_count(id, content)
        await add_to_message_history(id, encrypted_prompt)
        llm_response = await get_completion([*message_history, {"role": role, "content": content}], params={"model": "gpt-3.5-turbo", **params})
        await add_token_count(id, llm_response.content)
        message = await add_to_message_history(id, encrypt_prompt(llm_response))
        return {"id": message.to_json()["id"]}
    except (DocumentNotFound, ValidationError) as e:
        print(e)
        return JSONResponse(content=STATUS_404, status_code=404)
    except HTTPException as e:
        print(e)
        return JSONResponse(content=STATUS_422, status_code=422)
    except Exception as e:
        print(e)
        return JSONResponse(content=STATUS_500, status_code=500)

# Request Validation Exception Handler


@app.exception_handler(RequestValidationError)
async def invalid_parameter_error(request: Request, exc: ValidationError):
    """handles invalid parameters"""
    return JSONResponse(content=STATUS_400, status_code=400)

if __name__ == "__main__":
    pass
