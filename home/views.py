# Create your views here.
from django.shortcuts import render, redirect
from . import forms
from .models import Details
from .models import Compose
import imaplib, email
from gtts import gTTS
import os
from playsound import playsound
from django.http import HttpResponse
import speech_recognition as sr
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from django.http import JsonResponse
import re

file = "good"
i="0"
passwrd = ""
addr = ""
item =""
subject = ""
body = ""
s = smtplib.SMTP('smtp.gmail.com', 587)
s.ehlo()
s.starttls()
s.ehlo()
imap_url = 'imap.gmail.com'
conn = imaplib.IMAP4_SSL(imap_url)
attachment_dir = 'C:/Users/Britney/Desktop/'

def texttospeech(text, filename):  #converts text to speech 
    filename = filename + '.mp3'
    while True:
        try:
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(filename)
            break
        except:
            print('Trying again')
    playsound(filename)
    os.remove(filename)
    return

def speechtotext(duration):      #converst what the user says into text and stores into file 
    global i, addr, passwrd
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        playsound('speak.mp3')
        audio = r.listen(source, phrase_time_limit=duration)
    try:
        response = r.recognize_google(audio)
    except:
        response = 'N'
    return response

def convert_special_char(text):  #takes words and makes sure they are converted into their character
    key=text
    special_chars = ['at','dot','underscore','dollar','hash','star','plus','minus','space','dash']
    for character in special_chars:
        while(True):
            pos=key.find(character)
            if pos == -1:
                break
            else :
                if character == 'at':
                    key=key.replace('at','@')
                elif character == 'dot':
                    key=key.replace('dot','.')
                elif character == 'underscore':
                    key=key.replace('underscore','_')
                elif character == 'dollar':
                    key=key.replace('dollar','$')
                elif character == 'hash':
                    key=key.replace('hash','#')
                elif character == 'star':
                    key=key.replace('star','*')
                elif character == 'plus':
                    key=key.replace('plus','+')
                elif character == 'minus':
                    key=key.replace('minus','-')
                elif character == 'space':
                    key = key.replace('space', '')
                elif character == 'dash':
                    key=key.replace('dash','-')
    return key

def home(request):
    addr = ""
    passwrd = ""

    return render(request, 'home/homepage.html')

def login_type_view(request):
    global i, addr, passwrd 

    if request.method == 'POST':
        addr = request.POST.get("email")
        passwrd = request.POST.get("password")
        print(addr, passwrd)
        request.email = addr

        imap_url = 'imap.gmail.com'
        #passwrd = ''
        #addr = ''
        conn = imaplib.IMAP4_SSL(imap_url)
        try:
            conn.login(addr, 'vuzaialuwrljbxit')
            #conn.login(addr, 'lpohepufhxyeoslv')
            #myyckrhcpkrkxagg
            s.login(addr, 'vuzaialuwrljbxit')
            #s.login(addr, 'lpohepufhxyeoslv')
            texttospeech("Congratulations. You have logged in successfully. You will now be redirected to the menu page.", file + i)
            i = i + str(1)
            return redirect('/options/')
            #return JsonResponse({'result' : 'success'})
        except:
            texttospeech("Invalid Login Details. Please try again.", file + i)
            i = i + str(1)
            return redirect('/login.html/')

    detail  = Details()
    detail.email = addr
    detail.password = passwrd
    
    #return render(request, 'home/login.html', {'detail' : detail}) 

