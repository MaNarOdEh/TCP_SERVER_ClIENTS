import socket  # Import socket module
from queue import Queue
import threading
import sys

NUMBER_THREAD = 2
"""

 Thread 1--> Connect with The Server And Receiving Messages
 Thread 2--> Sending Messages

"""
JOB_NUMBER = [1, 2]  # give each thread his job!
queue = Queue()


# connecting to the server!
def connect_to_the_server():
    global s  # define the socket as public to use them from put side
    try:
        s = socket.socket()
        host = socket.gethostname()  # should be a static IP address
        port = 1997
        s.connect((host, port))
        print("Connection Done!")
        receiving_message()
    except socket.error as msg:
        print("\nSocket Error ", str(msg))
        print("Retrying! ...")
        close()


def receiving_message():
    global s
    global open
    open = True
    while open:
        data = s.recv(1024)
        if len(data) > 0:
            # print the string output
            print("Received Message is :", data[:].decode("utf-8"))
            if data[:].decode("utf-8") == 'close':
                open = False
                s.send(str.encode('close'))
                print("The connection with that server is closed!!")
            s.send(str.encode("Message Is Received Correctly"))  # send the output to the server!!
    print("the System should be closed!! ")
    close()


def send_message():
    global open
    open = True
    while open:
        msg = input("\nInput the Message You wan't to send: ")
        try:
            s.send(str.encode(msg))  # send the output to the server!!
            print("\nThe Server Received The Message!")
        except socket.error:
            print("\nYour message is not received")
    close()


# create two necessary thread
def create_thread():
    for i in range(NUMBER_THREAD):
        t = threading.Thread(target=job)  # creating a thread !
        """
        target =work that's means we will define a function that his name is work that it will till each thread what 
        will he do (what his job)

        """
        t.daemon = True  # this means that will the main thread will kill then make sure that also that thread will stop
        t.start()


def job():
    while True:
        x = queue.get()
        if x == 1:
            connect_to_the_server()
        if x == 2:
            send_message()

        queue.task_done()


# define jobs and put each them in a queue
def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)

    queue.join()


def close():
    print("we will close the programme now!!")
    global open
    open = False
    sys.exit()
    quit()


def main():
    create_thread()
    create_jobs()
    if open == False:
        sys.exit()


main()
