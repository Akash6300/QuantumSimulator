import numpy as np
from collections import OrderedDict,Counter
import copy
from string import ascii_lowercase
from Gates import *
import matplotlib.pyplot as plt

class QCircuit:
    def __init__(self,n:int) -> None:
        '''number of qubits'''
        try:
            assert(n>0)
        except AssertionError:
            print('number of qubits must be greater than zero')
        else:
            self.n=n
            self.statevector=np.zeros(2**n,dtype=float)
            self.statevector[0]=1
            gate_operations=[]
            self.__gate_operations=gate_operations

            self.ideal_dict=OrderedDict()
            for i in range(n):
                self.ideal_dict[i]=[]
            self.letters=list(ascii_lowercase)
            self.cx_gate_index=[]


    def x(self,qubit:int)->None:
        self.__gate_operations.append((qubit,'x'))
    
    def y(self,qubit:int)->None:
        self.__gate_operations.append((qubit,'y'))

    def z(self,qubit:int)->None:
        self.__gate_operations.append((qubit,'z'))

    def h(self,qubit:int)->None:
        self.__gate_operations.append((qubit,'h'))

    def s(self,qubit:int)->None:
        self.__gate_operations.append((qubit,'s'))

    def t(self,qubit:int)->None:
        self.__gate_operations.append((qubit,'t'))

    def sdg(self,qubit:int)->None:
        self.__gate_operations.append((qubit,'sdg'))

    def tdg(self,qubit:int)->None:
        self.__gate_operations.append((qubit,'tdg'))

    def cnot(self,control,target)->None:
        if(control>target):
            self.__gate_operations.append((control,'h'))
            self.__gate_operations.append((target,'h'))
            self.__gate_operations.append((target,control,'cx'))
            self.__gate_operations.append((control,'h'))
            self.__gate_operations.append((target,'h'))
        else:
            self.__gate_operations.append((control,target,'cx'))

    def cx(self,control,target)->None:
        if(control>target):
            self.__gate_operations.append((control,'h'))
            self.__gate_operations.append((target,'h'))
            self.__gate_operations.append((target,control,'cx'))
            self.__gate_operations.append((control,'h'))
            self.__gate_operations.append((target,'h'))
        else:
            self.__gate_operations.append((control,target,'cx'))


    def __depth(self)->OrderedDict:
        remove=[]
        self.cx_gate_index.clear()
        gate_list=copy.deepcopy(self.ideal_dict)
        for i in self.__gate_operations:
            if(len(i)==3):
                if(i[0]not in self.cx_gate_index and i[1] not in self.cx_gate_index):
                    self.cx_gate_index.append(i[0])
                    self.cx_gate_index.append(i[1])
                    pass
                else:
                    break
            else:
                if i[0] not in self.cx_gate_index:
                    gate_list[i[0]].append(i[1])
                    remove.append(i)
                else:
                    break
        for i in remove:self.__gate_operations.remove(i)
        return gate_list

    def __index_generator(self,length:int)->str:
        index_list=''
        for i in range(length):
            index_list+=str(str(self.letters[i])+str(self.letters[i+1])+',')
        index_list=index_list[0:-1]
        return index_list
    
    def __inner_product_gates(self):
        gate_list:dict=self.__depth()
        single_depth_operations=copy.deepcopy(self.ideal_dict)
        for i in range(self.n):
            length=len(gate_list[i])
            if(length>1):
                gate_list[i].reverse()
                matrix=np.einsum(self.__index_generator(length),*[gate(j) for j in gate_list[i]])
                single_depth_operations[i]=matrix
            elif(length==1):
                single_depth_operations[i]=gate(gate_list[i][0])
            else:
                single_depth_operations[i]=gate('i')
        return single_depth_operations
    
    def __final_tensor_gate(self):
        final_gate_dict:dict=self.__inner_product_gates()
        length=self.n
        if length>1:
            final=final_gate_dict[length-1]
            for i in range(length-2,-1,-1):
                final=np.kron(final,final_gate_dict[i])
            return final
        elif(length==1):
            return final_gate_dict[0]
        
    def return_cnot(self):
        i=self.__gate_operations[0]
        if(len(i)==3):
            control,target=i[0],i[1]
            self.__gate_operations.remove(i)
            return cnot(control,target,self.n)
        else:
            print('error cnot in returning cnot')
            raise AttributeError
        
    def measure(self,iters=1):
        while(len(self.__gate_operations)!=0):
            if(len(self.__gate_operations[0])==2):
                matrix=self.__final_tensor_gate()
                self.statevector=np.inner(matrix,self.statevector)
                norm=np.linalg.norm(self.statevector)
                self.statevector=self.statevector/norm
            if(len(self.__gate_operations)!=0):
                if(len(self.__gate_operations[0])==3):
                    matrix=self.return_cnot()
                    self.statevector=np.inner(matrix,self.statevector)
                    norm=np.linalg.norm(self.statevector)
                    self.statevector=self.statevector/norm

        probobalities=np.abs(self.statevector)**2
        count=[]
        for i in range(iters):
            val=np.random.choice(len(self.statevector),p=probobalities)
            val=bin(val)[2:].zfill(self.n)
            count.append(val)
        counts=Counter(count)
        counts=counts.most_common()
        return dict(counts)
    
    @classmethod
    def __info__(cls):
        print(f'Qsimulator')
        print(f'Maximum number of qubits = 14')
        print(f'Supported gate operations\n\t[pauli-X Gate,\n\tpauli-Y Gate,\n\tpauli-Z Gate,\n\tHadamard Gate,\n\tS Gate,\n\tT Gate,\n\tSDG Gate,\n\tTDG Gate]\n\t[CNOT Gate]')

def visualize_counts(counts:dict,color='r')->None:
    ''' 
        Args:
            counts: dict -> counts from the circuit
            color: string -> optional argument to specify color of histogram
    '''
    plt.bar(list(counts.keys()),list(counts.values()),align='center',width=0.3,color=color)
    plt.xticks(list(counts.keys()))
    plt.xlabel('measurements')
    plt.ylabel('counts')
    plt.show()
