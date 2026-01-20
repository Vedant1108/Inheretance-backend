from fastapi import FastAPI
from routes.records import router as records_router
from routes.access import router as access_router

app = FastAPI()

app.include_router(records_router)

app.include_router(access_router)
