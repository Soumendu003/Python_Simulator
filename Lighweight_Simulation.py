import numpy as np
import sys

look_up_table=[
    ['U','X','0','1','U'],
    ['U','X','X','X','X'],
    ['U','X','0','X','0'],
    ['U','X','X','1','1'],
    ['U','X','0','1','Z']]

index_table={'U':0,'X':1,'0':2,'1':3,'Z':4}

'''
    not == -1
    and == -2
    or == -3
    'U' == -4
    'X' == -5
    '0' == -6
    '1' == -7
    'Z' == -8

    Value of Signal == 0 means Empty Assignment

    signal >=0
'''

Light_look_up_table=[
    [-4,-5,-6,-7,-4],
    [-4,-5,-5,-5,-5],
    [-4,-5,-6,-5,-6],
    [-4,-5,-5,-7,-7],
    [-4,-5,-6,-7,-8]]

def Light_index_table(a):

    if(a <= -4 and a>= -8 ):

        return (a+4)*-1

def Resolve_Value(a,b):

    return Light_look_up_table[Light_index_table(a)][Light_index_table(b)]


def Put_Value_in_Driver(Signal_Hash,Signal_Driver_index,value,event,Light_Signal):

    if(Light_Signal[Signal_Hash]['Update_Bit']==0):

        Light_Signal[Signal_Hash]['Update_Bit']=1

        Light_Signal[Signal_Hash]['Driver_Head']=0

        Light_Signal[Signal_Hash]['Process_Driver_Hash_Map'][Signal_Driver_index]=0

        Light_Signal[Signal_Hash]['Driver'][0][0]=Signal_Driver_index
        Light_Signal[Signal_Hash]['Driver'][0][1]=value

        event.Signal_Update_Event_Head+=1

        event.Signal_Update_Events[event.Signal_Update_Event_Head]=Signal_Hash

    
    else:

        Driver_Head=Light_Signal[Signal_Hash]['Driver_Head']

        Process_Driver_index=Light_Signal[Signal_Hash]['Process_Driver_Hash_Map'][Signal_Driver_index]

        if(Process_Driver_index>Driver_Head):

            Light_Signal[Signal_Hash]['Driver_Head']+=1

            Light_Signal[Signal_Hash]['Process_Driver_Hash_Map'][Signal_Driver_index]=Light_Signal[Signal_Hash]['Driver_Head']

            Light_Signal[Signal_Hash]['Driver'][Light_Signal[Signal_Hash]['Driver_Head']][0]=Signal_Driver_index
            Light_Signal[Signal_Hash]['Driver'][Light_Signal[Signal_Hash]['Driver_Head']][1]=value

        else:

            if(Light_Signal[Signal_Hash]['Driver'][Process_Driver_index][0]==Signal_Driver_index):

                Light_Signal[Signal_Hash]['Driver'][Process_Driver_index][1]=value
            
            else:

                Light_Signal[Signal_Hash]['Driver_Head']+=1

                Light_Signal[Signal_Hash]['Process_Driver_Hash_Map'][Signal_Driver_index]=Light_Signal[Signal_Hash]['Driver_Head']

                Light_Signal[Signal_Hash]['Driver'][Light_Signal[Signal_Hash]['Driver_Head']][0]=Signal_Driver_index
                Light_Signal[Signal_Hash]['Driver'][Light_Signal[Signal_Hash]['Driver_Head']][1]=value


def not_operation(a):

    if(a == -4 or a == -5):
         return -5
    
    if(a == -6 ):
        return -7
    
    if(a == -7 ):
        return -6
    
    return a

def and_operation(a,b):

    if(a== -4  and b == -4 ):
        return -5
    
    elif(a== -6 or b== -6 ):
        return -6
    
    elif(a== -5 or b== -5 ):
        return -5

    else:
        return -7

def or_operation(a,b):

    if(a== -7  or b== -7 ):
        return -7
    
    elif(a== -5 or b== -5 ):
        return -5

    elif(a== -4 and b== -4 ):
        return -5

    else:
        return -6

