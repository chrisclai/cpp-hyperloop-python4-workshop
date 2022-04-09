import socket
import random

from _thread import *
import threading

# [THREAD] Takes data and sends it to the client
def servproc(conn, addr):
    print(f"Server Control Function Activated in {addr}!")
    datalength = 25
    while True:
        if conn:
            data = [0] * datalength
            send = ""
            for i in range(len(data)):
                data[i] = random.randint(0, 100)
                send += str(data[i]) + " "
            conn.send(bytes(send, 'utf-8'))
        else:
            conn.close()
            break

# [THREAD] Receives data from the server
def datarecv_client(conn, addr):
    print("Client Data Retrieval Thread Activated!")
    while True:
        try:
            msg = conn.recv(16).decode('utf-8')
            if not msg:
                pass
            else:
                print(msg)
        except Exception as e:
            print(f"Error: {e}. Could not receive data. Terminating thread.")
            conn.close()
            break       

# [FUNCTION] Main function, where everything happens
def main():
    # Setup Server Variables
    HOST = '127.0.0.1'
    PORT = 8009
    BUFFER_SIZE = 8162
    TIME_OUT = 10
    SENSOR_COUNT = 1

    # Bind to Port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(SENSOR_COUNT)
    s.settimeout(TIME_OUT)
    print("Listening on %s:%s..." % (HOST, str(PORT)))

    while True:
        try:
            # Server Activation
            conn, addr = s.accept()
            print('GOT CONNECTION FROM:', addr)

            # Thread it (Send data to client)
            thread_send = threading.Thread(target = servproc, args = (conn, addr))
            thread_send.start()

            # Thread it again (Receive data from client)
            thread_recv = threading.Thread(target = datarecv_client, args = (conn, addr))
            thread_recv.start()
        except KeyboardInterrupt:
            print("I'm outta here Ctrl+C")
        except:
            print("No Client! Trying Again...")

if __name__ == "__main__":
    main()