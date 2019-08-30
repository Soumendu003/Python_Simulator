'''  This Module basically parse the VHDL source codes and
creates the data structures for further  evaluation     '''
import Datastructures as D


def ParseEntities(file,Signals,Entities):
    ''' only one entity allowed per file '''

    f=open(file,"r")

    lines=f.readlines()


    state=0

    for line in lines:

        words=line.split()

        if(len(words)>0 and state==0 and words[0]=='entity'):

            state=1

            entity=D.Entity(words[1])
            Entities.update({words[1]:entity})
            
        if(state==1 and len(words)>0 and ':' in words[0]):

            signal_name=words[0][0:-1]
            
            entity.ports.append(signal_name)
            Signal_object=D.Signal()

            Signal_object.name=signal_name+"."+entity.name

            signal_hash=hash((entity.name,signal_name))

            Signal_object.hash=signal_hash

            Signals.update({signal_hash:Signal_object})

        if(state==1 and len(words)>0 and words[0]=='end'):

            break

def Resolve_key(val,entity,Signals,signal_map):

    if(val=="'1'" or val=="'0'" or val=="'X'" or val=="'U'" or val=="'Z'"):

        return "Val"+val

    Ret=hash((entity,val))

    if(Ret not in Signals):

        Val=signal_map[val]

        Ret=hash((Val[0],Val[1]))

       # print("Sig_name = "+str(val)+" entity = "+entity_name+" hash = "+str(Ret))

        

    return str(Ret)

def Make_Postfix_Expression(tokens,entity,Signals,signal_map):

    #print(tokens)

    Y=[]

    Stack=[]

    Stack.append('(')
    tokens.append(')')

    for token in tokens:

        if(token=='('):

            Stack.append(token)

        elif(token=='and' or token=='or' or token=='not'):

            while(Stack[-1]!='('):

                Y.append(Stack.pop())

            Stack.append(token)
        
        elif(token==')'):

            while(Stack[-1]!='('):

                Y.append(Stack.pop())
                
            Stack.pop()
        else:
            Y.append(Resolve_key(token,entity,Signals,signal_map))


    return Y

def ParseInstructions(process,entity,Signals,Instructions,signal_map):

    #print("Instructions number ="+str(len(Instructions)))
    
    for inst in Instructions:

        tokens=inst.split()

        if('<=' and 'after' in inst):

            left_val=Resolve_key(tokens[0],entity,Signals,signal_map)

            command='Delay'

            indx=tokens.index('after')

            postfix_expression=Make_Postfix_Expression(tokens[2:indx],entity,Signals,signal_map)

            Delay_val=int(tokens[indx+1])

            Id=['S',Signals[int(left_val)],'!']

            process.instructions.append([command,left_val,postfix_expression,Delay_val,Id])

            #print([command,left_val,postfix_expression,Delay_val,Id])


        elif('<=' in inst):

            left_val=Resolve_key(tokens[0],entity,Signals,signal_map)

            command='<='

            postfix_expression=Make_Postfix_Expression(tokens[2:-1],entity,Signals,signal_map)

            #print("Post_Fix = "+str(postfix_expression))
            #print(str([command,left_val,postfix_expression]))

            process.instructions.append([command,left_val,postfix_expression])


        elif('wait' in inst):

            command='wait'

            val=int(tokens[2])

            process.instructions.append([command,val])

            #print(str([command,val]))

        elif('report' in inst):

            command = 'report'

            for token in tokens:

                if('&std_logic\'image' in token):

                    sig = token[token.index('(')+1:-1]
                    break
            
            Sig_Val = Resolve_key(sig,entity,Signals,signal_map)
            process.instructions.append([command,Sig_Val])


def ParseProcess(lines,Signals,entity,signal_map,Process_Set):

    state=0
    for line in lines:

        words=line.split()

        if(len(words)>0):

            if(state==0 and '(' in words[0]):

                process=D.Process()
                Process_Set.add(process)
                process.Id=['X',process]

                Instructions=[]
                Sensitivity_list=words[0][words[0].index('(')+1:-1].split(',')

                for ele in Sensitivity_list:
                        
                    sig_hash=hash((entity,ele))
                    Signals[sig_hash].processes.append(process.Id)
        
                state=1
            
            if(state==0 and '(' not in words[0]):

                process=D.Process()
                Process_Set.add(process)
                process.Id=['P',process]
                Instructions=[]
                state=1
            
            if(state==1 and words[0]=='begin'):

                state=2

            elif(state==2 and words[0]!='end'):

                #print(line)

                Instructions.append(line)
            
            if(state==2 and words[0]=='end'):

                ParseInstructions(process,entity,Signals,Instructions,signal_map)
                break


def ParseArchitectures(file,Signals,Entities,Process_Set):

    ''' only one architecture allowed per entity'''

    f=open(file,"r")
    #print("\n \n File Name ="+file+"\n \n")

    lines=f.readlines()

    inst_lst=[]

    signal_map={}


    state=0
    count=-1

    for line in lines:

        words=line.split()

        #print("Line no ="+str(lines.index(line))+" Line = "+line)
        count+=1
        if(len(words)>0):
            
            if(state==0 and words[0]=='architecture'):

                #architec=words[1]
                entity=words[3]
                state=1
        
            if(state==1 and words[0]=='signal'):

                signal_name=words[1][0:-1]
            

                Signal_object=D.Signal()

                Signal_object.name=signal_name+"."+entity

                signal_hash=hash((entity,signal_name))

                Signal_object.hash=signal_hash

                Signals.update({signal_hash:Signal_object})
        
            if(state==1 and words[0]=='begin'):

                state=2                          # Inside Architecture Body
            

            if(state==2 and 'port map' in line):

                ported_entity=words[1]
                signals=words[3][words[3].index('(')+1:-2].split(',')
                
                cnt=0

                obj=Entities[ported_entity]

                #print("Original port names : "+str(obj.ports))

                for sig in signals:

                    if(hash((entity,sig)) in Signals):

                        del Signals[hash((entity,sig))]

                        print("Deleted Signal = "+str([entity,sig]))

                    ori_name=obj.ports[cnt]

                    val=[ported_entity,ori_name]

                    signal_map.update({sig:val})
                    cnt+=1

            if(state==2 and 'process' in words[0]):

                state=3
                #print("Index = "+str(count))

                ParseProcess(lines[count:],Signals,entity,signal_map,Process_Set)

            if(state==3 and words[0]=='end'):
                
                state=2
            
            if(state==2 and words[0]!='end' and 'begin' not in line and 'port' not in line):

                inst_lst.append(line)

            if(state==2 and words[0]=='end' and 'end process' not in line):
                break
            
        

    
    if(len(inst_lst)>0):

        print("Instruction List= "+str(inst_lst))

        process=D.Process()
        Process_Set.add(process)
        tem=['P',process]
        ParseInstructions(process,entity,Signals,inst_lst,signal_map)


def Parser(FileNames):

    Signals={}
    Entities={}
    Process_Set=set()

    for file in FileNames:

        ParseEntities(file,Signals,Entities)
    
    for file in FileNames:
        
        ParseArchitectures(file,Signals,Entities,Process_Set)



    return Signals,Process_Set



