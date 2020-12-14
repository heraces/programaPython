from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError
import sys, csv, random, emoji
import sys
import csv
import random
import time

api_id = #API
api_hash = #HAS
phone = #TLF

SLEEP_TIME = 60
client = TelegramClient(phone, api_id, api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))


#hay que pasarle el nombre del archivo como argumento.
input_file = sys.argv[1]

users = []
with open(input_file, encoding='UTF-8') as f:
    rows = csv.reader(f,delimiter=";",lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {}
        user['id'] = int(row[0])
        user['access_hash'] = int(row[1])
        user['name'] = row[2]
        users.append(user)
        
#mode 1 para asegurarnos que enviamos por id y hash.
mode = 1

#ESTO DEBE CAMBIARSE MANUALMENTE
        
#Idioma 1 = ingles  Idioma 2 = Español.
#Hay que poner manualmente el nombre del grupo

idioma = 1
nombregrupo = "Soccer Betting Win System-FREE"

#ESTO DEBE CAMBIARSE MANUALMENTE

if idioma == 1:
    message =  (emoji.emojize(':folded_hands:') +" Sorry for the inconvenience but since you are a member of " + nombregrupo + ", let me send you this valuable information:\n"
                + emoji.emojize(':money_bag:') +"October: 2.566€ Profit\n"
                + emoji.emojize(':speaking_head:')+"3-7 Picks Daily\n"
                + emoji.emojize(':bar_chart:')+"Historical Results\n"
                + emoji.emojize(':wrapped_gift:')+"Free Channel (1 Pick per Day):\n"
                + emoji.emojize(':link:'))+"More info: https://1xdraw.com\n"
    
elif idioma == 2:
    message =  (emoji.emojize(':folded_hands:') +"Perdona las molestias, pero ya que formas parte del grupo " + nombregrupo + ", te envío esta información que quizás te interese:\n"
                + emoji.emojize(':money_bag:') +"Octubre: 2.566€ Beneficio\n"
                + emoji.emojize(':speaking_head:')+"3-7 Picks al Día\n"
                + emoji.emojize(':bar_chart:')+"Histórico de Resultados\n"
                + emoji.emojize(':wrapped_gift:')+" Canal Gratuito (1 Pick Diario)\n"
                + emoji.emojize(':link:'))+"Más info: 1xdraw.com/es\n"

for user in users:
    if  mode == 1:
        receiver = InputPeerUser(user['id'],user['access_hash'])
    else:
        print("Invalid Mode. Exiting.")
        client.disconnect()
        sys.exit()
    try:
        print("Sending Message to:", user['id'], user['name'])
        client.send_message(receiver, message.format(user['name']))
        print("Waiting {} seconds".format(SLEEP_TIME))
        time.sleep(SLEEP_TIME)
    except PeerFloodError:
        print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time. ")
        client.disconnect()
        sys.exit()
    except Exception as e:
        print("Error:", e)
        print("Trying to continue...")
        continue
    
client.disconnect()


