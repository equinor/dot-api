import uvicorn
from fastapi import FastAPI, status,Depends
from src.auth.auth import verify_token
import src.routes.decision_routes as decision_routes
import src.routes.edge_routes as edge_routes
import src.routes.graph_routes as graph_routes
import src.routes.node_routes as node_routes
import src.routes.objective_routes as objective_routes
import src.routes.opportunity_routes as opportunity_routes
import src.routes.probability_routes as probability_routes
import src.routes.project_routes as project_routes

from src.config import Config

config = Config()

app = FastAPI(swagger_ui_init_oauth={
        "usePkceWithAuthorizationCodeGrant": True,
        "clientId": config.CLIENT_ID,
        "redirectUrl": "http://localhost:8000/docs/oauth2-redirect",
    },)


@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Welcome to the DOT api"}

app.include_router(decision_routes.router,dependencies=[Depends(verify_token)])
app.include_router(edge_routes.router,dependencies=[Depends(verify_token)])
app.include_router(graph_routes.router,dependencies=[Depends(verify_token)])
app.include_router(node_routes.router,dependencies=[Depends(verify_token)])
app.include_router(objective_routes.router,dependencies=[Depends(verify_token)])
app.include_router(opportunity_routes.router,dependencies=[Depends(verify_token)])
app.include_router(probability_routes.router,dependencies=[Depends(verify_token)])
app.include_router(project_routes.router,dependencies=[Depends(verify_token)])

if __name__ == "__main__":
    uvicorn.run("src.main:app", port=8080)