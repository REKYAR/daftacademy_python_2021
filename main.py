import hashlib
import datetime
from fastapi import FastAPI, Response, status, Request, Depends, Cookie
from typing import Optional
from pydantic import BaseModel
from fastapi.responses import JSONResponse, HTMLResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
security = HTTPBasic()
templates = Jinja2Templates(directory="templates")
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
#zrobić dla geta
# @app.post("/auth")
# async def hashver(password:str, password_hash:str):
#     if (not password)or(not password_hash):
#         return Response(status_code=status.HTTP_401_UNAUTHORIZED)
#     print(hashlib.sha512(password.replace("\n","").strip().encode('utf-8')))
#     if hashlib.sha512(password.replace("\n","").strip().encode('utf-8')).hexdigest()==password_hash:
        
#         return Response(status_code=status.HTTP_204_NO_CONTENT)
#     else:
#         return Response(status_code=status.HTTP_401_UNAUTHORIZED)



@app.get("/auth")
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

    app.records[app.id]={"id":app.id, 
    "name":inputJSON.name,
    "surname":inputJSON.surname,
    "register_date": now,
    "vaccination_date": nxt}

    return JSONResponse(content={"id":app.id, 
    "name":inputJSON.name,
    "surname":inputJSON.surname,
    "register_date": now,
    "vaccination_date": nxt}, status_code=status.HTTP_201_CREATED)

@app.get("/patient/{inid}")
async def access_record(inid):
    inid =int(inid)
    print((inid, type(inid)))
    print(app.records)
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

@app.get("/hello", response_class=HTMLResponse)
async def helloer(request: Request):
    now=datetime.datetime.today()
    now = str(now.year)+"-"+str(now.month).rjust(2,'0')+"-"+str(now.day).rjust(2,'0')
    return templates.TemplateResponse("ninja21.html.j2", {"request": request, "now":now})


@app.post("/login_session")
async def establish_session(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    l="4dm1n"
    p="NotSoSecurePa$$"
    if  l == credentials.username and credentials.password==p:
        #return Response(status_code=status.HTTP_202_ACCEPTED)
        response.set_cookie(key="session_token", value="rather epic content of session cookie")
        response.status_code=status.HTTP_201_CREATED
    else:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED )


@app.post("/login_token")
async def give_cookie(credentials: HTTPBasicCredentials = Depends(security), session_token: str = Cookie(None)):
    l="4dm1n"
    p="NotSoSecurePa$$"
    if  l == credentials.username and credentials.password==p:
        #return Response(status_code=status.HTTP_202_ACCEPTED)
        return JSONResponse(content={"token": session_token}, status_code= status.HTTP_201_CREATED)
    else:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)



@app.get("/welcome_session")
async def welcome_sessioner( format:Optional[str]=None, session_token: str = Cookie(None)):
    print(session_token)
    print(format)
    if session_token=="rather epic content of session cookie":
        if format=="json":
            return JSONResponse(content={"message": "Welcome!"})
        elif format=="html":
            return HTMLResponse(content="<h1>Welcome!</h1>",)
        else:
            return PlainTextResponse(content="Welcome!")
    else:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)



@app.get("/welcome_token")
async def welcome_tokener(token:str, format:Optional[str]=None):
    if token=="rather epic content of session cookie":
        if format=="json":
            return JSONResponse(content={"message": "Welcome!"})
        elif format=="html":
            return HTMLResponse(content="<h1>Welcome!</h1>",)
        else:
            return PlainTextResponse(content="Welcome!")
    else:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
