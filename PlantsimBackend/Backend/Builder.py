from PlantsimBackend.entities.Source import Source 
from PlantsimBackend.entities.Station import Station
from PlantsimBackend.entities.Drain import Drain
from PlantsimBackend.entities.Conveyor import Conveyor
import PlantsimBackend.config as config

class PlantBuilder:
    def __init__(self):
        self.components=[]
    
    def ParsePlantInfo(self,flow:dict):
        components = flow.get("components", [])
    
    # Extract nodes and edges
        nodes = []
        edges = []
        
        for component in components:
            comp_type = component.get("type", "")
            
            if comp_type != "edge":
                # Extract node parameters
                node_info = {
                    "id": component.get("id", ""),
                    "type": comp_type,
                    "parameters": {}
                }
                
                # Extract all parameters from data
                if "data" in component:
                    data = component["data"]
                    # Add all data fields as parameters
                    for key, value in data.items():
                        if(key=='label' or key=='color'):
                            continue
                        node_info["parameters"][key] = value
                    
                nodes.append(node_info)
            else:
                # Extract edge parameters
                edge_info = {
                    "id": component.get("id", ""),
                    "type": "edge",
                    "parameters": {
                        "source": component.get("source", ""),
                        "target": component.get("target", "")
                    }
                }
                edges.append(edge_info)
        
        # Combine all components
        all_components = nodes
        self.components = all_components
        return all_components
    
    def Initialize(self):
       
        component_dict = {}
        config.Sources.clear()
        config.Drains.clear()
        config.Conveyors.clear()
        config.Stations.clear()
        for component in self.components:
            if (component["type"] == "source"):
                id=component["id"]
                endTime=0
                startTime=0
                limit=0
                interval=0
                outputs=[]
                strategy=""
                for key, value in component["parameters"].items():
                    if key=="endTime":
                        endTime=int(value)
                    if key=="startTime":
                        startTime=int(value)
                    if key=="limit":
                        limit=int(value)
                    if key=="interval":
                        interval=int(value)
                    if(key=="outputs"):
                        outputs=value
                    if(key=="strategy"):
                        strategy=value
                current_source=Source(limit,interval,startTime,endTime,id,strategy)
                current_source.outputs=outputs
                config.Sources.append(current_source)
                component_dict[id] = current_source
            
            elif (component["type"] == "station"):
                id=component["id"]
                capacity=0
                processingTime=0
                outputs=[]
                strategy=""
                for key, value in component["parameters"].items():
                    if key=="capacity":
                        capacity=int(value)
                    if key=="processingTime":
                        processingTime=int(value)
                    if key=="outputs":
                        outputs=value
                    if(key=="strategy"):
                        strategy=value
                current_station=Station(id,processingTime,capacity,strategy)
                current_station.outputs=outputs
                config.Stations.append(current_station)
                component_dict[id] = current_station
            
            elif (component["type"] == "drain"):
                
                id=component["id"]
                capacity=0
                processingTime=0
                
                for key, value in component["parameters"].items():
                    if key=="capacity":
                        capacity=int(value)
                    if key=="processingTime":
                        processingTime=int(value)
                    if key=="outputs":
                        outputs=value
                   
                current_drain=Drain(id,capacity,processingTime)
                current_drain.outputs=outputs
                config.Drains.append(current_drain)
                component_dict[id] = current_drain
            
            else:
                id=component["id"]
                length=0
                speed=0
                capacity=0
                outputs=[]
                strategy=""
                for key, value in component["parameters"].items():
                    if key=="length":
                        length=int(value)
                    if key=="speed":
                        speed=int(value)
                    if key=="capacity":
                        capacity=int(value)
                    if key=="outputs":
                        outputs=value
                    if key=="strategy":
                        strategy=value
                current_conveyor=Conveyor(id,speed,length,capacity,strategy)
                current_conveyor.outputs=outputs
                config.Conveyors.append(current_conveyor)
                component_dict[id] = current_conveyor
        
        for source in config.Sources:
        # Convert string IDs to component references
            resolved_outputs = []
            for output_id in source.outputs:
                if output_id in component_dict:
                    resolved_outputs.append(component_dict[output_id])
                else:
                    print(f"Warning: Could not find component with ID {output_id}")
            source.outputs = resolved_outputs
    
        for station in config.Stations:
            # Convert string IDs to component references
            resolved_outputs = []
            for output_id in station.outputs:
                if output_id in component_dict:
                    resolved_outputs.append(component_dict[output_id])
                else:
                    print(f"Warning: Could not find component with ID {output_id}")
            station.outputs = resolved_outputs
        
        # Do the same for other component types
        for conveyor in config.Conveyors:
            resolved_outputs = []
            for output_id in conveyor.outputs:
                if output_id in component_dict:
                    resolved_outputs.append(component_dict[output_id])
                else:
                    print(f"Warning: Could not find component with ID {output_id}")
            conveyor.outputs = resolved_outputs

        for drain in config.Drains:
            resolved_outputs = []
            for output_id in drain.outputs:
                if output_id in component_dict:
                    resolved_outputs.append(component_dict[output_id])
                else:
                    print(f"Warning: Could not find component with ID {output_id}")
            drain.outputs = resolved_outputs