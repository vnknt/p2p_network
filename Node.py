import socket
import time
import threading
import commands
import random
import json
import hashlib

from settings.terminal_set import bcolors
from helpers.terminal_helper import print_colored
from Message import Message




import os


os.system("color")






class Node:

    SERVER_IP=socket.gethostbyname(socket.gethostname())
    SERVER_PORT=None
    SERVER_ADDR=None


    
    GENESIS_NODE_ADDR="192.168.56.1"         #boot node address
    GENESIS_NODE_PORT=5050                   #boot node port


    nodes=list()                        #connections
    connections=list()                  #connection addresses
    incomingConnections=list()
    connections_json=list()

    message_logs=list()

    nodes_in_network=list()



    








    isJoinedNetwork=False


    def __init__(self,ip=SERVER_IP,port=SERVER_PORT):


        self.SERVER_IP=ip
        self.SERVER_PORT=port
        self.SERVER_ADDR=(ip,port)

        








    def totalConection(self):
        return len(self.connections)



    def find_addr_index(self,ip,port):
        index=0
        result=-1
        for node in self.connections:
            if(node[0] == ip and node[1] == port):
                result=index
                break
            index+=1

        return result


    def find_connection_index(self,ip,port):
        index=0
        result=-1


        for node in self.nodes:

            peername=node.getpeername()
            
            if(peername[0] == ip and peername[1] == port):
                
                result=index
                break
            index+=1


        return result




 
    def find_json_index(self,ip,port):
        index=0
        result=-1
        
        for node in self.connections_json:
            if(node["ip_addr"] == ip and node["port"] == port):
                result=index
                break
            index+=1

        return result


    def getRandomNode(self):

        json_temp=self.connections_json.copy()                              #all active connections are copied
  
        total_node=self.totalConection()                                    #calculate total connected node


        if total_node==0:                                                   
            return None      #if there is no any connection, return self ip and port



        rnd=random.randint(0,total_node-1)                                  #random index

        return json_temp[rnd]





    def remove_connection(self,conn,ip,port):

        try:
            conn_index = self.find_connection_index(ip,port)
        except:
            conn_index=-1
        if(conn_index!=-1):
            self.nodes.pop(conn_index)
        

        try:
            node_index=self.find_addr_index(ip, port)
        except:
            node_index=-1
        
        if(node_index!=-1):
            
            self.connections.pop(node_index)

        try:
            node_index=self.find_json_index(ip, port)(ip, port)
        except:
            node_index=-1
        
        if(node_index!=-1):
            self.connections_json.pop(node_index)



        
        print(self.nodes)
        print(self.connections)



    def getSelfOrAdjacent(self):


        total_adj = self.totalConection()
        server_json={"ip_addr":self.SERVER_IP,"port":self.SERVER_PORT}
        if total_adj == 0 :



            return self.merge_command(commands.NODE_CON_ADDR, f"({self.SERVER_IP},{self.SERVER_PORT})")
            


        if total_adj == 1:

            temp_json_list=self.connections_json.copy()
            
            temp_json_list.append(server_json)

            return temp_json_list




        #If total_adjacent>=2 , return 2 or more node 


        if(total_adj>=2):  
            copy_json = self.connections_json.copy()
            copy_json.append(server_json)


            total_return = random.randint(2, total_adj+1)           #+1 is for self address



            arr=list(range(0,total_adj+1))
            
            random.shuffle(arr)
            
            arr=arr[0:total_return]
            
            print(f"{total_return} , {arr}")

            temp_json_list = list()

            for i in arr:
                temp_json_list.append(copy_json[i])
            
            print(temp_json_list)
            return temp_json_list





























    
    @classmethod
    def set_node(cls,ip,port):
        cls.SERVER_PORT=port
        cls.SERVER_IP=ip
        cls.SERVER_ADDR=(ip,port)






    @staticmethod
    def calculateMsgLen(self,msg):
        message = msg.encode(self.FORMAT)
        msg_len = len(message)
        send_len = str(msg_len).encode(self.FORMAT)
        send_len += b' ' * (self.HEADER_LEN - len(send_len))
        return send_len


    @staticmethod
    def merge_command(cmd,msg):

        message=f"{cmd}({msg})"
        print(message)
        return message


    @staticmethod
    def split_command(cmd,msg):
        length=len(cmd)

        message=msg[length+1:-1]
        print(message)
        return message



    def create_message(self,msg,title,sender_ip=SERVER_IP,sender_port=SERVER_PORT,reciever_ip="all",reciever_port=None):
        if(sender_port== None):
            sender_port=self.SERVER_PORT 
        message = Message(sender_ip,sender_port,reciever_ip,reciever_port)
        
        return message.msg(msg,title)




