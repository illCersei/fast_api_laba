from fastapi import FastAPI
from app.api.endpoints import usersAuth
import uvicorn


app = FastAPI()

app.include_router(usersAuth.router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
