import os
import sys
import datetime
from argparse import ArgumentParser
from smtplib import  SMTP_SSL as SMTP
from email.mime.text import MIMEText

class globvars():
    POS = []
    RECEIVERS = ["empfaenger1@email.de", "empfaenger2@email.com"]

def readList(arg):
    for file in arg.c: 
        with open(file, "r") as f:
            lines = f.readlines()
        
        tomorrow = datetime.timedelta(days=1) + datetime.datetime.now()
        tomorrow = tomorrow.strftime("%d.%m.%Y")
        for line in lines:
         if tomorrow in line.strip():
           globvars.POS.append(os.path.splitext(os.path.basename(file))[0])


def sendMail(receiver):

    SERVER = ""    #smtp server
    USER = "" #email Nutzername
    PASSWORD = "" #email Passwort
    text_subtype = 'plain'
    sender = ""  #Absenderemail
    pos_list = ""
    for elem in globvars.POS:
        pos_list += "- " + elem + os.linesep
    message = str("Liebe Gemeinde,\r\n"
     "Morgen werden folgende Tonnen abgeholt : \r\n" + pos_list +  
      "\r\n Es wäre sehr nett, wenn ihr mal bis heute Abend gucken könntet, ob die Tonnen wirklich (bis auf Restmüll) draußen sind.\r\n"
                                       "\r\n"
     "Beep Bop Beep,\r\n"
     "Dein Abfallbot")
    msg = MIMEText(message, text_subtype)
    msg['Subject'] = "Müllabholtermin"   #email Betreff
    msg["From"] = ""  #Dieses Feld wird dem Empfänger als Absender angezeigt. Format "Vorname Nachname <email@emailanbieter.com>"

    s = SMTP(SERVER)
    s.set_debuglevel(False)
    s.login(USER, PASSWORD)
    s.sendmail(sender, receiver, msg.as_string())
    s.quit()
    return True

def main(argv = sys.argv[1:]):

    parser = ArgumentParser()
    parser.add_argument("-c", help="list txt file" , nargs="+")
    arg = parser.parse_args()
    if arg.c is None:
        print("No list specified")
        exit()
    readList(arg)
    if not len(globvars.POS) == 0:
        print("Benachrichtigung für folgende Tonne(n) wird verschickt:")
        print(*globvars.POS, sep="\r\n")
        for receiver in globvars.RECEIVERS:
         sendMail(receiver)
    else:
        print("Morgen muss man keine Tonne rausstellen")
if __name__ == "__main__":
    main()
