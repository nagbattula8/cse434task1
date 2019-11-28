import socket
import secrets
import time

# set up the socket using local address
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket.bind(("", 9999))

clientdb = {}

sessiondb = {}

subsdb = {}

postdb = {}

#posts = ['hi','hello','salaam']

while 1:

    # get the data sent to us
    data, ip = socket.recvfrom(65536)
    #print(data)
    #print(ip)

    # display
    #print("{}: {}".format(ip, data.decode(encoding="utf-8").strip()))

    message = data.decode(encoding="utf-8").strip()


    print(message)

    if ( message[:4] == 'reg#'):

        message = message[4:]
        print(message)
        login_pass = message.split('##')
        print(login_pass)
        usernameExits = False
        if ip not in clientdb:

            for i in clientdb.values():
                if ( i[0] == login_pass[0]):
                    username_error = "ID taken"
                    usernameExits = True
                    username_error = username_error.encode()
                    socket.sendto(username_error,ip)

            if ( usernameExits == False ):
                clientdb[ip] = login_pass[0:2]
                str_user_registered = "Registered successfully"
                str_user_registered = str_user_registered.encode()
                socket.sendto(str_user_registered,ip)
        else:
            reg_error = "Already registered"
            reg_error = reg_error.encode()
            socket.sendto(reg_error,ip)

    elif ( message[:6] == 'login#'):

        message = message[6:]
        #print(message)
        login_pass = message.split('##')
        #print(login_pass)

        if ip not in sessiondb:
            if ip not in clientdb:
                str_invalid = "Invalid login"
                print(str_invalid)
                str_invalid = str_invalid.encode()
                socket.sendto(str_invalid,ip)
            else:
                client_details = clientdb[ip]
                print(client_details)
                if ( login_pass[0] == client_details[0] and login_pass[1] == client_details[1]):
                    millis = int(round(time.time() * 1000))
                    sessiondb[ip] = str(millis)
                    token_str = sessiondb[ip] + "#" + "Logged in successfully"
                    token_str = token_str.encode()
                    socket.sendto(token_str,ip)
                else:
                    str_invalid = "Invalid login"
                    print(str_invalid)
                    str_invalid = str_invalid.encode()
                    socket.sendto(str_invalid,ip)
        else:
            if ( sessiondb[ip] == login_pass[2] ):
                mes = "Already logged in#"
                millis = int(round(time.time() * 1000))
                millis = str(millis)
                sessiondb[ip] = millis
                mes = mes+millis
                mes = mes.encode()
                print("Already logged in")
                socket.sendto(mes,ip)
    elif ( message[:5] == "post#" ):
        post_split = message.split('#')
        if ip not in sessiondb:
            sending_message = "Session expired. Login again"
            sending_message = sending_message.encode()
            socket.sendto(sending_message,ip)
        elif ( sessiondb[ip] == post_split[2] ):
            sess_mills = int(sessiondb[ip])
            millis = int(round(time.time() * 1000))

            if ( (millis - sess_mills) > 60000):
                sessiondb.pop(ip)
                sending_message = "Session expired. Login again"
                sending_message = sending_message.encode()
                socket.sendto(sending_message,ip)
                continue

            if ( ip not in postdb ):
                postdb[ip] = []
            postdb[ip].append(post_split[1])
            print( postdb )
            millis = int(round(time.time() * 1000))
            millis = str(millis)
            post_data = post_split[1] + "#"+ "Posted successfully#" + millis
            sessiondb[ip] = millis
            post_data = post_data.encode()
            socket.sendto(post_data,ip)
        else:
            sending_message = "Session expired. Log in again"
            sessiondb.pop(ip)
            sending_message = sending_message.encode()
            socket.sendto(sending_message,ip)

    elif ( message[:8] == "clients#" ):
        clients = ""
        client_message = message.split('#')
        if ip not in sessiondb.keys():
            sending_message = "Session expired. Login again"
            sending_message = sending_message.encode()
            socket.sendto(sending_message,ip)        

        elif ( sessiondb[ip] == client_message[1] ):
            sess_mills = int(sessiondb[ip])
            millis = int(round(time.time() * 1000))

            if ( (millis - sess_mills) > 60000):
                sessiondb.pop(ip)
                sending_message = "Session expired. Login again"
                sending_message = sending_message.encode()
                socket.sendto(sending_message,ip)
                continue

            for i in clientdb.keys():
                clients = clients + clientdb[i][0] + "#"
            millis = int(round(time.time() * 1000))
            millis = str(millis)
            client = client + millis
            clients = clients.encode()
            socket.sendto(clients,ip)
        else:
            sending_message = "Session expired. Login again"
            sessiondb.pop(ip)
            sending_message = sending_message.encode()
            socket.sendto(sending_message,ip)
    elif ( message[:10] == "subscribe#" ):
        subscribe_message = message.split("#")
        #print(subscribe_message)
        if ip not in sessiondb.keys():
            sending_message = "Session expired. Login again"
            sending_message = sending_message.encode()
            socket.sendto(sending_message,ip)
        elif ( sessiondb[ip] == subscribe_message[2] ):
            sess_mills = int(sessiondb[ip])
            millis = int(round(time.time() * 1000))

            if ( (millis - sess_mills) > 60000):
                sessiondb.pop(ip)
                sending_message = "Session expired. Login again"
                sending_message = sending_message.encode()
                socket.sendto(sending_message,ip)
                continue
            if ip not in subsdb:
                subsdb[ip] = []
            for key in clientdb.keys():
                if ( clientdb[key][0] == subscribe_message[1] ):
                    print(subscribe_message[1], key)
                    subsdb[ip].append(key)
                    sub_success = "subscribed successfully"
                    print(subsdb)
                    millis = int(round(time.time() * 1000))
                    millis = str(millis)
                    sub_success+= "#"+millis
                    sessiondb[ip] = millis
                    sub_success = sub_success.encode()
                    socket.sendto(sub_success,ip)
        else:
            sending_message = "Session expired. Login again"
            sessiondb.pop(ip)
            sending_message = sending_message.encode()
            socket.sendto(sending_message,ip)

    elif ( message[:9] == "retrieve#"):
        print("retrieve entry")
        retrieve_message = message.split("#")
        if ip not in sessiondb.keys():
            print("1")
            sending_message = "Session expired. Login again"
            sending_message = sending_message.encode()
            socket.sendto(sending_message,ip)
        elif ( sessiondb[ip] == retrieve_message[2]):
            sess_mills = int(sessiondb[ip])
            millis = int(round(time.time() * 1000))

            if ( (millis - sess_mills) > 60000):
                sessiondb.pop(ip)
                print("2")
                sending_message = "Session expired. Login again"
                sending_message = sending_message.encode()
                socket.sendto(sending_message,ip)
                continue

            if (ip not in subsdb or subsdb[ip] == []):
                no_subs_message = "Subscribed to no one#0"
                no_subs_message = no_subs_message.encode()
                socket.sendto(no_subs_message,ip)
            else:
                print("Entered")
                length_subs = len(subsdb[ip])
                print(clientdb) 
                posts = []
                requirement_length = int(retrieve_message[1])
                length_check = 0
                for client in subsdb[ip]:
                    for post in postdb[client][::-1]:
                        posts.append("Post by " + str(clientdb[client][0]) + " : " + post)
                        length_check+=1
                        if (length_check == requirement_length):
                            break
                    length_check = 0
                print(posts)
                post_length = len(posts)
                post_length = str(post_length)
                millis = int(round(time.time() * 1000))
                millis = str(millis)
                sessiondb[ip] = millis
                post_length+= "#"+millis
                post_length = post_length.encode()
                socket.sendto(post_length,ip)
                for post in posts:
                    sending_message = post.encode()
                    socket.sendto(sending_message,ip)
        else:
            sending_message = "Session expired. Login again"
            print("3")
            sessiondb.pop(ip)
            sending_message = sending_message.encode()
            socket.sendto(sending_message,ip)


    elif ( message[:12] == "unsubscribe#" ):
        unsubscribe_message = message.split("#")
        #print(subscribe_message)
        if ip not in sessiondb.keys():
            sending_message = "Session expired. Log in again"
            sending_message = sending_message.encode()
            socket.sendto(sending_message,ip)
        elif ( sessiondb[ip] == unsubscribe_message[2] ):
            sess_mills = int(sessiondb[ip])
            millis = int(round(time.time() * 1000))

            if ( (millis - sess_mills) > 60000):
                sessiondb.pop(ip)
                sending_message = "Session expired. Login again"
                sending_message = sending_message.encode()
                socket.sendto(sending_message,ip)
                continue
            
            millis = int(round(time.time() * 1000))
            millis = str(millis)

            if ip not in subsdb:
                sending_message = "Didnt subscribe to anyone"
                sending_message = sending_message.encode()
                socket.sendto(sending_message,ip)
            else:
                for key in clientdb.keys():
                    if ( clientdb[key][0] == unsubscribe_message[1] ):
                        #print(subscribe_message[1], key)
                        subsdb[ip].remove(key)
                        print(subsdb)
                        sub_success = "Unsubscribed successfully#"+millis
                        sessiondb[ip] = millis
                        print(sub_success)
                        print(subsdb)
                        sub_success = sub_success.encode()
                        socket.sendto(sub_success,ip)
        else:
            sending_message = "Session expired. Log in again"
            sessiondb.pop(ip)
            sending_message = sending_message.encode()
            socket.sendto(sending_message,ip)
    elif ( message == "logout" ):
        sending_message = "Logged out successfully. Session reset"
        if ip in sessiondb:
            sessiondb.pop(ip)
        else:
            sending_message = "Already logged out."
        sending_message = sending_message.encode()
        socket.sendto(sending_message,ip)

    elif ( message == "spurious#" ):
        sending_message = "Server corrupted#"
        print(sending_message)
        clientdb = {}

        sessiondb = {}

        subsdb = {}

        postdb = {}
        sending_message = sending_message.encode()
        socket.sendto(sending_message,ip)




    else:
        sending_message = "Message type unidentified. Closing session. Please login again"
        if ip in sessiondb:
            sessiondb.pop(ip)
        sending_message = sending_message.encode()
        socket.sendto(sending_message,ip)


