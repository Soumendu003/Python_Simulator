import numpy as np
import Lighweight_Functions as LF

'''
    Id of Signal == 0
    Id of Process == 1
'''

class Light_Time:

    def __init__(self,time):

        self.value=0

        self.Delayed_Assignment=np.ndarray((len(time.Delayed_Assignment),),dtype=[('Id','i1'),('Sig_Hash','i4'),('Value','i1'),('Delay','i4')])

        self.Triggered_Process=np.ndarray((len(time.processes),),dtype=[('Id','i1'),('Pro_Hash','i4')])

        self.Event_list=[[0]]


class Event:

    def __init__(self):

        self.Process_Event_Hash_Map=None

        self.Process_Event_Head=-1

        self.Process_Events=None                 # Hash Val of the Processes to be triggered are stored

        self.Signal_Update_Event_Head=-1

        self.Signal_Update_Events=None           # Hash Val of the Signals to be triggered are stored

        self.Oprnd=[]



def Initialize(time,Entities,Signals,Process_Set):

    Signal_Event_Hash={}

    # Creates Light Signal Array
    Light_Signal=np.ndarray((len(Signals,)),dtype=[('Eff_Val','i1'),('Sig_Hash','i4'),('Driver_Head','i4'),('Processes','object'),('Process_Driver_Hash_Map','object'),('Driver','object'),('Delay_Driver','i1'),('Update_Bit','i1')])
    
    # Creates Dictionary to store map from Signal Hash to Signal Name
    Signal_To_Signal_Name={}

    '''
        Initializes Effective Value of each Signal
        Sets Hash Val of Each Signal
        Sets Default Driver Head to -1
        Creates triggering process array
        Stores Signal_hash to Signal_Name in Dictionary
    '''

    i=-1
    for signal in Signals.values():

        i+=1

        Light_Signal[i][0]=-4                         # Sets Effective Value 0 (i.e 'U')
        Light_Signal[i][1]=i                         # Sets Signal Hash as its index in Signal Array
        Light_Signal[i][2]=-1                        # Default Driver Head is -1
        Light_Signal[i][3]=np.ndarray((len(signal.processes),),dtype='i4')   # Creates a Array to store sensitive Process Hash **
        Light_Signal[i]['Delay_Driver']=-8             # Defalut value is 'Z'
        Light_Signal[i]['Update_Bit']=0                # By Default no update required

        Signal_To_Signal_Name.update({i:signal.name})

        signal.Hash_Val=i

    # Creates Light Process Array
    Light_Process=np.ndarray((len(Process_Set),),dtype=[('Process_Hash','i4'),('Execution_Context','i4'),('Instructions','object'),('Look_Up_Table','object'),('Delay_index','i4')])

    '''
        Sets Process Hash
        Sets Execution Context of Each Process
    ''' 
    i=-1
    for process in Process_Set:

        i+=1

        Light_Process[i][0]=i                       # Sets Process Hash as its index in Process Array
        Light_Process[i][1]=0                       # Sets Execution Context 0
        Light_Process[i][2]=np.ndarray((len(process.instructions),),dtype=object) # creates a pointer array to each Instruction
        process.Hash_Val=i

    # Parses Instruction In Lighweight Manner
    LF.Parse_Light_Instructions(time,Process_Set,Signals,Light_Process)

    ''' 
        Updates Look Up Table of Each Process
        Creats Driver Array of Each Signal
        Created Driver Hash Map of each Signal
        Updated Process Triggered
    ''' 

    i=-1
    for signal in Signals.values():

        i+=1

        LF.Update_Process_Triggered(signal,Light_Signal,Signal_Event_Hash)        

        if(-1 in signal.Driver):
            Light_Signal[i]['Driver']=np.ndarray((len(signal.Driver)-1,),dtype=[('Process_Hash','i4'),('Value','i1')])
            Light_Signal[i]['Process_Driver_Hash_Map']=np.zeros((len(signal.Driver)-1,),dtype='i4')
        else:
            Light_Signal[i]['Driver']=np.ndarray((len(signal.Driver),),dtype=[('Process_Hash','i4'),('Value','i1')])
            Light_Signal[i]['Process_Driver_Hash_Map']=np.zeros((len(signal.Driver),),dtype='i4')
        
        Light_Signal[i]['Driver'].fill((-1,0))

        index=0

        for key in signal.Driver:

            if(key!=-1):

                LF.Update_look_up_table(signal.Hash_Val,index,Light_Process,signal.Driver[key])
                index+=1
                
    light_time=Light_Time(time)

    print(time.Delayed_Assignment)

    for key in time.Delayed_Assignment:

        light_time.Delayed_Assignment[key]['Id']=0
        light_time.Delayed_Assignment[key]['Sig_Hash']=time.Delayed_Assignment[key][0]
        light_time.Delayed_Assignment[key]['Delay']=time.Delayed_Assignment[key][2]

    print(light_time.Delayed_Assignment)

    i=-1
    for process in time.processes:

        i+=1
        light_time.Triggered_Process[i]['Id']=1
        light_time.Triggered_Process[i]['Pro_Hash']=process.Hash_Val
        Light_Process[process.Hash_Val]['Delay_index']=i

    event=Event()

    event.Process_Event_Hash_Map=np.zeros((len(Signal_Event_Hash),),dtype=[('Process_Hash','i4'),('Process_Event_Index','i4')])
    event.Process_Events=np.zeros((len(Signal_Event_Hash),),dtype='i4')
    event.Signal_Update_Events=np.zeros((len(Signals),),dtype='i4')

    i=-1
    for key in Signal_Event_Hash:

        i+=1
        Signal_Event_Hash[key]=i
        event.Process_Event_Hash_Map[i][0]=key

    # Updates Triggering Process Hash of Each Signal    
    LF.Update_Signal_Event_Hash(Light_Signal,Signal_Event_Hash)


    # Initialises the Event_list of Light_time object

    for i in range(0,light_time.Triggered_Process.shape[0]):

        light_time.Event_list[0].append(light_time.Triggered_Process[i])

    #print(light_time.Event_list)

    return Signal_To_Signal_Name,event,light_time,Light_Signal,Light_Process



    


