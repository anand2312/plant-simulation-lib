import PlantsimBackend.config as config
import simpy
import random
class Conveyor:
    def __init__(self,id:str|None,speed:int,length:int,capacity:int,strategy:str):
        self.id=id
        self.speed=speed
        self.length=length
        self.capacity=capacity
        self.env=config.env
        self.resource=simpy.Resource(env=self.env,capacity=self.capacity)
        self.outputs=[]
        self.OrdersProcessed=0
        self.processingTime=((length+(speed-1))/speed)
        self.strategy=strategy
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
        print("Drain", self.id,"Recieved: ", self.OrdersRecieved,"Orders")
        print("Drain", self.id,"Processed: ", self.OrdersProcessed,"Orders")