import base64
import datetime
import hashlib
import json
import random
from email import charset
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.core.mail import send_mail,EmailMessage
import string
from django.conf import settings

import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

import pyotp
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import CreateUserForm,AccountDetailsForm, UserAddressForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import *

# Create your views here.

def home(request):
    return render(request,'detection/home.html')

def signup(request):
    if request.user.is_authenticated:
        return render(request,'detection/card.html')
    else:

        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():

                user=form.save()
                username = form.cleaned_data.get('username')
                email=form.cleaned_data.get('email')
                password=form.cleaned_data.get('password1')
                print(username)

                #new_user = User.objects.create(username=username, email=email, password=password)
                new_user = form.save(commit=False)



                messages.success(request, 'Account was created for ' + username)
                return redirect('signin')

        context = {'form': form}

    return render(request, 'detection/register.html', context)

def signin(request):
    if request.user.is_authenticated:
        return render(request, 'detection/card.html')
    else:
        if request.method == 'POST':
         # get post parameters
            username=request.POST['username']
            password=request.POST['password']
            print(username)
            user=authenticate(username=username,password=password)

            if user is not None:
                login(request,user)
                messages.success(request, 'Account is logged in as ' + username)
                return render(request,'detection/card.html')
            else:
           #message
                messages.info(request, 'username or password is incorrect')
        return render(request,'detection/login.html')


# login required
def bank_account(request):
    if request.user.is_authenticated:
        account_form = AccountDetailsForm(
            request.POST or None,
            request.FILES or None
        )
        address_form = UserAddressForm(
            request.POST or None
        )

        if account_form.is_valid() and address_form.is_valid():

            account_details = account_form.save(commit=False)
            address = address_form.save(commit=False)

            account_details.user = request.user
            account_details.account_no=int("%0.12d" % random.randint(10000000,999999999999))
            account_details.save()
            address.user = request.user
            address.save()
            messages.success(request, 'Bank account created ')

            return redirect('signin')





        context = {
            "title": "Create a Bank Account",

            "account_form": account_form,
            "address_form": address_form,
        }

        return render(request, "detection/bank.html", context)
    else:
        return redirect('home')

def luhn(first_6):

    card_no = [int(i) for i in str(first_6)]  # To find the checksum digit on
    card_num = [int(i) for i in str(first_6)]  # Actual account number
    seventh_15 = random.sample(range(9), 9)  # Acc no (9 digits)
    for i in seventh_15:
        card_no.append(i)
        card_num.append(i)
    for t in range(0, 15, 2):  # odd position digits
        card_no[t] = card_no[t] * 2
    for i in range(len(card_no)):
        if card_no[i] > 9:  # deduct 9 from numbers greater than 9
            card_no[i] -= 9
    s = sum(card_no)
    mod = s % 10
    check_sum = 0 if mod == 0 else (10 - mod)
    card_num.append(check_sum)
    card_num = [str(i) for i in card_num]
    return ''.join(card_num)



def credit_card_generator(request):
    if request.user.is_authenticated:
        acc=AccountDetails.account_no

        print(request.user.username)


        qs=AccountDetails.objects.filter(user_id=request.user.id)
        username=request.user.username
        qs=list(qs)

        print(qs[0])
        acc_no=qs[0]
        st=str(qs[0])
        first_6=st[:6]
        first_6=int(first_6)
        number_16=luhn(first_6)   #used luhn algo
        print(number_16)

        cc_code=("%0.3d" % random.randint(300,999))
        cc_expiry= datetime.date(2030, 11, 5)

        ask = Payment(acc=acc_no,cc_number=number_16,cc_expiry=cc_expiry,cc_code=cc_code)

        ask.save()
        messages.success(request, 'Username: ' + username+ '  credit card no:  '+ str(number_16)+'   cvv:   '+str(cc_code))
        return redirect('signin')

import math
def generateOTP():
    # Declare a digits variable
    # which stores all digits
    digits = "0123456789"
    OTP = ""

    # length of password can be chaged
    # by changing value in range
    for i in range(4):
        OTP += digits[math.floor(random.random() * 10)]

    return OTP

import time
def getOtp():

    totp = pyotp.TOTP('base32secret3232')
    otp = totp.now()
    return otp

