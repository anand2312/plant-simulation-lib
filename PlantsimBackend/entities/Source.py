import PlantsimBackend.config as config
import random
class Source:
    def __init__(self,limit:int,interval:int,startTime:int,endTime:int,id:str|None,strategy:str):
        self.limit = limit
        self.interval = interval
        self.startTime = startTime
        self.endTime = endTime
        self.OrdersGenerated=0
        self.OrdersPushedOut=0
        self.env=config.env
        self.outputs=[]
        self.strategy=strategy
        self.id=id
        

    def Generate(self):
        if self.startTime>0:
            yield self.env.timeout(self.startTime)
        
        while True:
            if self.limit is not None and self.OrdersGenerated >= self.limit:
                break
                
            # Check if we've reached the end time
            if self.endTime is not None and self.env.now >= self.endTime:
                break
                
            # Create a new order
            order = self.Create_MU()
            # order=self.env.process(self.create_MU)
            self.OrdersGenerated += 1
            
            # Send to next component(s)
            self.send_to_outputs(order)
            
            # Wait for the interval before next generation
            yield self.env.timeout(self.interval)

    def Create_MU(self):
         return {
            "id": f"order_{self.OrdersGenerated}",
            "created_at": self.env.now,
            "source": self.id
        }

    def send_to_outputs(self, order):
        """Send the order to all output connections"""
        # This would be implemented based on your connection logic
        # For now, just yield a timeout of 0
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
        print("Source",self.id," Generated: ", self.OrdersGenerated," Orders")