def login_view(request):
    global i, addr, passwrd 

    if request.method == 'POST':
        text1 = "Welcome to our Email Voice Assistant App, evoice. Login with your gmail account to continue. "
        texttospeech(text1, file + i)
        i = i + str(1)
        flag = True
        while (flag):
            texttospeech("Enter your Email", file + i)
            i = i + str(1)
            addr = speechtotext(10)
            
            if addr != 'N':
                texttospeech("You meant " + addr + " say yes to confirm or no to enter again", file + i)
                i = i + str(1)
                say = speechtotext(3)
                if say == 'yes' or say == 'Yes':
                    flag = False
            else:
                texttospeech("could not understand what you meant:", file + i)
                i = i + str(1)
        addr = addr.strip()
        addr = addr.replace(' ', '')
        addr = addr.lower()
        addr = convert_special_char(addr)
        print(addr)
        request.email = addr
        flag = True
        while (flag):
            texttospeech("Enter your password", file + i)
            i = i + str(1)
            passwrd = speechtotext(20)
            
            if addr != 'N':
                texttospeech("You meant " + passwrd + " say yes to confirm or no to enter again", file + i)
                i = i + str(1)
                say = speechtotext(3)
                if say == 'yes' or say == 'Yes':
                    flag = False
            else:
                texttospeech("could not understand what you meant:", file + i)
                i = i + str(1)
        passwrd = passwrd.strip()
        passwrd = passwrd.replace(' ', '')
        passwrd = passwrd.lower()
        passwrd = convert_special_char(passwrd)
        print(passwrd)

        imap_url = 'imap.gmail.com'
        #passwrd = ''
        #addr = ''
        conn = imaplib.IMAP4_SSL(imap_url)
        try:
            conn.login(addr, 'vuzaialuwrljbxit')
            s.login(addr, 'vuzaialuwrljbxit')
            texttospeech("Congratulations. You have logged in successfully. You will now be redirected to the menu page.", file + i)
            i = i + str(1)
            return JsonResponse({'result' : 'success'})
        except:
            texttospeech("Invalid Login Details. Please try again.", file + i)
            i = i + str(1)
            return JsonResponse({'result': 'failure'})

    detail  = Details()
    detail.email = addr
    detail.password = passwrd
    return render(request, 'home/login.html', {'detail' : detail}) 

def options_view(request):
    global i, addr, passwrd
    if request.method == 'POST':
        flag = True
        texttospeech("You are logged into your account. What would you like to do ?", file + i)
        i = i + str(1)
        while(flag):
            texttospeech("To compose an email say compose. To open Inbox folder say Inbox. To open Sent folder say Sent. To open Trash folder say Trash. To Logout say Logout. Do you want me to repeat?", file + i)
            i = i + str(1)
            say = speechtotext(3)
            if say == 'No' or say == 'no':
                flag = False

        texttospeech("Enter your choice", file + i)
        i = i + str(1)
        act = speechtotext(5)
        act = act.lower()
        if act == 'compose':
            return JsonResponse({'result' : 'compose'})
        elif act == 'inbox':
            return JsonResponse({'result' : 'inbox'})
        elif act == 'sent':
            return JsonResponse({'result' : 'sent'})
        elif act == 'trash':
            return JsonResponse({'result' : 'trash'})
        elif act == 'logout':
            addr = ""
            passwrd = ""
            texttospeech("You have been logged out of your account and now will be redirected back to the login page.",file + i)
            i = i + str(1)
            #return redirect('/')
            return JsonResponse({'result': 'logout'})
        else:
            texttospeech("Invalid action. Please try again.", file + i)
            i = i + str(1)
            return JsonResponse({'result': 'failure'})
    elif request.method == 'GET':
        return render(request, 'home/options.html')

