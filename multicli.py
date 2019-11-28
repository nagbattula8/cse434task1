import socket

import secrets

session_id = ""
login_id_c = ""
password_c = ""
sess_retrieval = False
client_receive = False

# create our udp socket
try:
    socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print("Oops, something went wrong connecting the socket")
    exit()

while 1:
    message = input("> ")
    message_copy = message

    if ( message == 'reg'):
        login_id = input("login_id > ")
        password = input("password > ")
        # encode the message
        message = message+'#'+login_id+'##'+password
        message = message.encode()
    elif ( message == 'login'):
        login_id = input("login_id > ")
        password = input("password > ")

        message = message + "#"+login_id+"##"+password+"##"+session_id
        sess_retrieval = True
        message = message.encode()

    elif message == "session":
        print(session_id)   
        continue

    elif message == "post":
        input_message = input("Enter message > ")
        message = message + "#" + input_message + "#" + session_id
        print(message[:5])
        message = message.encode()

    elif message == "clients":
        message = message+"#"+session_id
        message = message.encode()
        client_receive = True

    elif message == "subscribe":
        input_message = input("subscribe to: > ")
        message+= "#" + input_message + "#" + session_id
        message = message.encode()
    elif message == "retrieve":
        input_message = input("How many latest posts from each client: > ")
        message+= "#" + input_message + "#" + session_id
        message = message.encode()
    elif message == "unsubscribe":
        input_message = input("unsubscribe from > ")
        message+= "#"+input_message + "#" + session_id
        message = message.encode()
    elif message == "spurious":
        message+= "#"
        message = message.encode()
    elif message == "logout":
        message = message.encode()
    else:
        message = message.encode()

    


    try:
        # send the message
        if ( message_copy == "retrieve"):
            '''socket.sendto(message, ("10.157.222.173", 9999))

            # output the response (if any)
            data, ip = socket.recvfrom(1024)

            print("{}: {}".format(ip, data.decode()))
            if ( sess_retrieval == True ):
                session_id = data.decode()
                sess_retrieval = False
                print(session_id)

            if ( client_receive == True ):
                clients = data.decode()
                clients = clients.split('#')
                clients.remove("")
                client_receive = False
                print(clients)'''

            socket.sendto(message, ("192.168.0.253", 9999))
            data, ip = socket.recvfrom(65536)
            print("{}: {}".format(ip, data.decode()))

            data2 = data.decode()

            if ( data2 == "Subscribed to no one#0"):
                print( "No posts retrieved")
            else:
                posts_leng = data.decode()
                if (posts_leng == "Session expired. Login again" ):
                    continue
                posts_leng = posts_leng.split('#')
                posts_len = int(posts_leng[0])
                session_id = str(posts_leng[1])

                for i in range(posts_len):
                    data, ip = socket.recvfrom(65536)
                    print("{}: {}".format(ip, data.decode()))

        else:
            socket.sendto(message, ("192.168.0.253", 9999))
            # output the response (if any)
            
            data, ip = socket.recvfrom(65536)

            print("{}: {}".format(ip, data.decode()))
            data2 = data.decode()

            if( data2 == "Session expired. Login again" or data2 == "Message type unidentified. Closing session. Please login again"):
                session_id = ""
                continue

            elif ( sess_retrieval == True ):
                session_var = data.decode()
                session_var = session_var.split("#")
                if session_var[0] == "Already logged in":
                    session_id = session_var[1]
                    continue
                session_id = session_var[0]
                sess_retrieval = False
                print(session_id)
                continue
            
            data2 = data2.split('#')
            if (data2[0] == "Logged out successfully. Session reset" or data2[0] == "Already logged out."):
                continue

            if ( data2[0] == "Registered successfully" or data2[0] == "ID taken" or data2[0] == "Already registered" ):
                continue
            elif ( data2[1] == "Posted successfully"):
                session_id = data2[2]
                continue

            elif ( data2[0] == "subscribed successfully"):
                session_id = data2[1]
                continue

            elif ( data2[0] == "Unsubscribed successfully"):
                session_id = data2[1]
                print(session_id)
                continue
            elif (data2[0] == "Server corrupted" ):
                message = data2[0].encode()
                print("Unidentified message. Reset triggered")
                socket.sendto(message, ("192.168.0.253", 9999) )
                data12, ip12 = socket.recvfrom(65536)

                print("{}: {}".format(ip12, data12.decode()))

            if ( client_receive == True ):
                clients = data.decode()
                clients = clients.split('#')
                clients.remove("")
                client_receive = False
                print(clients)



    except socket.error:
        print("Error! {}".format(socket.error))
        exit()