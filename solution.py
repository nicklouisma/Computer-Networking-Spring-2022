# import socket module
from socket import *
# In order to terminate the program
import sys


def webServer(port=13331):
  serverSocket = socket(AF_INET, SOCK_STREAM)
  #Prepare a server socket
  serverSocket.bind(("", port))
  #Fill in start
  #print("socket binded to %s", port)
  serverSocket.listen(1)
  #print('Listening on port %s...', port)

  #Fill in end

  while True:
    #Establish the connection
    #print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    #Fill in start
    connectionSocket.recv(1024).decode()
         
    #Fill in end
    try:
      try:
        message = 'GET /hellowworld.html\r\n'
        
        #Fill in start    
        #Fill in end

        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()
        
        #Fill in start  
           
        #Fill in end
        
        #Send one HTTP header line into socket.
        #Fill in start
        send200 = 'HTTP/1.1 200 OK\r\n'
        connectionSocket.send(send200.encode())
        #Fill in end

        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
          connectionSocket.send(outputdata[i].encode())

        connectionSocket.send("\r\n".encode())
        connectionSocket.close()
      except IOError:
        # Send response message for file not found (404)
        #Fill in start
        send404 = 'HTTP/1.1 404 Not Found\r\n'
        connectionSocket.send(send404.encode())
        #Fill in end


        #Close client socket
        connectionSocket.close()
        #Fill in start

        #Fill in end

    except (ConnectionResetError, BrokenPipeError):
      pass

  serverSocket.close()
  sys.exit()  # Terminate the program after sending the corresponding data

if __name__ == "__main__":
  webServer(13331)
