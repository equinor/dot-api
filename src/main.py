import uvicorn
from fastapi import FastAPI, status
import src.routes.decision_routes as decision_routes

app = FastAPI()

@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Welcome to the DOT api"}

app.include_router(decision_routes.router)

if __name__ == "__main__":
    uvicorn.run("src.main:app", port=8080)