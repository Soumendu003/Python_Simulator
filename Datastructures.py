
class Entity():

    def __init__(self,name):

        self.name=name

        self.ports=[]


class Process:

    def __init__(self):

        self.timer=0

        self.Hash_Val=-1

        self.Id=[]

        self.Look_up_count=0

        self.Look_up_table_dict={}                     # { Lighweight_Signal_index : Look_up_table_index }   # Delay key =-1

        self.execution_contex=0

        self.instructions=[]

        self.Instruction_Start = -1
        self.Instruction_End = -1



class Signal:

    def __init__(self):

        self.value='U'

        self.name=''

        self.Hash_Val=-1                # Corresponding Index of Signal in Light_Signal Array

        self.hash=''

        self.Driver={}      # Make a mapping from process to  here   { Process_Hash : process_object }

        self.Delay_Driver = []

        self.processes=[]

        self.Driving_Head = -1

        self.Driving_Count = 0

        self.Triggering_Process_Start = -1
    

class Time:

    def __init__(self):

        self.value=0

        self.processes=[]

        self.Delayed_Head=0
        self.Delayed_Assignment={}         # Every Instruction Which Has Delayed Assignment sends { index : [Signal_hash,Value,Delay] }

        self.Events=[[0]]