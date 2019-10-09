import socket
import threading
from queue import Queue
import sys

#  Two Thread

"""


Thread 1--> Listen and accept connections from other clients(listening for new client and establish connection with them)
Thread 2--> Sending commands to an already connected client(dealing with connecting client)
Thread 3--> Receiving message From any connected Clients


"""
NUMBER_OF_THREAD = 2

JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_address = []


#  create a socket to connect two computers
def create_socket():
    try:
        # define those variable as global to use them from out side that functions
        global mSocket  # end point connection between two computer
        global host  # that should be a static host for that server
        global port  # any  number larger than 1024
        mSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
        host = socket.gethostname()  # Get local machine name
        port = 1997  # Reserve a port for your service.
        #  Port to listen on (non-privileged ports are > 1023)
        print("Set Server port number As: ", port)  # print server host number
        print("Set Server host name As: ", host)  # print server host name
    except socket.error as msg:
        print("socket error occurs: ", str(msg))


#  binding the socket and listening for any connections
def bind_socket():
    try:
        global mSocket
        global host
        global port
        print("Binding the port number: ", port)
        mSocket.bind((host, port))  # Bind to the port (host name,port number pair)
        """
            The server should continually listening to the computers how wan't to connect to that server
        """
        mSocket.listen(5)

        #  Now wait for client connection. sets up and start TCP listener.
    except socket.error as msg:
        print("socket error occurs: " + str(msg) + "\nRetrying! ...")
        bind_socket()


# handling connection from all client ans save the connection
# that methods will call when the server is restart so you should close all the previous connection
def accepting_connection():
    """
      open connections between server and clients along with the address of the client
      and accepting any incoming connections from clients
     """
    """
      Establish connection with client(This passively accept TCP client connection, waiting until connection arrives 
      (blocking)
      remove all the connections and address and close all the connections when the server is restarted
    """
    for connection in all_connections:
        connection.close()

    del all_connections[:]  # [:] --> means select all the values inside that list and deleted them
    del all_address[:]
    while True:
        try:
            connection, address = mSocket.accept()
            mSocket.setblocking(1)
            """
             set blocking -->that's methods used when the time out while trying to receive this connections
             to stop ..so the main idea for using it to prevent the time ut from happening
            """
            all_address.append(address)
            all_connections.append(connection)
            print("\nConnection has been established! " + " IP " + address[0] + " | Port " + str(address[1]))
        except socket.error:
            print("Error Accepting Connection ")


"""
 second thread can see all client , selecting a special client ,sending a special message to the connected clients

"""


def start_accept_orders():
    while True:
        cmd = input("\ninput (list to show all connected clients or select any target client"
                    "by input select id_client:\n")
        # print(cmd)
        if cmd == 'list':
            show_all_connection()
        elif 'select' in cmd:
            connection = get_selected_connection(cmd)
            if connection is not None:
                print("send target messages! ")
                send_message_to_special_client(connection)
        else:
            print("Your commend is un Recognizable!")


# display all current connection with server
def show_all_connection():
    active_connection = ''
    for index, connection in enumerate(all_connections):
        try:
            connection.send(str.encode('  '))
            connection.recv(20480)  # if you don't receive any thing then that connection is useless
            active_connection += str(index) + "   " + str(all_address[index][0]) + "   " + str(
                all_address[index][1]) + "\n"
        except socket.error:
            del all_connections[index]
            del all_address[index]
            continue

    print(" <<Clients>>: " + "\n" + active_connection)


# get the target or selected connection
def get_selected_connection(cmd):
    try:
        target_index = cmd.replace('select', '')  # target = id
        target_index = int(target_index)
        connection = all_connections[target_index]
        print("You are now connected to :" + str(all_address[target_index][0]))
        print(str(all_address[target_index][0]) + " > ", end="")
        return connection
    except:
        print("Selection not valid")
        return None


# send message to target clients
def send_message_to_special_client(connection):
    while True:
        try:
            cmd = input("\nInput the Message You wan't to send to the chosen client: ")
            if cmd == 'quit':
                break
            if len(str.encode(cmd)) > 0:
                connection.send(str.encode(cmd))
                client_response = str(connection.recv(20480), "utf-8")
                print("the Result Message From Our client: ", client_response, end="")
                if client_response == 'close':
                    connection.close()
                    print("\nConnection with that clients is closed! ")
                    break

                """ 
                receive --> the result form the clients and convert it from byte to a string
                1024 --> when the data is to big then it will junk and receiving as 1024 each time
                utf-8 --> stand for encoding type it's basically means convert the message into formats that can be 
                                    converted into string 

                end --> is for continue to the next line  allow you to enter a ney commends

                """
        except:
            print("Error sending commands")
            break


# create two necessary thread
def create_thread():
    for i in range(NUMBER_OF_THREAD):
        t = threading.Thread(target=job)  # creating a thread !
        """
        target =work that's means we will define a function that his name is work that it will till each thread what 
        will he do (what his job)

        """
        t.daemon = True  # this means that will the main thread will kill then make sure that also that thread will stop
        t.start()


# Do next job that is in the queue (handle connections, send commands)
def job():
    global mSocket
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connection()
        if x == 2:
            start_accept_orders()
        queue.task_done()


# define jobs and put each them in a queue
def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)

    queue.join()


def main():
    create_thread()
    create_jobs()


main()