def card_details(request):
    if request.user.is_authenticated:
        true_name=request.user.username
        qs = AccountDetails.objects.filter(user_id=request.user.id)
        qs = list(qs)
        acc_no = qs[0]

        qp=Payment.objects.filter(acc=acc_no)
        qpp=list(qp)
        true_cno=qp.values()[0]['cc_number']
        true_ccv=qp.values()[0]['cc_code']
        true_name = request.user.username
        print(true_cno)
        print(true_ccv)





        if request.method == 'POST' and 'sent' in request.POST:
            name = request.POST['name']
            cvv = request.POST['cvv']
            cno = request.POST['cno']


            print(name)
            print(true_name)
            print(type(cno))
            print(type(true_cno))
            print(type(cvv))
            print(type(true_ccv))

            if(len(str(cno))==16 and len(str(cvv))==3 and len(name)!=0):
                if(name==true_name and cvv == true_ccv and cno==true_cno):



                    return redirect('otp_validation')

            else:
                print("Incorrect details")
    return render(request,"detection/card_details.html")
otp=getOtp()
def otp_validation(request):
    if request.user.is_authenticated:
        qs = AccountDetails.objects.filter(user_id=request.user.id)   # picture
        totp = pyotp.TOTP('base32secret3232')

        print(request.user.email)
        #print(qs.values()[0]['picture'])

        s=request.user.email
        email=request.user.email
        s=s[0:3]
        context={'email':s}

        print(otp,"original")
        send_mail('Core_Dumped', "Your OTP for transactions is"+ f'{otp}'
                  , settings.EMAIL_HOST_USER,
                 [email], fail_silently=False
                )




        if request.method == 'POST' and 'sent_otp' in request.POST:

            user_totp = request.POST['totp']
            print(user_totp)
            if user_totp == otp:
                print("You can access")
                return redirect('biometric_validation')
            else:
                print("Fraud")



        return render(request, "detection/otp.html",context)

def findEncodings(image):
    encodeList=[]
    for img in image:
        img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

