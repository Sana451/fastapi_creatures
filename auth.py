import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

secret_user: str = "sana"
secret_password: str = "password"

basic = HTTPBasic()


@app.get("/who")
def get_user(credentials: HTTPBasicCredentials = Depends(basic)) -> dict:
    if (credentials.username == secret_user and
            credentials.password == secret_password):
        return {"username": credentials.username, "password": credentials.password}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Hey!")


if __name__ == '__main__':
    uvicorn.run("auth:app", reload=True)
