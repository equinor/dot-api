import uvicorn
from fastapi import FastAPI, status,Depends
from src.auth.auth import verify_token
import src.routes.decision_routes as decision_routes
import src.routes.edge_routes as edge_routes
import src.routes.scenario_routes as scenario_routes
import src.routes.node_routes as node_routes
import src.routes.objective_routes as objective_routes
import src.routes.opportunity_routes as opportunity_routes
import src.routes.uncertainty_routes as uncertainty_routes
import src.routes.utility_routes as utility_routes
import src.routes.value_metric_routes as value_metric_routes
import src.routes.project_routes as project_routes
import src.routes.issue_routes as issue_routes
from src.config import Config
from fastapi.middleware.cors import CORSMiddleware

config = Config()

app = FastAPI(swagger_ui_init_oauth={
        "usePkceWithAuthorizationCodeGrant": True,
        "clientId": config.CLIENT_ID,
        "redirectUrl": "http://localhost:8000/docs/oauth2-redirect",
    },)



# Adding CORS middleware to the FastAPI application
app.add_middleware(
CORSMiddleware,
allow_origins=config.ORIGINS, # List of allowed origins
allow_credentials=True, # Allow credentials (cookies, authorization headers, etc.)
allow_methods=["*"], # Allow all HTTP methods
allow_headers=["*"], # Allow all HTTP headers
)

@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Welcome to the DOT api"}

app.include_router(decision_routes.router, dependencies=[Depends(verify_token)])
app.include_router(edge_routes.router, dependencies=[Depends(verify_token)])
app.include_router(scenario_routes.router, dependencies=[Depends(verify_token)])
app.include_router(node_routes.router, dependencies=[Depends(verify_token)])
app.include_router(objective_routes.router, dependencies=[Depends(verify_token)])
app.include_router(opportunity_routes.router, dependencies=[Depends(verify_token)])
app.include_router(uncertainty_routes.router, dependencies=[Depends(verify_token)])
app.include_router(utility_routes.router, dependencies=[Depends(verify_token)])
app.include_router(value_metric_routes.router, dependencies=[Depends(verify_token)])
app.include_router(project_routes.router, dependencies=[Depends(verify_token)])
app.include_router(issue_routes.router, dependencies=[Depends(verify_token)])

if __name__ == "__main__":
    uvicorn.run("src.main:app", port=8080)