def compose_view(request):  
    global i, addr, passwrd, s, item, subject, body
    if request.method == 'POST':
        text1 = "You have reached the page where you can compose and send an email. "
        texttospeech(text1, file + i)
        i = i + str(1)
        flag = True
        flag1 = True
        fromaddr = addr
        toaddr = list()
        while flag1:
            while flag:
                texttospeech("Enter receiver's email address:", file + i)
                i = i + str(1)
                to = ""
                to = speechtotext(15)
                if to != 'N':
                    
                    texttospeech("You meant " + to + " say yes to confirm or no to enter again", file + i)
                    i = i + str(1)
                    say = speechtotext(5)
                    if say == 'yes' or say == 'Yes':
                        toaddr.append(to)
                        flag = False
                else:
                    texttospeech("Could not understand what you meant", file + i)
                    i = i + str(1)
            texttospeech("Do you want to enter more recipients ?  Say yes or no.", file + i)
            i = i + str(1)
            say1 = speechtotext(3)
            if say1 == 'No' or say1 == 'no':
                flag1 = False
            flag = True

        newtoaddr = list()
        for item in toaddr:
            item = item.strip()
            item = item.replace(' ', '')
            item = item.lower()
            item = convert_special_char(item)
            newtoaddr.append(item)
            print(item)

        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = ",".join(newtoaddr)
        flag = True
        while (flag):
            texttospeech("enter subject", file + i)
            i = i + str(1)
            subject = speechtotext(10)
            if subject == 'N':
                texttospeech("could not understand what you meant", file + i)
                i = i + str(1)
            else:
                flag = False
        msg['Subject'] = subject
        flag = True
        while flag:
            texttospeech("enter body of the mail", file + i)
            i = i + str(1)
            body = speechtotext(20)
            if body == 'N':
                texttospeech("could not understand what you meant", file + i)
                i = i + str(1)
            else:
                flag = False

        msg.attach(MIMEText(body, 'plain'))
        try:
            s.sendmail(fromaddr, newtoaddr, msg.as_string())
            texttospeech("Your email has been sent successfully. You will now be redirected to the menu page.", file + i)
            i = i + str(1)
        except:
            texttospeech("Sorry, your email failed to send. please try again. You will now be redirected to the the compose page again.", file + i)
            i = i + str(1)
            return JsonResponse({'result': 'failure'})
        s.quit()
        return JsonResponse({'result' : 'success'})
    
    compose  = Compose()
    compose.recipient = item
    compose.subject = subject
    compose.body = body

    return render(request, 'home/compose.html', {'compose' : compose})

def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)

def reply_mail(id, message):
    global i,s
    TO_ADDRESS = message['From']
    FROM_ADDRESS = addr
    msg = email.mime.multipart.MIMEMultipart()
    msg['to'] = TO_ADDRESS
    msg['from'] = FROM_ADDRESS
    msg['subject'] = message['Subject']
    msg.add_header('In-Reply-To', id)
    flag = True
    while(flag):
        texttospeech("Enter body.", file + i)
        i = i + str(1)
        body = speechtotext(20)
        print(body)
        try:
            msg.attach(MIMEText(body, 'plain'))
            s.sendmail(msg['from'], msg['to'], msg.as_string())
            texttospeech("Your reply has been sent successfully.", file + i)
            i = i + str(1)
            flag = False
        except:
            texttospeech("Your reply could not be sent. Do you want to try again? Say yes or no.", file + i)
            i = i + str(1)
            act = speechtotext(3)
            act = act.lower()
            if act != 'yes':
                flag = False

def forward_mail(item, message):
    global i,s
    flag1 = True
    flag = True
    global i
    newtoaddr = list()
    while flag:
        while flag1:
            while True:
                texttospeech("Enter receiver's email address", file + i)
                i = i + str(1)
                to = speechtotext(15)
                texttospeech("You meant " + to + " say yes to confirm or no to enter again", file + i)
                i = i + str(1)
                yn = speechtotext(3)
                yn = yn.lower()
                if yn == 'yes':
                    to = to.strip()
                    to = to.replace(' ', '')
                    to = to.lower()
                    to = convert_special_char(to)
                    print(to)
                    newtoaddr.append(to)
                    break
            texttospeech("Do you want to add more receiver?", file + i)
            i = i + str(1)
            ans1 = speechtotext(3)
            ans1 = ans1.lower()
            print(ans1)
            if ans1 == "no" :
                flag1 = False

        message['From'] = addr
        message['To'] = ",".join(newtoaddr)
        try:
            s.sendmail(addr, newtoaddr, message.as_string())
            texttospeech("Your mail has been forwarded successfully.", file + i)
            i = i + str(1)
            flag = False
        except:
            texttospeech("Your mail could not be forwarded. Do you want to try again? Say yes or no.", file + i)
            i = i + str(1)
            act = speechtotext(3)
            act = act.lower()
            if act != 'yes':
                flag = False