def Get_Value(instruction,index,Light_Signal,Light_Process,oprnd):

    del oprnd[:]
    #print("Operand Stack address = "+str(hex(id(oprnd))))

    for i in range(index,instruction.shape[0]):

        if(instruction[i]>=0):                              # Signal Hash

            Value=Light_Signal[instruction[i]]['Eff_Val']

            #print("Value got = "+str(Value)+"\t From Signal = "+str(instruction[i]))

            oprnd.append(np.int8(Value))
        
        elif(instruction[i] == -1 ):                          # Not gate

            a=oprnd.pop()

            oprnd.append(np.int8(not_operation(a)))
        
        elif(instruction[i] == -2 ):                          # And Gate

            a=oprnd.pop()
            b=oprnd.pop()

            oprnd.append(np.int8(and_operation(a,b)))

        elif(instruction[i] == -3 ):                          # Or Gate

            a=oprnd.pop()
            b=oprnd.pop()

            oprnd.append(np.int8(or_operation(a,b)))

        else:

            oprnd.append(np.int8(instruction[i]))

    Val=oprnd.pop()
    #print("Returning value = "+str(Val))
    
    return Val


def Schedule_Light_Process_Event(process_hash,Delay_Value,light_time,Light_Process):

    delay_index=Light_Process[process_hash]['Delay_index']

    obj=light_time.Triggered_Process[delay_index]

    count=0
    flag=0

    for event in light_time.Event_list:

        if(event[0]==light_time.value+Delay_Value):
            
            event.append(obj)
            flag=1
            break

        elif(event[0]>light_time.value+Delay_Value):

            light_time.Event_list.insert(count,[light_time.value+Delay_Value,obj])
            flag=1
            break

        count+=1

    if(flag==0):

        light_time.Event_list.append([light_time.value+Delay_Value,obj])

def Schedule_Delayed_Assignment_Event(Delayed_Assignment_array_index,value,light_time):

    obj=light_time.Delayed_Assignment[Delayed_Assignment_array_index]

    Delay_Value=obj['Delay']

    obj['Value']=value

    count=0
    flag=0

    for event in light_time.Event_list:

        if(event[0]==light_time.value+Delay_Value):
            
            event.append(obj)
            flag=1
            break

        elif(event[0]>light_time.value+Delay_Value):

            light_time.Event_list.insert(count,[light_time.value+Delay_Value,obj])
            flag=1
            break

        count+=1

    if(flag==0):

        light_time.Event_list.append([light_time.value+Delay_Value,obj])





def Execute_Light_Instruction(process_hash,event,light_time,Light_Signal,Light_Process):

    instruction=Light_Process[process_hash]['Instructions'][Light_Process[process_hash]['Execution_Context']]

    #print("Ins == "+str(instruction))

    if(instruction[0]==-2):                    # '<=' operation

        value = Get_Value(instruction,2,Light_Signal,Light_Process,event.Oprnd)

        Signal_Hash=Light_Process[process_hash]['Look_Up_Table'][instruction[1]][0]
        Signal_Driver_index=Light_Process[process_hash]['Look_Up_Table'][instruction[1]][1]


        Put_Value_in_Driver(Signal_Hash,Signal_Driver_index,value,event,Light_Signal)

        return 0

    elif(instruction[0]==-1):

        Delay_Value=instruction[1]

        Schedule_Light_Process_Event(process_hash,1+Delay_Value,light_time,Light_Process)

        return 1

    elif(instruction[0]==-3):

        Delayed_Assignment_array_index=instruction[1]

        value=Get_Value(instruction,2,Light_Signal,Light_Process,event.Oprnd)

        Schedule_Delayed_Assignment_Event(Delayed_Assignment_array_index,value,light_time)

        return 0


def Execute_Light_Process(process_hash,process_type,event,light_time,Light_Signal,Light_Process):

    suspend=0

    if(Light_Process[process_hash]['Execution_Context']>=Light_Process[process_hash]['Instructions'].shape[0]):

        Light_Process[process_hash]['Execution_Context']=0
    
    while(suspend==0):

        if(Light_Process[process_hash]['Execution_Context']>=Light_Process[process_hash]['Instructions'].shape[0]):

            Light_Process[process_hash]['Execution_Context']=0
            suspend=1

            if(process_type==0):

                Schedule_Light_Process_Event(process_hash,1,light_time,Light_Process)
        
        else:

            suspend=Execute_Light_Instruction(process_hash,event,light_time,Light_Signal,Light_Process)

            Light_Process[process_hash]['Execution_Context']+=1


