import PlantsimBackend.config as config
import simpy
import random
class Station:
    def __init__(self,id:str|None,processingTime:int,capacity:int,strategy:str):
        self.processingTime = processingTime
        self.outputs = []
        self.capacity = capacity
        self.id = id
        self.env=config.env
        self.strategy=strategy
        self.resource=simpy.Resource(env=self.env,capacity=self.capacity)
        self.OrdersProcessed=0
        self.OrdersRecieved=0

    def Process_Order(self,order):
        with self.resource.request() as request:
            self.OrdersRecieved+=1
            # Wait until the resource becomes available
            
            yield request
            
            # Process the order (this takes processing_time)
            # print(" Station", self.id, "Processing At ",config.env.now)
            yield self.env.timeout(self.processingTime)
            # print(" Station", self.id, "Ending At ",config.env.now)
            # Update the order with processing information
           
            self.OrdersProcessed += 1
            self.send_to_outputs(order)
            # Send the order to the next component(s)

    def send_to_outputs(self, order):
        if(len(self.outputs)==0):
            raise IndexError("No output connections")
        if not hasattr(self, 'last_output_index'):
            self.last_output_index = -1
        
        if self.strategy == "RoundRobin":
            # Round-robin selection
            self.last_output_index = (self.last_output_index + 1) % len(self.outputs)
            output = self.outputs[self.last_output_index]
        elif self.strategy == "Random":
            # Random selection
        
            output = random.choice(self.outputs)
        else:
            output=self.outputs[0]
        self.env.process(output.Process_Order(order))
    def PrintStatistics(self):
        print("Station", self.id,"Recieved: ", self.OrdersRecieved,"Orders")
        print("Station", self.id,"Processed: ", self.OrdersProcessed,"Orders")