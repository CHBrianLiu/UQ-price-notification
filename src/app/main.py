import fastapi

from src.app import routes

app = fastapi.FastAPI()

app.include_router(routes.router)