def Resolve_Light_Signal(Signal_Hash,event,light_time,Light_Signal,Light_Process):

    final_val = -8
    flag=0
    #print("Resolving Signal = "+str(Signal_Hash))
    #print("Driver Head = "+str(Light_Signal[Signal_Hash]['Driver_Head']) )
    if(Light_Signal[Signal_Hash]['Delay_Driver'] != -8 ):
        #print("Delayed Driver Triggered")
        flag=1
        final_val = Resolve_Value(final_val,Light_Signal[Signal_Hash]['Delay_Driver'])
        Light_Signal[Signal_Hash]['Delay_Driver']=-8
    #print("Initially Final Val "+str(final_val))
    #print("initially Effective Value = "+str(Light_Signal[Signal_Hash]['Eff_Val']))
    for i in range(0,Light_Signal[Signal_Hash]['Driver_Head']+1):

        flag=1
        #print("Competing Value = "+str(Light_Signal[Signal_Hash]['Driver'][i][1]))
        final_val = Resolve_Value(final_val,Light_Signal[Signal_Hash]['Driver'][i][1])
        #print("Final Val = "+str(final_val))
        Light_Signal[Signal_Hash]['Driver'][i][1] = -8

    Light_Signal[Signal_Hash]['Driver_Head'] = -1
    Light_Signal[Signal_Hash]['Update_Bit'] = 0

    if(Light_Signal[Signal_Hash]['Eff_Val'] != final_val and flag==1 ):

        #print("Going to Change Eff Val")

        Light_Signal[Signal_Hash]['Eff_Val'] = final_val

        #print("Effective Val = "+str(Light_Signal[Signal_Hash]['Eff_Val']))

        for i in range(0,Light_Signal[Signal_Hash]['Processes'].shape[0]):

            Event_Process_Hash_Index=Light_Signal[Signal_Hash]['Processes'][i]

            Pro_Hash=event.Process_Event_Hash_Map[Event_Process_Hash_Index][0]
            Event_index=event.Process_Event_Hash_Map[Event_Process_Hash_Index][1]

            if(Event_index > event.Process_Event_Head):

                event.Process_Event_Head+=1
                event.Process_Events[event.Process_Event_Head]=Pro_Hash
                event.Process_Event_Hash_Map[Event_Process_Hash_Index][1]=event.Process_Event_Head

            else:

                if(event.Process_Events[Event_index] != Pro_Hash ):

                    event.Process_Event_Head+=1
                    event.Process_Events[event.Process_Event_Head]=Pro_Hash
                    event.Process_Event_Hash_Map[Event_Process_Hash_Index][1]=event.Process_Event_Head
    

def Trigger_Current_Time_Events(event,light_time,Light_Signal,Light_Process):

    for ele in light_time.Event_list[0][1:]:

        if(ele[0]==0):                     # Signal
            
            #print("Triggering Delayed Signal")
            sig_hash=ele[1]
            value=ele[2]

            if(Light_Signal[sig_hash]['Delay_Driver']!=-8 or Light_Signal[sig_hash]['Delay_Driver']!=0):
                Light_Signal[sig_hash]['Delay_Driver']=Resolve_Value(Light_Signal[sig_hash]['Delay_Driver'],value)

            else:
                Light_Signal[sig_hash]['Delay_Driver']=value

            if(Light_Signal[sig_hash]['Update_Bit']==0):
                Light_Signal[sig_hash]['Update_Bit']=1
                event.Signal_Update_Event_Head+=1
                event.Signal_Update_Events[event.Signal_Update_Event_Head]=sig_hash
        
        elif(ele[0]==1):
            
            #print("Triggering Time Sensitive process")
            Execute_Light_Process(ele[1],0,event,light_time,Light_Signal,Light_Process)

    light_time.Event_list.pop(0)

    for i in range(0,event.Signal_Update_Event_Head+1):

        #print("Going to Resolve Signal "+str(event.Signal_Update_Events[i]))

        Resolve_Light_Signal(event.Signal_Update_Events[i],event,light_time,Light_Signal,Light_Process)

    event.Signal_Update_Event_Head=-1

    while(event.Process_Event_Head>=0):

        for i in range(0,event.Process_Event_Head+1):

            Execute_Light_Process(event.Process_Events[i],1,event,light_time,Light_Signal,Light_Process)

        event.Process_Event_Head=-1

        for i in range(0,event.Signal_Update_Event_Head+1):

            Resolve_Light_Signal(event.Signal_Update_Events[i],event,light_time,Light_Signal,Light_Process)

        event.Signal_Update_Event_Head=-1




def Simulator(Max_time,Signal_To_Signal_Name,event,light_time,Light_Signal,Light_Process):

    Value_Map={-4:'U',-5:'X',-6:'0',-7:'1',-8:'Z'}

    while(light_time.value<Max_time):

        Trigger_Current_Time_Events(event,light_time,Light_Signal,Light_Process)

        #print(light_time.Event_list)

        print(" Time = "+str(light_time.value))

        for key in Signal_To_Signal_Name:

            print("Signal [ "+Signal_To_Signal_Name[key]+" ]= "+Value_Map[Light_Signal[key]['Eff_Val']])

        light_time.value+=1              # check next event time 