def read_mail(mailList, folder):
    global s, i
    mailList.reverse()
    mailCount = 0
    readList = list()

    for item in mailList:
        result, emailData = conn.fetch(item, '(RFC822)')
        rawEmail = emailData[0][1].decode()
        message = email.message_from_string(rawEmail)
        To = message['To']
        From = message['From']
        Subject = message['Subject']
        Id = message['Message-ID']

        '''texttospeech("Email number " + str(mailCount+1) + " .The mail's from " + From + "  . The subject is " + Subject, file + i)
        i = i + str(1)

        print('Message ID= ', Id)
        print('From :', From)
        print('To :', To)
        print('Subject :', Subject)
        print("\n")'''

        readList.append(Id)
        mailCount = mailCount + 1

    flag = True
    while flag:
        n = 0
        flag1 = True
        while flag1:
            texttospeech("Enter the email number you want to read.", file + i)
            i = i + str(1)
            n = speechtotext(3)
            print(n)
            texttospeech("You meant " + str(n) + ". Say yes or no.", file + i)
            i = i + str(1)
            say = speechtotext(2)
            say = say.lower()
            if say == 'yes':
                flag1 = False
    
        n = int(n)
        msg_id = readList[n - 1]
        print('Message ID = ', msg_id)
        typ, data = conn.search(None, '(HEADER Message-ID "%s")' % msg_id)
        data = data[0]
        result, emailData = conn.fetch(data, '(RFC822)')
        rawEmail = emailData[0][1].decode()
        message = email.message_from_string(rawEmail)
        
        To = message['To']
        From = message['From']
        Subject = message['Subject']
        Id = message['Message-ID']
        print('From :', From)
        print('To :', To)
        print('Subject :', Subject)

        texttospeech("The mail is from " + From + " to " + To + " . The subject of the mail is " + Subject, file + i)
        i = i + str(1)

        Body = get_body(message)
        Body = Body.decode()
        Body = re.sub('<.*?>', '', Body)
        Body = os.linesep.join([s for s in Body.splitlines() if s])
        if Body != '':
            texttospeech("The content of the mail is ", file + i)
            i = i + str(1)
            texttospeech(Body, file + i)
            i = i + str(1)
        else:
            texttospeech("Body is empty", file + i)
            i = i + str(1)
        #get_attachment(message)

        if folder == 'inbox':
            texttospeech("Do you want to reply to this mail? Say Yes or No ", file + i)
            i = i + str(1)
            ans = speechtotext(3)
            ans = ans.lower()
            print(ans)
            if ans == "yes":
                reply_mail(Id, message)
        
        if folder == 'inbox' or folder == 'sent':
            texttospeech("Do you want to forward this mail to anyone? Say yes or no. ", file + i)
            i = i + str(1)
            ans = speechtotext(3)
            ans = ans.lower()
            print(ans)
            if ans == "yes":
                forward_mail(Id, message)

        if folder == 'inbox' or folder == 'sent':
            texttospeech("Do you want to delete this mail? Say yes or no. ", file + i)
            i = i + str(1)
            ans = speechtotext(3)
            ans = ans.lower()
            print(ans)
            if ans == "yes":
                try:
                    conn.store(data, '+X-GM-LABELS', '\\Trash')
                    conn.expunge()
                    texttospeech("The mail has been deleted successfully.", file + i)
                    i = i + str(1)
                    print("mail deleted")
                except:
                    texttospeech("Sorry, could not delete this mail. Please try again later.", file + i)
                    i = i + str(1)

        if folder == 'trash':
            texttospeech("Do you want to delete this mail? Say yes or no. ", file + i)
            i = i + str(1)
            ans = speechtotext(3)
            ans = ans.lower()
            print(ans)
            if ans == "yes":
                try:
                    conn.store(data, '+FLAGS', '\\Deleted')
                    conn.expunge()
                    texttospeech("The mail has been deleted permanently", file + i)
                    i = i + str(1)
                    print("Mail deleted")
                except:
                    texttospeech("Could not delete this mail. Please try again later", file + i)
                    i = i + str(1)
        
        texttospeech("Email ends here", file + i)
        i = i + str(1)
        texttospeech("Do you want to read more mails?", file + i)
        i = i + str(1)
        ans = speechtotext(3)
        ans = ans.lower()
        if ans == 'no':
            flag = False

