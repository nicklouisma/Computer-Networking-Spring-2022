from socket import *
from ssl import CHANNEL_BINDING_TYPES


def smtp_client(port=1025, mailserver='127.0.0.1'):
    msg = "\r\n My message"
    endmsg = "\r\n.\r\n"

    # Choose a mail server (e.g. Google mail server) if you want to verify the script beyond GradeScope
    mailServer = 'localhost'
    mailPort = 1025

    # Create socket called clientSocket and establish a TCP connection with mailserver and port

    # Fill in start
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((mailServer, mailPort))
    # Fill in end

    recv = clientSocket.recv(1024).decode()
    if recv[:3] != '220':
        clientSocket.close()
    #You can use these print statement to validate return codes from the server.

    # Send HELO command and print server response.
    heloCommand = 'HELO Alice\r\n'
    clientSocket.send(heloCommand.encode())
    recvHELO = clientSocket.recv(1024).decode()
    if recvHELO[:3] != '250':
        clientSocket.close()


    # Send MAIL FROM command and handle server response.
    # Fill in start
    mailfromCommand = 'MAIL FROM:<nicklouisma@gmail.com>\r\n'
    clientSocket.send(mailfromCommand.encode())
    recvMAIL = clientSocket.recv(1024).decode()
    if recvMAIL[:3] != '250':
        clientSocket.close()
    # Fill in end

    # Send RCPT TO command and handle server response.
    # Fill in start
    rcptToCommand = 'RCPT TO:<louismanick@gmail.com>\r\n'
    clientSocket.send(rcptToCommand.encode())
    recvRCPT = clientSocket.recv(1024).decode()
    if recvRCPT[:3] != '250':
        clientSocket.close()
    # Fill in end

    # Send DATA command and handle server response.
    # Fill in start
    data = "DATA\r\n"
    clientSocket.send(data.encode())
    recvDATA = clientSocket.recv(1024).decode()
    if recvDATA[:3] != '354':
        clientSocket.close()
    # Fill in end

    # Send message data.
    # Fill in start
    clientSocket.send(msg)
    # Fill in end

    # Message ends with a single period, send message end and handle server response.
    # Fill in start
    clientSocket.send(endmsg)
    # Fill in end

    # Send QUIT command and handle server response.
    # Fill in start
    quit = "QUIT\r\n"
    clientSocket.send(quit.encode())
    recvQUIT = clientSocket.recv(1024).decode()
    clientSocket.close()
    # Fill in end


if __name__ == '__main__':
    smtp_client(1025, '127.0.0.1')