import socket
def biometric_validation(request):
    if request.user.is_authenticated:
        email = request.user.email
        path = 'media'
        qs = AccountDetails.objects.filter(user_id=request.user.id)  # picture
        uimg= qs.values()[0]['picture']

        imgUser = face_recognition.load_image_file(f'{path}/{uimg}')
        imgUser=cv2.resize(imgUser,(512,512))
        imgUser = cv2.cvtColor(imgUser, cv2.COLOR_BGR2RGB)

        faceLoc = face_recognition.face_locations(imgUser)[0]
        encodeElon = face_recognition.face_encodings(imgUser)[0]

        cv2.rectangle(imgUser, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (255, 0, 255), 2)




        print("Encoding complete")
        if not os.path.exists('data'):
            os.makedirs('data')
        cap = cv2.VideoCapture(0)
        i=0
        cf=0
        img_list=[]
        while i<4:
            success, img = cap.read()

            #imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            if success:
                nam = "data/"+f'{request.user.username}'+ str(cf) + '.jpg'
                print('creating..' + nam)
                cv2.imwrite(nam,img)
                img_list.append(nam)
                cf+=1
            i=i+1
        print(img_list[0])
        cap.release()
        cv2.destroyAllWindows()
        imm=cv2.imread(f'{img_list[0]}')
        #cv2.imshow("image",imm)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        if len(img_list)!=0:
            imgTest = cv2.cvtColor(imm, cv2.COLOR_BGR2RGB)


            faceLocTest = face_recognition.face_locations(imgTest)[0]

            encodeTest = face_recognition.face_encodings(imgTest)[0]
            cv2.rectangle(imm, (faceLocTest[3], faceLocTest[0]), (faceLocTest[1], faceLocTest[2]), (255, 0, 255), 2)

            results = face_recognition.compare_faces([encodeElon], encodeTest)
            faceDis = face_recognition.face_distance([encodeElon], encodeTest)
            print(results, faceDis)


            cv2.putText(imm, f'{results} {round(faceDis[0], 2)}', (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)


            nam1 = "detection/static/img/" + f'{request.user.username}' +"cap" + '.jpg'
            cv2.imwrite(nam1, imm)

            nam2 = "detection/static/img/" + f'{request.user.username}' + "reg" + '.jpg'
            cv2.imwrite(nam2, imgUser)





        with open(nam1, "rb") as image_file:
            image_data1 = base64.b64encode(image_file.read()).decode('utf-8')

        with open(nam2, "rb") as image_file:
            image_data2 = base64.b64encode(image_file.read()).decode('utf-8')

        ## getting the hostname by socket.gethostname() method
        hostname = socket.gethostname()
        ## getting the IP address using socket.gethostbyname() method
        ip_address = socket.gethostbyname(hostname)
        ## printing the hostname and ip_address
        print(f"Hostname: {hostname}")
        print(f"IP Address: {ip_address}")


        if results[0]:
            context={'image_cap':image_data1,'image_reg':image_data2,'info':"Face Recognised !! Your real time image and registered image got matched, Now you are ready to perform transaction",'greet':"Congratulations"}
        else:
            now= datetime.datetime.now()
            dt_string= now.strftime("%d/%m/%Y %H:%M:%S")
            msg = EmailMessage(
                'Biometric validation',
                'Recently an unknown person is trying to access your credit card for transaction. Timestamp: '+f'{dt_string}'+ "  "+f"Hostname: {hostname}"+"  "+f"IP Address: {ip_address}",
                'cipherx2510@gmail.com',
                [email],


                headers={'Message-ID': 'foo'},
            )
            msg.content_subtype = "html"



            with open(nam1, "rb") as image_file:
                mime_image = MIMEImage(image_file.read())
                mime_image.add_header('Content-ID', '<image_file>')
                msg.attach(mime_image)

            msg.send()





            context = {'image_cap': image_data1, 'image_reg': image_data2,
                       'info': "Face not Recognised !! Your real time image and registered image not Matched, Image of unknown will be send to Account holder for verification",'greet':"Sorry"}
        return render(request, 'detection/face.html', context)

















        return render(request,'detection/face.html',context)



########################################################### Machine Learning part ###########################################

import pandas as pd
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
import joblib

def ml_card_transaction(request):
    if request.user.is_authenticated:
        true_name=request.user.username
        qs = AccountDetails.objects.filter(user_id=request.user.id)
        qs = list(qs)
        acc_no = qs[0]

        qp=Payment.objects.filter(acc=acc_no)
        qpp=list(qp)
        true_cno=qp.values()[0]['cc_number']
        true_ccv=qp.values()[0]['cc_code']
        true_name = request.user.username
        print(true_cno)
        print(true_ccv)





        if request.method == 'POST' and 'sent_ml' in request.POST:
            name = request.POST['name']
            cvv = request.POST['cvv']
            cno = request.POST['cno']


            print(name)
            print(true_name)
            print(type(cno))
            print(type(true_cno))
            print(type(cvv))
            print(type(true_ccv))
            filename1='detection/ml_models/LogReg_saved.pk1'                        # Logistic regression model
            filename2='detection/ml_models/RForest_saved.pk1'                       #  Random Forest model
            filename3='detection/ml_models/DTree_saved.pk1'
            filename4= 'detection/ml_models/naivebayes_saved.pk1'
            filename5= 'detection/ml_models/IForest_saved.pk1'


            if(len(str(cno))==16 and len(str(cvv))==3 and len(name)!=0):
                if(name==true_name and cvv == true_ccv and cno==true_cno):
                    loaded_model_log = joblib.load(filename1)
                    loaded_model_rf = joblib.load(filename2)
                    loaded_model_dt = joblib.load(filename3)
                    loaded_model_nb = joblib.load(filename4)
                    loaded_model_if = joblib.load(filename5)

                    test=pd.read_csv('detection/ml_models/valid.csv') # taking user transaction details
                    test.drop(['Unnamed: 0'],axis=1,inplace=True)
                    print(test.head())
                    prediction_log=loaded_model_log.predict(test)
                    prediction_rf = loaded_model_rf.predict(test)
                    prediction_dt = loaded_model_dt.predict(test)
                    prediction_nb = loaded_model_nb.predict(test)
                    prediction_if = loaded_model_if.predict(test)


                    result_log=list(prediction_log)[0]
                    result_rf = list(prediction_rf)[0]

                    result_dt = list(prediction_dt)[0]
                    result_nb = list(prediction_nb)[0]
                    result_if = list(prediction_if)[0]

                    count_zero=0
                    count_one=0

                    if result_log == 0:
                        result_log=90
                        count_zero=count_zero+1
                    else:
                        count_one=count_one+1
                    if result_rf == 0:
                        result_rf=90
                        count_zero=count_zero+1
                    else:
                        count_one=count_one+1
                    if result_dt == 0:
                        result_dt=90
                        count_zero = count_zero + 1
                    else:
                        count_one=count_one+1
                    if result_nb == 0:
                        result_nb=90
                        count_zero = count_zero + 1
                    else:
                        count_one=count_one+1
                    if result_if == 0:
                        result_if=90
                        count_zero = count_zero + 1
                    else:
                        count_one=count_one+1

                    majority='Fraud not detected'
                    if count_one > count_zero:
                        majority="Fraud detected"


                    #print(type(result))
                    #print(result[0])

                    context={'result_log':result_log,'result_rf':result_rf,'accuracy_log':97.3,'accuracy_rf':99.98,'accuracy_dt':99.83,'result_dt':result_dt,
                             'result_nb':result_nb,'result_if':result_if,'acc_if':48.3,'acc_nb':84.9,
                             'count_z':count_zero,'count_o':count_one,'majority':majority
                             }



                    return render(request,'detection/card_issuing_bank.html',context)

            else:
                print("Incorrect details")

    return render(request,"detection/ml_card.html")

######################################################  QR code cryptography ##################################################
import qrcode

####################################### Basic blockchain ############################

import hashlib
import json
import datetime
from urllib.parse import urlparse
from uuid import uuid4


class BlockChain:

    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof=1, previous_hash='0',location='xyz')
        self.nodes = set()

    def create_block(self, proof, previous_hash,location):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash,
            'location':location,
            'transactions': self.transactions
        }
        self.transactions = []
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False

        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof = new_proof + 1

        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index = block_index + 1

            return True


