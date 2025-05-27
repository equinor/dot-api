import uvicorn
from fastapi import FastAPI, status
import src.routes.decision_routes as decision_routes
import src.routes.edge_routes as edge_routes
import src.routes.scenario_routes as scenario_routes
import src.routes.node_routes as node_routes
import src.routes.objective_routes as objective_routes
import src.routes.opportunity_routes as opportunity_routes
import src.routes.probability_routes as probability_routes
import src.routes.project_routes as project_routes

app = FastAPI()

@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Welcome to the DOT api"}

app.include_router(decision_routes.router)
app.include_router(edge_routes.router)
app.include_router(scenario_routes.router)
app.include_router(node_routes.router)
app.include_router(objective_routes.router)
app.include_router(opportunity_routes.router)
app.include_router(probability_routes.router)
app.include_router(project_routes.router)

if __name__ == "__main__":
    uvicorn.run("src.main:app", port=8080)