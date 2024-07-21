from fastapi import FastAPI

from fastzero.routers.auth import router as auth_router
from fastzero.routers.todos import router as todos_router
from fastzero.routers.users import router as users_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(todos_router)

@app.get("/")
def root():
    return {"message": "Olá Mundo!"}