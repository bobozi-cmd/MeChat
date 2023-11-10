# MeChat 0.1.0
We use C/S architecture and UDP communication to realize `MeChat`.
In this architecture, We have only one server which public ip is `server_ip`, 
and two client which public ips are `client_ip_1` and `client_ip_2` respectively.

## Conventions
- Massage format: tag content
    - tag: `register` -> A new client register to server use its name
    - tag: `select` -> A client select other client to talk with
    - tag: `message` -> A client send a message whose length is less than `msg_len` to server

## TODO list
[X] client-to-server, client1 talk with server in single thread
[X] client-to-client, client1 talk with client2 in single thread
[X] realize `Message` class and transport this between clients.
