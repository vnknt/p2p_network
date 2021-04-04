import time
import hashlib
import random


class Message:


    message_index=0
    MESSAGE=None
    SENDER_IP=None
    SENDER_PORT=None
    RECIEVER_IP=None
    RECIEVER_PORT=None




    def __init__(self,sender_ip=None,sender_port=None,reciever_ip="all",reciever_port=None):
        self.increase_msg_index()
        self.SENDER_IP=sender_ip
        self.SENDER_PORT=sender_port
        self.RECIEVER_IP=reciever_ip
        self.RECIEVER_PORT=reciever_port






    def msg(self,message,title):
        
        
        ts = time.time()
        id=hashlib.sha256( f"{self.SENDER_IP}:{self.SENDER_PORT}{self.RECIEVER_IP}:{self.RECIEVER_PORT}:{self.message_index}{ts}{self.MESSAGE}".encode() ).hexdigest()



        msg_obj={
            "index":self.message_index,
            "id":id,
            "sender_ip":self.SENDER_IP,
            "sender_port":self.SENDER_PORT,
            "title":title,
            "message":message,
            "time":ts,
            "reciever_ip":self.RECIEVER_IP,
            "reciever_port":self.RECIEVER_PORT
 
            
            }

        self.increase_msg_index()
        
        return msg_obj




    def short_msg(self,title,message=""):

        ts=time.time()
        id=hashlib.sha256(f"{random.randint(0,99999)}{title}{message}{time}".encode()).hexdigest()
        msg_obj={
            "id"    :id,
            "title":title,
            "message":message,
            "time":ts,
        }


        return msg_obj












    @classmethod
    def increase_msg_index(cls):

        cls.message_index+=1


















