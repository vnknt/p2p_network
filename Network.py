import socket
import time
import threading
import commands
import random
import json
import hashlib
from settings.terminal_set import bcolors
from helpers.terminal_helper import print_colored
import os
import Node
from Node import Node
from Message import Message


class Network(Node):

    
    HEADER_LEN = 10     
    FORMAT = "utf-8"
    DISCONNECT_MSG = "!DISCONNECT"
    CONN_PORT    =None
    CONN_ADDR    =None
    def __init__(self,ip="",port=None):
        self.SERVER_IP=ip
        
        self.nodes_in_network.append({"ip_addr":self.GENESIS_NODE_ADDR,"port":self.GENESIS_NODE_PORT})


 
    def bindAndListen(self,port):
        self.SERVER_PORT=port
        self.SERVER_ADDR = (self.SERVER_IP, self.SERVER_PORT)

        self.server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
        self.server.bind(self.SERVER_ADDR)

        
        print("[LISTENING...]")

        self.server.listen()

        while True:
            (conn,addr)=self.server.accept()
            #print(f"{conn} {addr}")

            thread=threading.Thread(target=self.handle,args=(conn,addr))
            thread.start()

           #print(f"{conn} connected")

    def start(self,port):

        Node.SERVER_PORT=port

        thread = threading.Thread(target=self.bindAndListen, args=(port,))
        thread.start()
        return


    def handle(self,conn,addr):

        client_ip=None
        client_port=None
        

        
        print_colored(f"{addr} connected to server", "green",5)
        
        connected = True

        connectionError=True
        ind=0

        flag = 1

        msg_buffer=''
        flag = 1
        while (connected):
            


            full_msg=''

            new_msg=True

            while(True):
                if(new_msg):
                    if(flag == 1 ):
                        msg=msg_buffer + conn.recv(2048).decode(self.FORMAT)
                    else:
                        msg=msg_buffer



                    #Controlling if msg is bigger than header
                    if(len(msg) >=self.HEADER_LEN):
                        msg_len=int(msg[:self.HEADER_LEN])
                    else:
                        msg_buffer=msg
                        flag=1
                        continue
                    






                    full_msg+=msg
                    if(len(full_msg )-self.HEADER_LEN == msg_len ):
                        msg_buffer = full_msg[self.HEADER_LEN  + msg_len:]
                        new_msg = False

                        break
                    elif(len(full_msg )-self.HEADER_LEN > msg_len ):
                        msg_buffer = full_msg[self.HEADER_LEN  + msg_len:]
                        full_msg = full_msg[:self.HEADER_LEN  + msg_len]
                        new_msg = False
                        flag = 0
                        break
                    else:
                        msg_buffer=full_msg
                        flag=1
                        full_msg=''

                        continue


            
            
            if (msg_len):
                ind+=1
                


                full_msg=full_msg[self.HEADER_LEN:]


                
                try:
                    msg = json.loads(full_msg)
                except:
                    print_colored(msg,"green")
                #msg=json.loads(msg)


                try:
                    index = self.message_logs.index(msg["id"])

                except:
                    index=-1
                    self.message_logs.append(msg["id"])


                if(index!=-1):
                    continue


                if(len(self.message_logs) >=50000):
                    print(f"---{len(self.message_logs)}")
                    self.message_logs.pop(0)








                if(commands.NODE_CON_ADDR in msg['title']):                                           #CONNECT TO ME COMMAND
                    
                    print_colored(f" {conn.getsockname()}","blue")


                    message=msg["message"]


                    conn_addr=msg["message"].split(",")                                            #split ip and port
                    
                    conn_ip=conn_addr[0]
                    conn_port=conn_addr[1]


                    client_ip=conn_ip
                    client_port=conn_port

                    
                    if(client_ip == "" or len(client_ip)==0):


                        peername=conn.getpeername()
                        client_ip=peername[0]


                    conn_ip = client_ip
                    
                    addr=(client_ip,int(conn_port))

                    print_colored(f"{addr} wants to establish connection", "yellow")


                    try:
                        conn_index=self.connections.index(addr)     
                    except:
                        conn_index=-1

                    if conn_index==-1:
                        self.connectToNode(conn_ip,int(conn_port))                      #if connection has not established so far, connect to the node
                        print_colored(f"{addr} Connection Established", "green")

                    else:
                        print_colored(f"{addr} 2 Way Connection Established...", "green")








                if(commands.CMD_JOIN_MSG in msg):

                    mssg = json.dumps(self.getSelfOrAdjacent())
                    mssg=f"{commands.MULTI_CONN_ADDR}{mssg}"
                    print(mssg)
                    conn.send(f"{mssg}".encode(self.FORMAT))
                    #(self.connections)
                    pass



        
                
                if(commands.ASK_RANDOM_NODE in msg["title"]):
                    print_colored(f"{addr} ASKED RANDOM NODE ", "yellow")

                    conn_addr=msg["message"].split(",")                                            #split ip and port
                    
                    conn_ip=conn_addr[0]
                    conn_port=conn_addr[1]

                    rndNode=json.dumps(self.getRandomNode())
                    
                    conn.send(f"{rndNode}".encode(self.FORMAT))






                if(commands.ASK_NODES_TO_CONNECT in msg["title"]):
                    print_colored(f"{addr} ASKED NODES TO CONNECT","yellow",2)
                    
                    got_nodes=self.getSelfOrAdjacent()
                    message=self.short_json_msg("",got_nodes)
                    self.reply(conn,message)
                    print("asdasfa------------")
                    print(message)
                    #conn.send(f"{got_nodes}".encode(self.FORMAT))

                if("#GIVE_NODES_IN_NETWORK" in msg["title"] ):

                        node_msg=self.short_json_msg("",self.nodes_in_network)

                        print(node_msg)

                        self.reply(conn,node_msg)




                if ( self.DISCONNECT_MSG in msg["title"]):
                    connected = False
                    
                    print_colored(f"{client_ip}:{client_port} DISCONNECTED", "red",2)

                    self.remove_connection(conn,addr[0], addr[1])
                    break



                if("#BROADCAST" == msg["title"]):

                    self.broadcast(msg,True)
                    
                    print(f"{msg}")

                    if(msg['message']=="#JOINED_IN_NETWORK"):

                        msg_sender_ip   =msg['sender_ip']
                        msg_sender_port =msg['sender_port']
                        if(msg_sender_ip == "" or msg_sender_ip ==None or len(msg_sender_ip) ==0):
                            msg_sender_ip = conn.getpeername()
                            msg_sender_ip= msg_sender_ip[0]

                        print(conn.getpeername())


                        print_colored(f"{msg['sender_ip']}:{msg['sender_port']} has joined to network","green")


                        self.nodes_in_network.append({"ip_addr":msg_sender_ip, "port":msg['sender_port']})
                        print("NODES IN NETWORK ")
                        print(self.nodes_in_network)
                else:
                    
                    print(msg["message"])



        conn.close()
        
        return



    def reply(self,conn,msg_json):
        

        message=json.dumps(msg_json)
        message=message.encode(self.FORMAT)
        conn.send(message)

        

    def join_network(self    ,ip=None,port=None):
        
        if ip==None:
            ip=self.GENESIS_NODE_ADDR
        if port==None:
            port=self.GENESIS_NODE_PORT


        print(f"{ip}{port}")
        conn=self.create_connection(ip, port)


        """
            Genesis node will return a ip address of a node
            new node will connect to this node
            new node will connect discover adjacent node
            #MULTI_CONN_ADDR
        """

        random_node = self.ask_random_node(conn,self.GENESIS_NODE_ADDR,self.GENESIS_NODE_PORT)
            
        node = json.loads(random_node)

        print(f"------->{node}")
        if node==None:

            self.remove_connection(conn, ip, port)

            print("Network is not exist...")
            print("Connecting to Genesis Node",end="\n\n")


            self.connectToNode(self.GENESIS_NODE_ADDR, self.GENESIS_NODE_PORT)
            print("asadasd")
            
        else:
            """
                Ask adjacent from random node that given by network
            """
            self.remove_connection(conn, ip, port)
            #self.connectToNode(self.GENESIS_NODE_ADDR, self.GENESIS_NODE_PORT)
            print(node["ip_addr"])
            response = self.askNodes(node["ip_addr"], node["port"])
            
        temp_node = self.nodes[0]
        

        print(self.nodes[0])


        msg=Message().short_msg("#GIVE_NODES_IN_NETWORK","")

        broadcast_msg=Message(self.SERVER_IP,self.SERVER_PORT).msg("#JOINED_IN_NETWORK","#BROADCAST")

        self.broadcast(broadcast_msg,isJson=True)

        nodes = self.send(temp_node,msg,1)

        nodes=json.loads(nodes)

        nodes=nodes["message"]



        for node in nodes:
            
            try:
                index = self.nodes_in_network.index(node)
            except:
                index = -1

            if index ==-1 :

                self.nodes_in_network.append(node)



    def ask_random_node(self,conn,address,port):

        #test_askRandMsg = Message().short_msg(commands.ASK_RANDOM_NODE, f"{self.SERVER_IP},{self.SERVER_PORT}")

        ask_random_message=self.short_json_msg(commands.ASK_RANDOM_NODE,f"{self.SERVER_IP},{self.SERVER_PORT}")


        message = ask_random_message

        msg = self.send(conn,message,1)
        print(f"RESPONSE_RAND_NODE:{msg}")

        disconnect_msg=self.short_json_msg(self.DISCONNECT_MSG)
        self.send(conn,disconnect_msg)

        return msg



    def short_json_msg(self,title,message=""):

        message=Message().short_msg(title,message)
        return message



    def askNodes(self,ip,port):

        conn = self.create_connection(ip, port)

        

        msg_json=self.short_json_msg(commands.ASK_NODES_TO_CONNECT)
        
        msg = self.send(conn,msg_json,1)

        disconnect_msg=self.short_json_msg(self.DISCONNECT_MSG)

        self.send(conn,disconnect_msg)

        msg=json.loads(msg)
        nodes=msg["message"]
        print(type(nodes))

        
        print_colored(f"{len(nodes)} Node address recieved...","cyan")
        print(nodes)


        for node in nodes:
            self.connectToNode(node["ip_addr"], node["port"])
            


    def create_connection(self,ip,port):

        CONN_ADDR=(ip,port)
        connection=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        connection.connect(CONN_ADDR)
        return connection





    def send(self,conn,msg_json,hasResponse=0):
        

        message=json.dumps(msg_json)
        temp_len=len(message)

        message=f'{temp_len:^{self.HEADER_LEN}}'+message
        message=message.encode(self.FORMAT)
        conn.send(message)
        if(hasResponse):
            msg = conn.recv(1024).decode(self.FORMAT)
        else:
            msg=""
        return msg
    

    def connectToNode(self,address,port):
        print(f"_______{address}_{port}_______________________-")
        self.CONN_ADDR=(address,port)

        if(self.CONN_ADDR not in self.connections):

            connection=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            connection.connect(self.CONN_ADDR)

            x={"ip_addr":address,"port":port}

            self.nodes.append(connection)
            self.connections.append(self.CONN_ADDR)
            self.connections_json.append(x)

            #msg=f"#NODE_CONN_ADDR({self.SERVER_IP},{self.SERVER_PORT})"


            msg=self.short_json_msg(commands.NODE_CON_ADDR,f"{self.SERVER_IP},{self.SERVER_PORT}")

            
            self.send(connection,msg)



        print_colored(f"Connected To->{address}:{port}","green",2)
        return







    def broadcast(self,data,isJson=False):


        if isJson==False:
            msg = self.short_json_msg("#BROADCAST",data)
        else:
            msg=data

        try:
            index = self.message_logs.index(msg["id"])

        except:
            index=-1
            self.message_logs.append(msg["id"])




        for node in self.nodes:

            try:
                self.send(node,msg) 

            except:
                print_colored("MESSAGE COULDN'T SEND, RECIEVER MAY BE DISCONNECTED ","red")



