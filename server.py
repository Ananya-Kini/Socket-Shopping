import socket
import sys
import json
import threading
import ssl

# Sample product data
products = [
    {"id": 1, "name": "Classmate spiral bound notebook", "price": 144},
    {"id": 2, "name": "Voylla round cut gem earrings", "price": 116},
    {"id": 3, "name": "Biba Women's printed palazzos", "price": 739},
    {"id": 4, "name": "boAt airdopes", "price": 899},
    {"id": 5, "name": "Michael Kors analog white dial women's watch", "price": 8998},
    {"id": 6, "name": "Tees Maar Khan dvd", "price": 799},
    {"id": 7, "name": "Multi tool pocket knife", "price": 499},
    {"id": 9, "name": "Pride and Prejudice hardcover", "price": 699},
    {"id": 10, "name": "MARS matte lipstick", "price": 199},
    {"id": 11, "name": "Zart deer showpiece", "price": 899},
    {"id": 12, "name": "Parker galaxy roller ball pen", "price": 405},
    {"id": 13, "name": "Harry Potter and the Goblet of Fire", "price": 542},
    {"id": 14, "name": "Britannia Treat Chilli Guava cream", "price": 10},
    {"id": 15, "name": "Blue eyes keychain", "price": 159}       
]

def handle_client(client_socket):
    # Product list is sent to client
    client_socket.sendall(json.dumps(products).encode())

    # Receive cart from client
    cart_data = client_socket.recv(1024).decode()
    cart = json.loads(cart_data)

    # Total bill calculation
    total_bill = 0
    for item in cart:
        product_id = item["id"]
        quantity = item["quantity"]
        for product in products:
            if product["id"] == product_id:
                total_bill += product["price"] * quantity
                break

    # Bill is sent to the client
    client_socket.sendall(str(total_bill).encode())

    client_socket.close()

def main(host, port):
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    server.bind((host,port))

    certfile = 'server.crt'
    keyfile = 'server.key'

    # Create SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile, keyfile)

    server.listen(5)

    print("Server listening on {}:{}".format(host,port))

    while True:
        # Accept a client connection
        client_socket, client_address = server.accept()
        print("Connected to client:", client_address)

        # Wrap the client socket with SSL/TLS
        ssl_client = context.wrap_socket(client_socket, server_side=True)

        # Handle client in a new thread
        client_handler = threading.Thread(target=handle_client, args=(ssl_client,))
        client_handler.start()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python server.py <host> <port>")
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])

    main(host, port)
