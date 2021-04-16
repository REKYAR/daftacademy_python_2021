import hashlib
import datetime
from fastapi import FastAPI, Response, status, Request
from typing import Optional
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI()
app.counter = 0
app.id=0
app.records={}


class HelloResp(BaseModel):
    msg:str

class InputJSON(BaseModel):
    name:str
    surname:str


@app.get("/")
def root():
    return {"message": "Hello world!"}


@app.get("/method")
async def getres():
    return {"method":"GET"}

@app.post("/method", status_code=201)
async def getres():
    return {"method":"POST"}

@app.post("/auth")
async def hashver(password:str, password_hash:str):
    if (not password)or(not password_hash):
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    print(hashlib.sha512(password.replace("\n","").strip().encode('utf-8')))
    if hashlib.sha512(password.replace("\n","").strip().encode('utf-8')).hexdigest()==password_hash:
        
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)

@app.post("/register")
async def register_reciver(inputJSON: InputJSON):
    app.id+=1

    now=datetime.datetime.today()
    delta=len(inputJSON.name+inputJSON.surname)
    nxt = now+datetime.timedelta(days=delta)
    now = str(now.year)+"-"+str(now.month).rjust(2,'0')+"-"+str(now.day).rjust(2,'0')
    nxt =str(nxt.year)+"-"+str(nxt.month).rjust(2,'0')+"-"+str(nxt.day).rjust(2,'0')

    app.records[id]={"id":app.id, 
    "name":inputJSON.name,
    "surname":inputJSON.surname,
    "register_date": now,
    "vaccination_date": nxt}

    return JSONResponse(content={"id":app.id, 
    "name":inputJSON.name,
    "surname":inputJSON.surname,
    "register_date": now,
    "vaccination_date": nxt}, status_code=status.HTTP_201_CREATED)

@app.get("/patient/{id}")
async def access_record(inid: int):
    if inid<1:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    elif  inid in app.records:
        return JSONResponse(content=app.records[inid], status_code=status.HTTP_200_OK)
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

# @app.get("/hello/{name}", response_model=HelloResp)
# async def read_item(name: str):
#     return HelloResp(msg=f"Hello {name}")


# @app.get('/counter')
# def counter():
#     app.counter += 1
#     return app.counter
