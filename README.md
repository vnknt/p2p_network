# p2p_network

# Peer-to-Peer  Network Project 
<details open="open">
  <summary>Contents</summary>
  <ol>
    <li>
      <a href="#about">About</a>
      <ul>
        <li><a href="#what-is-peer-to-peer-network">What is Peer-to-peer Network</a></li>
		<li><a href="#about-the-project">About the project</a></li>
		<li><a href="#code">Explanation of source code</a></li>
   </ul>
   </li>

   <li><a href="#usage">Usage</a></li>
   
   <li><a href="#roadmap">Roadmap</a></li>
   <li><a href="#contact">Contact</a></li>

  </ol>
</details>









# ABOUT


### What is Peer-to-Peer Network

P2P network is a distruted network architecture that doesn't need a server for comminication. In p2p network, each computer that joined the network called Peer (or Node) and they are connected to each other directly. Mainly this network is used in file sharing and blockchain applications.



### About the project

This project is coded for creating peer-to-peer network  and you can modify and use it in your projects. 

A point of departure in this project is that I tried to create my own blockchain application, but I needed a peer-to-peer network , but I couldn't find a well-rounded example of p2p network. As a result of this, I created this p2p network project to use in my blockchain based application . 



### How does it work

The network based on **TCP/IP** connections. To create the network, there should be at least one peer that every other peers know its IP address and port. In this project this Peer (or peers) will be called as **GENESIS NODE**. 

As I mentioned, **everyone know genesis node's IP address and port.** Otherwise, *if a peer wants to join the network, it couldn't know which ip addresses to connect.*


If a device wants to join the p2p network, following will be take place: 

- Candicate node will connect to **Genesis node** firstly,
- This node  ask for address and port of a random peer in the network from genesis node, 
- If there exist one or more node in network (except for genesis node), the genesis node will send this existing ip address to the candicate device in json structure. Otherwise, candicate node will connect to genesis node
- After that, this node is a peer of the network. Now, the node will ask for other

















#
#
#
#
#
#
#
#
#
#
