from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import simpy
env=simpy.Environment()
import PlantsimBackend.config as config

import PlantsimBackend.Backend.Builder as Builder
import PlantsimBackend.Simulations.Simulator as Simulator
app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def root():
    print("Hello")
    return {"Hello": "World"}


@app.post("/submit-flow")
def submit_flow(flow:dict):
    # components = flow.get("components", [])
    
    # # Extract nodes and edges
    # nodes = []
    # edges = []
    
    # for component in components:
    #     comp_type = component.get("type", "")
        
    #     if comp_type != "edge":
    #         # Extract node parameters
    #         node_info = {
    #             "id": component.get("id", ""),
    #             "type": comp_type,
    #             "parameters": {}
    #         }
            
    #         # Extract all parameters from data
    #         if "data" in component:
    #             data = component["data"]
    #             # Add all data fields as parameters
    #             for key, value in data.items():
    #                 if(key=='label' or key=='color'):
    #                     continue
    #                 node_info["parameters"][key] = value
                
    #         nodes.append(node_info)
    #     else:
    #         # Extract edge parameters
    #         edge_info = {
    #             "id": component.get("id", ""),
    #             "type": "edge",
    #             "parameters": {
    #                 "source": component.get("source", ""),
    #                 "target": component.get("target", "")
    #             }
    #         }
    #         edges.append(edge_info)
    
    # # Combine all components
    # all_components = nodes
    
    # # Print for debugging
    # print(f"Extracted {len(nodes)} nodes and {len(edges)} edges")
    # print(all_components)
    builder=Builder.PlantBuilder()
    builder.ParsePlantInfo(flow)
    builder.Initialize()
    print("Success")
    # print(config.Sources)
    # print(config.Drains)
    sim=Simulator.Simulator()
    sim.StartSimulation(100)
    for source in config.Sources:
        source.PrintStatistics()
    
    for conveyor in config.Conveyors:
        conveyor.PrintStatistics()
    
    for station in config.Stations:
        station.PrintStatistics()
    
    for drain in config.Drains:
        drain.PrintStatistics()
    return {
        "success": True,
        # "components": all_components
    }