# Add transactions

    def add_transactions(self, sender, reciever, amount,location):
        self.transactions.append({
            'sender': sender,
            'reciever': reciever,
            'amount': amount,
            'location':location
        })
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1

import datetime
import requests

blockchain = BlockChain()
url = "https://ip-geo-location.p.rapidapi.com/ip/check"

querystring = {"format":"json"}

headers = {
    'x-rapidapi-key': "b91dbffe60msh23244f2e8f264d4p1909adjsn5ee08d0d2669",
    'x-rapidapi-host': "ip-geo-location.p.rapidapi.com"
    }


response={}
def qr_activate(request):

    if request.user.is_authenticated:


        #img = qrcode.make(st + f'{"Agartala"}')                           # fraud user
        #img.save("QR2" + f'{request.user.username}' + ".jpg")

        st = "612113138972Agartala"




        d = cv2.QRCodeDetector()
        cap=cv2.VideoCapture(0)
        k=0
        while True:
            success, img = cap.read()
            val,points,straight_qrcode=d.detectAndDecode(img)
            if len(val)!=0:
                messages.success(request,
                                 "Hello user, Your QR code has been scanned, Now go to your email and click the link for further proceedings..")
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            cv2.imshow("QR CODE SCANNER",img)


        cap.release()
        cv2.destroyAllWindows()
        location=val[12:]



        now = datetime.datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        email=request.user.email
        respons = requests.request("GET", url, headers=headers, params=querystring)

        res = json.loads(respons.text)

        area = res['area']
        code = area['code']
        ip = res['ip']
        postcode = res['postcode']
        state = area['name']
        city = res['city']
        loc = city['name']
        gid = city['geonameid']


        send_mail('Core_Dumped_QR validation','http://127.0.0.1:8000/transaction_permission  Recently an unknown person is trying to access your credit card for transaction.'+"   Location: " +"IP address: "+f'{ip}'+"  postcode: "+f'{postcode}'+"  location: "+f'{loc}'+"  state: "+f'{state}'+"  geoid: "+f'{gid}'
                  , settings.EMAIL_HOST_USER,
                  [email], fail_silently=False
                  )

        print(email)

         # store time stamp and location
        json1 = {
            'sender': f"{request.user.username}",
            'reciever': "XYZ",
            'amount': 5000,
            'location': loc,
        }

        transaction_keys = ['sender', 'reciever', 'amount', 'location']
        if not all(key in json1 for key in transaction_keys):
            print("Some elements are missing")
        index = blockchain.add_transactions(json1['sender'], json1['reciever'], json1['amount'], json1['location'])
        #resp = {'message': f'your location will be added to block {index}'}
        resp=f'your location will be added to block {index}'
        node_address = str(uuid4()).replace('-', '')
        previous_block = blockchain.get_previous_block()
        previous_proof = previous_block['proof']

        proof = blockchain.proof_of_work(previous_proof)
        blockchain.add_transactions(sender=node_address, reciever='XYZ', amount=5000,location=loc)
        previous_hash = blockchain.hash(previous_block)
        block = blockchain.create_block(proof, previous_hash,loc)
        response = {
            'index': block['index'],
            'timestamp': block['timestamp'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash'],
            'transactions': block['transactions'],
             'location':block['location']  }

        print(response)

        qs = AccountDetails.objects.filter(user_id=request.user.id)
        qs = list(qs)
        acc_no = qs[0]
        qp = Payment.objects.filter(acc=acc_no)
        qpp = list(qp)
        true_cno = qp.values()[0]['cc_number']
        true_ccv = qp.values()[0]['cc_code']
        true_expiry = qp.values()[0]['cc_expiry']
        true_name = request.user.username
        mod_cvv = str(true_ccv)[0:1] + "XX"
        mod_cno = str(true_cno)[0:6] + "XXXXXXXXXX"

        nam1 = "detection/static/img/" + "QR1" + f'{request.user.username}' + '.jpg'
        with open(nam1, "rb") as image_file:
            image_data1 = base64.b64encode(image_file.read()).decode('utf-8')

        context = {'cno': mod_cno, 'cvv': mod_cvv, 'true_ex': true_expiry, 'uname': true_name, 'QR': image_data1,'resp':resp}

        return render(request, 'detection/qr_form_scanner.html', context)



def yes(request):

    respons = requests.request("GET", url, headers=headers, params=querystring)

    res = json.loads(respons.text)

    area = res['area']
    code = area['code']
    ip = res['ip']
    postcode = res['postcode']
    state = area['name']
    city = res['city']
    loc = city['name']
    gid = city['geonameid']
    json1 = {
        'sender': f"{request.user.username}",
        'reciever': "XYZ",
        'amount': 5000,
        'location': loc,
    }

    transaction_keys = ['sender', 'reciever', 'amount', 'location']
    if not all(key in json1 for key in transaction_keys):
        print("Some elements are missing")
    index = blockchain.add_transactions(json1['sender'], json1['reciever'], json1['amount'], json1['location'])
    # resp = {'message': f'your location will be added to block {index}'}
    resp = f'your location will be added to block {index}'
    node_address = str(uuid4()).replace('-', '')
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']

    proof = blockchain.proof_of_work(previous_proof)
    blockchain.add_transactions(sender=node_address, reciever='XYZ', amount=5000, location=loc)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash, loc)
    response = {
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
        'transactions': block['transactions'],
        'location': block['location']}


    context={"response":response}


    return render(request,"detection/yes.html",context)






