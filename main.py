from hashlib import sha256
import datetime
from fastapi import FastAPI, Response, status, Request, Depends, Cookie, HTTPException
from typing import Optional
from pydantic import BaseModel
from fastapi.responses import JSONResponse, HTMLResponse, PlainTextResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
security = HTTPBasic()
templates = Jinja2Templates(directory="templates")
app.counter = 0
app.id=0
app.records={}
app.secret_key = "placeholder secret"
app.access_tokens = []
app.token_values=[]

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


@app.get("/hello", response_class=HTMLResponse)
async def helloer(request: Request):
    now=datetime.datetime.today()
    now = str(now.year)+"-"+str(now.month).rjust(2,'0')+"-"+str(now.day).rjust(2,'0')
    return templates.TemplateResponse("ninja21.html.j2", {"request": request, "now":now})


@app.post("/login_session")
async def establish_session(request:Request,response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    l="4dm1n"
    p="NotSoSecurePa$$"
    if  l == credentials.username and credentials.password==p:
        session_token=sha256(f"{app.secret_key}{credentials.username}{credentials.password}{datetime.datetime.today()}".encode()).hexdigest()
        app.access_tokens.append(session_token)
        if len(app.access_tokens) ==4:
            app.access_tokens= app.access_tokens[1:]
        response.set_cookie(key="session_token", value=session_token)
        response.status_code=status.HTTP_201_CREATED
    else:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED )


@app.post("/login_token")
async def give_cookie(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    l="4dm1n"
    p="NotSoSecurePa$$"
    if  l == credentials.username and credentials.password==p:
        token_value=sha256(f"{app.secret_key}{credentials.username}{credentials.password}{datetime.datetime.today()}".encode()).hexdigest()
        app.token_values.append(token_value)
        if len(app.token_values)==4:
            app.token_values= app.token_values[1:]
        return JSONResponse(content={"token": token_value}, status_code= status.HTTP_201_CREATED)
    else:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)



@app.get("/welcome_session")
async def welcome_sessioner(response: Response,  session_token: str = Cookie(None), format:Optional[str]=None):
    #print(session_token)
    #print(format)
    #print(request.cookies)
    if session_token in app.access_tokens:
        if format=="json":
            return JSONResponse(content={"message": "Welcome!"})
        elif format=="html":
            return HTMLResponse(content="<h1>Welcome!</h1>",)
        else:
            return PlainTextResponse(content="Welcome!")
    else:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)



@app.get("/welcome_token")
async def welcome_tokener(response: Response, token:str, format:Optional[str]=None):
    if token in app.token_values:
        if format=="json":
            return JSONResponse(content={"message": "Welcome!"})
        elif format=="html":
            return HTMLResponse(content="<h1>Welcome!</h1>",)
        else:
            return PlainTextResponse(content="Welcome!")
    else:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)


@app.delete("/logout_session")
async def logout_sessioner(response: Response,  session_token: str = Cookie(None), format:Optional[str]=None):

    if session_token in app.access_tokens:
        app.access_tokens.remove[session_token]
        return RedirectResponse("https://daftacademy-initial.herokuapp.com/logged_out", status_code=status.HTTP_302_FOUND)
    else:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)



@app.delete("/logout_token")
async def logout_tokener(response: Response, token:str, format:Optional[str]=None):
    if token in app.token_values:
        app.token_values.remove[token]
        return RedirectResponse("https://daftacademy-initial.herokuapp.com/logged_out", status_code=status.HTTP_302_FOUND)
    else:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)



@app.get("/logged_out")
async def logout_logout(response: Response, format:Optional[str]=None):
    if format=="json":
            return JSONResponse(content={"message": "Logged out!"})
    elif format=="html":
            return HTMLResponse(content="<h1>Logged out!</h1>")
    else:
            return PlainTextResponse(content="Logged out!")

