import numpy as np

'''
    not == -1
    and == -2
    or == -3
    'U' == -4
    'X' == -5
    '0' == -6
    '1' == -7
    'Z' == -8

    signal >=0
'''


def get_Light_postfix(ret,i,ins,Signals):

    for ele in ins:

        if(ele=='and'):
            ret[i]=-2
        elif(ele=='not'):
            ret[i]=-1
        elif(ele=='or'):
            ret[i]=-3
        elif(ele=="Val'U'"):
            ret[i]=-4
        elif(ele=="Val'X'"):
            ret[i]=-5
        elif(ele=="Val'0'"):
            ret[i]=-6
        elif(ele=="Val'1'"):
            ret[i]=-7
        elif(ele=="Val'Z'"):
            ret[i]=-8
        else:
            ret[i]=Signals[int(ele)].Hash_Val

        i+=1


'''    wait == -1
       <= == -2
       Delay == -3
'''


def get_Instruction(ins,Signals,process,time):
    
    count=0
    #print(ins)

    if(ins[0]=='wait'):
        count=2

        ret=np.ndarray((count,),dtype='i4')
        ret[0] = -1
        ret[1] = int(ins[1])

    elif(ins[0]=='<='):
        count=2
        count+=len(ins[2])

        ret = np.ndarray((count,),dtype='i4')

        ret[0] = -2

        sig_hash=Signals[int(ins[1])].Hash_Val                   # Gets the Light_Signal index of the corresponding signal

        Signals[int(ins[1])].Driver.update({process.Hash_Val:process})      # Register for a driver 

        ''' Gets the Look up Table index of the Corresponding Signal '''

        if(sig_hash in process.Look_up_table_dict):

            ret[1] = process.Look_up_table_dict[sig_hash]
        else:
            ret[1] = process.Look_up_count                                            
            process.Look_up_table_dict.update({sig_hash:process.Look_up_count})
            process.Look_up_count+=1

        get_Light_postfix(ret,2,ins[2],Signals)

    elif(ins[0]=='Delay'):

        count=2
        count+=len(ins[2])
        ret = np.ndarray((count,),dtype='i4')

        ret[0]=-3
        sig_hash=Signals[int(ins[1])].Hash_Val                    # stores the Light_Signal array index of corresponding signal

        Signals[int(ins[1])].Driver.update({-1:process})            # Register for a delay driver

        ret[1]=int(time.Delayed_Head)                            # Stores the Delayed Assignment array index in light time object 

        time.Delayed_Assignment.update({time.Delayed_Head:[sig_hash,'Z',int(ins[3])]})

        time.Delayed_Head+=1

        get_Light_postfix(ret,2,ins[2],Signals)

    return ret




def Parse_Light_Instructions(time,Process_Set,Signals,Light_Process):

    for process in Process_Set:

        #print("Val = "+str(process.Hash_Val)+"\t val="+str(Light_Process[process.Hash_Val][0]))

        #print("Process id ="+str(process.Id))

        #print("Total Instructions = "+str(len(process.instructions)))
        #print("Instruction Array Len = "+str(Light_Process[process.Hash_Val]['Instructions'].shape[0]))
        i=0
        for ins in process.instructions:

            Light_Process[process.Hash_Val]['Instructions'][i]=get_Instruction(ins,Signals,process,time)
            #print(Light_Process[process.Hash_Val]['Instructions'][i])
            i+=1
            #print("Len = "+str(count))

        Light_Process[process.Hash_Val]['Look_Up_Table']=np.ndarray((len(process.Look_up_table_dict),2),dtype='i4')



def Update_look_up_table(signal_hash,driver_map_index,Light_Process,process):

    index=process.Look_up_table_dict[signal_hash]

    Light_Process[process.Hash_Val]['Look_Up_Table'][index][0]=signal_hash

    Light_Process[process.Hash_Val]['Look_Up_Table'][index][1]=driver_map_index


def Update_Process_Triggered(signal,Light_Signal,Signal_Event_Hash):

    i=-1
    for process in signal.processes:

        i+=1

        Light_Signal[signal.Hash_Val]['Processes'][i]=process[1].Hash_Val
        Signal_Event_Hash.update({process[1].Hash_Val:-1})
    
    #print(Light_Signal[signal.Hash_Val]['Processes'])

def Update_Signal_Event_Hash(Light_Signal,Signal_Event_Hash):

    for i in range(0,Light_Signal.shape[0]):

        for j in range(0,Light_Signal[i]['Processes'].shape[0]):
            Light_Signal[i]['Processes'][j]=Signal_Event_Hash[Light_Signal[i]['Processes'][j]]
        
        #print(Light_Signal[i]['Processes'])