def search_mail(folder, key, value, folderName):
    global i, conn
    conn.select(folder)
    result, data = conn.search(None, key, '"{}"'.format(value))
    mailList = data[0].split()
    if len(mailList) != 0:
        texttospeech("There are " + str(len(mailList)) + " emails with this email address", file + i)
        i = i + str(1)
    if len(mailList) == 0:
        texttospeech("There are no emails with this email address", file + i)
        i = i + str(1)
    else:
        read_mail(mailList, folderName)

def inbox_view(request):
    global i, addr, passwrd, conn
    if request.method == 'POST':
        imap_url = 'imap.gmail.com'
        conn = imaplib.IMAP4_SSL(imap_url)
        conn.login(addr, 'vuzaialuwrljbxit')
        conn.select('"INBOX"')
        result, data = conn.search(None, '(UNSEEN)')
        unreadList = data[0].split()
        num = len(unreadList)
        result1, data1 = conn.search(None, "ALL")
        mailList = data1[0].split()
        texttospeech("You have reached your inbox. There are " + str(len(mailList)) + " total mails in your inbox. You have " + str(num) + " unread emails" + ". To read unread emails say unread. To search an email say search. To go back to the menu page say back.", file + i)
        i = i + str(1)

        flag = True
        while flag:
            act = speechtotext(5)
            act = act.lower()
            print(act)
            if act == "unread":
                flag = False
                if num != 0:
                    read_mail(unreadList, 'inbox')
                else:
                    texttospeech("There are no unread emails", file + i)
                    i = i + str(1)

            elif act == "search":
                flag = False
                emailID = ""
                while True:
                    texttospeech("Enter email address you want to search", file + i)
                    i = i + str(1)
                    emailID = speechtotext(15)
                    texttospeech("You meant " + emailID + " say yes or no to confirm", file + i)
                    i = i + str(1)
                    yes = speechtotext(5)
                    yes = yes.lower()
                    if yes == 'yes':
                        break
                
                emailID = emailID.strip()
                emailID = emailID.replace(' ', '')
                emailID = emailID.lower()
                emailID = convert_special_char(emailID)
                search_mail('INBOX', 'FROM', emailID, 'inbox')
            
            elif act == "back":
                texttospeech("You will now be redirected to the menu page.", file + i)
                i = i + str(1)
                conn.logout()
                return JsonResponse({'result': 'success'})

            else:
                texttospeech("Invalid action. Please try again", file + i)
                i = i + str(1)
            
            texttospeech("Do you want to do anything else in the inbox? Say yes or no.", file + i)
            i = i + str(1)
            ans = speechtotext(3)
            ans = ans.lower()
            if ans == 'yes':
                flag = True
                texttospeech("Enter your choice. Say unread, search, or back. ", file + i)
                i = i + str(1)
        texttospeech("You will now be redirected to the menu page.", file + i)
        i = i + str(1)
        conn.logout()
        return JsonResponse({'result': 'success'})

    elif request.method == 'GET':
        return render(request, 'home/inbox.html')

def sent_view(request):
    global i, addr, passwrd, conn
    if request.method == 'POST':
        imap_url = 'imap.gmail.com'
        conn = imaplib.IMAP4_SSL(imap_url)
        conn.login(addr, 'mfpwszyziwxifpsu')
        conn.select('"[Gmail]/Sent Mail"')
        result1, data1 = conn.search(None, "ALL")
        mailList = data1[0].split()

        texttospeech("You have reached your sent folder. There are " + str(len(mailList)) + " mails in your sent folder. To search an email say search. To go back to the menu page say back.", file + i)
        i = i + str(1)
       
        flag = True
        while flag:
            act = speechtotext(5)
            act = act.lower()
            print(act)
            if act == 'search':
                flag = False
                emailID = ""
                while True:
                    texttospeech("Enter email address you want to search.", file + i)
                    i = i + str(1)
                    emailID = speechtotext(15)
                    texttospeech("You meant " + emailID + " say yes to confirm or no to enter again", file + i)
                    i = i + str(1)
                    yes = speechtotext(5)
                    yes = yes.lower()
                    if yes == 'yes':
                        break
                emailID = emailID.strip()
                emailID = emailID.replace(' ', '')
                emailID = emailID.lower()
                emailID = convert_special_char(emailID)
                search_mail('"[Gmail]/Sent Mail"', 'TO', emailID,'sent')

            elif act == 'back':
                texttospeech("You will now be redirected to the menu page.", file + i)
                i = i + str(1)
                conn.logout()
                return JsonResponse({'result': 'success'})

            else:
                texttospeech("Invalid action. Please try again.", file + i)
                i = i + str(1)

            texttospeech("Do you want to do anything else in the sent page? Say yes or no.", file + i)
            i = i + str(1)
            ans = speechtotext(3)
            ans = ans.lower()
            if ans == 'yes':
                flag = True
                texttospeech("Enter your choice. Say search or back. ", file + i)
                i = i + str(1)
        texttospeech("You will now be redirected to the menu page.", file + i)
        i = i + str(1)
        conn.logout()
        return JsonResponse({'result': 'success'})

    elif request.method == 'GET':
        return render(request, 'home/sent.html')

