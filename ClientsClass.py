import socket  # Import socket module
from queue import Queue
import threading
import sys


class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
        self.server = socket.gethostname()  # Get local machine name
        self.port = 1997
        self.addr = (self.server, self.port)
        self.JOB_NUMBER = [1, 2]  # give each thread his job!
        self.connect_to_the_server()
        self.queue = Queue()
        self.NUMBER_THREAD = 2
        self.create_thread()
        self.create_jobs()

        """

         Thread 1--> Connect with The Server And Receiving Messages
         Thread 2--> Sending Messages

        """
        self.JOB_NUMBER = [1, 2]  # give each thread his job!
        self.queue = Queue()
        print(id)

    def connect_to_the_server(self):
        try:
            self.client.connect(self.addr)
            print("Connection Done!")
        except socket.error as msg:
            print("\nSocket Error ", str(msg))
            print("Retrying! ...")

    # define jobs and put each them in a queue
    def create_jobs(self):
        for x in self.JOB_NUMBER:
            self.queue.put(x)

        self.queue.join()

    def close(self):
        print("we will close the programme now!!")
        global open
        open = False
        sys.exit()
        quit()

    # create two necessary thread
    def create_thread(self):
        for i in range(self.NUMBER_THREAD):
            t = threading.Thread(target=self.job)  # creating a thread !
            """
            target =work that's means we will define a function that his name is work that it will till each thread what 
            will he do (what his job)

            """
            t.daemon = True  # this means that will the main thread will kill then make sure that also that thread will stop
            t.start()

    def job(self):
        while True:
            x = self.queue.get()
            if x == 1:
                self.receiving_message()
            if x == 2:
                self.send_message()

            self.queue.task_done()

    def receiving_message(self):
        global s
        global open
        open = True
        while open:
            try:
                data = self.client.recv(1024)
                if len(data) > 0:
                    # print the string output
                    print("Received Message is :", data[:].decode("utf-8"))
                    if data[:].decode("utf-8") == 'close':
                        open = False
                        self.client.send(str.encode('close'))
                        print("The connection with that server is closed!!")
                    self.client.send(str.encode("Message Is Received Correctly"))  # send the output to the server!!
            except:
                print("Some Error Occurred")
                open = False
        print("the System should be closed!! ")

    def send_message(self):
        global open
        while open:
            msg = input("\nInput the Message You wan't to send: ")
            try:
                self.client.send(str.encode(msg))  # send the output to the server!!
                print("\nThe Server Received The Message!")
            except socket.error:
                print("\nYour message is not received")


if __name__ == '__main__':
    client = Client()
