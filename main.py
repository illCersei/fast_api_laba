from fastapi import FastAPI
from app.api.endpoints import usersAuth
import uvicorn
from app.api.endpoints import ws 


app = FastAPI()

app.include_router(usersAuth.router)
app.include_router(ws.router) 

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