def trash_view(request):
    global i, addr, passwrd, conn
    if request.method == 'POST':
        imap_url = 'imap.gmail.com'
        conn = imaplib.IMAP4_SSL(imap_url)
        conn.login(addr, 'mfpwszyziwxifpsu')
        conn.select('"[Gmail]/Trash"')
        result1, data1 = conn.search(None, "ALL")
        mailList = data1[0].split()
        
        texttospeech("You have reached your trash folder. There are " + str(len(mailList)) + " mails in your trash folder. To search an email say search. To go back to the menu page say back.", file + i)
        i = i + str(1)
        flag = True
        while flag:
            act = speechtotext(5)
            act = act.lower()
            print(act)
            if act == 'search':
                flag = False
                emailID = ""
                while True:
                    texttospeech("Enter email address you want to search.", file + i)
                    i = i + str(1)
                    emailID = speechtotext(15)
                    texttospeech("You meant " + emailID + " say yes to confirm or no to enter again", file + i)
                    i = i + str(1)
                    yes = speechtotext(5)
                    yes = yes.lower()
                    if yes == 'yes':
                        break
                emailID = emailID.strip()
                emailID = emailID.replace(' ', '')
                emailID = emailID.lower()
                emailID = convert_special_char(emailID)
                search_mail('"[Gmail]/Trash"', 'FROM', emailID, 'trash')

            elif act == 'back':
                texttospeech("You will now be redirected to the menu page.", file + i)
                i = i + str(1)
                conn.logout()
                return JsonResponse({'result': 'success'})

            else:
                texttospeech("Invalid action. Please try again.", file + i)
                i = i + str(1)

            texttospeech("Do you want to do anything else in the trash page? Say yes or no.", file + i)
            i = i + str(1)
            ans = speechtotext(3)
            ans = ans.lower()
            print(ans)
            if ans == 'yes':
                flag = True
                texttospeech("Enter your choice. Say search or back. ", file + i)
                i = i + str(1)
        texttospeech("You will now be redirected to the menu page.", file + i)
        i = i + str(1)
        conn.logout()
        return JsonResponse({'result': 'success'})
    elif request.method == 'GET':
        return render(request, 'home/trash.html')

def compose_type_view(request):
    global i, addr, passwrd, s, item, subject, body

    if request.method == 'POST':
        fromaddr = addr
        toaddr = list()

        item = request.POST.get("receiver")
        subject = request.POST.get("subject")
        body = request.POST.get("body")

        newtoaddr = list()
        newtoaddr.append(item)
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = ",".join(newtoaddr)
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            s.sendmail(fromaddr, newtoaddr, msg.as_string())
            texttospeech("Your email has been sent successfully. You will now be redirected to the menu page.", file + i)
            i = i + str(1)
        except:
            texttospeech("Sorry, your email failed to send. please try again. You will now be redirected to the the compose page again.", file + i)
            i = i + str(1)
            #return JsonResponse({'result': 'failure'})
            return redirect('/compose/')
        s.quit()

        return redirect('/options/')

    compose  = Compose()
    compose.recipient = item
    compose.subject = subject
    compose.body = body
