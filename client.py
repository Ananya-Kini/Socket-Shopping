import socket
import sys
import json
import ssl

def main():
    # Get server host and port
    if len(sys.argv) != 3:
        print("Usage: python client.py <host> <port>")
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        #SSL connection to the server
        ssl_client = ssl.wrap_socket(client, ssl_version=ssl.PROTOCOL_TLS)
        ssl_client.connect((host, port))

        # Receive product data
        data = ssl_client.recv(1024).decode()
        products = json.loads(data)


        print("Available products:")
        for product in products:
            print("ID: {}, Name: {}, Price: Rs.{}".format(product["id"], product["name"], product["price"]))

        # Store products to buy in an array cart
        cart = []
        while True:
            product_id = input("Enter the ID of the product you want to buy (or 'done' to finish): ")
            if product_id.lower() == 'done':
                break
            quantity = int(input("Enter the quantity: "))
            cart.append({"id": int(product_id), "quantity": quantity})

        # Send the online cart to the server
        ssl_client.sendall(json.dumps(cart).encode())

        # Bill is received from server
        bill = ssl_client.recv(1024).decode()

        print("\nYour total bill is: Rs.{}".format(bill))
        print("Thank you for shopping with us!")

    except ConnectionRefusedError:
        print("Failed to connect to the server.")
    finally:
        # Close the SSL connection
        ssl_client.close()

if __name__ == "__main__":
    main()
