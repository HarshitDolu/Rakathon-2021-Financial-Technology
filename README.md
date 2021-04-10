# Rakathon-2021-Financial-Technology

### Project Title: Credit Card Fraud Detection and Prevention System.

### Theme: Financial Technology

## Project Description:

### Objective:

E-commerce and many other online sites have increased the online 
payment modes, increasing the risk for online frauds.
The challenge is to recognize fraudulent credit card transactions so 
that the customers of credit card companies are not charged for items 
that they did not purchase.
The main aim for our system will be to analyse the past transaction 
details of the customers and extract the behavioural patterns
depending on which cardholders are clustered into different groups 
based on their transaction information.

### Future scope:

We can make the system completely decentralized using blockchain.
Can add activation and deactivation of Credit card on timely basis.

### Tools

1.Django Web Framework<br>
2.Machine Learning Models<br>
3.OpenCV<br>
4.Face Recognition<br>
5.Cryptography<br>
6.QR Codes<br>
7.Basic Blockchain

### Instructions for project set up

Step 1: Grab a copy of the project. <br>
 git clone https://github.com/HarshitDolu/Rakathon-2021-Financial-Technology.git <br>
Step 2: Create a virtual environment and install dependencies. <br>
      mkvirtualenv creditcard
      venv\Scripts\activate
      pip install -r requirements.txt<br>
      
Step 3: Initialize database.
 cd dbase
 python ./manage.py syncdb
 python ./manage.py migrate
 <br>
Step 4: create a new superuser for the admin.
python ./manage.py createsuperuser<br>

Step 5: Run the development server to verify everything 
is working.
 python manage.py runserver
 
 ### System work flow
 
 1. Register and Login <br>
 2. create your bank account and credit card in the website <br>
 3. Use the same credit card for transaction<br>
 4. First card in the website is having implementation of ML models for Credit card detection. (use the same credit card which you created)<br>
 5. Second card in the website is for credit card fraud prevention using OTP and Face recognition.<br>
 6. Third card is having Qr codes and basic blockchain stuffs for authentication and block creation (having location and timestamp)

## Snapshot

<img src ="https://github.com/HarshitDolu/Rakathon-2021-Financial-Technology/blob/main/demo%20images/Snapshot.png"/><br>



## Demo images
<p align="center">
<img src ="https://github.com/HarshitDolu/Rakathon-2021-Financial-Technology/blob/main/demo%20images/1.png" height="500"/><br>
<img src ="https://github.com/HarshitDolu/Rakathon-2021-Financial-Technology/blob/main/demo%20images/2.png" height="500"/><br>
<img src ="https://github.com/HarshitDolu/Rakathon-2021-Financial-Technology/blob/main/demo%20images/3.png" height="500"/><br>
<img src ="https://github.com/HarshitDolu/Rakathon-2021-Financial-Technology/blob/main/demo%20images/4.png" height="500"/><br>
<img src ="https://github.com/HarshitDolu/Rakathon-2021-Financial-Technology/blob/main/demo%20images/5.png" height="500"/>
                                                                                                                        </p>







