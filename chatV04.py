import time
import sys
import os
import paho.mqtt.client as mqtt

msg = ''

#---------------------------MQTT DATA-------------------------------------------
MQTTusr = "hgvybxzp"
MQTTpsw = "xH06RYvLNNTF"
MQTTadr = "m14.cloudmqtt.com"
MQTTport = 11754
#-------------------------------------------------------------------------------

class User(object):
    """docstring for user."""
    def __init__(self, nick, topic):
        super(User, self).__init__()
        self.nick = nick
        self.topic = topic

    def chNick(self):
        self.nick = input('\n\n\n\n\t\t\t    Insert your displayname:\n\n\t\t\t\t    ')

    def chTopic(self):
        self.topic = input('\n\n\n\n\t\t\t\tInsert the topic:\n\n\t\t\t\t     ')


class Console(object):
    """docstring for console."""
    def __init__(self):
        super(Console, self).__init__()

    #Callback method for clear connsole
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    #Callback method for clear the line
    def clearLine(self):
        sys.stdout.write('\x1b[1A')
        sys.stdout.write('\x1b[2K')

    #Callback method for call the menu, here you can change topic and displayname
    def menu(self, User, Client):   #TODO PROVA A SPOSTARE TUTTO SOTTO USER
        self.clear()
        swt = int(input('Select one of the following option:\n0-Change displayname\n1-Change topic\n\nOr press another key to quit\n'))
        if swt==0:
            self.clear()
            usr.chNick()
        elif swt==1:
            self.clear()
            usr.chTopic()
            client.subscribe(usr.topic)
        self.clear()
        self.header(usr)

    def header(self, User):
        self.clear()
        print('¯ ¯ ¯ ¯ ¯ ¯ ¯ ¯ ¯ ¯ ¯ ¯ ¯ ¯ ¯ ¯ ¯ ¯ ¯ ¯ ¯ ¯ ¯ ¯ ¯ ¯ ¯ ¯ ¯ ¯ ¯ ¯ ¯ ¯ ¯ ¯ ¯ ¯ ¯ ¯')
        print('  CONNECTED as ' + usr.nick + ' to ' + usr.topic + '')
        print('_______________________________________________________________________________')


cons = Console()
usr = User('','')
cons.clear()
usr.chNick()
cons.clear()
usr.chTopic()


# Callback Function on Connection with MQTT Server              #TODO convertire a oggetti
def on_connect( client, userdata, flags, rc):
    #print ("Connected with Code :" +str(rc))
    if(rc==0):
        cons.header(usr)
    else:
        print('Error: ' + rc)
    # Subscribe Topic from here
    client.subscribe(usr.topic)

# Callback Function on Receiving the Subscribed Topic/Message
def on_message( client, userdata, msg):
    # print the message received from the subscribed topic
    sys.stdout.write(u"\u001b[1000D")   #Delate the line and return at starting position
    newMsg = str(msg.payload)
    print ( newMsg.replace("b","",1) )

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(MQTTusr, MQTTpsw)
client.connect(MQTTadr, MQTTport, 60)

# client.loop_forever()
client.loop_start()
time.sleep(1)
while True:

    msg=input('')
    if msg=="--menu":
        cons.menu(usr, client)
    else:
        pack = usr.nick + ": " + msg
        cons.clearLine()
        client.publish(usr.topic,pack)


client.loop_stop()
client.disconnect()
