import PlantsimBackend.config as config
import simpy
import PlantsimBackend.config as config
from PlantsimBackend.entities.Source import Source
from PlantsimBackend.entities.Station import Station
from PlantsimBackend.entities.Conveyor import Conveyor
from PlantsimBackend.entities.Drain import Drain
class Simulator:
    def __init__(self):
        self.env=config.env

    def StartSimulation(self,Time):
        
        for source in config.Sources:
            config.env.process(source.Generate())
        
        config.env.run(until=Time)