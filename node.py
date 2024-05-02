import asyncio 

class Node:
    def __init__(self, id, task, send_output_to=[], receive_input_from=[], sim_id=0):
        self.sim_id = sim_id
        self.id = id
        self.inputs = []
        self.output = None
        self.evaluation = None
        self.send_output_to = send_output_to
        self.receive_input_from = receive_input_from
        self.task = task
        self.input_event = asyncio.Event()

    async def process(self):
        self.output = await asyncio.to_thread(self.task.execute, self.inputs)
        self.send_output()
        print("Processed", self.send_output_to)

    async def evaluate(self):
        self.evaluation = await asyncio.to_thread(self.task.evaluate, self.output)
        print("Evaluated: ", self.sim_id, self.id)

    async def start(self):
        if len(self.inputs) != len(self.receive_input_from):
            # wait for the inputs to be available
            await self.input_event.wait()

        if self.output is None:
            await self.process()

        if self.evaluation is None:
            await self.evaluate()
        return True

    def receive_input(self, input):
        self.inputs.append(input)
        if len(self.inputs) == len(self.receive_input_from):
            self.input_event.set()

    def send_output(self):
        assert self.output is not None, "NotExpected: Sending None as ouptut"
        
        for node in self.send_output_to:
            node.receive_input(self.output)

    def __repr__(self):
        incoming_nodes = ", ".join(str(x.id) for x in self.receive_input_from)
        outgoing_nodes = ", ".join(str(x.id) for x in self.send_output_to)
        return f"Sim:{self.sim_id} ID:{self.id}\tIncoming nodes: [{incoming_nodes}]\tOutgoing nodes: [{outgoing_nodes}]"