import qrcode

def qr_transaction(request):
    if request.user.is_authenticated:

        st = "%0.12d" % random.randint(10000000, 999999999999)
        img = qrcode.make(st + f'{"kolkata"}')  # actual user
        img.save("QR1" + f'{request.user.username}' + ".jpg")

        path="QR1"+f'{request.user.username}' + '.jpg'
        im=cv2.imread(path)

        nam1 = "detection/static/img/" + "QR1" + f'{request.user.username}' + '.jpg'
        cv2.imwrite(nam1,im)

        qs = AccountDetails.objects.filter(user_id=request.user.id)
        qs = list(qs)
        acc_no = qs[0]
        qp = Payment.objects.filter(acc=acc_no)
        qpp = list(qp)
        true_cno = qp.values()[0]['cc_number']
        true_ccv = qp.values()[0]['cc_code']
        true_expiry=qp.values()[0]['cc_expiry']
        true_name = request.user.username
        mod_cvv=str(true_ccv)[0:1]+"XX"
        mod_cno=str(true_cno)[0:6]+"XXXXXXXXXX"
        print(true_cno)
        print(true_ccv)
        nam1 = "detection/static/img/"+"QR1"+f'{request.user.username}' + '.jpg'
        with open(nam1, "rb") as image_file:
            image_data1 = base64.b64encode(image_file.read()).decode('utf-8')

        resp = "Click on Scan QR code button"
        context={'cno':mod_cno,'cvv':mod_cvv,'true_ex':true_expiry,'uname':true_name,'QR':image_data1,'resp':resp}

        return render(request,'detection/qr_form_scanner.html',context)

def yesno(request):

    return render(request,'detection/yesno.html')

def no(request):
    return render(request,'detection/no.html')


def handle_logout(request):
    logout(request)
    return redirect('home')