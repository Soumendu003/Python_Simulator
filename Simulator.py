import numpy as np
import Datastructures as D


def and_gate(a,b):

    if(a=='U' and b=='U'):
        return 'X'

    elif(a=='0' or b=='0'):
        return '0'
    
    elif(a=='X' or b=='X'):
        return 'X'
    
    else:
        return '1'

def or_gate(a,b):

    if(a=='1' or b=='1'):
        return '1'
    
    elif(a=='X' or b=='X'):
        return 'X'

    elif(a=='U' and b=='U'):
        return 'X'

    else:
        return '0'

def not_gate(a):

    if(a=='U'):
        return 'X'
    
    if(a=='X'):

        return 'X'
    
    if(a=='1'):
        return '0'

    if(a=='0'):
        return '1'


def Get_val(inst,Signals):

    oprnd=[]

    for ele in inst:

        if(ele[0]=='V'):

            if('1' in ele):
                oprnd.append('1')
            elif('0' in ele):
                oprnd.append('0')
            elif('X' in ele):
                oprnd.append('X')
            else:
                oprnd.append('U')
        
        elif(ele=='and'):

            a=oprnd.pop()
            b=oprnd.pop()

            oprnd.append(and_gate(a,b))

        elif(ele=='or'):

            a=oprnd.pop()
            b=oprnd.pop()

            oprnd.append(or_gate(a,b))
        
        elif(ele=='not'):

            a=oprnd.pop()

            oprnd.append(not_gate(a))

        else:
            
            hash_val=int(ele)

            oprnd.append(Signals[hash_val].value)

    #print(oprnd)
    Val=oprnd.pop()

    #print(Val)

    return Val


def EventSchedule(offset,Time,Id):
    
    count=0
    flag=0
    #print("Time Val + Offset = "+str(Time.value+offset))

    for event in Time.Events:
        
        if(event[0]==Time.value+offset):
            
            event.append(Id)
            flag=1
            break

        elif(event[0]>Time.value+offset):

            Time.Events.insert(count,[Time.value+offset,Id])
            flag=1
            break

        count+=1
        
    if(flag==0):

        Time.Events.append([Time.value+offset,Id])


def Execute_Instruction(Id,Signals,Time):

    process=Id[1]

    inst=process.instructions[process.execution_contex]

    if(inst[0]=='<='):

        #print("Signal name = "+str(Signals[int(inst[1])].name))
        signal=inst[1]

        val=Get_val(inst[2],Signals)

        Signals[int(signal)].Driver.update({process:val})

        return 0

    elif(inst[0]=='wait'):

        val=int(inst[1])

        #print("Calling Event Schedule")
        EventSchedule(val,Time,Id)

        return 1
    elif(inst[0]=='Delay'):

        signal=inst[1]

        val=Get_val(inst[2],Signals)

        inst[4][2]=val

        EventSchedule(inst[3],Time,inst[4])

        return 0


def Execute_Process(Id,Signals,Time):


    process=Id[1]

    suspend=0

    if(process.execution_contex>=len(process.instructions)):

        process.execution_contex=0

    while(suspend==0):

        if(process.execution_contex>=len(process.instructions)):

            process.execution_contex=0
            suspend=1
            if(Id[0]=='P'):
                EventSchedule(1,Time,Id)

        else:

            suspend=Execute_Instruction(Id,Signals,Time)

            process.execution_contex+=1


look_up_table=[
    ['U','X','0','1','U'],
    ['U','X','X','X','X'],
    ['U','X','0','X','0'],
    ['U','X','X','1','1'],
    ['U','X','0','1','Z']]

index_table={'U':0,'X':1,'0':2,'1':3,'Z':4}

def resolve(last,new):

    #print("las_val ="+last+"\t new val ="+new)
    row=index_table[last]
    col=index_table[new]

    val=look_up_table[row][col]

    return val

def Append_value_change(Hash,value_change):

    p=value_change[0]+1

    value_change[p]=Hash

    value_change[0]=p

def Resolve_signal(signal,value_change):

    final_val='Z'
    flag=0

    for key in signal.Driver:

        if(signal.Driver[key]!='!'):
            
            flag=1
            final_val=resolve(final_val,signal.Driver[key])
            signal.Driver[key]='!'

    if(signal.value!=final_val and flag==1):

        signal.value=final_val

        Append_value_change(signal.hash,value_change)
        return



def Trigger_Time_Sesitive_Processes(Time,Signals,Value_Change):

    for ele in Time.Events[0][1:]:

        if(ele[0]=='S'):

            print("delayed value = "+ele[2]+" Signal ="+ele[1].name)
            ele[1].Driver.update({'Delay':ele[2]})
        
        else:

            Execute_Process(ele,Signals,Time)

    Time.Events.pop(0)

    Value_Change[0]=0                        # Stores the adress of changed signals

    for signal in Signals.values():

        #print("Sig Driver "+str(signal.Driver))
        
        Resolve_signal(signal,Value_Change)     # after resolving each signal Driver list should be removed        

    while(Value_Change[0]>0):

        for i in range(1,Value_Change[0]):

            signal=Signals[Value_Change[i]]

            for process in signal.processes:

               Execute_Process(process,Signals,Time)
        
        Value_Change[0]=0

        for signal in Signals.values():
            Resolve_signal(signal,Value_Change)
    
    print("Time is "+str(Time.value))
    for signal in Signals.values():
        print("Signal "+str(signal.name)+" = "+str(signal.value))


def Simulator(max_time,Time,Entities,Signals):

    S=len(Signals.values())
    Value_Change=np.zeros((S+1,),dtype=np.int64)

    print(Time.Events)
    
    while(Time.value<max_time):

        Trigger_Time_Sesitive_Processes(Time,Signals,Value_Change)

        Time.value+=1
    
