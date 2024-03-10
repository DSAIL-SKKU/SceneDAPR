from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse

# graphql
import strawberry
from strawberry.asgi import GraphQL
from apis.resolvers import Mutation, Query
from apis.typeDefs import Participant
from context import db

import asyncio
import time

from starlette.status import HTTP_504_GATEWAY_TIMEOUT

# env
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()
allow_origins_domains = os.getenv('ALLOW_ORIGINS', '').split(',')
REQUEST_TIMEOUT_ERROR = 360000

# GraphQL
schema = strawberry.Schema(query=Query, mutation=Mutation, types=[Participant])
graphql_app = GraphQL(schema)

app = FastAPI()
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)

"""CORS Setting
reference: https://fastapi.tiangolo.com/tutorial/cors/?h=cors
"""

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins_domains,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variable
items = {}


@app.on_event("startup")
async def startup_event():
    """
    Initialize FastAPI and load model
    """
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

# for test
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post('/graphql')
async def graphql(request: Request):
    data = await request.json()
    result = await schema.execute_async(data['query'], variable_values=data.get('variables'))
    if result.errors:
        raise HTTPException(status_code=400, detail=str(result.errors))
    return result.to_dict()



# Adding a middleware returning a 504 error if the request processing time is above a certain threshold
@app.middleware("http")
async def timeout_middleware(request: Request, call_next):
    try:
        start_time = time.time()
        return await asyncio.wait_for(call_next(request), timeout=REQUEST_TIMEOUT_ERROR)

    except asyncio.TimeoutError:
        process_time = time.time() - start_time
        return JSONResponse({'detail': 'Request processing time excedeed limit',
                             'processing_time': process_time},
                            status_code=HTTP_504_GATEWAY_TIMEOUT)