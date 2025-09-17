import PlantsimBackend.config as config
import simpy
import random
class Drain:
    def __init__(self,id:str|None,capacity:int,processingTime:int):
        self.capacity=capacity
        self.processingTime=processingTime
        self.id = id
        self.env=config.env
        self.resource=simpy.Resource(env=self.env,capacity=self.capacity)
        self.OrdersProcessed=0
        self.OrdersRecieved=0
        
    def Process_Order(self,order):
         with self.resource.request() as request:
            # Wait until the resource becomes available
            self.OrdersRecieved+=1
            yield request
            
            # Process the order (this takes processing_time)
            
            yield self.env.timeout(self.processingTime)
            
            # Update the order with processing information
           
            self.OrdersProcessed += 1
            
            # Send the order to the next component(s)

    def PrintStatistics(self):
        print("Drain", self.id,"Recieved: ", self.OrdersRecieved,"Orders")
        print("Drain", self.id,"Processed: ", self.OrdersProcessed,"Orders")