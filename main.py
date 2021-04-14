import hashlib
from fastapi import FastAPI, Response, status
from pydantic import BaseModel

app = FastAPI()
app.counter = 0


class HelloResp(BaseModel):
    msg:str

@app.get("/")
def root():
    return {"message": "Hello World"}


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
# @app.get("/hello/{name}", response_model=HelloResp)
# async def read_item(name: str):
#     return HelloResp(msg=f"Hello {name}")


# @app.get('/counter')
# def counter():
#     app.counter += 1
#     return app.counter