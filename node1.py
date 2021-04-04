from Network import Network
from helpers.terminal_helper import print_colored


node2 = Network("192.168.56.1")
node2.start(5050)

print("SERVER-1 (GERMANY)")
print_colored("PORT 5050 is started active Please enter a key to continue","green")










while True:
    data=input()
    
    node2.broadcast(data)
    


