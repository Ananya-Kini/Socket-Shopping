# Socket-Shopping
An online shopping system implemented using socket programming using TCP in Python. 

Instructions:
1.Download ```server.py``` and ```client.py```
2.To create private key, run ```openssl genpkey -algorithm RSA -aes256 -out server.key``` and to create self signed certificate, run ```openssl req -x509 -new -days 365 -key server.key -out server.crt ```
3. Run the command on your terminal after going into the respective file directory ```python server.py <Your IP Address> <any port number>```
Open another terminal(on same device or different), and run ```python client.py <Server IP Address> <Server port number>```
