import textwrap
from flask import session,Flask, render_template, request, redirect, url_for, session, flash,jsonify, make_response,Response,send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import pandas as pd
from pymongo import MongoClient
from datetime import timedelta
from datetime import datetime
import calendar
import logging
from uuid import uuid4
from threading import Timer

import string
import zipfile
import io
import re
import json
import numpy as np
import bcrypt
import os
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bson import ObjectId
import uuid 
from datetime import datetime, timedelta
from collections.abc import Iterable
import random
from tabulate import tabulate
from itertools import product
from flask import send_file
import tempfile
import csv    
from random import sample   
import time
import threading  
import shutil
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, Spacer, PageBreak,TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
import urllib
import schedule
import base64
from PIL import Image
from flask_cors import CORS, cross_origin
from functools import wraps
from flask_simple_captcha import CAPTCHA

# configure email sending
smtp_server = "smtp.gmail.com"
smtp_port = 587  # Typically 587 for TLS
sender_email = "sruthi.k@pinacalabs.com"
sender_password = "mjnpmuzudfpjuybc"


app = Flask(__name__)
cors = CORS(app)


secret_key = secrets.token_hex(16)
app.secret_key = secret_key

app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = 1800 
app.config['SESSION_COOKIE_NAME'] = 'session'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_PATH'] = '/'
app.config['SESSION_COOKIE_DOMAIN'] = None


YOUR_CONFIG = {
    'SECRET_CAPTCHA_KEY': secret_key,
    'CAPTCHA_LENGTH': 6,
    'CAPTCHA_DIGITS': False,
    'EXPIRE_SECONDS': 600,
}
SIMPLE_CAPTCHA = CAPTCHA(config=YOUR_CONFIG)
app = SIMPLE_CAPTCHA.init_app(app)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.permanent_session_lifetime = timedelta(minutes=30)


# MongoDB Configuration
client = MongoClient('mongodb://127.0.0.1:27017/')
db = client['zen_eye']
credit_card_db1 = client["credit_card_monitoring_5_1"]
users_collection = db['userdetails']
offline_collection= db['offline_details']
CASE_collection = db['CASE_Created']
CLOSE_CASE_collection = db['CLOSE_CASE_Created']
Finnet_collection = db['FINnet_Report']
TM_collection = db['TM']
TY_collection = db['TY']
RM_collection = db['RM']
sdn_collection =db['SDN_Details']
SDN_customers_collection = db['SDN_customers_name']
TELE_MON = db['tele_mon']
TELE_MON_1 = db['Tele_MON_1']
FIU =db['FIU']
LEA =db['LEA']
txn_collection=db['Account_Transactions_Details']
db_5_1 = client["credit_card_monitoring_5_1"]
db_5_2 = client["credit_card_monitoring_5_2"]
db_5_3 = client["credit_card_monitoring_5_3"]
db_5_6 = client["credit_card_monitoring_5_6"]
db_5_7 = client["credit_card_monitoring_5_7"]
TENLAKS = db['TenLaks']
active_sessions = {}
# ================== Dummy cloude database & collections for sdn ==================

cloud_cluster = MongoClient("mongodb+srv://Bhuvana:"+ urllib.parse.quote("Bhuv@cluster") + "@cluster0.nhqdnbn.mongodb.net/")
cloud_db = cloud_cluster['Bank_Details']
cloud_collection = cloud_db['SDN_Cloud']
local_col = db['Customer_Details']

# ================== kamal database & collections ==================

kamaldb = client['kamal']
Absconding_Criminals = kamaldb['Absconding_Criminals']
Adverse_Media = kamaldb['Adverse_Media']
Associated_Entity = kamaldb['Associated_Entity']
BSE_Defaulters_Expelled = kamaldb['BSE_Defaulters_Expelled']
BSE_Delist_Companies = kamaldb['BSE_Delist_Companies']
BSE_Suspended_Companies = kamaldb['BSE_Suspended_Companies']
Blacklisted_Doctors = kamaldb['Blacklisted_Doctors']
Blacklisted_NGOs = kamaldb['Blacklisted_NGOs']
CBI = kamaldb['CBI']
CIBIL = kamaldb['CIBIL']
CVC = kamaldb['CVC']
EOCN_UAE = kamaldb['EOCN_UAE']
EU_Sanction_List = kamaldb['EU_Sanction_List']
Enforcement = kamaldb['Enforcement']
FATF = kamaldb['FATF'] 
FCRA_Cancelled = kamaldb['FCRA_Cancelled']
FIU_Defaulter_List = kamaldb['FIU_Defaulter_List']
IRDA = kamaldb['IRDA']
Interpol = kamaldb['Interpol']
MCA_Defaulter_Company = kamaldb['MCA_Defaulter_Company']
MCA_Defaulter_Director = kamaldb['MCA_Defaulter_Director']
MCA_Disqualified_Directors = kamaldb['MCA_Disqualified_Directors']
MCA_Dormant_Directors = kamaldb['MCA_Dormant_Directors']
MCA_MLM_Company = kamaldb['MCA_MLM_Company']
MCA_Proclaimed_Offenders = kamaldb['MCA_Proclaimed_Offenders']
MCX_Defaulters = kamaldb['MCX_Defaulters']
MHA_UAPA = kamaldb['MHA_UAPA']
NBFC = kamaldb['NBFC']
NCDEX_Cessation_Members = kamaldb['NCDEX_Cessation_Members']
NCDEX_Defaulter_Members = kamaldb['NCDEX_Defaulter_Members']
NCDEX_Expelled_Members = kamaldb['NCDEX_Expelled_Members']
NIA_Arrested_Person = kamaldb['NIA_Arrested_Person']
NIA_Most_Wanted = kamaldb['NIA_Most_Wanted']
OFAC = kamaldb['OFAC']
OFAC_SDN_Criminal_Individuals_List = kamaldb['OFAC_SDN_Criminal_Individuals_List']
OFSI_UK_Sanction_list = kamaldb['OFSI_UK_Sanction_list']
PEP = kamaldb['PEP']
Registrations = kamaldb['Registrations']
SFIO_Conviction = kamaldb['SFIO_Conviction']
SFIO_Proclaimed = kamaldb['SFIO_Proclaimed']
SFIO_Prosecution = kamaldb['SFIO_Prosecution']
SOE = kamaldb['SOE']
Sanction_List = kamaldb['Sanction_List']
UN_Sanction_List = kamaldb['UN_Sanction_List']
World_Bank = kamaldb['World_Bank']
demo = kamaldb['demo']



@app.after_request
def add_security_headers(response):
    csp_directives = {
        'default-src': "'self' data:",
        'script-src': "'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdn.datatables.net https://ajax.googleapis.com https://cdnjs.cloudflare.com https://gyrocode.github.io https://maxcdn.bootstrapcdn.com https://unpkg.com https://d3js.org",
        'style-src': "'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com https://maxcdn.bootstrapcdn.com https://cdn.datatables.net https://gyrocode.github.io https://stackpath.bootstrapcdn.com",
        'font-src': "'self' https://fonts.gstatic.com https://stackpath.bootstrapcdn.com https://cdn.jsdelivr.net",
        'img-src': "'self' data: https://cdn.datatables.net",
        'frame-ancestors': "'none'"
    }
    csp_header = "; ".join([f"{directive} {csp_directives[directive]}" for directive in csp_directives])
    response.headers['Content-Security-Policy'] = csp_header
    return response

# @app.after_request
# def add_security_headers(response):
#     response.headers['Content-Security-Policy'] = "default-src 'self' data:; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdn.datatables.net https://ajax.googleapis.com https://cdnjs.cloudflare.com http://gyrocode.github.io https://maxcdn.bootstrapcdn.com https://d3js.org; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com https://maxcdn.bootstrapcdn.com https://cdn.datatables.net http://gyrocode.github.io https://stackpath.bootstrapcdn.com; font-src 'self' https://fonts.gstatic.com https://stackpath.bootstrapcdn.com; img-src 'self' data: https://cdn.datatables.net;"
#     response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
#     return response


# ================================================= Socket IO Usage =====================================================================

def notification(mails):
     userinfo = users_collection.find_one({'emailid':mails})
    # =========== Taking the array's of the tickets which are storing the cases ========================== 
     
     if "allocated_tickets" in userinfo:
        pendingAlertsNotfy = len(userinfo['allocated_tickets'])
     else:
         pendingAlertsNotfy = 0
     
     if "Sent_Back_Case_Alerts" in userinfo:
        unsuffeccientAlerst = len(userinfo['Sent_Back_Case_Alerts'])
     else:
         unsuffeccientAlerst = 0
     
     if "rised_closed_tickets" in userinfo:
        rised_closed_tickets = len(userinfo['rised_closed_tickets'])
     else:
         rised_closed_tickets = 0
     
     if "Sent_Back_Alerts" in userinfo:
        Sent_Back_Alerts = len(userinfo['Sent_Back_Alerts'])
     else:
         Sent_Back_Alerts = 0
     
     if "Offline_assigned_tickets" in userinfo:
        offlineCases = len(userinfo['Offline_assigned_tickets'])
     else:
         offlineCases = 0

# ============================
     if userinfo['role'] == 'CM/SM':
        users_collection.update_one({'emailid':mails},{"$set":{'pendingAlertsNotfy':pendingAlertsNotfy,'unsufecientAlertsNotfy':unsuffeccientAlerst,"risedClosedCount":rised_closed_tickets}})
     elif userinfo['role'] == 'MLRO':
        users_collection.update_one({'emailid':mails},{"$set":{'pendingAlertsNotfy':pendingAlertsNotfy,'unsufecientAlertsNotfy':unsuffeccientAlerst,"sentBackClosedCount":Sent_Back_Alerts}})  
     else:
        users_collection.update_one({'emailid':mails},{"$set":{'pendingAlertsNotfy':pendingAlertsNotfy,'unsufecientAlertsNotfy':unsuffeccientAlerst,"offlineCasesCount":offlineCases}})
    
    # ============================
     if "pendingAlertsNotfy" in userinfo:
        prvPendingAlertsNotfy = userinfo['pendingAlertsNotfy']
     else:
        prvPendingAlertsNotfy = 0  

     if "unsufecientAlertsNotfy" in userinfo:
        prvunsufecientAlertsNotfy = userinfo['unsufecientAlertsNotfy']
     else:
         prvunsufecientAlertsNotfy = 0
     
     if "risedClosedCount" in userinfo:
        prvrisedClosedCount = userinfo['risedClosedCount']
     else:
         prvrisedClosedCount = 0
     
     if "sentBackClosedCount" in userinfo:
        prvsentClosedCount = userinfo['sentBackClosedCount']
     else:
         prvsentClosedCount = 0
     
     if "offlineCasesCount" in userinfo:
        prvofflineCount = userinfo['offlineCasesCount']
     else:
         prvofflineCount = 0

# ===================================================
         
     mainInfo = users_collection.find_one({'emailid':mails})

     presentpen = mainInfo['pendingAlertsNotfy']
     if "prvPendingAlertsNotfy" in mainInfo:
        prevpen = mainInfo['prvPendingAlertsNotfy']
     else:
         prevpen = 0
         users_collection.update_one({'emailid':mails},{"$set":{'prvPendingAlertsNotfy':prevpen}})

     presentuns = mainInfo['unsufecientAlertsNotfy']
     if "prvunsufecientAlertsNotfy" in mainInfo:
        prvuns = mainInfo['prvunsufecientAlertsNotfy']
     else:
         prvuns = 0
         users_collection.update_one({'emailid':mails},{"$set":{'prvunsufecientAlertsNotfy':prvuns}})
    
     if "risedClosedCount" in mainInfo:
        presentclosed = mainInfo['risedClosedCount']
        if "prvrisedClosedCount" in mainInfo:
            prvclosed = mainInfo['prvrisedClosedCount']
        else:
            prvclosed = 0
            users_collection.update_one({'emailid':mails},{"$set":{'prvrisedClosedCount':prvclosed}})
     
     if "sentBackClosedCount" in mainInfo:
        presentsentclosed = mainInfo['sentBackClosedCount']
        if "prvsentClosedCount" in mainInfo:
            prvsentclosed = mainInfo['prvsentClosedCount']
        else:
            prvsentclosed = 0
            users_collection.update_one({'emailid':mails},{"$set":{'prvsentClosedCount':prvsentclosed}})
     
     if "offlineCasesCount" in mainInfo:
        presentofflineclosed = mainInfo['offlineCasesCount']
        if "prvofflineCount" in mainInfo:
            prvofflineclosed = mainInfo['prvofflineCount']
        else:
            prvofflineclosed = 0
            users_collection.update_one({'emailid':mails},{"$set":{'prvofflineCount':prvofflineclosed}})

    #  ================================
     print("prevpen : ",prevpen)
     print("presentpen : ",presentpen)
     
     if prevpen > presentpen:
         users_collection.update_one({'emailid':mails},{"$set":{'prvPendingAlertsNotfy':prvPendingAlertsNotfy}})
     if prvuns > presentuns:
         users_collection.update_one({'emailid':mails},{"$set":{'prvunsufecientAlertsNotfy':prvunsufecientAlertsNotfy}})
     
     if userinfo['role'] == 'AGM' or userinfo['role'] == 'DGM/PO' or userinfo['role'] == 'ROS':
        if prvofflineclosed > presentofflineclosed:
            users_collection.update_one({'emailid':mails},{"$set":{'prvofflineCount':prvofflineCount}})
     if userinfo['role'] == 'CM/SM':
        if prvclosed > presentclosed:
            users_collection.update_one({'emailid':mails},{"$set":{'prvrisedClosedCount':prvrisedClosedCount}})
     if userinfo['role'] == 'MLRO':
        if prvsentclosed > presentsentclosed:
            users_collection.update_one({'emailid':mails},{"$set":{'prvsentClosedCount':prvsentClosedCount}})
     
     
# ===================================================


     main = users_collection.find_one({'emailid':mails})
     
     if "pendingAlertsNotfy" in main and "prvPendingAlertsNotfy" in main:
        presentPendingAlertsNotfy  = main['pendingAlertsNotfy']
        prvPendingAlertsNotfy  = main['prvPendingAlertsNotfy']
     else:
        presentPendingAlertsNotfy  = 0
        prvPendingAlertsNotfy  = 0

     print("presentPendingAlertsNotfy : ",presentPendingAlertsNotfy)
     print("prvPendingAlertsNotfy : ",prvPendingAlertsNotfy)

     if "unsufecientAlertsNotfy" in main and "prvunsufecientAlertsNotfy" in main:
        presentunsufecientAlertsNotfy  = main['unsufecientAlertsNotfy']
        prvunsufecientAlertsNotfy  = main['prvunsufecientAlertsNotfy']
     else:
        presentunsufecientAlertsNotfy  = 0
        prvunsufecientAlertsNotfy  = 0
     
     if "risedClosedCount" in main and "prvrisedClosedCount" in main:
        presentclosedNotfy  = main['risedClosedCount']
        prvclosedNotfy  = main['prvrisedClosedCount']
     else:
        presentclosedNotfy  = 0
        prvclosedNotfy  = 0
     
     if "sentBackClosedCount" in main and "prvsentClosedCount" in main:
        presentsentclosedNotfy  = main['sentBackClosedCount']
        prvsentclosedNotfy  = main['prvsentClosedCount']
     else:
        presentsentclosedNotfy  = 0
        prvsentclosedNotfy  = 0
     
     if "offlineCasesCount" in main and "prvofflineCount" in main:
        presentofflineNotfy  = main['offlineCasesCount']
        prvofflineNotfy  = main['prvofflineCount']
     else:
        presentofflineNotfy  = 0
        prvofflineNotfy  = 0


# ===================================================
        
     if presentPendingAlertsNotfy and (presentPendingAlertsNotfy > prvPendingAlertsNotfy):
         pendingcount = presentPendingAlertsNotfy - prvPendingAlertsNotfy
     else:
         pendingcount = 0
     print("pendingcount : ",pendingcount)    
    
     if presentunsufecientAlertsNotfy and (presentunsufecientAlertsNotfy > prvunsufecientAlertsNotfy):
         unsuffeccientcount = presentunsufecientAlertsNotfy - prvunsufecientAlertsNotfy
     else:
         unsuffeccientcount = 0
     
     if presentclosedNotfy and (presentclosedNotfy > prvclosedNotfy):
         verifyClosedcount = presentclosedNotfy - prvclosedNotfy
     else:
         verifyClosedcount = 0
    
     if presentsentclosedNotfy and (presentsentclosedNotfy > prvsentclosedNotfy):
         sentClosedcount = presentsentclosedNotfy - prvsentclosedNotfy
     else:
         sentClosedcount = 0
     
     if presentofflineNotfy and (presentofflineNotfy > prvofflineNotfy):
         risedofflinecount = presentofflineNotfy - prvofflineNotfy
     else:
         risedofflinecount = 0

         
# ===============================================================================

# ============================ DashBoard Per Day Logic ===========================================

     current_datetime = datetime.now()
     # Extract only the date and set the time to midnight
     current_date = str(current_datetime.date())
    #  current_date = '2024-01-23'
     print('current_date : ',current_date)

    #  if pendingcount != 0:

    #                 perDay = users_collection.find_one({"emailid":mails,"pendingAlerts_perDay":{"$exists":True}})

    #                 if perDay:
    #                     print("holaa.................")
    #                     dateExists = users_collection.find_one({"emailid": mails, f'pendingAlerts_perDay.{current_date}': {"$exists": True}})
    #                     if dateExists:
    #                         users_collection.update_one(
    #                                 {"emailid": mails, f'pendingAlerts_perDay.{current_date}': {"$exists": True}},
    #                                 {"$inc": {f'pendingAlerts_perDay.$.{current_date}': pendingcount}}
    #                             )
    #                     else:
    #                         users_collection.update_one({"emailid":mails},{"$push":{"pendingAlerts_perDay":{current_date:pendingcount}}})

    #                 else:
    #                     users_collection.update_one({"emailid":mails},{"$set":{"pendingAlerts_perDay":[{current_date:pendingcount}]}})

   

# ================================================================================================

     return {"pendingcount":pendingcount,"unsuffeccientcount":unsuffeccientcount,"verifyClosedcount":verifyClosedcount,'sentBackClosed':sentClosedcount,"offlineCases":risedofflinecount}

# ===============Clearing the notification function ===========================

def clearnotification(mails,endpoint):
     userinfo = users_collection.find_one({'emailid':mails})

# ====================================
  

     
     if "allocated_tickets" in userinfo:
        pendingAlertsNotfy = len(userinfo['allocated_tickets'])
     else:
         pendingAlertsNotfy = 0
     
     if "Sent_Back_Case_Alerts" in userinfo:
        unsuffeccientAlerst = len(userinfo['Sent_Back_Case_Alerts'])
     else:
         unsuffeccientAlerst = 0
     
     if "rised_closed_tickets" in userinfo:
        rised_closed_tickets = len(userinfo['rised_closed_tickets'])
     else:
         rised_closed_tickets = 0
     
     if "Sent_Back_Alerts" in userinfo:
        Sent_Back_Alerts = len(userinfo['Sent_Back_Alerts'])
     else:
         Sent_Back_Alerts = 0
     
     if "Offline_assigned_tickets" in userinfo:
        offlineCases = len(userinfo['Offline_assigned_tickets'])
     else:
         offlineCases = 0
    
# =====================================================
         
     if endpoint == 'nextLevel':
        users_collection.update_one({'emailid':mails},{"$set":{'pendingAlertsNotfy':pendingAlertsNotfy}})
     if endpoint == 'sentBack':
        users_collection.update_one({'emailid':mails},{"$set":{'unsufecientAlertsNotfy':unsuffeccientAlerst}})
     if endpoint == 'closedVerify':
        users_collection.update_one({'emailid':mails},{"$set":{'risedClosedCount':rised_closed_tickets}})
     if endpoint == 'sentBackClosed':
        users_collection.update_one({'emailid':mails},{"$set":{'sentBackClosedCount':Sent_Back_Alerts}})
     if endpoint == 'offline':
        users_collection.update_one({'emailid':mails},{"$set":{'offlineCasesCount':offlineCases}})
     

    # ==========================================================
        
    
     if "pendingAlertsNotfy" in userinfo:
        prvPendingAlertsNotfy = userinfo['pendingAlertsNotfy']
     else:
        prvPendingAlertsNotfy = 0  

     if "unsufecientAlertsNotfy" in userinfo:
        prvunsufecientAlertsNotfy = userinfo['unsufecientAlertsNotfy']
     else:
         prvunsufecientAlertsNotfy = 0
     
     if "risedClosedCount" in userinfo:
        prvclosedNotfy = userinfo['risedClosedCount']
     else:
         prvclosedNotfy = 0
     
     if "sentBackClosedCount" in userinfo:
        prvsentclosedNotfy = userinfo['sentBackClosedCount']
     else:
         prvsentclosedNotfy = 0
     
     if "offlineCasesCount" in userinfo:
        prvofflineNotfy = userinfo['offlineCasesCount']
     else:
         prvofflineNotfy = 0

# ==============================================
         
     if endpoint == 'nextLevel':
        users_collection.update_one({'emailid':mails},{"$set":{'prvPendingAlertsNotfy':prvPendingAlertsNotfy}})
    
     if endpoint == 'sentBack':
        users_collection.update_one({'emailid':mails},{"$set":{'prvunsufecientAlertsNotfy':prvunsufecientAlertsNotfy}})
    
     if endpoint == 'closedVerify':
        users_collection.update_one({'emailid':mails},{"$set":{'prvrisedClosedCount':prvclosedNotfy}})
    
     if endpoint == 'sentBackClosed':
        users_collection.update_one({'emailid':mails},{"$set":{'prvsentClosedCount':prvsentclosedNotfy}})
    
     if endpoint == 'offline':
        users_collection.update_one({'emailid':mails},{"$set":{'prvofflineCount':prvofflineNotfy}})
    
     
         
# ====================================================================



     main = users_collection.find_one({'emailid':mails})
     
     if "pendingAlertsNotfy" in main and "prvPendingAlertsNotfy" in main:
        presentPendingAlertsNotfy  = main['pendingAlertsNotfy']
        prvPendingAlertsNotfy  = main['prvPendingAlertsNotfy']
     else:
        presentPendingAlertsNotfy  = 0
        prvPendingAlertsNotfy  = 0

     if "unsufecientAlertsNotfy" in main and "prvunsufecientAlertsNotfy" in main:
        presentunsufecientAlertsNotfy  = main['unsufecientAlertsNotfy']
        prvunsufecientAlertsNotfy  = main['prvunsufecientAlertsNotfy']
     else:
        presentunsufecientAlertsNotfy  = 0
        prvunsufecientAlertsNotfy  = 0

     if "risedClosedCount" in main and "prvrisedClosedCount" in main:
        presentclosedNotfy  = main['risedClosedCount']
        prvclosedNotfy  = main['prvrisedClosedCount']
     else:
        presentclosedNotfy  = 0
        prvclosedNotfy  = 0
     
     if "sentBackClosedCount" in main and "prvsentClosedCount" in main:
        presentsentclosedNotfy  = main['sentBackClosedCount']
        prvsentclosedNotfy  = main['prvsentClosedCount']
     else:
        presentsentclosedNotfy  = 0
        prvsentclosedNotfy  = 0
    
     if "offlineCasesCount" in main and "prvofflineCount" in main:
        presentofflineNotfy  = main['offlineCasesCount']
        prvofflineNotfy  = main['prvofflineCount']
     else:
        presentofflineNotfy  = 0
        prvofflineNotfy  = 0

# =====================================================
     
     if presentPendingAlertsNotfy and (presentPendingAlertsNotfy > prvPendingAlertsNotfy):
         pendingcount = presentPendingAlertsNotfy - prvPendingAlertsNotfy
     else:
         pendingcount = 0
    
     if presentunsufecientAlertsNotfy and (presentunsufecientAlertsNotfy > prvunsufecientAlertsNotfy):
         unsuffeccientcount = presentunsufecientAlertsNotfy - prvunsufecientAlertsNotfy
     else:
         unsuffeccientcount = 0

     if presentclosedNotfy and (presentclosedNotfy > prvclosedNotfy):
         verifyClosedcount = presentclosedNotfy - prvclosedNotfy
     else:
         verifyClosedcount = 0
     
     if presentsentclosedNotfy and (presentsentclosedNotfy > prvsentclosedNotfy):
         sentClosedcount = presentsentclosedNotfy - prvsentclosedNotfy
     else:
         sentClosedcount = 0
     
     if presentofflineNotfy and (presentofflineNotfy > prvofflineNotfy):
         risedofflinecount = presentofflineNotfy - prvofflineNotfy
     else:
         risedofflinecount = 0


    # ============================

     return {"pendingcount":pendingcount,"unsuffeccientcount":unsuffeccientcount,"verifyClosedcount":verifyClosedcount,'sentBackClosed':sentClosedcount,"offlineCases":risedofflinecount}


# ============================ END OF THE NOTIFICATION FUNTION'S BOTH GETTING AND CLEARING===============================================






# ======== File Uploding starts =======
# file_path = "Book2_5_7.xlsx"

# # Read Excel data
# df = pd.read_excel(file_path)

# # Connect to MongoDB and create a new database
# database = client["credit_card_monitoring_5_7"]

# # Iterate through unique 'Card Number' values
# for card_number in df['Card Number'].unique():
#     # Create a collection name based on the 'Card Number'
#     collection_name = str(card_number)
    
#     # Filter data for the current 'Card Number'
#     filtered_data = df[df['Card Number'] == card_number]
    
#     # Prepare data for insertion
#     data_list = filtered_data.to_dict(orient="records")
    
#     # Create a new collection and insert data
#     collection = database[collection_name]
#     collection.insert_many(data_list)

# # Close the MongoDB connection and print a completion message
# # database.close()
# print("Data inserted into collections based on Card Number.")

# ======== File Uploding ends =======

CORS(app)

current_directory = os.getcwd()
# for bcrypted passwords
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

# For to send the email
def send_password_reset_email(to_email, reset_link,scenario):
    subject = "Password Reset Request From ZenEye "
    if scenario == 'userRevived':
       message = f"{to_email} was enabled ,if you want, you can reset your password \n Click the following link to reset your password: {reset_link}"
    else:
        message = f"User Mail Id: {to_email}\n\n"
    
    message += f"Click the following link to reset your password\n\n{reset_link}\n\n"
    message += "Note: This link will expires in 30 minutes."

    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print("Error sending email:", str(e))


def generate_unique_id():
    return str(uuid.uuid4())

last_execution_time = None
def add_fields_to_records(records,code):
    current_datetime = datetime.now()
    # Extract only the date and set the time to midnight
    current_date = current_datetime.date()
    midnight_datetime = datetime.combine(current_date, datetime.min.time())
    for i, record in enumerate(records):
        # record['ticket_id'] = str(uuid.uuid4())  # Assign a unique UUID
        record['ticket_id'] = f"ARM-VRV-{str(i + 1)}-{current_date}-{str(uuid.uuid4())}"  # Assign a unique ticket ID
        record['scenario_code'] = code
       
        record['status'] = {
            'mlro_officer': None,
            'cm_officer': None,
            'agm_officer': None,
            'dgm_officer': None
        }
        record['levels'] = {
            'mlro_level': None,
            'cm_level': None,
            'agm_level': None,
            'dgm_level': None
        }
        record['allocate_to'] = None
        record['alert_created_on'] = midnight_datetime
        record['alert_allocated_on'] = None
        record['updated_on'] = None
      

def run_tm_functions(user_role):
    global last_execution_time
    desired_execution_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    if datetime.now() >= desired_execution_time and (last_execution_time is None or (datetime.now() - last_execution_time) >= timedelta(days=1)):
        print(f"Running run_tm_functions for role: {user_role}")
        if user_role in ['DGM/PO', 'IT Officer']:
            total_df_1, total_df_non_1, tm_sub_heading_1 = TM_1_1()
            total_df_2, total_df_non_2, tm_sub_heading_2 = TM_1_2()
            # total_df_3, total_df_non_3, tm_sub_heading_3 = TM_1_3()

            

            # Assign unique IDs and other fields to objects in the arrays using UUID
            total_df_1_records = total_df_1.to_dict(orient='records')
            total_df_2_records = total_df_2.to_dict(orient='records')
            # total_df_3_records = total_df_3.to_dict(orient='records')
            total_df_non_1_records = total_df_non_1.to_dict(orient='records')
            total_df_non_2_records = total_df_non_2.to_dict(orient='records')
            # total_df_non_3_records = total_df_non_3.to_dict(orient='records')

            add_fields_to_records(total_df_1_records)
            add_fields_to_records(total_df_2_records)
            add_fields_to_records(total_df_non_1_records)
            add_fields_to_records(total_df_non_2_records)
            # add_fields_to_records(total_df_non_3_records)
            # add_fields_to_records(total_df_3_records)

            # Assuming you have a MongoDB collection called 'output_data'
            TM_collection.insert_many([
                {
                    'code': tm_sub_heading_1,
                    'output_data1': total_df_1_records,
                    'output_data2': total_df_non_1_records
                },
                {
                    'code': tm_sub_heading_2,
                    'output_data1': total_df_2_records,
                    'output_data2': total_df_non_2_records
                }
                # {
                #     'code': tm_sub_heading_3,
                #     'output_data1': total_df_3_records,
                #     'output_data2': total_df_non_2_records
                # }
            ])
            print("Data stored in 'TM_collection")

        if user_role in ['DGM/PO', 'IT Officer']:
            tm_sub_hedding_ty_1_1, total_df_ty_1_1, filtered_df_total_ty_1_1, count_df_gt_1_ty_1_1 = TY_1_1()

            # Assign unique IDs and other fields to objects in the TY data array using UUID
            total_df_ty_1_1_records = total_df_ty_1_1.to_dict(orient='records')
            filtered_df_total_ty_1_1_records = filtered_df_total_ty_1_1.to_dict(orient='records')
            count_df_gt_1_ty_1_1_records = count_df_gt_1_ty_1_1.to_dict(orient='records')

            add_fields_to_records(total_df_ty_1_1_records)
            add_fields_to_records(filtered_df_total_ty_1_1_records)
            add_fields_to_records(count_df_gt_1_ty_1_1_records)

            # Store TY data in 'TY_collection'
            TY_collection.insert_one({
                'code': tm_sub_hedding_ty_1_1,
                'output_data1': total_df_ty_1_1_records,
                'output_data2': filtered_df_total_ty_1_1_records,
                'output_data3': count_df_gt_1_ty_1_1_records
            })
            print("TY data stored in 'TY_collection'")

        if user_role in ['DGM/PO', 'IT Officer']:
                total_df_1, rm_sub_heading_1 = RM_1_1()
                total_df_2, rm_sub_heading_2 = RM_1_3()

                # Assign unique IDs and other fields to objects in the arrays using UUID
                total_df_1_records = total_df_1.to_dict(orient='records')
                total_df_2_records = total_df_2.to_dict(orient='records')
               

                add_fields_to_records(total_df_1_records)
                add_fields_to_records(total_df_2_records)
               

                # Assuming you have a MongoDB collection called 'output_data'
                RM_collection.insert_many([
                    {
                        'code': rm_sub_heading_1,
                        'output_data1': total_df_1_records,
                        
                    },
                    {
                        'code': rm_sub_heading_2,
                        'output_data1': total_df_1_records,
                        
                    }
                ])
                print("Data stored in 'RM_collection")

        last_execution_time = datetime.now()

returning_data_enabled = False

def run_tm_functions(user_role):
    
    global returning_data_enabled
    current_datetime = datetime.now()
    current_date = current_datetime.date()
    midnight_datetime = datetime.combine(current_date, datetime.min.time())
    if (user_role=='IT Officer' or user_role=="DGM/PO") and users_collection.find_one({"role":user_role,"alerts_generated":midnight_datetime}):
        print("Alerts already generated")
    elif user_role=='IT Officer' or user_role=="DGM/PO":
        returning_data_enabled = True
        functions_to_run = [
            {'function': TM_1_1, 'collection': TM_collection, 'output_names': ['output_data1', 'output_data2']},
            {'function': TM_1_2, 'collection': TM_collection, 'output_names': ['output_data1', 'output_data2']},
            {'function': TM_1_3, 'collection': TM_collection, 'output_names': ['output_data1', 'output_data2']},
            {'function': TM_1_4, 'collection': TM_collection, 'output_names': ['output_data1', 'output_data2']},
            {'function': TM_2_1, 'collection': TM_collection, 'output_names': ['output_data1', 'output_data2']},
            {'function': TM_2_2, 'collection': TM_collection, 'output_names': ['output_data1', 'output_data2']},
            {'function': TM_2_3, 'collection': TM_collection, 'output_names': ['output_data1', 'output_data2']},
            {'function': TM_2_4, 'collection': TM_collection, 'output_names': ['output_data1', 'output_data2']},
            {'function': TM_2_5, 'collection': TM_collection, 'output_names': ['output_data1']},
            {'function': TM_2_6, 'collection': TM_collection, 'output_names': ['output_data1']},
            # {'function': TM_3_1, 'collection': TM_collection, 'output_names': ['output_data1']},  # ===== taking more time to run =====
            {'function': TM_3_2, 'collection': TM_collection, 'output_names': ['output_data1']},
            {'function': TM_3_3, 'collection': TM_collection, 'output_names': ['output_data1']},
            {'function': TM_3_4, 'collection': TM_collection, 'output_names': ['output_data1']},
            {'function': TM_3_5, 'collection': TM_collection, 'output_names': ['output_data1']},
            {'function': TM_3_6, 'collection': TM_collection, 'output_names': ['output_data1']},
            {'function': TM_4_1, 'collection': TM_collection, 'output_names': ['output_data1']},
            {'function': TM_4_2, 'collection': TM_collection, 'output_names': ['output_data1']},
            {'function': TM_6_1, 'collection': TM_collection, 'output_names': ['output_data1','output_data2']},
            {'function': TM_6_2, 'collection': TM_collection, 'output_names': ['output_data1']},
            {'function': TM_8_1, 'collection': TM_collection, 'output_names': ['output_data1']},
            {'function': TM_8_2, 'collection': TM_collection, 'output_names': ['output_data1']},
            # {'function': TM_8_3, 'collection': TM_collection, 'output_names': ['output_data1']},#  ===== taking more time to run =====
            {'function': TM_9_1, 'collection': TM_collection, 'output_names': ['output_data1']},
            {'function': TM_9_2, 'collection': TM_collection, 'output_names': ['output_data1']},
            {'function': TY_1_1, 'collection': TY_collection, 'output_names': ['output_data1']},
            {'function': TY_1_2, 'collection': TY_collection, 'output_names': ['output_data1']},
            {'function': TY_1_3, 'collection': TY_collection, 'output_names': ['output_data1']},
            {'function': TY_1_4, 'collection': TY_collection, 'output_names': ['output_data1']},
            {'function': TY_1_5, 'collection': TY_collection, 'output_names': ['output_data1']},
            # {'function': TY_2_2, 'collection': TY_collection, 'output_names': ['output_data1']},
            {'function': TY_3_1, 'collection': TY_collection, 'output_names': ['output_data1']},
            # {'function': TY_3_2, 'collection': TY_collection, 'output_names': ['output_data1']},
            {'function': TY_3_3, 'collection': TY_collection, 'output_names': ['output_data1']},
            {'function': TY_3_5, 'collection': TY_collection, 'output_names': ['output_data1']},
            {'function': TY_6_1, 'collection': TY_collection, 'output_names': ['output_data1']},
            {'function': TY_6_3, 'collection': TY_collection, 'output_names': ['output_data1']},
            # {'function': TY_10_2, 'collection': TY_collection, 'output_names': ['output_data1']},  #  ===== taking more time to run =====
            # {'function': TY_10_4, 'collection': TY_collection, 'output_names': ['output_data1', 'output_data2']}, # ===== taking more time to run =====
            {'function': TY_11_1, 'collection': TY_collection, 'output_names': ['output_data1']},
            # {'function': TY_7_2, 'collection': TY_collection, 'output_names': ['output_data1']},
            {'function': TY_8_2, 'collection': TY_collection, 'output_names': ['output_data1']},
            # {'function': TY_5_1, 'collection': TY_collection, 'output_names': ['output_data1']},
            {'function':TY_5_3,'collection':TY_collection,'output_names':['output_data1']},
            {'function':TY_5_6,'collection':TY_collection,'output_names':['output_data1']},
            {'function':TY_5_7,'collection':TY_collection,'output_names':['output_data1']},
            {'function': RM_1_1, 'collection': RM_collection, 'output_names': ['output_data1']},
            {'function': RM_1_3, 'collection': RM_collection, 'output_names': ['output_data1']},
            {'function': RM_1_4, 'collection': RM_collection, 'output_names': ['output_data1']},
            {'function': RM_2_1, 'collection': RM_collection, 'output_names': ['output_data1']},
            {'function': RM_2_2, 'collection': RM_collection, 'output_names': ['output_data1']},
            {'function': RM_2_3, 'collection': RM_collection, 'output_names': ['output_data1']},
            {'function': RM_3_1, 'collection': RM_collection, 'output_names': ['output_data1']},
            {'function': RM_3_2, 'collection': RM_collection, 'output_names': ['output_data1']}
        ]
        for function_info in functions_to_run:
            function = function_info['function']
            collection = function_info['collection']
            output_names = function_info['output_names']
            # Execute 
            # the function
            outputs = function()
            # Create a dictionary to hold all the output data
            # data_dict['alerts_created']=datetime.now()
            if outputs is not None:
                existing_document = collection.find_one({"code": function.__name__})
                for output_name, output_data in zip(output_names, outputs):
                    if isinstance(output_data, np.float64):
                        # Handle NumPy float64 differently
                        records = [{'data': output_data.item()}]
                    elif isinstance(output_data, pd.Index):
                        # Convert the Index object to a list or extract relevant information

                        records = [{'data': index_value} for index_value in output_data.tolist()]
                    elif isinstance(output_data, str):
                        # Handle string data appropriately (e.g., convert it to a dictionary if needed)

                        records = [{'data': output_data}]
                    else:
                        # Assume it's a DataFrame or similar, convert it to records
                        print("polkjhbqwesdfgh..................................")

                        records = output_data.to_dict(orient='records')
                        # Add extra fields to records
                    # add_fields_to_records(records)
                    add_fields_to_records(records, function.__name__)
                    if existing_document:
                        alerts_updated_date = existing_document.get("alerts_updated")
                        alerts_created = existing_document.get("alerts_created")
                        if alerts_updated_date!=None and alerts_updated_date.date() == current_datetime.date():
                            print("Skipping Update")
                        elif alerts_updated_date!=None and alerts_created!=None and alerts_updated_date.date() != current_datetime.date():
                            print(function.__name__)
                            print("Updating")
                            collection.update_one({'code': function.__name__}, {'$set': {
                                "alerts_updated":midnight_datetime}}, upsert=True)
                            for record in records:
                                collection.update_one({'code':function.__name__},{"$push": {f"{output_name}": record}})
                            print("Updated")
                        elif alerts_created==None and alerts_updated_date==None:
                            print("Inserting alert data into the code document")
                            collection.update_one({'code': function.__name__}, {'$set':{'alerts_created':midnight_datetime,'alerts_updated':midnight_datetime}}, upsert=True)
                            for record in records:
                                collection.update_one({'code':function.__name__},{"$push": {f"{output_name}": record}})
                            print(f"Data stored in '{collection.name}' for function: {function.__name__}")
        # =================== Ten Laks Collection Quire ===================
        startDate = '2021-06-25'
        formatedDate = datetime.strptime(startDate,"%Y-%m-%d")
        thresholdAmount = 1000000
        pipeline = [
                {
                    '$unwind':'$TXNDATA'
                },
                {
                    '$match':{
                        'TXNDATA.Transaction Type':'Cash',
                        'TXNDATA.Transaction Date':formatedDate,
                        'TXNDATA.Transaction Amount':{'$gte':thresholdAmount},
                    }
                },
                {
                    '$group':{
                        '_id':'nonee',
                        'uploaded Date' : {'$first':midnight_datetime} ,
                        "output_data1":{'$push':'$TXNDATA'}
                    }
                }
            ]
            # ,
            #     {
            #         '$out':'TenLaks'
            #     }
        tenlaksCollection = list(txn_collection.aggregate(pipeline))
        TENLAKS.insert_one({
            'uploaded Date': tenlaksCollection[0]['uploaded Date'],
            'output_data1': tenlaksCollection[0]['output_data1']
        })
        # ================ Ten Laks Quire End ==========================
                    
        users = ['IT Officer','DGM/PO']
        for user in users:
            users_collection.update_one({"role":user},{"$set":{
                "alerts_generated":midnight_datetime
            }})
        returning_data_enabled = False
        # for function_info in functions_to_run:
        #     function = function_info['function']
        #     collection = function_info['collection']
        #     output_names = function_info['output_names']
        #     # Execute the function
        #     outputs = function()
        #     for output_name, output_data in zip(output_names, outputs):
        #         if isinstance(output_data, np.float64):
        #     # Handle NumPy float64 differently
        #             records = [{'data': output_data.item()}]
        #         elif isinstance(output_data, pd.Index):
        #     # Convert the Index object to a list or extract relevant information
        #             records = [{'data': index_value} for index_value in output_data.tolist()]
        #         elif isinstance(output_data, str):
        #             # Handle string data appropriately (e.g., convert it to a dictionary if needed)
        #             records = [{'data': output_data}]
        #         else:
        #             # Assume it's a DataFrame or similar, convert it to records
        #             records = output_data.to_dict(orient='records')
        #         # Add extra fields to records
        #         add_fields_to_records(records)
        #         # Insert records into the collection
        #         collection.insert_one({'code': function.__name__, output_name: records})
        #         print(f"Data stored in '{collection.name}' for function: {function.__name__} and output: {output_name}")
        # last_execution_time = datetime.now()


# def RMCode():
#         collections = [RM_collection]
#         # Query the first MongoDB collection
#         for collection in collections:
#             for document in collection.find():
#                 for array_name in ["output_data1", "output_data2", "output_data3"]:
#                     if array_name in document:
#                         for obj in document[array_name]:
#                             if 'Transaction Currency' in obj and 'scenario_code' in obj:
#                                 print("Transaction Currency : ",obj['Transaction Currency'],"  ","scenario_code : ",obj['scenario_code'])

# RMCode()


def secure_route(required_role=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print("Middleware executing...")
            if 'email_id' not in session:
                

                session['pls_login'] = 'Unauthorized access to this page.'
                flash('Access denied. Please sign in.', 'error')
                return redirect(url_for('sign_in'))  # Redirect to the same page
            if isinstance(required_role, list):
                if required_role and 'user_role' in session and session['user_role'] not in required_role:
                            session['pls_login'] = 'Unauthorized access to this page.'
                            flash('Access denied. You do not have the required role.', 'error')
                            return redirect(url_for('sign_in'))  # Redirect to the same page
            else:
                if required_role and 'user_role' in session and session['user_role'] != required_role:
                    session['pls_login'] = 'Unauthorized access to this page.'
                    flash('Access denied. You do not have the required role.', 'error')
                    return redirect(url_for('sign_in'))  # Redirect to the same page
            return func(*args, **kwargs)
        return wrapper
    return decorator
def apply_secure_route_to_all_routes():
    for rule in app.url_map.iter_rules():
        endpoint = rule.endpoint
        if endpoint != 'static':
            view_func = app.view_functions[endpoint]
            app.view_functions[endpoint] = secure_route()(view_func)
# Apply secure_route dynamically to all routes
apply_secure_route_to_all_routes()



@app.route('/ItFileUploder',methods=['GET','POST'])
@secure_route(required_role=['IT Officer'])
def ItFileUploder():
    role = session['user_role']
    print("role ; ",role)
    
    uploadedFile = request.files['alertsFile']
    print("uploaded file : ",uploadedFile)


    if role == 'IT Officer' :
        df = pd.read_excel(uploadedFile.read())
        print("df_data : ",df.head())

        listDf = df.to_dict(orient='records')


        current_datetime = datetime.now()
        current_date = current_datetime.date()
        midnight_datetime = datetime.combine(current_date, datetime.min.time())
        

        for doc in listDf:
            for key,values in doc.items():
                if pd.isna(values):
                    doc[key] = 'Nill'
                if isinstance(values, float):
                    doc[key] = None
                if isinstance(doc.get('Account Number'), int):
                     doc['Account Number'] = str(doc['Account Number'])
                if isinstance(doc.get('Transaction Amount'), int):
                     doc['Transaction Amount'] = int(doc['Transaction Amount'])

            accNum = doc.get('Account Number')
            if accNum:
                accNum = str(accNum)

                allAccountDetails = txn_collection.find_one({'Account Number': accNum})

                if allAccountDetails:
                    txn_collection.update_one(
                        {'Account Number': accNum},
                        {'$push': {'XLData': doc}}
                    )
                else:
                    txn_collection.insert_one(
                        {'Account Number': accNum,'XLData': [doc]}
                    )   
        print("Data stored successfully....")
        # ================== only file is uploaded but the due to some reasons the Quires was not runed =============================
        users_collection.update_one({'role':role},{"$set":{"file":True}})
        # ===========================================================================================================================  
        run_tm_functions(role)
        if role == 'IT Officer':
            return redirect(url_for("ITdashboard"))

@app.route('/', methods=['GET', 'POST'])
def sign_in():
    msg = None
    if 'msgg' in session:
        msg = session.pop("msgg", None)
    if "success_reg_msg" in session:
        msg = session.pop("success_reg_msg", None)
    if "Invalid_password" in session:
        msg = session.pop("Invalid_password", None)
    if "no_user_found" in session:
        msg = session.pop("no_user_found", None)
    if "pls_login" in session:
        msg = session.pop("pls_login", None)
    if "login_required_success" in session:
        msg = session.pop("login_required_success", None)
    if "File_Not_Uploaded" in session:
        msg = session.pop("File_Not_Uploaded", None)
    if "incorrect_captcha" in session:
        msg = session.pop("incorrect_captcha", None)
    new_captcha_dict = SIMPLE_CAPTCHA.create()
    return render_template('sign_in.html', msg=msg, captcha=new_captcha_dict)



#clumsy
# @app.route('/', methods=['GET', 'POST'])
# def sign_in():
#     msg = None
#     if 'msgg' in session:
#         msg = session.pop("msgg", None)
#         print(f"Message for user: {msg}")
#     if "success_reg_msg" in session:
#         msg = session.pop("success_reg_msg", None)
#     if "Invalid_password" in session:
#         msg = session.pop("Invalid_password", None)
#     if "no_user_found" in session:
#         msg = session.pop("no_user_found", None)
#     if "pls_login" in session:
#         msg = session.pop("pls_login", None)
#     if "login_required_success" in session:
#         msg = session.pop("login_required_success", None)
#     if "File_Not_Uploaded" in session:
#         msg = session.pop("File_Not_Uploaded", None)
#     if "incorrect_captcha" in session:
#         msg = session.pop("incorrect_captcha", None)
#     new_captcha_dict = SIMPLE_CAPTCHA.create()
#     return render_template('sign_in.html', msg=msg, captcha=new_captcha_dict)




    
@app.route('/refresh_captcha')
def refresh_captcha():
    new_captcha_dict = SIMPLE_CAPTCHA.create()
    return {"captcha_html":new_captcha_dict}        


import secrets

# def generate_session_token():
#     """
#     Generate a secure random session token.
#     """
#     # Generate a 32-byte random token
#     token_bytes = secrets.token_bytes(32)
#     # Convert the random bytes to a hexadecimal string
#     token_hex = token_bytes.hex()
#     return token_hex




# def generate_session_token():
#     return str(uuid4())
@app.before_request
def ensure_email_id():
    # Ensure email_id is set for logout operations
    if 'msgg' in session and 'email_id' not in session:
        session['email_id'] = session.pop('temp_email_id', None)
        





@app.route("/post_login", methods=["POST", "GET"])
def post_login():
    print("Accessed post_login endpoint")
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        c_hash = request.form.get('captcha-hash')
        c_text = request.form.get('captcha-text')

        if SIMPLE_CAPTCHA.verify(c_text, c_hash):
            user = users_collection.find_one({'emailid': email})
            # user = next((user for user in users_collection if user['emailid'] == email), None)
            current_datetime = datetime.now()
            current_date = current_datetime.date()
            midnight_datetime = datetime.combine(current_date, datetime.min.time())

            if user:
                if bcrypt.checkpw(password.encode("utf-8"), user["password"]):
                    print("Password check passed")
                    user_role = user.get("role")
                    # active_session = users_collection.find_one({"emailid": email, "session_token": {"$ne": None}})
                    # active_session = any(u['session_token'] and u['emailid'] != email for u in users_collection)
                    # if active_session:
                    #     print('Active session detected.')
                    #     session["msgg"] = "This user is already logged in another session via another browser or device. Please logout the active session and try again later."
                    #     session["email_id"] = email
                    #     session['just_logged_in'] = False
                    #     print("just_logged_in active sessions:", session.get('just_logged_in')) 
                    #     return redirect(url_for("sign_in"))

                    # session['just_logged_in'] = True
                    # print("just_logged_in:", session.get('just_logged_in')) 

                    if user.get("status") == "Approved":
                        
                        # session_token = str(uuid4())
                        # session["session_token"] = session_token
                        session["email_id"] = email
                        session["user_role"] = user.get("role")
                        # users_collection.update_one({'emailid': email}, {"$set": {"session_token": session_token}})
                        
                        if user_role == "IT Officer":
                            userLogin = users_collection.find_one({'role':"IT Officer","alerts_generated":{"$exists":True},"alerts_generated":midnight_datetime,"file":True})
                            if userLogin:
                                run_tm_functions(user_role)
                                return redirect(url_for("ITdashboard"))
                            else:
                                users_collection.update_one({'role':user_role},{"$set":{"file":False}})
                                new_captcha_dict = SIMPLE_CAPTCHA.create()
                                return render_template('sign_in.html',active=True,captcha=new_captcha_dict)
                            
                            
                        elif user_role == "AGM":
                            # session["email_id"]=str(user["emailid"])
                            return redirect(url_for("AGMdashboard"))
                        elif user_role == "MLRO":
                            # session["email_id"] = user["emailid"]
                            return redirect(url_for("MLROdashboard"))
                        elif user_role == "CM/SM":
                            return redirect(url_for("CM_SM_dashboard"))
                        elif user_role == "DGM/PO":

                            userLogin = users_collection.find_one({'role':"IT Officer","alerts_generated":midnight_datetime,"file":True})
                            if userLogin:
                                run_tm_functions(user_role)
                                return redirect(url_for("DGMdashboard"))
                            else:
                                session["File_Not_Uploaded"] = "File Not Uploaded Yet By IT Officer"
                                return redirect(url_for("sign_in"))

                            
                        elif user_role == "BranchMakers":
                            return redirect(url_for("branchmakers"))
                        elif user_role == "ROS":
                            return redirect(url_for("ROSDashboard"))
                        elif user_role == "SDN/USER":
                            return redirect(url_for("SDN_user"))

                    elif user.get("status") == "Rejected":
                        session["pls_login"] = "Your account has been rejected. Please contact support."
                        print("Account rejected for user:", email)
                        return redirect(url_for("sign_in"))

                    elif user.get("status") == "Created":
                        session["pls_login"] = "Your account is not yet approved. Please wait for approval."
                        print("Account not yet approved for user:", email)
                        return redirect(url_for("sign_in"))
                else:
                    session["Invalid_password"] = "Invalid Credentials"
                    print("Invalid credentials for user:", email)
                    return redirect(url_for("sign_in"))
            else:
                session["no_user_found"] = "No user found, please register"
                return redirect(url_for("sign_in"))
        else:
            session["incorrect_captcha"] = "Incorrect Captcha, please enter correct captcha"
            return redirect(url_for("sign_in"))
    else:
        return redirect(url_for("sign_in"))
    











@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
      msg = None 
      if "password_mismatch_msg" in session:
        msg = session.pop("password_mismatch_msg",None)
      if "missing_val_msg" in session:
        msg = session.pop("missing_val_msg",None)
      
      if "ps_error_msg" in session:
        msg = session.pop("ps_error_msg",None)
      if "mobile_error_msg" in session:
        msg = session.pop("mobile_error_msg",None)
      if "email_error_msg" in session:
        msg = session.pop("email_error_msg",None)
      return render_template('sign_up.html',msg=msg)



@app.route('/newUser',methods=['POST','GET'])
@secure_route(required_role=['IT Officer'])
def newUser():
    
    empid_pattern = r'^[a-zA-Z0-9]{1,10}$'
    email_pattern = r'^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$'
    mobileno_pattern= r'^\d{10}$'
    username_pattern = r'^[a-zA-Z0-9]{1,20}$'

    username = request.form['username']
    emailid = request.form['emailid']
    empid = request.form['empid']
    mobileno = request.form['mobileno']
    role = request.form['role']
    address = request.form['address']
    if not re.match(username_pattern, username):
        session['ps_error'] = "Username must contain only letters  and numbers and be up to 20 characters long."
        return redirect(url_for('AllUsers'))
    if not re.match(empid_pattern, empid):
        session['ps_error'] = "EMPid must contain only letters  or numbers and be up to 10 characters long."
        return redirect(url_for('AllUsers'))
    if not re.match(email_pattern, emailid):
        session['ps_error'] = "Enter a valid Emailid "
        return redirect(url_for('AllUsers'))
    if not re.match(mobileno_pattern, mobileno):
        session['ps_error'] = "Mobile Number must be only ten digits long and must be numbers only "
        return redirect(url_for('AllUsers'))


    users_collection.insert_one({
        'name':username,
        'emailid':emailid,
        'mobileno':mobileno,
        'address':address,
        'role':role,
        'empid':empid
    })
    return redirect(url_for('AllUsers'))


@app.route('/multiUsersCreation',methods=['POST','GET'])
@secure_route(required_role=['IT Officer'])
def multiUsersCreation():
    file = request.files['multUsers']

    usersMail = users_collection.find()
    mails = []
    for info in usersMail:
        mails.append(info['emailid'])
    df = pd.read_excel(file.read())

   
    filtered_emails = df[~df['emailid'].isin(mails)]


    for index, row in filtered_emails.iterrows():
        mobilenumber = str(row['mobileno'])
        empi = str(row['empid'])
        users_collection.insert_one({
            'name': row['name'],
            'emailid': row['emailid'], 
            'mobileno': mobilenumber,
            'address': row['address'],
            'role': row['role'],
            'empid':empi
        })
    
    return redirect(url_for('AllUsers'))








@app.route("/AddUser")
@secure_route(required_role='IT Officer')
def AddUser():
    user = users_collection.find_one({'role': 'IT Officer'})

    ituser = {'image': ""}
    if user:
        ituser = users_collection.find_one({'emailid': user.get('emailid')})

        if ituser and 'image' in ituser:
            ituser['image'] = base64.b64encode(ituser['image']).decode('utf-8')

    msg=None
    if 'ps_error' in session:
        msg = session.pop('ps_error',None)
    if 'user_exists' in session:
        msg = session.pop('user_exists',None)
    if msg!=None:
        return render_template("AddUser.html",msg=msg,ituser=ituser,type='AddUser',role='IT Officer')
    else:
        return render_template("AddUser.html",ituser=ituser,type='AddUser',role='IT Officer')

@app.route('/searchUser',methods=['POST'])
@secure_route(required_role=['IT Officer'])
def searchUser():
    userInfo = request.get_json()
    user = userInfo["user"]
    field = userInfo["field"]
    userDetails = users_collection.find_one({field:user},{"_id":0})
    if userDetails and "password" not in userDetails:
        finalDetails ={
            "name":userDetails["name"],
            "emailid":userDetails["emailid"],
            "mobileno":userDetails["mobileno"],
            "role":userDetails["role"],
            "address":userDetails["address"],
            "empid":userDetails["empid"],
        }
        return finalDetails
    elif userDetails and "password" in userDetails:
        return {"none":"exists"}
    else:
        return {"none":"no data"}


@app.route('/enableUser',methods=['POST'])
@secure_route(required_role=['IT Officer'])
def enableUser():
    if request.method == 'POST':
        email = request.form['emailid']

       
        users_collection.update_one({'emailid':email},{"$unset": {'partial_Delete': 1},"$set":{'status':'Approved',"leaveStatus":'On Leave'}},upsert=False)
        user = users_collection.find_one({'emailid':email})
        allocated_to = user['assigned_to']

        users_collection.update_one(
            {'emailid': allocated_to, 'mlros_assigned': {'$in': [email]}},
            {'$push': {'mlros_assigned': email}}
        ) 


        if user:
                    base_url = "http://127.0.0.1:5000/reset_password"
                    reset_token = secrets.token_hex(10)
                    users_collection.update_one({'emailid':email},{"$set":{"reset_password_token":hash_password(reset_token)}})
                    reset_link = f"{base_url}?user_id={email}&token={reset_token}"
                    send_password_reset_email(email,reset_link,'userRevived')
        
        
                   
        
        return redirect(url_for('AllUsers'))



def is_password_valid(password):
    # Define the regex for password validation
    password_pattern = re.compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,16}$')
    return bool(password_pattern.match(password))




@app.route('/submit-form', methods=['POST'])
@secure_route(required_role=['IT Officer'])
def submit_form():
    if request.method=='POST':
        empid_pattern = r'^[a-zA-Z0-9]{1,10}$'
        email_pattern = r'^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$'
        mobileno_pattern= r'^\d{10}$'
        username_pattern = r'^[a-zA-Z0-9]{1,20}$'
        try:
            name = request.form['name']
            # emailid = request.form['emailid']
            # role = request.form['role']
            mobileno = request.form['mobileno']
            # password = request.form['password']
            empid=request.form['empid']
            # re_entered_password = request.form['Re-Enter Password']
            emailid = request.form['emailid']
            role = request.form['role']
        # mobileno = request.form['mobileno']
            password = request.form['password']
            re_entered_password = request.form['Re-Enter Password']
            status = "Created"
            hashed_password = hash_password(password)
        except:
            print('errorrrrrrrrrrrrr')
        status = "Created"
        if not re.match(username_pattern, name):
            session['ps_error'] = "Username must contain only letters and numbers and be up to 20 characters long."
            return redirect(url_for('AddUser'))
        if not re.match(empid_pattern, empid):
            session['ps_error'] = "EMPid must contain only letters or numbers and be up to 10 characters long."
            return redirect(url_for('AddUser'))
        if not re.match(email_pattern, emailid):
            session['ps_error'] = "Enter a valid Emailid "
            return redirect(url_for('AddUser'))
        if not re.match(mobileno_pattern, mobileno):
            session['ps_error'] = "Mobile Number must be only ten digits long and must be numbers only "
            return redirect(url_for('AddUser'))
        if not is_password_valid(password):
            # print('%%%%%%%%%%%%%%%',password)
            session['ps_error'] = 'The password must be between 8 to 16 characters in length and must include at least one number, one uppercase letter, one lowercase letter, and one special character.'
            return redirect(url_for('AddUser'))

        hashed_password = hash_password(password)
        if password != re_entered_password:
            session['ps_error']='Passwords do not match. Please try again.'
            return redirect(url_for('AddUser'))
        # elif users_collection.find_one({'emailid': emailid, 'status': 'Approved'}):
        #     session['user_exists']='Email ID already exists. Please use a different email.'
        #     return redirect(url_for('AddUser'))
        if users_collection.find_one({'emailid': emailid}):
            existing_user = users_collection.find_one({'emailid': emailid})
        if role == 'CM/SM':
            users_collection.update_one(
                {'_id': existing_user['_id']},
                {'$set': {
                    # 'name': name,
                    # 'role': role,
                    # 'mobileno': mobileno,
                    'password': hashed_password,
                    'status': status,
                    'mlros_assigned':[],
                    'assigned_to_agm':''
                }}
            )
            mlros_data = users_collection.find({"role":"MLRO","assigned_to":"","status":{"$in":["Created","Approved"]}})
            for mlro_doc in mlros_data:
                cm_user = users_collection.find_one({"_id":existing_user['_id'],"role":"CM/SM","status":{"$in":["Created"]}})
                cm_user_assigned_docs = cm_user["mlros_assigned"]
                if len(cm_user_assigned_docs)<5:
                    users_collection.update_one({"_id":mlro_doc["_id"],"emailid":mlro_doc["emailid"],"role":"MLRO","status":{"$in":["Created","Approved"]}},{"$set":{"assigned_to":cm_user['emailid']}})
                    users_collection.update_one({"role":"CM/SM","emailid":cm_user['emailid']},{"$push": {"mlros_assigned": mlro_doc["emailid"]}})
            
            agm_data = users_collection.find({"role":"AGM","status":{"$in":["Created","Approved"]}})
            cm_user = users_collection.find_one({"_id":existing_user['_id'],"role":"CM/SM","assigned_to_agm":"","status":"Created"})
            for agm_doc in agm_data:
                agm_user_assigned_docs = agm_doc["cms_assigned"]
                if cm_user is not None and agm_user_assigned_docs is not None and len(agm_user_assigned_docs) < 3 and cm_user['assigned_to_agm'] == '':
                    users_collection.update_one({"_id":existing_user['_id'],"role":"CM/SM"},{"$set":{"assigned_to_agm":agm_doc['emailid']}})
                    users_collection.update_one({"role":"AGM","emailid":agm_doc['emailid']},{"$push": {"cms_assigned": cm_user["emailid"]}})
                    break;
        elif role=='MLRO':
            users_collection.update_one(
                {'_id': existing_user['_id']},
                {'$set':
                    {
                    # 'name': name,
                    # 'emailid': emailid,
                    # 'role': role,
                    # 'mobileno': mobileno,
                    'password': hashed_password,
                    'status': status,
                    'assigned_to':"",
                    'assigned_to_ros':"",
                }}
            )
            cmsm_data = users_collection.find({"role":"CM/SM","status":{"$in":["Created","Approved"]}})
            mlro_user = users_collection.find_one({"_id":existing_user['_id'],"role":"MLRO","assigned_to":"","status":{"$in":["Created"]}})
            for cmsm_doc in cmsm_data:
                cm_user_assigned_docs = cmsm_doc["mlros_assigned"]
                if mlro_user is not None and cm_user_assigned_docs is not None and len(cm_user_assigned_docs) < 5 and mlro_user['assigned_to'] == '':
                    users_collection.update_one({"_id":existing_user['_id'],"role":"MLRO"},{"$set":{"assigned_to":cmsm_doc['emailid']}})
                    users_collection.update_one({"role":"CM/SM","emailid":cmsm_doc['emailid']},{"$push": {"mlros_assigned": mlro_user["emailid"]}})
            
            
        elif role == 'AGM':
            users_collection.update_one(
                {'_id': existing_user['_id']},
                {'$set': {
                    # 'name': name,
                    # 'role': role,
                    # 'mobileno': mobileno,
                    'password': hashed_password,
                    'status': status,
                    'cms_assigned':[],
                    'ros_assigned':[]
                }}
            )
            agm_data = users_collection.find({"role":"AGM","status":{"$in":["Created","Approved"]}})
            for agm_doc in agm_data:
                cm_user = users_collection.find_one({"role":"ROS","assigned_to_agm":"","status":"Created"})
                agm_user_assigned_docs = agm_doc["ros_assigned"]
                print("done by befor for loop......")
                if cm_user:
                    if len(agm_user_assigned_docs) < 2 and cm_user['assigned_to_agm'] == '':
                        users_collection.update_one({"role":"ROS",'emailid':cm_user['emailid']},{"$set":{"assigned_to_agm":agm_doc['emailid']}})
                        users_collection.update_one({"role":"AGM","emailid":agm_doc['emailid']},{"$push": {"ros_assigned": cm_user["emailid"]}})
                        print("done by after for loop......")

            cm_user = users_collection.find({"role":"CM/SM","assigned_to_agm":"","status":"Created"})
            for cm_doc in cm_user:
                agm_data = users_collection.find({"role":"AGM","status":{"$in":["Created","Approved"]}})
                for agm_doc in agm_data:
                    agm_user_assigned_docs = agm_doc["cms_assigned"]
                    print("done by befor for loop......")
                    if len(agm_user_assigned_docs) < 3 and cm_doc['assigned_to_agm'] == '':
                        users_collection.update_one({"role":"CM/SM",'emailid':cm_doc["emailid"]},{"$set":{"assigned_to_agm":agm_doc['emailid']}})
                        users_collection.update_one({"role":"AGM","emailid":agm_doc['emailid']},{"$push": {"cms_assigned": cm_doc["emailid"]}})
                        print("done by after for loop......")
            
        elif role == 'ROS':
            users_collection.update_one(
                {'_id': existing_user['_id']},
                {'$set': {
                    # 'name': name,
                    # 'role': role,
                    # 'mobileno': mobileno,
                    'password': hashed_password,
                    'status': status,
                    'assigned_to_agm':''
                }}
            )
            agm_data = users_collection.find({"role":"AGM","status":{"$in":["Created","Approved"]}})
            cm_user = users_collection.find_one({"_id":existing_user['_id'],"role":"ROS","assigned_to_agm":"","status":"Created"})
            for agm_doc in agm_data:
                agm_user_assigned_docs = agm_doc["ros_assigned"]
                if cm_user is not None and agm_user_assigned_docs is not None and len(agm_user_assigned_docs) < 2 and cm_user['assigned_to_agm'] == '':
                    users_collection.update_one({"_id":existing_user['_id'],"role":"ROS"},{"$set":{"assigned_to_agm":agm_doc['emailid']}})
                    users_collection.update_one({"role":"AGM","emailid":agm_doc['emailid']},{"$push": {"ros_assigned": cm_user["emailid"]}})
                    break;
                    
                
        elif role == 'BranchMakers':
            users_collection.update_one(
                {'_id': existing_user['_id']},
                {'$set': {
                    'password': hashed_password,
                    'status': status
                }}
            )
        elif role == 'SDN/USER':
            users_collection.update_one(
                {'_id': existing_user['_id']},
                {'$set': {
                    'password': hashed_password,
                    'status': status
                }}
            )
        session['user_created_again']="User Added Successfully with Password"
        return redirect(url_for('AllUsers')) 

        




    # if request.method=='POST':
    #     # name = request.form['name']
    #         emailid = request.form['emailid']
    #         role = request.form['role']
    #     # mobileno = request.form['mobileno']
    #         password = request.form['password']
    #         re_entered_password = request.form['Re-Enter Password']
    #         status = "Created"
    #         hashed_password = hash_password(password)
    #         if password != re_entered_password:
    #             session['ps_error']='Passwords do not match. Please try again.'
    #             return redirect(url_for('AddUser'))
    #     # elif users_collection.find_one({'emailid': emailid, 'status': 'Approved'}):
    #     #     session['user_exists']='Email ID already exists. Please use a different email.'
    #     #     return redirect(url_for('AddUser'))
    #         if users_collection.find_one({'emailid': emailid}):
    #             existing_user = users_collection.find_one({'emailid': emailid})
    #         if role == 'CM/SM':
    #             users_collection.update_one(
    #                 {'_id': existing_user['_id']},
    #                 {'$set': {
    #                     # 'name': name,
    #                     # 'role': role,
    #                     # 'mobileno': mobileno,
    #                     'password': hashed_password,
    #                     'status': status,
    #                     'mlros_assigned':[],
    #                     'assigned_to_agm':''
    #                 }}
    #             )
    #             mlros_data = users_collection.find({"role":"MLRO","assigned_to":"","status":{"$in":["Created","Approved"]}})
    #             for mlro_doc in mlros_data:
    #                 cm_user = users_collection.find_one({"_id":existing_user['_id'],"role":"CM/SM","status":{"$in":["Created"]}})
    #                 cm_user_assigned_docs = cm_user["mlros_assigned"]
    #                 if len(cm_user_assigned_docs)<5:
    #                     users_collection.update_one({"_id":mlro_doc["_id"],"emailid":mlro_doc["emailid"],"role":"MLRO","status":{"$in":["Created","Approved"]}},{"$set":{"assigned_to":cm_user['emailid']}})
    #                     users_collection.update_one({"role":"CM/SM","emailid":cm_user['emailid']},{"$push": {"mlros_assigned": mlro_doc["emailid"]}})
                
                
    #             agm_data = users_collection.find({"role":"AGM","status":{"$in":["Created","Approved"]}})
    #             cm_user = users_collection.find_one({"_id":existing_user['_id'],"role":"CM/SM","assigned_to_agm":"","status":"Created"})
    #             for agm_doc in agm_data:
    #                 agm_user_assigned_docs = agm_doc["cms_assigned"]
    #                 if cm_user is not None and agm_user_assigned_docs is not None and len(agm_user_assigned_docs) < 3 and cm_user['assigned_to_agm'] == '':
    #                     users_collection.update_one({"_id":existing_user['_id'],"role":"CM/SM"},{"$set":{"assigned_to_agm":agm_doc['emailid']}})
    #                     users_collection.update_one({"role":"AGM","emailid":agm_doc['emailid']},{"$push": {"cms_assigned": cm_user["emailid"]}})
    #                     break;
    #         elif role=='MLRO':
    #             users_collection.update_one(
    #                 {'_id': existing_user['_id']},
    #                 {'$set':
    #                  {
    #                     # 'name': name,
    #                     # 'emailid': emailid,
    #                     # 'role': role,
    #                     # 'mobileno': mobileno,
    #                     'password': hashed_password,
    #                     'status': status,
    #                     'assigned_to':"",
    #                     'assigned_to_ros':"",
    #                 }}
    #             )
    #             cmsm_data = users_collection.find({"role":"CM/SM","status":{"$in":["Created","Approved"]}})
    #             mlro_user = users_collection.find_one({"_id":existing_user['_id'],"role":"MLRO","assigned_to":"","status":{"$in":["Created"]}})
    #             for cmsm_doc in cmsm_data:
    #                 cm_user_assigned_docs = cmsm_doc["mlros_assigned"]
    #                 if mlro_user is not None and cm_user_assigned_docs is not None and len(cm_user_assigned_docs) < 5 and mlro_user['assigned_to'] == '':
    #                     users_collection.update_one({"_id":existing_user['_id'],"role":"MLRO"},{"$set":{"assigned_to":cmsm_doc['emailid']}})
    #                     users_collection.update_one({"role":"CM/SM","emailid":cmsm_doc['emailid']},{"$push": {"mlros_assigned": mlro_user["emailid"]}})
                
                
    #         elif role == 'AGM':
    #             users_collection.update_one(
    #                 {'_id': existing_user['_id']},
    #                 {'$set': {
    #                     # 'name': name,
    #                     # 'role': role,
    #                     # 'mobileno': mobileno,
    #                     'password': hashed_password,
    #                     'status': status,
    #                     'cms_assigned':[],
    #                     'ros_assigned':[]
    #                 }}
    #             )
    #             agm_data = users_collection.find({"role":"AGM","status":{"$in":["Created","Approved"]}})
    #             for agm_doc in agm_data:
    #                 cm_user = users_collection.find_one({"role":"ROS","assigned_to_agm":"","status":"Created"})
    #                 agm_user_assigned_docs = agm_doc["ros_assigned"]
    #                 print("done by befor for loop......")
    #                 if cm_user:
    #                  if len(agm_user_assigned_docs) < 2 and cm_user['assigned_to_agm'] == '':
    #                     users_collection.update_one({"role":"ROS",'emailid':cm_user['emailid']},{"$set":{"assigned_to_agm":agm_doc['emailid']}})
    #                     users_collection.update_one({"role":"AGM","emailid":agm_doc['emailid']},{"$push": {"ros_assigned": cm_user["emailid"]}})
    #                     print("done by after for loop......")

    #             cm_user = users_collection.find({"role":"CM/SM","assigned_to_agm":"","status":"Created"})
    #             for cm_doc in cm_user:
    #               agm_data = users_collection.find({"role":"AGM","status":{"$in":["Created","Approved"]}})
    #               for agm_doc in agm_data:
    #                 agm_user_assigned_docs = agm_doc["cms_assigned"]
    #                 print("done by befor for loop......")
    #                 if len(agm_user_assigned_docs) < 3 and cm_doc['assigned_to_agm'] == '':
    #                     users_collection.update_one({"role":"CM/SM",'emailid':cm_doc["emailid"]},{"$set":{"assigned_to_agm":agm_doc['emailid']}})
    #                     users_collection.update_one({"role":"AGM","emailid":agm_doc['emailid']},{"$push": {"cms_assigned": cm_doc["emailid"]}})
    #                     print("done by after for loop......")
                
    #         elif role == 'ROS':
    #             users_collection.update_one(
    #                 {'_id': existing_user['_id']},
    #                 {'$set': {
    #                     # 'name': name,
    #                     # 'role': role,
    #                     # 'mobileno': mobileno,
    #                     'password': hashed_password,
    #                     'status': status,
    #                     'assigned_to_agm':''
    #                 }}
    #             )
    #             agm_data = users_collection.find({"role":"AGM","status":{"$in":["Created","Approved"]}})
    #             cm_user = users_collection.find_one({"_id":existing_user['_id'],"role":"ROS","assigned_to_agm":"","status":"Created"})
    #             for agm_doc in agm_data:
    #                 agm_user_assigned_docs = agm_doc["ros_assigned"]
    #                 if cm_user is not None and agm_user_assigned_docs is not None and len(agm_user_assigned_docs) < 2 and cm_user['assigned_to_agm'] == '':
    #                     users_collection.update_one({"_id":existing_user['_id'],"role":"ROS"},{"$set":{"assigned_to_agm":agm_doc['emailid']}})
    #                     users_collection.update_one({"role":"AGM","emailid":agm_doc['emailid']},{"$push": {"ros_assigned": cm_user["emailid"]}})
    #                     break;
                        
                    
    #         elif role == 'BranchMakers':
    #             users_collection.update_one(
    #                 {'_id': existing_user['_id']},
    #                 {'$set': {
    #                     'password': hashed_password,
    #                     'status': status
    #                 }}
    #             )
    #         elif role == 'SDN/USER':
    #             users_collection.update_one(
    #                 {'_id': existing_user['_id']},
    #                 {'$set': {
    #                     'password': hashed_password,
    #                     'status': status
    #                 }}
    #             )
    #         session['user_created_again']="User Added Successfully with Password"
    #         return redirect(url_for('AllUsers')) 

        
@app.route('/updateUser',methods=['POST'])
@secure_route(required_role=['IT Officer'])
def updateUser():
    email_pattern = r'^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$'
    mobileno_pattern= r'^\d{10}$'
    username_pattern = r'^[a-zA-Z0-9]{1,20}$'
    idNo = request.form.get("id")
    updateName = request.form.get("name")
    updateEmail = request.form.get("emailid")
    updateMobile = request.form.get("mobileno")
    updateAddress = request.form.get("address")
    updateRole = request.form.get("role")
    updatePassword = request.form.get("Password")
    updateRePassword = request.form.get("Re-Enter Password")
    updateLeave = request.form.get("leave")
    if not re.match(username_pattern, updateName):
        session['ps_error'] = "Username must contain only letters  and numbers and be up to 20 characters long."
        return redirect(url_for('AllUsers'))
    if not re.match(email_pattern, updateEmail):
        session['ps_error'] = "Enter a valid Emailid "
        return redirect(url_for('AllUsers'))
    if not re.match(mobileno_pattern, updateMobile):
        session['ps_error'] = "Mobile Number must be only ten digits long and must be numbers only "
        return redirect(url_for('AllUsers'))
    users_collection.update_one(
        {"emailid":updateEmail},
        {"$set": {"name": updateName,"emailid":updateEmail,"mobileno":updateMobile,"address":updateAddress,"role":updateRole,"leaveStatus":updateLeave}}
    )
    return redirect(url_for('AllUsers'))


@app.route('/deleteUser',methods=['POST'])
@secure_route(required_role=['IT Officer'])
def deleteUser():
    if request.method == 'POST':
        email = request.form['emailid']
        user = users_collection.find_one({'emailid':email,'status':{'$exists':True},'status':'Approved','leaveStatus':{'$exists':True}})
        if user :
            allocated_to = user['assigned_to']
            users_collection.update_one({'emailid':email},{"$set":{"partial_Delete":True,'status':'Deleted',"leaveStatus":'On Leave'}})

            users_collection.update_one(
                {'emailid': allocated_to, 'mlros_assigned': {'$in': [email]}},
                {'$pull': {'mlros_assigned': email}}
            )

        return redirect(url_for('AllUsers'))


@app.route("/AllUsers", methods=['GET'])
@secure_route(required_role='IT Officer')
def AllUsers():
    user = users_collection.find_one({'role': 'IT Officer'})

    ituser = {'image': ""}
    if user:
        ituser = users_collection.find_one({'emailid': user.get('emailid')})

        if ituser and 'image' in ituser:
            ituser['image'] = base64.b64encode(ituser['image']).decode('utf-8')
    msg = None
    if 'ps_error' in session:
        msg = session.pop('ps_error',None)
    
    if "user_created_again" in session:
        msg = session.pop('user_created_again',None)
    if 'success_user_created' in session:
        msg = session.pop('success_user_created',None)
    if msg!=None:
        users = users_collection.find()
        return render_template("AllUsers.html",users=users,msg=msg,ituser=ituser,type='AllUsers',role='IT Officer')
    else:                                       
        users = users_collection.find()
        return render_template("AllUsers.html",users=users,ituser=ituser,type='AllUsers',role='IT Officer')
    
@app.route('/VerifyUser', methods=['GET', 'POST'])
@secure_route(required_role=['AGM','DGM/PO'])
def VerifyUser():
    # try:
    #     session['user_role']
    # except:
        # session["Pls_login"]="Session expired, Login again" 
    #     return redirect(url_for('sign_in'))
    user_role = session.get('user_role')
    emailid = session.get('email_id')
    notify = notification(emailid)

    
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        role = request.form.get('role')
        mail = request.form.get('emailid')
        action = request.form.get('action')
        if action == 'approve':
            users_collection.update_one({'_id': ObjectId(user_id)}, {'$set': {'status': 'Approved','leaveStatus':"Working"}})
            user = users_collection.find_one({'emailid':mail})

            
            if user:
                    base_url = "http://127.0.0.1:5000/reset_password"
                    reset_token = secrets.token_hex(10)
                    users_collection.update_one({'emailid':mail},{"$set":{"reset_password_token":hash_password(reset_token)}})
                    reset_link = f"{base_url}?user_id={mail}&token={reset_token}"
                    send_password_reset_email(mail,reset_link,'general')
            
            

            if role == "AGM":
                
                cmsm_data = users_collection.find({"role":"CM/SM","assigned_to_agm":"","status":"Created"})
                for cmsm_doc in cmsm_data:
                    agm_user = users_collection.find_one({"_id":ObjectId(user_id),"role":"AGM","status":"Approved"})
                    agm_user_assigned_cmsm = agm_user["cms_assigned"]
                    if len(agm_user_assigned_cmsm)<3:
                        users_collection.update_one({"_id":cmsm_doc["_id"],"emailid":cmsm_doc["emailid"],"role":"CM/SM","status":"Created"},{"$set":{"assigned_to_agm":agm_user['emailid']}})
                        users_collection.update_one({"_id":ObjectId(user_id),"role":"AGM","emailid":agm_user['emailid'],"status":"Approved"},{"$push": {"cms_assigned": cmsm_doc["emailid"]}})
        elif action == 'reject':
            users_collection.update_one({'_id': ObjectId(user_id)}, {'$set': {'status': 'Rejected'}})
            if role == "MLRO":
                users_collection.update_one({'_id': ObjectId(user_id)}, {'$set': {"assigned_to":"","assigned_to_ros":""}})
            user = users_collection.find_one({'_id': ObjectId(user_id),'status': 'Rejected'})
            user_email = user.get('emailid','')

            users_collection.update_many(
                {
                    "$or": [
                        {"cms_assigned": {"$in": [user_email]}},
                        {"mlros_assigned": {"$in": [user_email]}}
                    ]
                },
                {"$pull": {
                    "cms_assigned": user_email,
                    "mlros_assigned": user_email
                }}
            )

            users_collection.update_many(
                {
                    "$or": [
                        {"assigned_to": user_email},
                        {"assigned_to_ros": user_email}
                    ]
                },
                {"$set": {
                    "assigned_to": {
                        "$cond": {
                            "if": {
                                "$eq": ["$assigned_to", user_email]
                            },
                            "then": "",
                            "else": "$assigned_to"
                        }
                    },
                    "assigned_to_ros": {
                        "$cond": {
                            "if": {
                                "$eq": ["$assigned_to_ros", user_email]
                            },
                            "then": "",
                            "else": "$assigned_to_ros"
                        }
                    }
                }}
            )
    
    if user_role=="AGM":
        agm_user = users_collection.find_one({'role':"AGM",'emailid':emailid,'status':"Approved"})
        info = users_collection.find_one({'emailid':emailid,'status':'Approved'})
        if 'image' in info:
            # Encode the image data as a base64 string
            info['image'] = base64.b64encode(info['image']).decode('utf-8')
        
        print("infoooo" , info)
        if agm_user:
            cm_users_list = agm_user.get('cms_assigned', [])
            print(cm_users_list)
            cm_users = users_collection.find({'status':'Created','role':'CM/SM','emailid':{
                "$in":cm_users_list
            }})
            mlro_users=users_collection.find({'status':'Created','role':'MLRO','assigned_to':{
                "$in":cm_users_list
            }})
         
            users = list(cm_users) + list(mlro_users) 
            print("mlrousers",list(mlro_users))
            mlro_emailids = [user.get('emailid') for user in mlro_users]
            print("mlro_emailids",mlro_emailids)
            ros_users = users_collection.find({'status':'Created','role':'ROS','assigned_to_agm':emailid})

            users = users+list(ros_users)
            remaining_users = users_collection.find({'status': 'Created','role':{
                "$in":["BranchMakers"]
            }})
            users = users+list(remaining_users)
        else:
            users=[]

        return render_template("VerifyUser.html", users=users,ROLE="AGM",agmuser=info,type='VerifyUser',notify=notify)
    elif user_role == "DGM/PO":
        created_users = users_collection.find({'status': 'Created','role':'AGM'})
        sdn_users=users_collection.find({'status':'Created','role':'SDN/USER'})
        users = list(created_users) + list(sdn_users)
        agm_user = users_collection.find_one({'role':"AGM",'emailid':emailid,'status':"Approved"})
        info = users_collection.find_one({'emailid':emailid,'status':'Approved'})
        if 'image' in info:
            # Encode the image data as a base64 string
            info['image'] = base64.b64encode(info['image']).decode('utf-8')
        return render_template("VerifyUser.html", users=users,ROLE="DGM",dgmuser=info,type='VerifyUser',notify=notify)




@app.route('/post_registration', methods=['POST', 'GET'])
@secure_route(required_role=['IT Officer'])
def post_registration():
    if request.method == "POST":
        name = request.form.get("username")
        emailid = request.form.get("email")
        mobileno = request.form.get("mobileno")
        role = request.form.get("role")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if not name or not emailid or not mobileno or not password1 or not password2 or not role:
            session["missing_val_msg"] = "All fields are required"
            return redirect(url_for('sign_up'))

        if password1 != password2:
            session["ps_error_msg"] = 'Passwords Should Match!'
            return redirect(url_for('sign_up'))

        if users_collection.find_one({"mobileno": mobileno}) or users_collection.find_one({"emailid": emailid}):
            session["error_msg"] = 'This Mobile Number or Email Id already exists'
            return redirect(url_for('sign_up'))

        hashed_password = bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt())
        user_input = {
            'name': name,
            'emailid': emailid,
            'role': role,
            'mobileno': mobileno,
            'password': hashed_password
        }
        users_collection.insert_one(user_input)
        session["success_reg_msg"] = 'Registration successful'
        return redirect(url_for('sign_in'))

    return redirect(url_for('sign_up'))


# @app.route('/post_registration', methods=['POST', 'GET'])
# @secure_route(required_role=['IT Officer'])
# def post_registration():
#     if request.method == "POST":
#         # Get details from the filled form
#         name = request.form.get("username")
        
#         emailid = request.form.get("email")
#         mobileno = request.form.get("mobileno")
#         role = request.form.get("role")
#         password1 = request.form.get("password1")
#         password2 = request.form.get("password2")
#         # if not is_password_valid(password1):
#         #         # print('%%%%%%%%%%%%%%%',password)
#         #         session['ps_error'] = 'The password must be between 8 to 16 characters in length and must include at least one number, one uppercase letter, one lowercase letter, and one special character.'
#         #         return redirect(url_for('sign_up'))


#         if not name or not emailid or not mobileno or not password1 or not password2 or not role:
#             session["missing_val_msg"] = "All fields are required"
#             return redirect(url_for('sign_up'))

#         mobileno_found = users_collection.find_one({"mobileno": mobileno})
#         email_found = users_collection.find_one({"emailid": emailid})
       
#     #    Alert messages based on the conditions 
#         if password1 != password2:
#             session["ps_error_msg"] = 'Passwords Should Match!'
#             return redirect(url_for('sign_up'))
#         else:
#             if mobileno_found or email_found:
#                 if mobileno_found:
#                     session["mobile_error_msg"] = 'This Mobile Number Is Already Exists'
#                     return redirect(url_for('sign_up'))
#                 if email_found:
#                     session["email_error_msg"] = 'This Email Id Is Already Exists'
#                     return redirect(url_for('sign_up'))
#             else:
#                 hashed_password = hash_password(password1)
#                 user_input = {'name': name, 
#                                 'emailid':emailid,
#                                 'role':role,
#                                 'mobileno':mobileno,'password':hashed_password}
#                 users_collection.insert_one(user_input)
#                 session["success_reg_msg"] = 'Registration successful'
#                 return redirect(url_for('sign_in'))
#     else:
#         redirect(url_for('sign_up'))

@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    return response








def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        email_id = session.get("email_id")
        # session_token = session.get("session_token")
        # if not email_id or not session_token:
        #     return redirect(url_for("sign_in"))
        # user = users_collection.find_one({"emailid": email_id})
        # if not user or user.get("session_token") != session_token:
        #     return redirect(url_for("sign_in"))
        return f(*args, **kwargs)
    return decorated_function





@app.route('/logout')
def logout():
    try:
        del session
    except:
        pass
    # return redirect(url_for("sign_in"))
    response = make_response(redirect(url_for("sign_in")))

    # Add no-store headers to prevent caching
    response.cache_control.no_store = True

    return response

# @app.route('/logout', methods=['POST', 'GET'])
# def logout():
#     try:
#         email = session.get('email_id')
#         if email:
#             print(f"Attempting to log out user with email: {email}")
#             # users_collection.update_one({'emailid': email}, {"$set": {"session_token": None}})
#         else:
#             print("No email found in the session.")
#         session.clear()
#         print("Session cleared successfully")
#     except Exception as e:
#         print(f"Error during logout: {str(e)}")
#     return redirect(url_for("sign_in"))




# @app.route('/logout', methods=['POST'])
# def logout():
#     email = session.get('email_id')
#     if email:
#         users_collection.update_one({'emailid': email}, {"$set": {"session_token": None}})
#         session.clear()
#         print('Logged out successfully')
#     return 'Logged out successfully', 200

# @app.route('/logout', methods=['GET'])
# def logout_get():
#     try:
#         email = session.get('email_id')
#         print(f"Attempting to log out user with email: {email}")
#         if email:
#             users_collection.update_one({'emailid': email}, {"$set": {"session_token": None}})
#         else:
#             print("No email found in the session.")
#         session.clear()
#         print("Session cleared successfully")
#     except Exception as e:
#         print(f"Error during logout: {str(e)}")
#     return redirect(url_for("sign_in"))

# @app.route('/update_status', methods=['POST'])
# def update_status():
#     email = session.get('email_id')
#     print('emailid:',email)
#     if email:
#         users_collection.update_one({'emailid': email}, {"$set": {"session_token": None}})
#         print('Status updated to null')
#     session.clear()
#     return 'Status updated to null', 200



# @app.route('/update_active_status', methods=['POST'])
# def update_active_status():
#     email = session.get('email_id')
#     print('emailidddd:',email)
#     if email:
#         users_collection.update_one({'emailid': email}, {"$set": {"last_active": datetime.datetime.utcnow()}})
#         print('Active status updated')
#     return 'Active status updated', 200



@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
     msg =None
     if "no_user_found_fp" in session:
        msg = session.pop("no_user_found_fp",None)
     if "token_expired" in session:
        msg = session.pop("token_expired",None)
     return render_template('forgot_password.html',msg=msg)

@app.route("/postforgotpassword", methods=["POST", "GET"])
def postforgotpassword():
    if request.method == "POST":
        current_datetime = datetime.now()
        midnight_datetime = str(current_datetime.date())
        email = request.form.get('email')
        user = users_collection.find_one({'emailid': email})
        if ('reset_password_count' in user) and (midnight_datetime in user['reset_password_count']):
            reset_password_count = user['reset_password_count'].get(midnight_datetime)
        else:
            users_collection.update_one({'emailid':email},{"$set":{"reset_password_count":{midnight_datetime:0}}})
            reset_password_count = 1 
        if user and (reset_password_count < 30):
            base_url = "http://127.0.0.1:5000/reset_password" 
            reset_token = secrets.token_hex(10)
            reset_expiry = datetime.utcnow() + timedelta(minutes=30)
            hashed_token = hash_password(reset_token)
            users_collection.update_one({'emailid': email}, {
                "$set": {"reset_password_token": hashed_token, "reset_token_expiry": reset_expiry},
                "$inc": {"reset_password_count."+f'{midnight_datetime}': 1}
            }, upsert=True)
            reset_link = f"{base_url}?user_id={email}&token={reset_token}"
            send_password_reset_email(email, reset_link, 'general')
            return render_template("email_sent_for_fp.html")
        elif user:
            session["no_user_found_fp"]="User limit Exeited"
            return redirect(url_for("forgot_password"))
        else:
            session["no_user_found_fp"] = "No user found, please enter a valid email"
            return redirect(url_for("forgot_password"))


# def is_password_validd(new_password1):
#     # Define the regex for password validation
#     password_pattern = re.compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,16}$')
#     return bool(password_pattern.match(new_password1))


# @app.route("/reset_password", methods=["GET", "POST"])
# def reset_password():
#     if request.method == 'POST':
#         user_id = request.form.get('user_id')
#         token = request.form.get('token')
#         new_password1 = request.form.get('new_password1')
#         new_password2 = request.form.get('new_password2')
#         if new_password1 != new_password2:
#             session["password_mismatch_msg"] = "Passwords do not match"
#             return redirect(url_for('reset_password'))

#         if not is_password_valid(new_password1):
#             print('%%%%%%%%%%%%%%',new_password1)
#             # flash('The password must be between 8 to 16 characters in length and must include at least one number, one uppercase letter, one lowercase letter, and one special character.')
#             # session['invalid_pwd']="The password must be between 8 to 16 characters in length and must include at least one number, one uppercase letter, one lowercase letter, and one special character"
#             # return redirect(url_for('reset_password'))
#             return render_template('reset_password.html', user_id=user_id, token=token,msgg="The password must be between 8 to 16 characters in length and must include at least one number, one uppercase letter, one lowercase letter, and one special character.")
        
#         if not  new_password1 or not new_password2:
#             session["missing_val_msg"] = "All fields are required"
#             return redirect(url_for('reset_password'))
        
#         user_data = users_collection.find_one({"emailid": user_id})

#         if user_data:
#             reset_token = user_data.get("reset_password_token")
#             reset_token_expiry = user_data.get("reset_token_expiry", datetime.min)

#             if bcrypt.checkpw(token.encode('utf-8'), reset_token) and datetime.utcnow() <= reset_token_expiry:
#                 if new_password1 == new_password2:
#                     hashed_password = hash_password(new_password1)
                    
#                     # Update password and remove reset token from user data
#                     users_collection.update_one({"emailid": user_id}, {
#                         "$set": {"password": hashed_password},
#                         "$unset": {"reset_password_token": "", "reset_token_expiry": ""}
#                     })
                    
#                     session['password_changed_succesfully'] = "Password changed successfully"
#                     return redirect(url_for('sign_in'))  # Redirect to login page after resetting
#                 else:
#                     return render_template('reset_password.html', user_id=user_id, token=token, msg="Passwords should match")
#     else:
#         user_id = request.args.get('user_id')
#         token = request.args.get('token')
#         user_data = users_collection.find_one({"emailid": user_id})

#         if user_data:
#             reset_token = user_data.get("reset_password_token")
#             reset_token_expiry = user_data.get("reset_token_expiry", datetime.min)

#             if reset_token and bcrypt.checkpw(token.encode('utf-8'), reset_token) and datetime.utcnow() <= reset_token_expiry:
#                 return render_template('reset_password.html', user_id=user_id, token=token)
#             else:
#                 session["token_expired"] = "Reset Password link is either expired or not valid, try again"
#                 return redirect(url_for("forgot_password"))
#         # return render_template('sign_in.html', user_id=user_id, token=token)
   
@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    new_captcha_dict = SIMPLE_CAPTCHA.create()
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        token = request.form.get('token')
        new_password1 = request.form.get('new_password1')
        new_password2 = request.form.get('new_password2')

        # Check for missing fields
        if not user_id or not token or not new_password1 or not new_password2:
            session["missing_val_msg"] = "All fields are required"
            return redirect(url_for('reset_password', user_id=user_id, token=token))

        # Check if passwords match
        if new_password1 != new_password2:
            msg="Passwords do not match"
            return render_template('reset_password.html', user_id=user_id, token=token, msg=msg)

        # Check if password is valid
        if not is_password_valid(new_password1):
            msg = "The password must be between 8 to 16 characters in length and must include at least one number, one uppercase letter, one lowercase letter, and one special character."
            return render_template('reset_password.html', user_id=user_id, token=token, msg=msg)

        # Check user data and reset token
        user_data = users_collection.find_one({"emailid": user_id})
        if user_data:
            reset_token = user_data.get("reset_password_token")
            reset_token_expiry = user_data.get("reset_token_expiry", datetime.min)

            # Verify the token and expiry
            if bcrypt.checkpw(token.encode('utf-8'), reset_token) and datetime.utcnow() <= reset_token_expiry:
                hashed_password = hash_password(new_password1)

                # Update password and remove reset token from user data
                users_collection.update_one({"emailid": user_id}, {
                    "$set": {"password": hashed_password},
                    "$unset": {"reset_password_token": "", "reset_token_expiry": ""}
                })

                # session['password_changed_successfully'] = "Password changed successfully"
                msg="Password changed successfully"
                return render_template('sign_in.html', msg=msg,captcha=new_captcha_dict)

                # return redirect(url_for('sign_in'))  # Redirect to login page after resetting

            else:
                msg = "Invalid or expired reset token."
                return render_template('reset_password.html', user_id=user_id, token=token, msg=msg)

        else:
            msg = "User not found."
            return render_template('reset_password.html', user_id=user_id, token=token, msg=msg)

    else:  # GET request
        user_id = request.args.get('user_id')
        token = request.args.get('token')

        # Check user data and reset token
        user_data = users_collection.find_one({"emailid": user_id})
        if user_data:
            reset_token = user_data.get("reset_password_token")
            reset_token_expiry = user_data.get("reset_token_expiry", datetime.min)

            # Verify the token and expiry
            if reset_token and bcrypt.checkpw(token.encode('utf-8'), reset_token) and datetime.utcnow() <= reset_token_expiry:
                return render_template('reset_password.html', user_id=user_id, token=token)
            else:
                session["token_expired"] = "Reset Password link is either expired or not valid, try again"
                return redirect(url_for("forgot_password"))

        msg = "Invalid request."
        return render_template('reset_password.html', msg=msg)



@app.route('/dashbord', methods=['GET', 'POST'])
@secure_route(required_role=['DGM/PO'])
def dashbord():
    user = users_collection.find_one({'role': 'DGM/PO'})
    notify = notification(user.get('emailid'))


    ituser = {'image': None}
    if user:
        ituser = users_collection.find_one({'emailid': user.get('emailid')})
        if ituser and 'image' in ituser:
            ituser['image'] = base64.b64encode(ituser['image']).decode('utf-8')
# ==========
#  Summary Of Total Transactions In An Year --> Doneeee with new schema
# ==========
    target_year = 2021
    total_deposits = 0
    total_withdrawals = 0

    # Define the date range for the target year
    start_date = datetime(target_year, 1, 1)
    end_date = datetime(target_year + 1, 1, 1)

    # Calculate the sum of deposits and withdrawals in the current collection for the target year
    pipeline = [
        {
            "$unwind": "$TXNDATA"
        },
        {
            "$match": {
                "TXNDATA.Transaction Date": {
                    "$gte": start_date,
                    "$lt": end_date
                },
                "TXNDATA.Transaction Category": {"$in": ["Deposits", "Withdrawals"]}
            }
        },
        {
            "$group": {
                "_id": {
                    "category": "$TXNDATA.Transaction Category",
                    "account": "$TXNDATA.Account Number"
                },
                "total_amount": {"$sum": "$TXNDATA.Transaction Amount"}
            }
        }
    ]

    agg_result = list(txn_collection.aggregate(pipeline))

    # Separate deposits and withdrawals
    for doc in agg_result:
        category = doc['_id']['category']
        amount = int(doc['total_amount'])
        if category == 'Deposits':
            total_deposits += amount
        elif category == 'Withdrawals':
            total_withdrawals += amount

    Total_amount = total_deposits + total_withdrawals
    print("total_deposits",total_deposits)
    print("Total_amount",Total_amount)
    print("total_withdrawals",total_withdrawals)


    # ==========
    #  Last 3 Months Account Created and Highest Deposit And withdrawals transactions in That Accounts  --> Doneeee with new schema
    # ==========

    current_date = "2015-06-01"
    current_date = datetime.strptime(current_date, "%Y-%m-%d")
    #    three_months_ago = current_date - timedelta(days=90)
    three_months_ago = current_date - timedelta(days=90)


    # Initialize a variable to store the highest transaction amount
    sum_deposits = {}
    sum_withdrawals = {}
    data_deposits = []
    data_withdrawals = []

        # Define the date range for the last 3 months
    start_date = three_months_ago
    end_date = current_date

    # Calculate the sum of deposits and withdrawals in the current collection for the last 3 months
    pipeline = [
        {
            "$unwind": "$TXNDATA"
        },
        {
            "$match": {
                "TXNDATA.Acc_Opening_Date": {
                    "$gte": start_date,
                    "$lt": end_date
                }
            }
        },
        {
            "$group": {
                "_id": {
                    "category": "$TXNDATA.Transaction Category",
                    "account": "$TXNDATA.Account Number"
                },
                "total": {"$sum": "$TXNDATA.Transaction Amount"}
                # "opening_date":"$Acc_Opening_Date"
            }
        }
    ]

    agg_result = list(txn_collection.aggregate(pipeline))

    results = txn_collection.aggregate(pipeline)

    for doc in agg_result:
        category = doc['_id']['category']
        total_amount = int(doc["total"])
        # opening_date = result["opening_date"]
        # customer_id = result["Customer ID"]
        data = {
            "Account Number": doc['_id']['account'],
            "Total Amount": total_amount,
            "Transaction Category": category,
        }
        if category == "Deposits":
            data_deposits.append(data)
        elif category == "Withdrawals":
            data_withdrawals.append(data)

    # Find the top 5 deposits and withdrawals
    df_deposits = pd.DataFrame(data_deposits)
    df_withdrawals = pd.DataFrame(data_withdrawals)
    # Sort the DataFrames by the amount in descending order and select the top 5
    df_top_deposits = df_deposits.sort_values(by="Total Amount", ascending=False).head(5)
    df_top_withdrawals = df_withdrawals.sort_values(by="Total Amount", ascending=False).head(5)

    # Print the top 5 deposits and withdrawals DataFrames
    print("Top 5 Deposits:")
    print(df_top_deposits)
    print("="*30)
    print("Top 5 Withdrawals:")
    print(df_top_withdrawals)

    # ==========
    #  Highest Transactions in Current day
    # ==========
    current_date = "2021-10-20"
    current_date = datetime.strptime(current_date, "%Y-%m-%d")
    #    three_months_ago = current_date - timedelta(days=90)
    #    three_months_ago = current_date - timedelta(days=90)


    # Initialize a variable to store the highest transaction amount
    sum_deposits = {}
    sum_withdrawals = {}
    data_deposits_day = []
    data_withdrawals_day = []

    # Define the date range for the last 3 months


    # Calculate the sum of deposits and withdrawals in the current collection for the last 3 months
    pipeline = [
        {
            "$unwind": "$TXNDATA"
        },
        {
            "$match": {
                "TXNDATA.Transaction Date": {"$eq": current_date},
                }

        },
        {
            "$group": {
                "_id": {
                    "category": "$TXNDATA.Transaction Category",
                    "account": "$TXNDATA.Account Number"
                },
                "total": {"$sum": "$TXNDATA.Transaction Amount"}
                # "opening_date":"$Acc_Opening_Date"
            }
        }
    ]

    agg_result = list(txn_collection.aggregate(pipeline))

    for doc in agg_result:
        category = doc["_id"]["category"]
        total_amount = doc["total"]
        # opening_date = result["opening_date"]
        # customer_id = result["Customer ID"]
        data = {
            "Account Number": doc["_id"]["account"],
            "Total Amount": total_amount,
            "Transaction Category": category,

        }
        if category == "Deposits":
            data_deposits_day.append(data)
        elif category == "Withdrawals":
            data_withdrawals_day.append(data)

    # Find the top 5 deposits and withdrawals
    df_deposits_day = pd.DataFrame(data_deposits_day)
    df_withdrawals_day = pd.DataFrame(data_withdrawals_day)
    # Sort the DataFrames by the amount in descending order and select the top 5
    df_top_deposits_day = df_deposits_day.sort_values(by="Total Amount", ascending=False).head(2)
    df_top_withdrawals_day = df_withdrawals_day.sort_values(by="Total Amount", ascending=False).head(2)

    # Print the top 5 deposits and withdrawals DataFrames
    print("Top 2 Deposits:")
    print(df_top_deposits_day)
    print("="*30)
    print("Top 2 Withdrawals:")
    print(df_top_withdrawals_day)

    return render_template('dashbord.html',
                            total_amount=Total_amount,
                            total_withdrawals=total_withdrawals,
                            total_deposits=total_deposits,
                            df_top_deposits=df_top_deposits,
                            df_top_withdrawals=df_top_withdrawals,
                            df_top_withdrawals_day=df_top_withdrawals_day,
                            df_top_deposits_day=df_top_deposits_day,notify=notify,
                            dgmuser=ituser,role='DGM/PO',type='dashbord'
                            )



@app.route('/transaction_monitoring', methods=['GET', 'POST'])
@secure_route(required_role=['DGM/PO'])
def transaction_monitoring():
    crumbs_data = for_tm_ty_rm(TM_collection,"TM")
    
    user = users_collection.find_one({'role': 'DGM/PO'})

    notify = notification(user.get('emailid'))

    ituser = {'image': None}
    if user:
        ituser = users_collection.find_one({'emailid': user.get('emailid')})
        if ituser and 'image' in ituser:
            ituser['image'] = base64.b64encode(ituser['image']).decode('utf-8')

    return render_template('transaction_monitoring.html',crumbs_data=crumbs_data,type='dashbord',dgmuser=ituser,role='DGM/PO',notify=notify)
def group_by_main_category(dictionary):
    grouped_data = {}
    prefix_mapping = {"TM": "Transaction Monitoring", "TY": "Typology", "RM": "Risk Monitoring"}

    for key, value in dictionary.items():
        main_category_match = re.match(r'([A-Za-z]+_\d+)_\d+', key)
        if main_category_match:
            main_category = main_category_match.group(1)
            for prefix, replacement in prefix_mapping.items():
                if prefix in main_category:
                    main_category = main_category.replace(prefix, replacement)
                    break
            main_category = main_category.replace("_", " ")

            if main_category not in grouped_data:
                grouped_data[main_category] = {}
            grouped_data[main_category][key] = value
    return grouped_data

def for_tm_ty_rm(collection,col_code):
    data_from_col = collection.find({},{"code":1,"Alert_title":1,"_id":0})
    code_alert_title = {}
    for doc in data_from_col:
        code_alert_title[doc['code']]=doc['Alert_title']
    grouped_data = group_by_main_category(code_alert_title)
    return grouped_data
# @app.route('/DV_TM', methods=['GET','POST'])
# def Updatedthreshold():
#     document = db['TM'].find_one({'code': 'TM_1_1'})
    
#     # Extract current and previous values
#     current_values = document.get('Current_values', {})
#     previous_values = document.get('Previous_Values', [])
#     if not isinstance(previous_values, list):
#         previous_values = [previous_values]

#     return render_template('DV_TM.html', current_values=current_values, previous_values=previous_values)

def threshold_values_from_col(collection_name,alert_code):
    data_from_col = collection_name.find_one({"code":alert_code})
    current_values = data_from_col.get("Current_values")
    return current_values


@app.route(f"/DV_threshold_values", methods=['GET','POST'])
@secure_route(required_role=['DGM/PO'])
def DV_threshold_values():
    if request.method=="POST":
        route_code = request.form.get("route_code")
    else:
        route_code=session['route_code']
    if "TM" in route_code:
        document = TM_collection.find_one({'code': route_code})
    if "TY" in route_code:
        document = TY_collection.find_one({'code': route_code})
    if "RM" in route_code:
        document = RM_collection.find_one({'code': route_code})
    current_values = document.get('Current_values', {})
    previous_values = document.get('Previous_Values', [])
    tm_heading = document.get('Alert_title','')
    tm_sub_heading = route_code
    user = users_collection.find_one({'role': 'DGM/PO'})
    notify = notification(user.get('emailid'))

    ituser = {'image': None}
    if user:
        ituser = users_collection.find_one({'emailid': user.get('emailid')})
        if ituser and 'image' in ituser:
            ituser['image'] = base64.b64encode(ituser['image']).decode('utf-8') 

    return render_template('DV_TM.html', notify=notify ,current_values=current_values, previous_values=previous_values,
                            tm_heading=tm_heading, tm_sub_heading=tm_sub_heading,type='Updatedthreshold',role='DGM/PO',dgmuser=ituser)


@app.route(f'/update_threshold', methods=['POST'])
@secure_route(required_role=['DGM/PO'])
def update_threshold():
    if request.method == 'POST':
        route_code = request.form.get("route_code")
        if 'TM' in route_code:
            current_collection = TM_collection
        if 'TY' in route_code:
            current_collection = TY_collection
        if 'RM' in route_code:
            current_collection = RM_collection
        document = current_collection.find_one({'code': route_code})
        current_values = document.get('Current_values', {})
        try:
            from_form_values={}
            for val in list(current_values.keys()):
                from_form_values[f"{val}"]=int(request.form.get(f"{val}"))
        except ValueError:
            return "Invalid input. Please enter valid numbers."
        current_date_str = str(datetime.now())
        previous_values = document.get('Previous_Values', [])
        if not isinstance(previous_values, list):
            previous_values = [previous_values]
        current_values_dict=current_values.copy()
        current_values_dict['Date']=current_date_str
        updated_previous_values = previous_values + [current_values_dict]
        updated_document = {
            'Current_values':from_form_values,
            'Previous_Values': updated_previous_values
        }
        current_collection.update_one({'code': route_code}, {'$set': updated_document}, upsert=True)
        session['route_code']=route_code
        return redirect(url_for('DV_threshold_values'))


def for_threshold(collections_list):
    data=[]
    for col in collections_list:
        all_data={}
        data_from_col = col.find({},{"code":1,"_id":0})
        all_data[data_from_col.collection.name]=[]
        for doc in data_from_col:
            all_data[data_from_col.collection.name].append(doc['code'])
        data.append(all_data)
    return data

@app.route("/Updatedthreshold")
@secure_route(required_role=['DGM/PO'])
def Updatedthreshold():
    collections_list=[TM_collection,TY_collection,RM_collection]
    dropdown_data = for_threshold(collections_list)
    user = users_collection.find_one({'role': 'DGM/PO'})
    notify = notification(user.get('emailid'))


    ituser = {'image': None}
    if user:
        ituser = users_collection.find_one({'emailid': user.get('emailid')})
        if ituser and 'image' in ituser:
            ituser['image'] = base64.b64encode(ituser['image']).decode('utf-8')    

    return render_template("Updated_Threshold.html",dropdown_data=dropdown_data,dgmuser=ituser,type='Updatedthreshold',role='DGM/PO',notify=notify)


def image():
    user = users_collection.find_one({'role': 'DGM/PO'})

    ituser = {'image': None}
    if user:
        ituser = users_collection.find_one({'emailid': user.get('emailid')})
        if ituser and 'image' in ituser:
            ituser['image'] = base64.b64encode(ituser['image']).decode('utf-8') 
        return ituser; 



# Indicative rule added
@app.route('/TM_1_1',  methods=['GET', 'POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def TM_1_1():
    if request.method == 'POST':
        userEmail = session['email_id']
        notify = notification(userEmail)
        if 'download' in request.form:
            user_input_date_str = '2021-06-25'
        elif 'user_input_date_str' in request.form:
            user_input_date_str = request.form.get('user_input_date_str')
        else:
            user_input_date_str = '2021-06-25'
        user_input_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')
        current_values = threshold_values_from_col(TM_collection,'TM_1_1')

        total_df = pd.DataFrame()
        total_df_non = pd.DataFrame()
        pipeline = [
            {
                "$unwind": "$TXNDATA"
            },
            {
                "$match": {
                    "TXNDATA.Transaction Type": "Cash",
                    "TXNDATA.Transaction Date": {"$eq": user_input_date},
                    "TXNDATA.Transaction Category": "Deposits",
                    "TXNDATA.Transaction Currency": "INR"
                }
            },
            {
                "$group": {
                    "_id": "$TXNDATA.Account Number",
                    "total_amount": {"$sum": "$TXNDATA.Transaction Amount"},
                    "nature_of_account": {"$first": "$TXNDATA.Nature of account"},  # Assuming 'Nature of account' is present in each transaction
                    "data": {"$push": "$TXNDATA"}
                }
            },
            {
                "$match": {
                    "$or": [
                        {"nature_of_account": "Individual", "total_amount": {"$gte": current_values['Individual']}},
                        {"nature_of_account": "Non Ind", "total_amount": {"$gt": current_values['Non_Individual']}}
                    ]
                }
            }
        ]
        agg_result = list(txn_collection.aggregate(pipeline))
        data_from_col_df = pd.DataFrame()
        for doc in agg_result:
            data_from_col_df = pd.concat([data_from_col_df, pd.DataFrame(doc['data'])])
        if not data_from_col_df.empty:
            individual_values = data_from_col_df[data_from_col_df['Nature of account'] == 'Individual']
            columns_to_agg = [col for col in individual_values.columns if col != 'Account Number']
            # Group by 'Account Number' and sum 'Transaction Amount'
            total_df = individual_values.groupby('Account Number').agg({
                col: 'first' if col != 'Transaction Amount' else 'sum' for col in columns_to_agg
            }).reset_index().dropna(axis=1)

            def generate_indicative_rule(row):
               return f"Cash deposits made by {row['Account Number']} aggregating to or more than {current_values['Individual']} in a day has triggered one of the RFI and raised an alert for date {row['Transaction Date']}, {row['Account Number']} being an {row['Nature of account']} and {row['Customer Profile']} has made deposit transactions which aggregated to a total of {int(row['Transaction Amount'])} on {row['Transaction Date']}"
            
            total_df['Indicative_rule'] = total_df.apply(generate_indicative_rule, axis=1)
            
            non_individual_values = data_from_col_df[data_from_col_df['Nature of account'] == 'Non Ind']
            total_df_non = non_individual_values.groupby('Account Number').agg({
                col: 'first' if col != 'Transaction Amount' else 'sum' for col in columns_to_agg
            }).reset_index().dropna(axis=1)

            def generate_indicative_rule_non_ind(row):
               return f"Cash deposits made by {row['Account Number']} aggregating to or more than {current_values['Non_Individual']} in a day has triggered one of the RFI and raised an alert for date {row['Transaction Date']}, {row['Account Number']} being an {row['Nature of account']} and {row['Customer Profile']} has made withdrawal transactions which aggregated to a total of {int(row['Transaction Amount'])} on {row['Transaction Date']}"
            total_df_non['Indicative_rule'] = total_df_non.apply(generate_indicative_rule_non_ind, axis=1)
        
        
        processed_data = []
        for item in processed_data:
            print(item)
        if 'download' in request.form:
            
            excel_buffer = io.BytesIO()
            # Create an ExcelWriter object to write multiple DataFrames to different sheets
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                total_df.to_excel(writer, sheet_name='Individuals', index=False)
                total_df_non.to_excel(writer, sheet_name='Non-Individuals', index=False)
            # Set the position of the BytesIO object to the beginning
            excel_buffer.seek(0)
            # Generate the response to download the Excel file
            response = make_response(excel_buffer.read())
            response.headers["Content-Disposition"] = "attachment filename=TM_1_1_data.xlsx"
            response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            return response
        document =TM_collection.find_one({"code":"TM_1_1"})
        tm_heading = document.get("Alert_title","")
        tm_sub_hedding="TM 1.1"


        



        if returning_data_enabled:
            return [total_df,total_df_non]
        else:
            if session["user_role"]=="DGM/PO":
                return render_template("display_data.html",notify=notify,Individual_df=total_df,
                                  Non_individual_df=total_df_non,
                                 tm_heading=tm_heading,
                            tm_sub_hedding=tm_sub_hedding,dgmuser=image(),type='dashbord',role='DGM/PO')

# Indicative rule added
@app.route('/TM_1_2',  methods=['GET', 'POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def TM_1_2():
    if request.method == 'POST':
        userEmail = session['email_id']
        notify = notification(userEmail)
        if 'download' in request.form:
            user_input_date_str = '2021-05-20'  
        elif 'user_input_date_str' in request.form:
            user_input_date_str = request.form.get('user_input_date_str')
        else:
            user_input_date_str = '2021-05-20' 
        user_input_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')
        current_values = threshold_values_from_col(TM_collection,'TM_1_2')
        total_df = pd.DataFrame()
        total_df_non = pd.DataFrame()
        
        pipeline = [
            {
                "$unwind": "$TXNDATA"
            },
            {
                "$match": {
                    "TXNDATA.Transaction Type": "Cash",
                    "TXNDATA.Transaction Date": {"$eq": user_input_date},
                    "TXNDATA.Transaction Category": "Withdrawals",
                    "TXNDATA.Transaction Currency": "INR"
                }
            },
            {
                "$group": {
                    "_id": "$TXNDATA.Account Number",
                    "total_amount": {"$sum": "$TXNDATA.Transaction Amount"},
                    "nature_of_account": {"$first": "$TXNDATA.Nature of account"},  # Assuming 'Nature of account' is present in each transaction
                    "data": {"$push": "$TXNDATA"}
                }
            },
            {
                "$match": {
                    "$or": [
                        {"nature_of_account": "Individual", "total_amount": {"$gte": current_values['Individual']}},
                        {"nature_of_account": "Non Ind", "total_amount": {"$gt": current_values['Non_Individual']}}
                    ]
                }
            }
        ]

       
        agg_result = list(txn_collection.aggregate(pipeline))

        data_from_col_df = pd.DataFrame()
        for doc in agg_result:
            data_from_col_df = pd.concat([data_from_col_df, pd.DataFrame(doc['data'])])

        if not data_from_col_df.empty:
            individual_values = data_from_col_df[data_from_col_df['Nature of account'] == 'Individual']
            
            columns_to_agg = [col for col in individual_values.columns if col != 'Account Number']

            total_df = individual_values.groupby('Account Number').agg({
                col: 'first' if col != 'Transaction Amount' else 'sum' for col in columns_to_agg
            }).reset_index().dropna(axis=1)
           
            def generate_indicative_rule(row):
                return f"Cash Withdrawals made by {row['Account Number']} aggregating to or more than {current_values['Individual']} in a day has triggered one of the RFI and raised an alert for date {row['Transaction Date']}, {row['Account Number']} being an {row['Nature of account']} and and {row['Customer Profile']} has made deposit transactions which aggregated to a total of {int(row['Transaction Amount'])} on {row['Transaction Date']}"
                
            total_df['Indicative_rule'] = total_df.apply(generate_indicative_rule, axis=1)

            non_individual_values = data_from_col_df[data_from_col_df['Nature of account'] == 'Non Ind']
            total_df_non = non_individual_values.groupby('Account Number').agg({
                col: 'first' if col != 'Transaction Amount' else 'sum' for col in columns_to_agg
            }).reset_index().dropna(axis=1)

            def generate_indicative_rule_non_ind(row):
               return f"Cash Withdrawals made by {row['Account Number']} aggregating to or more than {current_values['Non_Individual']} in a day has triggered one of the RFI and raised an alert for date {row['Transaction Date']}, {row['Account Number']} being an {row['Nature of account']} and and {row['Customer Profile']} has made withdrawal transactions which aggregated to a total of {int(row['Transaction Amount'])} on {row['Transaction Date']}"
            
            total_df_non['Indicative_rule'] = total_df_non.apply(generate_indicative_rule_non_ind, axis=1)
                
        # Process the data or prepare it for rendering
        # For example, you can store the processed data in a list
        processed_data = []
        # print(total_df_non)
        for item in processed_data:
            print(item)
        
        if 'download' in request.form:
           
            excel_buffer = io.BytesIO()

            # Create an ExcelWriter object to write multiple DataFrames to different sheets
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                total_df.to_excel(writer, sheet_name='Individuals', index=False)
                total_df_non.to_excel(writer, sheet_name='Non-Individuals', index=False)

            # Set the position of the BytesIO object to the beginning
            excel_buffer.seek(0)

            # Generate the response to download the Excel file
            response = make_response(excel_buffer.read())
            response.headers["Content-Disposition"] = "attachment filename=TM_1_2_data.xlsx"
            response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            return response
        document =TM_collection.find_one({"code":"TM_1_2"})
        tm_heading = document.get("Alert_title","")
        tm_sub_hedding="TM 1.2"
        if returning_data_enabled:
            return [total_df,total_df_non]
        else:
            if session["user_role"] == "DGM/PO":
                return render_template("display_data.html",notify=notify,Individual_df=total_df,
                                  Non_individual_df=total_df_non,
                                 tm_heading=tm_heading,
                            tm_sub_hedding=tm_sub_hedding,dgmuser=image(),type='dashbord',role='DGM/PO')

# Indicative rule added
@app.route('/TM_1_3',  methods=['GET', 'POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def TM_1_3():
    if request.method == 'POST':
        userEmail = session['email_id']
        notify = notification(userEmail)
        if 'download' in request.form:
            user_input_date_str = '2021-10-20'  
        elif 'user_input_date_str' in request.form:
            user_input_date_str = request.form.get('user_input_date_str')
        else:
            user_input_date_str = '2021-10-20' 
        user_input_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')
        current_values = threshold_values_from_col(TM_collection,'TM_1_3')
         
        total_df = pd.DataFrame()
        total_df_non = pd.DataFrame()

        pipeline = [
        {
            "$unwind": "$TXNDATA"
        },
        {
            "$match": {
                "TXNDATA.Transaction Type": "Non-cash",
                "TXNDATA.Transaction Date": {"$eq": user_input_date},
                "TXNDATA.Transaction Category": "Deposits",
                "TXNDATA.Transaction Currency": "INR"
            }
        },
        {
            "$group": {
                "_id": "$TXNDATA.Account Number",
                "total_amount": {"$sum": "$TXNDATA.Transaction Amount"},
                "nature_of_account": {"$first": "$TXNDATA.Nature of account"},  # Assuming 'Nature of account' is present in each transaction
                "data": {"$push": "$TXNDATA"}
            }
        },
        {
            "$match": {
                "$or": [
                    {"nature_of_account": "Individual", "total_amount": {"$gte": current_values['Individual']}},
                    {"nature_of_account": "Non Ind", "total_amount": {"$gt": current_values['Non_Individual']}}
                ]
            }
        }
        ]
        agg_result = list(txn_collection.aggregate(pipeline))

        data_from_col_df = pd.DataFrame()
        for doc in agg_result:
            data_from_col_df = pd.concat([data_from_col_df, pd.DataFrame(doc['data'])])

        if not data_from_col_df.empty:
            individual_values = data_from_col_df[data_from_col_df['Nature of account'] == 'Individual']
            
            columns_to_agg = [col for col in individual_values.columns if col != 'Account Number']

            total_df = individual_values.groupby('Account Number').agg({
                col: 'first' if col != 'Transaction Amount' else 'sum' for col in columns_to_agg
            }).reset_index().dropna(axis=1)
            def generate_indicative_rule(row):
               return f"Non-Cash deposits made by {row['Account Number']} aggregating to or more than {current_values['Individual']} in a day has triggered one of the RFI and raised an alert for date {row['Transaction Date']}, {row['Account Number']} being an {row['Nature of account']} and {row['Customer Profile']} account has made deposit transactions which aggregated to a total of {row['Transaction Amount']} on {row['Transaction Date']}"
            
            total_df['Indicative_rule'] = total_df.apply(generate_indicative_rule, axis=1)

            non_individual_values = data_from_col_df[data_from_col_df['Nature of account'] == 'Non Ind']
            total_df_non = non_individual_values.groupby('Account Number').agg({
                col: 'first' if col != 'Transaction Amount' else 'sum' for col in columns_to_agg
            }).reset_index().dropna(axis=1)
            def generate_indicative_rule_non_ind(row):
               return f"Non-Cash deposits made by {row['Account Number']} aggregating to or more than {current_values['Non_Individual']} in a day has triggered one of the RFI and raised an alert for date {row['Transaction Date']}, {row['Account Number']} being an {row['Nature of account']} and {row['Customer Profile']} has made deposit transactions which aggregated to a total of {row['Transaction Amount']} on {row['Transaction Date']}"
            total_df_non['Indicative_rule'] = total_df_non.apply(generate_indicative_rule_non_ind, axis=1)

        
        # Process the data or prepare it for rendering
        # For example, you can store the processed data in a list
        processed_data = []
        print(total_df_non)
        for item in processed_data:
            print(item)
        
        if 'download' in request.form:
           
            excel_buffer = io.BytesIO()

            # Create an ExcelWriter object to write multiple DataFrames to different sheets
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                total_df.to_excel(writer, sheet_name='Individuals', index=False)
                total_df_non.to_excel(writer, sheet_name='Non-Individuals', index=False)

            # Set the position of the BytesIO object to the beginning
            excel_buffer.seek(0)

            # Generate the response to download the Excel file
            response = make_response(excel_buffer.read())
            response.headers["Content-Disposition"] = "attachment filename=TM_1_3_data.xlsx"
            response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            return response
        
        document =TM_collection.find_one({"code":"TM_1_3"})
        tm_heading = document.get("Alert_title","")
        tm_sub_hedding="TM 1.3"
        if returning_data_enabled:
            return [total_df,total_df_non]
        else:
            if session["user_role"]=="DGM/PO":            
                return render_template("display_data.html",notify=notify,Individual_df=total_df,
                                  Non_individual_df=total_df_non,
                                 tm_heading=tm_heading,
                            tm_sub_hedding=tm_sub_hedding,dgmuser=image(),type='dashbord',role='DGM/PO')

# Indicative rule added     
@app.route('/TM_1_4',  methods=['GET', 'POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def TM_1_4():
    if request.method == 'POST':
        userEmail = session['email_id']
        notify = notification(userEmail)
        if 'download' in request.form:
            user_input_date_str = '2021-10-20'  
        elif 'user_input_date_str' in request.form:
            user_input_date_str = request.form.get('user_input_date_str')
        else:
            # user_input_date_str = request.form['user_entered_date_tm1_4']
            user_input_date_str = '2021-10-20'
        user_input_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')
        current_values = threshold_values_from_col(TM_collection,'TM_1_4')
     
        
        total_df = pd.DataFrame()
        total_df_non = pd.DataFrame()

        pipeline = [
            {
                "$unwind": "$TXNDATA"
            },
            {
                "$match": {
                    "TXNDATA.Transaction Type": "Non-cash",
                    "TXNDATA.Transaction Date": {"$eq": user_input_date},
                    "TXNDATA.Transaction Category": "Withdrawals",
                    "TXNDATA.Transaction Currency": "INR"
                }
            },
            {
                "$group": {
                    "_id": "$TXNDATA.Account Number",
                    "total_amount": {"$sum": "$TXNDATA.Transaction Amount"},
                    "nature_of_account": {"$first": "$TXNDATA.Nature of account"},  # Assuming 'Nature of account' is present in each transaction
                    "data": {"$push": "$TXNDATA"}
                }
            },
            {
                "$match": {
                    "$or": [
                        {"nature_of_account": "Individual", "total_amount": {"$gte": current_values['Individual']}},
                        {"nature_of_account": "Non Ind", "total_amount": {"$gt": current_values['Non_Individual']}}
                    ]
                }
            }
        ]

        agg_result = list(txn_collection.aggregate(pipeline))

        data_from_col_df = pd.DataFrame()
        for doc in agg_result:
            data_from_col_df = pd.concat([data_from_col_df, pd.DataFrame(doc['data'])])

        if not data_from_col_df.empty:
            individual_values = data_from_col_df[data_from_col_df['Nature of account'] == 'Individual']
            
            columns_to_agg = [col for col in individual_values.columns if col != 'Account Number']

            total_df = individual_values.groupby('Account Number').agg({
                col: 'first' if col != 'Transaction Amount' else 'sum' for col in columns_to_agg
            }).reset_index().dropna(axis=1)
            
            def generate_indicative_rule(row):
               return f"Non-Cash Withdrawals made by {row['Account Number']} aggregating to or more than {current_values['Individual']} in a day has triggered one of the RFI and raised an alert for date {row['Transaction Date']}, {row['Account Number']} being an {row['Nature of account']} and {row['Customer Profile']} account has made Withdrawal transactions which aggregated to a total of {row['Transaction Amount']} on {row['Transaction Date']}"
            
            total_df['Indicative_rule'] = total_df.apply(generate_indicative_rule, axis=1)

            non_individual_values = data_from_col_df[data_from_col_df['Nature of account'] == 'Non Ind']
            total_df_non = non_individual_values.groupby('Account Number').agg({
                col: 'first' if col != 'Transaction Amount' else 'sum' for col in columns_to_agg
            }).reset_index().dropna(axis=1)
            def generate_indicative_rule_non_ind(row):
               return f"Non-Cash Withdrawals made by {row['Account Number']} aggregating to or more than {current_values['Non_Individual']} in a day has triggered one of the RFI and raised an alert for date {row['Transaction Date']}, {row['Account Number']} being an {row['Nature of account']} and {row['Customer Profile']} account has made Withdrawal transactions which aggregated to a total of {row['Transaction Amount']} on {row['Transaction Date']}"
            total_df_non['Indicative_rule'] = total_df_non.apply(generate_indicative_rule_non_ind, axis=1)
            
        
        # Process the data or prepare it for rendering
        # For example, you can store the processed data in a list
        processed_data = []
        print(total_df_non)
        for item in processed_data:
            print(item)
        
        if 'download' in request.form:
           
            excel_buffer = io.BytesIO()

            # Create an ExcelWriter object to write multiple DataFrames to different sheets
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                total_df.to_excel(writer, sheet_name='Individuals', index=False)
                total_df_non.to_excel(writer, sheet_name='Non-Individuals', index=False)

            # Set the position of the BytesIO object to the beginning
            excel_buffer.seek(0)

            # Generate the response to download the Excel file
            response = make_response(excel_buffer.read())
            response.headers["Content-Disposition"] = "attachment filename=TM_1_4_data.xlsx"
            response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            return response

        document =TM_collection.find_one({"code":"TM_1_4"})
        tm_heading = document.get("Alert_title","")
        tm_sub_hedding="TM 1.4"
        if returning_data_enabled:
            return [total_df,total_df_non]
        else:
            if session["user_role"]=="DGM/PO":
                return render_template("display_data.html",notify=notify,Individual_df=total_df,
                                  Non_individual_df=total_df_non,
                                 tm_heading=tm_heading,
                            tm_sub_hedding=tm_sub_hedding,dgmuser=image(),type='dashbord',role='DGM/PO')




        # ... (process the total_df and total_df_non data and add it to processed_data)
        # return render_template('display_data.html', Individual_df=total_df, Non_individual_df=total_df_non,
                            #    tm_heading=tm_heading,tm_sub_hedding=tm_sub_hedding)

    # return render_template('transaction_monitoring.html')



# @app.route('/tm2_displaying_data')
# def tm2_displaying_data():
#      return render_templ
# userEmail = session['email_id']ate('tm2_displaying_data.html
# notify = notification(userEmail)',type='tm2_displaying_data',dgmuser=image(),type='dashbord',role='DGM/PO')

# Indicative rule added
@app.route('/TM_2_1', methods=['GET', 'POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def TM_2_1():
    if request.method == 'POST':
        userEmail = session['email_id']
        notify = notification(userEmail)
        if 'download' in request.form:
            user_input_date_str = '2021-10-20'  
        elif 'user_input_date_str' in request.form:
            user_input_date_str = request.form.get('user_input_date_str')
        else:
            user_input_date_str = '2021-10-20'

        user_input_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')
        current_values = threshold_values_from_col(TM_collection,'TM_2_1')
        print(current_values)


        total_df = pd.DataFrame()

        total_df_non = pd.DataFrame()

        start_date = user_input_date-timedelta(days=30)

        pipeline = [
            {
                "$unwind": "$TXNDATA"
            },
            {
                "$match": {
                    "TXNDATA.Transaction Type": "Cash",
                    "TXNDATA.Transaction Date": {"$lte": user_input_date,
                                                "$gte":start_date},
                    "TXNDATA.Transaction Category": "Deposits",
                    "TXNDATA.Transaction Currency": "INR"
                }
            },
            {
                "$group": {
                    "_id": "$TXNDATA.Account Number",
                    # "total_amount": {"$sum": "$TXNDATA.Transaction Amount"},
                    # "nature_of_account": {"$first": "$TXNDATA.Nature of account"},  # Assuming 'Nature of account' is present in each transaction
                    "data": {"$push": "$TXNDATA"}
                }
            }
        ]

        agg_result = list(txn_collection.aggregate(pipeline))

        data_from_col_df = pd.DataFrame()
        for doc in agg_result:
            data_from_col_df = pd.concat([data_from_col_df, pd.DataFrame(doc['data'])])

        if not data_from_col_df.empty:
            individual_values = data_from_col_df[data_from_col_df['Nature of account'] == 'Individual']
            # columns_to_agg = [col for col in individual_values.columns if col != 'Account Number']

            ind_dfs = individual_values.groupby('Account Number')
            for gpname, gpdata in ind_dfs:
                if not gpdata.empty:
                    sum_df = pd.DataFrame({
                        'Transaction Amount': [gpdata['Transaction Amount'].sum()],
                        'Account Number': [gpname],
                        'Customer Profile':[gpdata['Customer Profile'].unique()[0]],
                        'Nature of account':[gpdata['Nature of account'].unique()[0]],
                        'From Transaction Date':[gpdata['Transaction Date'].unique()[0]],
                        'To Transaction Date':[gpdata['Transaction Date'].unique()[-1]]
                    })
                    filtered_df = sum_df[sum_df['Transaction Amount'] >= current_values['Individual']]
                    if not filtered_df.empty:
                        total_df = pd.concat([total_df,filtered_df])
                        def generate_indicative_rule(row):
                            return f"Cash deposits made by {row['Account Number']} aggregating to or more than {current_values['Individual']} in a day has triggered one of the RFI and raised an alert for a month triggered between dates {row['From Transaction Date']} and {row['To Transaction Date']}, {row['Account Number']} being an {row['Nature of account']} and {row['Customer Profile']} account has made deposit transactions which aggregated to a total of {row['Transaction Amount']} from {row['From Transaction Date']}" 
                        total_df['Indicative_rule'] = total_df.apply(generate_indicative_rule, axis=1)

            non_individual_values = data_from_col_df[data_from_col_df['Nature of account'] == 'Non Ind']
            non_ind_dfs = non_individual_values.groupby('Account Number')
            
            for gpname, gpdata in non_ind_dfs:
                if not gpdata.empty:
                    sum_df = pd.DataFrame({
                        'Transaction Amount': [gpdata['Transaction Amount'].sum()],
                        'Account Number': [gpname],
                        'Customer Profile':[gpdata['Customer Profile'].unique()[0]],
                        'Nature of account':[gpdata['Nature of account'].unique()[0]],
                        'From Transaction Date':[gpdata['Transaction Date'].unique()[0]],
                        'To Transaction Date':[gpdata['Transaction Date'].unique()[-1]]})
                    filtered_df = sum_df[sum_df['Transaction Amount'] >= current_values['Non_Individual']]
                    if not filtered_df.empty:
                        total_df_non = pd.concat([total_df_non,filtered_df])
                        def generate_indicative_rule_non_ind(row):
                            return f"Cash deposits made by {row['Account Number']} aggregating to or more than {current_values['Non_Individual']} in a day has triggered one of the RFI and raised an alert for a month triggered between dates {row['From Transaction Date']} and {row['To Transaction Date']}, {row['Account Number']} being an {row['Nature of account']} and {row['Customer Profile']} account has made deposit transactions which aggregated to a total of {row['Transaction Amount']} from {row['From Transaction Date']}"
                        total_df_non['Indicative_rule'] = total_df_non.apply(generate_indicative_rule_non_ind, axis=1)
            tm_sub_hedding="TM_2_1"
            tm_heading="Cash Deposits in a Day Aggregating to INR For Individuals and Non-individuals"
            if 'download' in request.form:
           
                excel_buffer = io.BytesIO()

                # Create an ExcelWriter object to write multiple DataFrames to different sheets
                with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                    total_df.to_excel(writer, sheet_name='Individuals', index=False)
                    total_df_non.to_excel(writer, sheet_name='Non-Individuals', index=False)

                # Set the position of the BytesIO object to the beginning
                excel_buffer.seek(0)

                # Generate the response to download the Excel file
                response = make_response(excel_buffer.read())
                response.headers["Content-Disposition"] = "attachment filename=TM_1_2_data.xlsx"
                response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                return response

            if returning_data_enabled:
                return [total_df,total_df_non]
            else:
                if session["user_role"]=="DGM/PO":
                    return render_template("display_data.html",notify=notify,Individual_df=total_df,
                                    Non_individual_df=total_df_non,
                                    tm_heading=tm_heading,
                                tm_sub_hedding=tm_sub_hedding,dgmuser=image(),type='dashbord',role='DGM/PO')

# Indicative rule added
@app.route('/TM_2_2', methods=['GET', 'POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def TM_2_2():
    if request.method == 'POST':
        userEmail = session['email_id']
        notify = notification(userEmail)
        if 'download' in request.form:
            user_input_date_str = '2021-10-20'  
        elif 'user_input_date_str' in request.form:
            user_input_date_str = request.form.get('user_input_date_str')
        else:
            user_input_date_str = '2021-10-20'

        user_input_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')

        current_values = threshold_values_from_col(TM_collection,'TM_2_2')


        total_df = pd.DataFrame()

        total_df_non = pd.DataFrame()

        start_date = user_input_date-timedelta(days=30)

        pipeline = [
            {
                "$unwind": "$TXNDATA"
            },
            {
                "$match": {
                    "TXNDATA.Transaction Type": "Cash",
                    "TXNDATA.Transaction Date": {"$lte": user_input_date,
                                                "$gte":start_date},
                    "TXNDATA.Transaction Category": "Withdrawals",
                    "TXNDATA.Transaction Currency": "INR"
                }
            },
            {
                "$group": {
                    "_id": "$TXNDATA.Account Number",
                    "data": {"$push": "$TXNDATA"}
                }
            }
        ]

        agg_result = list(txn_collection.aggregate(pipeline))

        data_from_col_df = pd.DataFrame()
        for doc in agg_result:
            data_from_col_df = pd.concat([data_from_col_df, pd.DataFrame(doc['data'])])

        if not data_from_col_df.empty:
            individual_values = data_from_col_df[data_from_col_df['Nature of account'] == 'Individual']
            # columns_to_agg = [col for col in individual_values.columns if col != 'Account Number']

            ind_dfs = individual_values.groupby('Account Number')
            for gpname, gpdata in ind_dfs:
                if not gpdata.empty:
                    sum_df = pd.DataFrame({
                        'Transaction Amount': [gpdata['Transaction Amount'].sum()],
                        'Account Number': [gpname],
                        'Customer Profile':[gpdata['Customer Profile'].unique()[0]],
                        'Nature of account':[gpdata['Nature of account'].unique()[0]],
                        'From Transaction Date':[gpdata['Transaction Date'].unique()[0]],
                        'To Transaction Date':[gpdata['Transaction Date'].unique()[-1]]
                    })
                    filtered_df = sum_df[sum_df['Transaction Amount'] >= current_values['Individual']]
                    if not filtered_df.empty:
                        total_df = pd.concat([total_df,filtered_df])
                        def generate_indicative_rule(row):
                            return f"Cash Withdrawals made by {row['Account Number']} aggregating to or more than {current_values['Individual']} in a day has triggered one of the RFI and raised an alert for a month triggered between dates {row['From Transaction Date']} and {row['To Transaction Date']}, {row['Account Number']} being an {row['Nature of account']} and {row['Customer Profile']} account has made Withdrawal transactions which aggregated to a total of {row['Transaction Amount']} from {row['From Transaction Date']}"
                            
                        total_df['Indicative_rule'] = total_df.apply(generate_indicative_rule, axis=1)

            non_individual_values = data_from_col_df[data_from_col_df['Nature of account'] == 'Non Ind']
            non_ind_dfs = non_individual_values.groupby('Account Number')
            
            for gpname, gpdata in non_ind_dfs:
                if not gpdata.empty:
                    sum_df = pd.DataFrame({
                        'Transaction Amount': [gpdata['Transaction Amount'].sum()],
                        'Account Number': [gpname],
                        'Customer Profile':[gpdata['Customer Profile'].unique()[0]],
                        'Nature of account':[gpdata['Nature of account'].unique()[0]],
                        'From Transaction Date':[gpdata['Transaction Date'].unique()[0]],
                        'To Transaction Date':[gpdata['Transaction Date'].unique()[-1]]})
                    filtered_df = sum_df[sum_df['Transaction Amount'] >= current_values['Non_Individual']]
                    if not filtered_df.empty:
                        total_df_non = pd.concat([total_df_non,filtered_df])
                        def generate_indicative_rule_non_ind(row):
                            return f"Cash Withdrawals made by {row['Account Number']} aggregating to or more than {current_values['Non_Individual']} in a day has triggered one of the RFI and raised an alert for a month triggered between dates {row['From Transaction Date']} and {row['To Transaction Date']}, {row['Account Number']} being an {row['Nature of account']} and {row['Customer Profile']} account has made Withdrawal transactions which aggregated to a total of {row['Transaction Amount']} from {row['From Transaction Date']}"
                        total_df_non['Indicative_rule'] = total_df_non.apply(generate_indicative_rule_non_ind, axis=1)
            total_df_non=total_df_non.dropna(axis=1)
            total_df=total_df.dropna(axis=1)
            
            tm_heading="TM 2.2"
            document =TM_collection.find_one({"code":"TM_2_2"})
            tm_sub_hedding = document.get("Alert_title","")
            if 'download' in request.form:
                excel_buffer = io.BytesIO()
                # Create an ExcelWriter object to write multiple DataFrames to different sheets
                with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                    total_df.to_excel(writer, sheet_name='Individuals', index=False)
                    total_df_non.to_excel(writer, sheet_name='Non-Individuals', index=False)

                # Set the position of the BytesIO object to the beginning
                excel_buffer.seek(0)

                # Generate the response to download the Excel file
                response = make_response(excel_buffer.read())
                response.headers["Content-Disposition"] = "attachment filename=TM_2_2_data.xlsx"
                response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                return response


        if returning_data_enabled:
            return [total_df,total_df_non]
        else:
            if session["user_role"]=="DGM/PO":
                return render_template("display_data.html",notify=notify,Individual_df=total_df,
                                    Non_individual_df=total_df_non,
                                    tm_heading=tm_sub_hedding,
                                tm_sub_hedding=tm_heading,dgmuser=image(),type='dashbord',role='DGM/PO')

# Indicative rule added
@app.route('/TM_2_3', methods=['GET', 'POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def TM_2_3():
    if request.method == 'POST':
        userEmail = session['email_id']
        notify = notification(userEmail)
        if 'download' in request.form:
            user_input_date_str = '2021-10-20'  
        elif 'user_input_date_str' in request.form:
            user_input_date_str = request.form.get('user_input_date_str')
        else:
            user_input_date_str = '2021-10-20'

        user_input_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')

        current_values = threshold_values_from_col(TM_collection,'TM_2_3')

        total_df = pd.DataFrame()

        total_df_non = pd.DataFrame()

        start_date = user_input_date-timedelta(days=30)

        pipeline = [
            {
                "$unwind": "$TXNDATA"
            },
            {
                "$match": {
                    "TXNDATA.Transaction Type": "Non-cash",
                    "TXNDATA.Transaction Date": {"$lte": user_input_date,
                                                "$gte":start_date},
                    "TXNDATA.Transaction Category": "Deposits",
                    "TXNDATA.Transaction Currency": "INR"
                }
            },
            {
                "$group": {
                    "_id": "$TXNDATA.Account Number",
                    "data": {"$push": "$TXNDATA"}
                }
            }
        ]

        agg_result = list(txn_collection.aggregate(pipeline))

        data_from_col_df = pd.DataFrame()
        for doc in agg_result:
            data_from_col_df = pd.concat([data_from_col_df, pd.DataFrame(doc['data'])])

        if not data_from_col_df.empty:
            individual_values = data_from_col_df[data_from_col_df['Nature of account'] == 'Individual']
            # columns_to_agg = [col for col in individual_values.columns if col != 'Account Number']

            ind_dfs = individual_values.groupby('Account Number')
            for gpname, gpdata in ind_dfs:
                if not gpdata.empty:
                    sum_df = pd.DataFrame({
                        'Transaction Amount': [gpdata['Transaction Amount'].sum()],
                        'Account Number': [gpname],
                        'Customer Profile':[gpdata['Customer Profile'].unique()[0]],
                        'Nature of account':[gpdata['Nature of account'].unique()[0]],
                        'From Transaction Date':[gpdata['Transaction Date'].unique()[0]],
                        'To Transaction Date':[gpdata['Transaction Date'].unique()[-1]]
                    })
                    filtered_df = sum_df[sum_df['Transaction Amount'] >= current_values['Individual']]
                    if not filtered_df.empty:
                        total_df = pd.concat([total_df,filtered_df])
                        def generate_indicative_rule(row):
                            return f"Non-Cash deposits made by {row['Account Number']} aggregating to or more than {current_values['Individual']} in a day has triggered one of the RFI and raised an alert for a month triggered between dates {row['From Transaction Date']} and {row['To Transaction Date']}, {row['Account Number']} being an {row['Nature of account']} and {row['Customer Profile']} account has made Withdrawal transactions which aggregated to a total of {row['Transaction Amount']} from {row['From Transaction Date']}"
                            
                        total_df['Indicative_rule'] = total_df.apply(generate_indicative_rule, axis=1)
            non_individual_values = data_from_col_df[data_from_col_df['Nature of account'] == 'Non Ind']
            non_ind_dfs = non_individual_values.groupby('Account Number')
            
            for gpname, gpdata in non_ind_dfs:
                if not gpdata.empty:
                    sum_df = pd.DataFrame({
                        'Transaction Amount': [gpdata['Transaction Amount'].sum()],
                        'Account Number': [gpname],
                        'Customer Profile':[gpdata['Customer Profile'].unique()[0]],
                        'Nature of account':[gpdata['Nature of account'].unique()[0]],
                        'From Transaction Date':[gpdata['Transaction Date'].unique()[0]],
                        'To Transaction Date':[gpdata['Transaction Date'].unique()[-1]]            })
                    filtered_df = sum_df[sum_df['Transaction Amount'] >= current_values['Non_Individual']]
                    if not filtered_df.empty:
                        total_df_non = pd.concat([total_df_non,filtered_df])
                        def generate_indicative_rule_non_ind(row):
                            return f"Non-Cash deposits made by {row['Account Number']} aggregating to or more than {current_values['Non_Individual']} in a day has triggered one of the RFI and raised an alert for a month triggered between dates {row['From Transaction Date']} and {row['To Transaction Date']}, {row['Account Number']} being an {row['Nature of account']} and {row['Customer Profile']} account has made deposit transactions which aggregated to a total of {row['Transaction Amount']} from {row['From Transaction Date']}"
                        total_df_non['Indicative_rule'] = total_df_non.apply(generate_indicative_rule_non_ind, axis=1)
            tm_sub_hedding="TM 2.3"
            document =TM_collection.find_one({"code":"TM_2_3"})
            tm_heading = document.get("Alert_title","")
            total_df=total_df.dropna(axis=1)
            total_df_non=total_df_non.dropna(axis=1)
            if 'download' in request.form:
           
                excel_buffer = io.BytesIO()

                # Create an ExcelWriter object to write multiple DataFrames to different sheets
                with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                    total_df.to_excel(writer, sheet_name='Individuals', index=False)
                    total_df_non.to_excel(writer, sheet_name='Non-Individuals', index=False)

                # Set the position of the BytesIO object to the beginning
                excel_buffer.seek(0)

                # Generate the response to download the Excel file
                response = make_response(excel_buffer.read())
                response.headers["Content-Disposition"] = "attachment filename=TM_2_3_data.xlsx"
                response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                return response

        
            if returning_data_enabled:
                return [total_df,total_df_non]
            else:
                if session["user_role"]=="DGM/PO":
                    return render_template("display_data.html",notify=notify,Individual_df=total_df,
                                    Non_individual_df=total_df_non,
                                    tm_heading=tm_heading,
                                tm_sub_hedding=tm_sub_hedding,dgmuser=image(),type='dashbord',role='DGM/PO')
    
# Indicative rule added
@app.route('/TM_2_4', methods=['GET', 'POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def TM_2_4():
    if request.method == 'POST':
        userEmail = session['email_id']
        notify = notification(userEmail)
        if 'download' in request.form:
            user_input_date_str = '2021-10-20'  
        elif 'user_input_date_str' in request.form:
            user_input_date_str = request.form.get('user_input_date_str')
        else:
            user_input_date_str = '2021-10-20'

        user_input_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')

        current_values = threshold_values_from_col(TM_collection,'TM_2_4')

        total_df = pd.DataFrame()

        total_df_non = pd.DataFrame()

        start_date = user_input_date-timedelta(days=30)

        pipeline = [
            {
                "$unwind": "$TXNDATA"
            },
            {
                "$match": {
                    "TXNDATA.Transaction Type": "Non-cash",
                    "TXNDATA.Transaction Date": {"$lte": user_input_date,
                                                "$gte":start_date},
                    "TXNDATA.Transaction Category": "Withdrawals",
                    "TXNDATA.Transaction Currency": "INR"
                }
            },
            {
                "$group": {
                    "_id": "$TXNDATA.Account Number",
                    "data": {"$push": "$TXNDATA"}
                }
            }
        ]

        agg_result = list(txn_collection.aggregate(pipeline))

        data_from_col_df = pd.DataFrame()
        for doc in agg_result:
            data_from_col_df = pd.concat([data_from_col_df, pd.DataFrame(doc['data'])])

        if not data_from_col_df.empty:
            individual_values = data_from_col_df[data_from_col_df['Nature of account'] == 'Individual']
            # columns_to_agg = [col for col in individual_values.columns if col != 'Account Number']

            ind_dfs = individual_values.groupby('Account Number')
            for gpname, gpdata in ind_dfs:
                if not gpdata.empty:
                    sum_df = pd.DataFrame({
                        'Transaction Amount': [gpdata['Transaction Amount'].sum()],
                        'Account Number': [gpname],
                        'Customer Profile':[gpdata['Customer Profile'].unique()[0]],
                        'Nature of account':[gpdata['Nature of account'].unique()[0]],
                        'From Transaction Date':[gpdata['Transaction Date'].unique()[0]],
                        'To Transaction Date':[gpdata['Transaction Date'].unique()[-1]]
                    })
                    filtered_df = sum_df[sum_df['Transaction Amount'] >= current_values['Individual']]
                    if not filtered_df.empty:
                        total_df = pd.concat([total_df,filtered_df])
                        def generate_indicative_rule(row):
                            return f"Non-Cash Withdrawals made by {row['Account Number']} aggregating to or more than {current_values['Individual']} in a day has triggered one of the RFI and raised an alert for a month triggered between dates {row['From Transaction Date']} and {row['To Transaction Date']}, {row['Account Number']} being an {row['Nature of account']} and {row['Customer Profile']} account has made Withdrawal transactions which aggregated to a total of {row['Transaction Amount']} from {row['From Transaction Date']}"
                            
                        total_df['Indicative_rule'] = total_df.apply(generate_indicative_rule, axis=1)
            non_individual_values = data_from_col_df[data_from_col_df['Nature of account'] == 'Non Ind']
            non_ind_dfs = non_individual_values.groupby('Account Number')
            
            for gpname, gpdata in non_ind_dfs:
                if not gpdata.empty:
                    sum_df = pd.DataFrame({
                        'Transaction Amount': [gpdata['Transaction Amount'].sum()],
                        'Account Number': [gpname],
                        'Customer Profile':[gpdata['Customer Profile'].unique()[0]],
                        'Nature of account':[gpdata['Nature of account'].unique()[0]],
                        'From Transaction Date':[gpdata['Transaction Date'].unique()[0]],
                        'To Transaction Date':[gpdata['Transaction Date'].unique()[-1]]            })
                    filtered_df = sum_df[sum_df['Transaction Amount'] >= current_values['Non_Individual']]
                    if not filtered_df.empty:
                        total_df_non = pd.concat([total_df_non,filtered_df])
                        def generate_indicative_rule(row):
                            return f"Non-Cash Withdrawals made by {row['Account Number']} aggregating to or more than {current_values['Non_Individual']} in a day has triggered one of the RFI and raised an alert for a month triggered between dates {row['From Transaction Date']} and {row['To Transaction Date']}, {row['Account Number']} being an {row['Nature of account']} and {row['Customer Profile']} account has made Withdrawal transactions which aggregated to a total of {row['Transaction Amount']} from {row['From Transaction Date']}"
                            
                        total_df_non['Indicative_rule'] = total_df_non.apply(generate_indicative_rule, axis=1)
            total_df_non=total_df_non.dropna(axis=1)
            total_df=total_df.dropna(axis=1)
            tm_sub_hedding="TM 2.4"
            document =TM_collection.find_one({"code":"TM_2_4"})
            tm_heading = document.get("Alert_title","")
            if 'download' in request.form:
           
                excel_buffer = io.BytesIO()

                # Create an ExcelWriter object to write multiple DataFrames to different sheets
                with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                    total_df.to_excel(writer, sheet_name='Individuals', index=False)
                    total_df_non.to_excel(writer, sheet_name='Non-Individuals', index=False)

                # Set the position of the BytesIO object to the beginning
                excel_buffer.seek(0)

                # Generate the response to download the Excel file
                response = make_response(excel_buffer.read())
                response.headers["Content-Disposition"] = "attachment filename=TM_2_4_data.xlsx"
                response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                return response
            if returning_data_enabled:
                return [total_df,total_df_non]
            else:
                if session["user_role"]=="DGM/PO":
                    return render_template("display_data.html",notify=notify,Individual_df=total_df,
                                    Non_individual_df=total_df_non,
                                    tm_heading=tm_heading,
                                tm_sub_hedding=tm_sub_hedding,dgmuser=image(),type='dashbord',role='DGM/PO')

# Indicative rule added
@app.route('/TM_2_5', methods=['GET', 'POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def TM_2_5():
    if request.method == 'POST':
        userEmail = session['email_id']
        notify = notification(userEmail)
        if 'download' in request.form:
            user_input_date_str = '2021-10-20'  
        elif 'user_input_date_str' in request.form:
            user_input_date_str = request.form.get('user_input_date_str')
        else:
            
            user_input_date_str = '2021-10-20'

        user_input_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')

        current_values = threshold_values_from_col(TM_collection,'TM_2_5')
    

        total_df = pd.DataFrame()


        start_date = user_input_date-timedelta(days=30)

        pipeline = [
            {
                "$unwind": "$TXNDATA"
            },
            {
                "$match": {
                    "TXNDATA.Transaction Type": "Cash",
                    "TXNDATA.Transaction Date": {"$lte": user_input_date,
                                                "$gte":start_date},
                    "TXNDATA.Transaction Currency": "INR",
                    "TXNDATA.PAN": { "$nin": ["Yes"]}
                }
            },
            {
                "$group": {
                    "_id": "$TXNDATA.Account Number",
                    "data": {"$push": "$TXNDATA"}
                }
            }
        ]

        agg_result = list(txn_collection.aggregate(pipeline))

        data_from_col_df = pd.DataFrame()
        for doc in agg_result:
            data_from_col_df = pd.concat([data_from_col_df, pd.DataFrame(doc['data'])])
        if not data_from_col_df.empty:
            individual_values = data_from_col_df[data_from_col_df['Nature of account'] == 'Individual']

            df_grp = individual_values.groupby('Account Number')
            for gpname, gpdata in df_grp:
                if not gpdata.empty:
                    sum_df = pd.DataFrame({
                        'Transaction Amount': [gpdata['Transaction Amount'].sum()],
                        'Account Number': [gpname],
                        'Nature of account':gpdata['Nature of account'].unique(),
                        'Customer Profile':gpdata['Customer Profile'].unique(),
                        'From Transaction Date':[gpdata['Transaction Date'].unique()[0]],
                        'To Transaction Date':[gpdata['Transaction Date'].unique()[-1]]
                    })
                    filtered_df = sum_df[sum_df['Transaction Amount'] >= current_values['X1']]
                    if not filtered_df.empty:
                        total_df = pd.concat([total_df,filtered_df])
                        def generate_indicative_rule(row):
                            return f"High value cash transaction made by {row['Account Number']} aggregating to or more than {current_values['X1']} in a month without PAN has triggered one of the RFI and raised an alert for a month triggered between dates {row['From Transaction Date']} and {row['To Transaction Date']}, {row['Account Number']} being an {row['Nature of account']} and {row['Customer Profile']} account has made transactions which aggregated to a total of {row['Transaction Amount']} from {row['From Transaction Date']}"
                            
                        total_df['Indicative_rule'] = total_df.apply(generate_indicative_rule, axis=1)
            tm_sub_hedding="TM 2.5"
            document =TM_collection.find_one({"code":"TM_2_5"})
            tm_heading = document.get("Alert_title","")
            total_df=total_df.dropna(axis=1)
            if 'download' in request.form:
           
                excel_buffer = io.BytesIO()

                # Create an ExcelWriter object to write multiple DataFrames to different sheets
                with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                    total_df.to_excel(writer, sheet_name='Individuals', index=False)

                # Set the position of the BytesIO object to the beginning
                excel_buffer.seek(0)

                # Generate the response to download the Excel file
                response = make_response(excel_buffer.read())
                response.headers["Content-Disposition"] = "attachment filename=TM_2_5data.xlsx"
                response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                return response
            if returning_data_enabled:

                return [total_df]
            else:
                if session["user_role"]=="DGM/PO":
        
            
                    return render_template("display_data.html",notify=notify,Individual_df=total_df,
                                    tm_heading=tm_heading,
                                tm_sub_hedding=tm_sub_hedding,dgmuser=image(),type='dashbord',role='DGM/PO')

# Indicative rule added             
@app.route('/TM_2_6', methods=['GET', 'POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def TM_2_6():
    if request.method == 'POST':
        userEmail = session['email_id']
        notify = notification(userEmail)
        if 'download' in request.form:
            user_input_date_str = '2021-10-20'  
        elif 'user_input_date_str' in request.form:
            user_input_date_str = request.form.get('user_input_date_str')
        else:
            
            user_input_date_str = '2021-10-20'

        user_input_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')

        current_values = threshold_values_from_col(TM_collection,'TM_2_6')
    
        total_df = pd.DataFrame()


        start_date = user_input_date-timedelta(days=30)

        pipeline = [
            {
                "$unwind": "$TXNDATA"
            },
            {
                "$match": {
                    "TXNDATA.Transaction Type": "Non-cash",
                    "TXNDATA.Transaction Date": {"$lte": user_input_date,
                                                "$gte":start_date},
                    "TXNDATA.Transaction Currency": "INR",
                    "TXNDATA.PAN": { "$nin": ["Yes"]}
                }
            },
            {
                "$group": {
                    "_id": "$TXNDATA.Account Number",
                    "data": {"$push": "$TXNDATA"}
                }
            }
        ]

        agg_result = list(txn_collection.aggregate(pipeline))

        data_from_col_df = pd.DataFrame()
        for doc in agg_result:

            data_from_col_df = pd.concat([data_from_col_df, pd.DataFrame(doc['data'])])
        if not data_from_col_df.empty:
            individual_values = data_from_col_df[data_from_col_df['Nature of account'] == 'Individual']

            df_grp = individual_values.groupby('Account Number')
            for gpname, gpdata in df_grp:
                if not gpdata.empty:
                    sum_df = pd.DataFrame({
                        'Transaction Amount': [gpdata['Transaction Amount'].sum()],
                        'Account Number': [gpname],
                        'Nature of account':gpdata['Nature of account'].unique(),
                        'Customer Profile':gpdata['Customer Profile'].unique(),
                        'From Transaction Date':[gpdata['Transaction Date'].unique()[0]],
                        'To Transaction Date':[gpdata['Transaction Date'].unique()[-1]]
                    })
                    filtered_df = sum_df[sum_df['Transaction Amount'] >= current_values['X1']]
                    if not filtered_df.empty:
                        total_df = pd.concat([total_df,filtered_df])
        if not total_df.empty:
            def generate_indicative_rule(row):
                return f"High value non-cash transaction made by {row['Account Number']} aggregating to or more than {current_values['X1']} in a month without PAN has triggered one of the RFI and raised an alert for a month triggered between dates {row['From Transaction Date']} and {row['To Transaction Date']}, {row['Account Number']} being an {row['Nature of account']} and {row['Customer Profile']} account has made transactions which aggregated to a total of {row['Transaction Amount']} from {row['From Transaction Date']}"    
            total_df['Indicative_rule'] = total_df.apply(generate_indicative_rule, axis=1)
        total_df=total_df.dropna(axis=1)
        if 'download' in request.form:
           
            excel_buffer = io.BytesIO()

            # Create an ExcelWriter object to write multiple DataFrames to different sheets
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                total_df.to_excel(writer, sheet_name='Individuals', index=False)

            # Set the position of the BytesIO object to the beginning
            excel_buffer.seek(0)

            # Generate the response to download the Excel file
            response = make_response(excel_buffer.read())
            response.headers["Content-Disposition"] = "attachment filename=TM_2_6_data.xlsx"
            response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            return response


        tm_sub_hedding="TM 2.6"
        document =TM_collection.find_one({"code":"TM_2_6"})
        tm_heading = document.get("Alert_title","")
        if returning_data_enabled:
                return [total_df]
        else:
            if session["user_role"]=="DGM/PO":
                return render_template("display_data.html",notify=notify,Individual_df=total_df,
                                    
                                    tm_heading=tm_heading,
                                tm_sub_hedding=tm_sub_hedding,dgmuser=image(),type='dashbord',role='DGM/PO')


# Added in the query code -- Need to add here
@app.route('/TM_3_1', methods=['GET', 'POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def TM_3_1():
    if request.method == 'POST':
        userEmail = session['email_id']
        notify = notification(userEmail)
        if 'download' in request.form:
            user_input_date_str = '2021-10-10'
        elif 'user_input_date_str' in request.form:
            user_input_date_str = request.form.get('user_input_date_str')
        else:
            user_input_date_str = '2021-10-10'
        end_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')
        current_values = threshold_values_from_col(TM_collection,'TM_3_1')
        start_date = end_date - timedelta(days=current_values['Y'])
        pipeline_first = [
            {"$unwind": "$TXNDATA"},
            {
                "$match": {
                    "TXNDATA.Transaction Date": {
                        "$gte": start_date,
                        "$lte": end_date - timedelta(days=30)
                    },
                    "TXNDATA.Transaction Currency": "INR"
                }
            },
            {
                "$group": {
                    "_id": "$TXNDATA.Account Number",
                    "data": {"$push": "$TXNDATA"}
                }
            }
        ]
        # Aggregate the data from MongoDB for the first pipeline
        agg_result = list(txn_collection.aggregate(pipeline_first))
        total_df_list = []
        # Process aggregated data from the first pipeline
        for doc in agg_result:
            df_from_transaction = pd.DataFrame(doc['data'])
            if not df_from_transaction.empty:
                number = df_from_transaction['Transaction Amount'].max()
                # Define the second pipeline for aggregation
                pipeline_second = [
                    {"$unwind": "$TXNDATA"},
                    {
                        "$match": {
                            "TXNDATA.Transaction Date": {
                                "$gt": end_date - timedelta(days=30),
                                "$lte": end_date
                            },
                            "TXNDATA.Account Number": doc['_id']
                        }
                    },
                    {
                        "$group": {
                            "_id": "$TXNDATA.Account Number",
                            "data": {"$push": "$TXNDATA"}
                        }
                    }
                ]
                # Aggregate the data from MongoDB for the second pipeline
                agg_result1 = list(txn_collection.aggregate(pipeline_second))
                if agg_result1:  # Check if the list is not empty
                    # Convert the list of dictionaries directly to a DataFrame
                    df_each_month = pd.DataFrame(agg_result1[0]['data'])
                    if not df_each_month.empty:
                        df_amount = df_each_month[df_each_month["Transaction Amount"] >= current_values['X']]
                        if not df_amount.empty:
                            for val in df_amount['Transaction Amount']:
                                percentage = ((val - number) / number) * 100
                                if percentage >= current_values['Z']:
                                    df = pd.DataFrame({
                                        "Percentage": [percentage],
                                        "Transaction Amount more than 2L": [val],
                                        "Highest Transaction Amount in last 3 months": [number],
                                        "Account Number": df_amount.loc[df_amount['Transaction Amount'] == val, 'Account Number'].values[0],
                                    })
                                    total_df_list.append(df)
        # Concatenate all DataFrames in the list
        if total_df_list:
            print("Data processing completed.")
            total_df = pd.concat(total_df_list, ignore_index=True)
            def generate_indicative_rule(row):
                return f"Value of transaction made by {row['Account Number']} triggered one of the RFI, where {row['Account Number']} made more than {current_values['X']} which is {row['Transaction Amount more than 2L']} and with percentage of {row['Percentage']} which is more than {current_values['Z']} percent of the previous largest transaction which is {row['Highest Transaction Amount in last 3 months']} for the client in previous 3 months"
            total_df['Indicative_rule'] = total_df.apply(generate_indicative_rule, axis=1)
        total_df=total_df.dropna(axis=1)
        if 'download' in request.form:
                excel_buffer = io.BytesIO()
                # Create an ExcelWriter object to write multiple DataFrames to different sheets
                with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                    total_df.to_excel(writer, sheet_name='totaldata', index=False)
                    # total_df_non.to_excel(writer, sheet_name='Non-Individuals', index=False)
                # Set the position of the BytesIO object to the beginning
                excel_buffer.seek(0)
                # Generate the response to download the Excel file
                response = make_response(excel_buffer.read())
                response.headers["Content-Disposition"] = "attachment filename=TM_3_1_data.xlsx"
                response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                return response
        tm_sub_hedding="TM 3.1"
        document =TM_collection.find_one({"code":"TM_3_1"})
        tm_heading = document.get("Alert_title","")
        if returning_data_enabled:
            return [total_df]
        else:
            if session["user_role"]=="DGM/PO":
                return render_template("display_data.html",notify=notify,Individual_df=total_df,
                                 tm_heading=tm_heading,
                            tm_sub_hedding=tm_sub_hedding,dgmuser=image(),type='dashbord',role='DGM/PO')
# Indicative rule added
@app.route('/TM_3_2',  methods=['GET', 'POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def TM_3_2():
    if request.method == 'POST':
        userEmail = session['email_id']
        notify = notification(userEmail)
        if 'download' in request.form:
            user_input_date_str = '2021-10-20'  
        elif 'user_input_date_str' in request.form:
            user_input_date_str = request.form.get('user_input_date_str')
        else:
            # user_input_date_str = request.form['user_entered_date_tm_3_2']
            user_input_date_str = '2021-10-20'
        

        end_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')
        current_values = threshold_values_from_col(TM_collection,'TM_3_2')

        total_df = pd.DataFrame()
        # Calculate start date (30 days before end date)
        start_date = end_date - timedelta(days=120)
        start_date_30_days = end_date - timedelta(days=30)


        print("start_date : ",start_date, "start_date_30_days : ",start_date_30_days)
        data_from_col_for_largest_transaction = txn_collection.aggregate([
            {
                "$unwind":"$TXNDATA"
            },
            {
        "$match": {
            "$and": [
                {
                    "TXNDATA.Transaction Date": {
                        "$gte": start_date,
                        "$lte": start_date_30_days
                    }
                },
                {
                    "TXNDATA.Transaction Currency": "INR"
                }
            ]
        }
        }      
        ])

        df_from_transaction = pd.DataFrame(data_from_col_for_largest_transaction)
        
        df_from_transaction['Transaction Amount'] = df_from_transaction['TXNDATA'].apply(lambda x: x.get('Transaction Amount') if x else None)
        p = df_from_transaction[['Transaction Amount', 'Account Number']]

        g=(p.groupby('Account Number')['Transaction Amount'].sum())/3
        f = pd.DataFrame(g)
        f = f.reset_index()
        f = f.rename(columns={'Transaction Amount': 'Transaction_Amount_quarter'})
        f['Transaction_Amount_quarter'] = f['Transaction_Amount_quarter'].astype(int)

        if not df_from_transaction.empty:
                print("data_from_col_for_largest_transaction : ",df_from_transaction)
                data_from = txn_collection.aggregate([
            {
                "$unwind":"$TXNDATA"
            },
            {
        "$match": {
            "$and": [
                {
                    "TXNDATA.Transaction Date": {
                        "$gte": start_date,
                        "$lte": start_date_30_days
                    }
                },
                {
                    "TXNDATA.Transaction Currency": "INR"
                }
            ]
        }
        }      
        ])
                
        df_each_month = pd.DataFrame(data_from)
        print("df_each_month : ",df_each_month)
        df_each_month['Transaction Amount'] = df_each_month['TXNDATA'].apply(lambda x: x.get('Transaction Amount') if x else None)
        ff = df_each_month[['Account Number','Transaction Amount']]

        if not ff.empty:
            p = ff.groupby('Account Number')['Transaction Amount'].sum()
            
            v = pd.DataFrame(p)
            v = v.reset_index()
            m = v[v['Transaction Amount'] > current_values['X']]
        #     # Merge the DataFrames
        merged_df_outer = pd.merge(f, m, on='Account Number', how='inner')
        merged_df_outer['percentage'] = ((merged_df_outer['Transaction Amount']-merged_df_outer['Transaction_Amount_quarter'])/merged_df_outer['Transaction_Amount_quarter']*100)
        h = merged_df_outer[merged_df_outer['percentage']>current_values['Z']]
        h=h.dropna(axis=1)
        
        # file_path = "TM 3.2.xlsx"
        # h.to_excel(file_path, index=False)

        # print(f"Excel file saved to: {file_path}")
        if not h.empty:
            def generate_indicative_rule(row):
                return (
                f"Customers monthly account turnover more than INR {current_values['X']} aggregated has {row['Transaction Amount']} exceeds the monthly average of account turnover aggregated has {row['Transaction_Amount_quarter']} for the preceding quarter by {current_values['Z']} percent or more aggregated has {row['percentage']} triggered one of the RFI and raised an alert with Account Number {row['Account Number']}"
            )
            h['Indicative_rule'] = h.apply(generate_indicative_rule, axis=1)


        if 'download' in request.form:
           
                excel_buffer = io.BytesIO()

                # Create an ExcelWriter object to write multiple DataFrames to different sheets
                with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                    h.to_excel(writer, sheet_name='totaldata', index=False)
                    # total_df_non.to_excel(writer, sheet_name='Non-Individuals', index=False)

                # Set the position of the BytesIO object to the beginning
                excel_buffer.seek(0)

                # Generate the response to download the Excel file
                response = make_response(excel_buffer.read())
                response.headers["Content-Disposition"] = "attachment filename=TM_3_2_data.xlsx"
                response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                return response
                
        tm_sub_hedding="TM 3.2"
        document =TM_collection.find_one({"code":"TM_3_2"})
        tm_heading = document.get("Alert_title","")
        if returning_data_enabled:

            return [h]
        else:
            if session["user_role"]=="DGM/PO":
        
                return render_template("display_data.html",notify=notify,Individual_df=total_df,
                                 tm_heading=tm_heading,
                            tm_sub_hedding=tm_sub_hedding,dgmuser=image(),type='dashbord',role='DGM/PO')
            
@app.route('/TM_3_3',  methods=['GET', 'POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def TM_3_3():
    if request.method == 'POST':
        userEmail = session['email_id']
        notify = notification(userEmail)
        if 'download' in request.form:
            user_input_date_str = '2021-10-20'  
        elif 'user_input_date_str' in request.form:
            user_input_date_str = request.form.get('user_input_date_str')
        else:
            user_input_date_str = '2021-10-20'
        end_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')
        current_values = threshold_values_from_col(TM_collection,'TM_3_3')


        total_df = pd.DataFrame()
        # Calculate start date (30 days before end date)
        start_date = end_date - timedelta(days=120)
        start_date_30_days = end_date - timedelta(days=30)
        data_from_col_for_largest_transaction = txn_collection.aggregate([
        {
            "$unwind":"$TXNDATA"
        },
        {
            "$match": {
                "$and": [
                    {
                        "TXNDATA.Transaction Date": {
                            "$gte": start_date,
                            "$lte": start_date_30_days
                        }
                    },
                    {
                        "TXNDATA.Transaction Currency": "INR"
                    }
                ]
            }
        }      
        ])
        df_from_transaction = pd.DataFrame(data_from_col_for_largest_transaction)
        df_from_transaction['Transaction Amount'] = df_from_transaction['TXNDATA'].apply(lambda x: x.get('Transaction Amount') if x else None)
        p = df_from_transaction[['Transaction Amount', 'Account Number']]

        g = p.groupby('Account Number')['Transaction Amount'].agg(['count', 'sum']).reset_index()
        g['count'] = g['count'] / 3
        g['sum'] = g['sum']/3
        g = g.rename(columns={'count': 'Avg No of transactions in preceeding quarter', 'sum': 'Transaction_Amount_quarter'})
        f = pd.DataFrame(g)
        f['Transaction_Amount_quarter'] = f['Transaction_Amount_quarter'].astype(int)

        if not f.empty:
                data_from = txn_collection.aggregate([
            {
                "$unwind":"$TXNDATA"
            },
            {
        "$match": {
            "$and": [
                {
                    "TXNDATA.Transaction Date": {
                        "$gte": start_date,
                        "$lte": start_date_30_days
                    }
                },
                {
                    "TXNDATA.Transaction Currency": "INR"
                }
            ]
        }
        }      
        ])
                
        df_each_month = pd.DataFrame(data_from)
        df_each_month['Transaction Amount'] = df_each_month['TXNDATA'].apply(lambda x: x.get('Transaction Amount') if x else None)
        ff = df_each_month[['Account Number','Transaction Amount']]



        if not ff.empty:
            h = p.groupby('Account Number')['Transaction Amount'].agg(['sum', 'size']).reset_index()
            h = h.rename(columns={'sum': 'Transaction_Amount_Month', 'size': 'num_transactions_in_month'})

            v = pd.DataFrame(h)
            v = v[v['Transaction_Amount_Month']>current_values['X']]
            merged_df_outer=  pd.merge(f, v, on='Account Number', how='inner')
            merged_df_outer['percentage'] = ((merged_df_outer["num_transactions_in_month"].astype(int) - 
            merged_df_outer["Avg No of transactions in preceeding quarter"].astype(int)) /merged_df_outer["Avg No of transactions in preceeding quarter"].astype(int)) * 100
            # Round the 'percentage' column to 2 decimal places
            merged_df_outer["percentage"] = merged_df_outer["percentage"].round(2)

        # based on the condition
        i = merged_df_outer[merged_df_outer['percentage'] > current_values['Z']]

        # Select columns of interest
        i = i[['percentage', 'num_transactions_in_month', 'Avg No of transactions in preceeding quarter', 'Account Number']]
        if not i.empty:
            def generate_indicative_rule(row):
                return (
                f"Customers monthly account activity more than INR {current_values['X']} (total number of debit and credit transactions in a month) aggregated has {row['num_transactions_in_month']} exceeds the monthly average of account activity aggregated has {row['Avg No of transactions in preceeding quarter']} for the preceding quarter by {current_values['Z']} percent or more aggregated has {row['percentage']} triggered one of the RFI and raised an alert with Account Number {row['Account Number']}"
            )
            i['Indicative_rule'] = i.apply(generate_indicative_rule, axis=1)
        i=i.dropna(axis=1)

        if 'download' in request.form:
           
                excel_buffer = io.BytesIO()

                # Create an ExcelWriter object to write multiple DataFrames to different sheets
                with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                    i.to_excel(writer, sheet_name='totaldata', index=False)
                    # total_df_non.to_excel(writer, sheet_name='Non-Individuals', index=False)

                # Set the position of the BytesIO object to the beginning
                excel_buffer.seek(0)

                # Generate the response to download the Excel file
                response = make_response(excel_buffer.read())
                response.headers["Content-Disposition"] = "attachment filename=TM_3_3_data.xlsx"
                response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                return response
                
                
        tm_sub_hedding="TM 3.3"
        document =TM_collection.find_one({"code":"TM_3_3"})
        tm_heading = document.get("Alert_title","")
        if returning_data_enabled:

                return [i]
        else:
            if session["user_role"]=="DGM/PO":
                return render_template("display_data.html",notify=notify,i=i,
                                  tm_heading=tm_heading,
                                   tm_sub_hedding=tm_sub_hedding,dgmuser=image(),type='dashbord',role='DGM/PO')
            
@app.route('/TM_3_4',  methods=['GET', 'POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def TM_3_4():
    if request.method == 'POST':
        userEmail = session['email_id']
        notify = notification(userEmail)
        if 'download' in request.form:
            user_input_date_str = '2021-10-20'  
        elif 'user_input_date_str' in request.form:
            user_input_date_str = request.form.get('user_input_date_str')
        else:
            # user_input_date_str = request.form['user_entered_date_tm_3_4']
            user_input_date_str = '2021-10-20'
        end_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')
        current_values = threshold_values_from_col(TM_collection,'TM_3_4')


        total_df = pd.DataFrame()
        # Calculate start date (30 days before end date)
        start_date = end_date - timedelta(days=120)
        start_date_30_days = end_date - timedelta(days=30)

        data_from_col_for_largest_transaction = txn_collection.aggregate([{"$unwind":"$TXNDATA"},
        {"$match" :{                                                    
        "TXNDATA.Transaction Date":{
            "$gte":start_date,
            "$lte":start_date_30_days
        },
        "TXNDATA.Transaction Currency":"INR",
        "TXNDATA.Transaction Category":"Deposits",
        "TXNDATA.Transaction Type":"Cash"
        }} ])
        df_from_transaction = pd.DataFrame(data_from_col_for_largest_transaction)
        df_from_transaction['Transaction Amount'] = df_from_transaction['TXNDATA'].apply(lambda x: x.get('Transaction Amount') if x else None)
        df_from_transaction = df_from_transaction[['Transaction Amount', 'Account Number']]

        g = df_from_transaction.groupby('Account Number')['Transaction Amount'].agg(['count', 'sum']).reset_index()
        g['count'] = g['count'] / 3
        g['sum'] = g['sum']/3
        g = g.rename(columns={'count': 'Avg No of transactions in preceeding quarter', 'sum': 'Transaction_Amount_quarter'})
        f = pd.DataFrame(g)
        f['Transaction_Amount_quarter'] = f['Transaction_Amount_quarter'].astype(int)

        print("df_from_transaction : ",df_from_transaction)

        if not df_from_transaction.empty:
            data_from = txn_collection.aggregate([{"$unwind":"$TXNDATA"},
        {"$match" :{                                                    
        "TXNDATA.Transaction Date":{
            "$gte":start_date,
            "$lte":start_date_30_days
        },
        "TXNDATA.Transaction Currency":"INR",
        "TXNDATA.Transaction Category":"Deposits",
        "TXNDATA.Transaction Type":"Cash"
        }} ])
        df_each_month = pd.DataFrame(data_from)
        print("df_each_month : ",df_each_month)
        df_each_month['Transaction Amount'] = df_each_month['TXNDATA'].apply(lambda x: x.get('Transaction Amount') if x else None)

        if not df_each_month.empty:
            h = df_each_month.groupby('Account Number')['Transaction Amount'].agg(['sum', 'size']).reset_index()
            h = h.rename(columns={'sum': 'Transaction_Amount_Month', 'size': 'num_transactions_in_month'})
            v = pd.DataFrame(h)
            v = v[v['Transaction_Amount_Month']>current_values['X']]
            v['Transaction_Amount_Month'] = v['Transaction_Amount_Month'].astype(int)

            merged_df_outer =  pd.merge(f, v, on='Account Number', how='inner')
            merged_df_outer['percentage'] = ((merged_df_outer["num_transactions_in_month"].astype(int) - 
            merged_df_outer["Avg No of transactions in preceeding quarter"].astype(int)) /merged_df_outer["Avg No of transactions in preceeding quarter"].astype(int)) * 100
            # Round the 'percentage' column to 2 decimal places
            merged_df_outer["percentage"] = merged_df_outer["percentage"].round(2)

        # based on the condition
        i = merged_df_outer[merged_df_outer['percentage'] > current_values['Z']]
        i = i[["Transaction_Amount_Month","Transaction_Amount_quarter","percentage","Account Number"]]

        # file_path = "TM_3.4.xlsx"
        # i.to_excel(file_path, index=False)
        if not i.empty:
            def generate_indicative_rule(row):
                    return (
                f"Cash deposits in client accounts aggregating to more than {current_values['X']} in a month aggregated has {row['Transaction_Amount_Month']} exceeds in a monthly average of cash deposits aggregated has {row['Transaction_Amount_quarter']} in the preceding quarter by {current_values['Z']} percent or more aggregated has {row['percentage']} triggered one of the RFI and raised an alert with Account Number {row['Account Number']}"
            )
            i['Indicative_rule'] = i.apply(generate_indicative_rule, axis=1)
        i=i.dropna(axis=1)
        # print(f"Excel file saved to: {file_path}")
        if 'download' in request.form:
           
                excel_buffer = io.BytesIO()

                # Create an ExcelWriter object to write multiple DataFrames to different sheets
                with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                    i.to_excel(writer, sheet_name='totaldata', index=False)
                    # total_df_non.to_excel(writer, sheet_name='Non-Individuals', index=False)

                # Set the position of the BytesIO object to the beginning
                excel_buffer.seek(0)

                # Generate the response to download the Excel file
                response = make_response(excel_buffer.read())
                response.headers["Content-Disposition"] = "attachment filename=TM_3_4_data.xlsx"
                response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                return response
                
        tm_sub_hedding="TM 3.4"
        document =TM_collection.find_one({"code":"TM_3_4"})
        tm_heading = document.get("Alert_title","")
        if returning_data_enabled:
                return [i]
        else:
            if session["user_role"]=="DGM/PO":
        
    
                return render_template("display_data.html",notify=notify,i=i,
                                  tm_heading=tm_heading,
                                   tm_sub_hedding=tm_sub_hedding,dgmuser=image(),type='dashbord',role='DGM/PO')
            

            
        # return render_template('tm3_data.html', total_df_3_4=total_df,
        #                             tm_heading=tm_heading,
        #                             tm_sub_hedding=tm_sub_hedding,
        #                         )

@app.route('/TM_3_5',methods=['GET','POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def TM_3_5():
        if request.method == 'POST':
            userEmail = session['email_id']
            notify = notification(userEmail)
            if 'download' in request.form:
                user_input_date_str = '2022-01-30'  
            elif 'user_input_date_str' in request.form:
                user_input_date_str = request.form.get('user_input_date_str')
            else:
                user_input_date_str = "2022-01-30"

            end_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')
            current_values = threshold_values_from_col(TM_collection,'TM_3_5')
            start_date = end_date-timedelta(days=current_values['Y'])

            pipeline = [
                            {
                                "$unwind": "$TXNDATA"
                            },
                            {
                                "$match": {
                                    "$and": [
                                        {"TXNDATA.Type of account": "Current Account"},
                                        {"TXNDATA.Nature of account": "Non Ind"},
                                        {
                                            "TXNDATA.Transaction Date": {
                                                "$gte": start_date,  # Assuming start_date is defined elsewhere
                                                "$lte": end_date    # Assuming end_date is defined elsewhere
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "$group": {
                                    "_id": "$TXNDATA.Account Number",
                                    "data": {"$push": "$TXNDATA"}
                                }
                            }
                        ]

            agg_result = txn_collection.aggregate(pipeline)

            data_from_col_df = pd.DataFrame()
            for doc in agg_result:
                data_from_col_df = pd.concat([data_from_col_df,pd.DataFrame(doc['data'])])


            ress = txn_collection.aggregate(pipeline)
            
            total_df = pd.DataFrame()
            for doc in ress:
                total_df = pd.concat([total_df,pd.DataFrame(doc['data'])])


            for doc in agg_result:
                total_df = pd.concat([total_df,pd.DataFrame(doc['data'])])

           

            if not data_from_col_df.empty:
                grouped_data = data_from_col_df.groupby('Account Number')
                for groupname,gdata in grouped_data:
                    print("gdata : ",gdata)
                    if len(gdata)>current_values['N']:
                        total_df = pd.concat([total_df,gdata])
            if not total_df.empty:
                columns_to_agg = [col for col in total_df.columns if col != 'Account Number']
                acc_num_dfs = total_df.groupby('Account Number')
                for gpname,gpdata in acc_num_dfs:
                    print("gpdata : ",gpdata)

                    total_df_new = gpdata.groupby('Account Number').agg({
                        col: 'first' if col != 'Transaction Amount' else 'sum' for col in columns_to_agg
                    }).reset_index()
                    def generate_indicative_rule(row):
                        transactions_list = ', '.join(map(str, gpdata['Transaction Amount']))
                        return f"{row['Account Number']} has triggered one of the RFI, {row['Account Number']} being an {row['Nature of account']} and {row['Customer Profile']} account has made {len(total_df)} number of transactions which is exceeding the count {current_values['N']} in Current Account, the aggregate value of the transactions made is {row['Transaction Amount']} whereas {transactions_list} is the list of the transactions made"    
                    total_df_new['Indicative_rule'] = total_df_new.apply(generate_indicative_rule, axis=1)
            total_df_new=total_df_new.dropna(axis=1)

            if 'download' in request.form:
           
                excel_buffer = io.BytesIO()

                # Create an ExcelWriter object to write multiple DataFrames to different sheets
                with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                    total_df.to_excel(writer, sheet_name='totaldata', index=False)
                    # total_df_non.to_excel(writer, sheet_name='Non-Individuals', index=False)

                # Set the position of the BytesIO object to the beginning
                excel_buffer.seek(0)

                # Generate the response to download the Excel file
                response = make_response(excel_buffer.read())
                response.headers["Content-Disposition"] = "attachment filename=TM_3_5_data.xlsx"
                response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                return response

            
            tm_sub_hedding="TM 3.5"
            document =TM_collection.find_one({"code":"TM_3_5"})
            tm_heading = document.get("Alert_title","")
            if returning_data_enabled:
                return [total_df_new]
            else:
                if session["user_role"]=="DGM/PO":
            
            
                    return render_template("display_data.html",notify=notify,total_df=total_df_new,
                                  tm_heading=tm_heading,
                                   tm_sub_hedding=tm_sub_hedding,dgmuser=image(),type='dashbord',role='DGM/PO')

# CHANGES          
@app.route('/TM_3_6',  methods=['GET', 'POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def TM_3_6():
    if request.method == 'POST':
        userEmail = session['email_id']
        notify = notification(userEmail)
        if 'download' in request.form:
            user_input_date_str = '2021-10-20'  
        elif 'user_input_date_str' in request.form:
            user_input_date_str = request.form.get('user_input_date_str')
        else:
            user_input_date_str = '2021-10-20'  
        end_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')
        current_values = threshold_values_from_col(TM_collection,'TM_3_6')

        total_df = pd.DataFrame()
        # Calculate start date (30 days before end date)
        start_date = end_date - timedelta(days=120)
        start_date_30_days = end_date - timedelta(days=30)

        data_from_col_for_largest_transaction = txn_collection.aggregate([
        {"$unwind":"$TXNDATA"},
        {"$match":{ "$and":[                                                           
            {"TXNDATA.Transaction Date":{
                "$gte":start_date,
                "$lte":start_date_30_days
            }},
            {"TXNDATA.Transaction Currency":"INR"},
            {"TXNDATA.Transaction Category":"Withdrawals"},
            {"TXNDATA.Transaction Type":"Cash"}
        ]
        }} ])
        df_from_transaction = pd.DataFrame(data_from_col_for_largest_transaction)
        df_from_transaction['Transaction Amount'] = df_from_transaction['TXNDATA'].apply(lambda x: x.get('Transaction Amount') if x else None)
        df_from_transaction = df_from_transaction[['Transaction Amount', 'Account Number']]

        g = df_from_transaction.groupby('Account Number')['Transaction Amount'].agg(['count', 'sum']).reset_index()
        g['count'] = g['count'] / 3
        g['sum'] = g['sum']/3
        g = g.rename(columns={'count': 'Avg No of transactions in preceeding quarter', 'sum': 'Transaction_Amount_quarter'})
        f = pd.DataFrame(g)
        f['Transaction_Amount_quarter'] = f['Transaction_Amount_quarter'].astype(int)

        if not df_from_transaction.empty:
            data_from = txn_collection.aggregate([
        {"$unwind":"$TXNDATA"},
        {"$match":{ "$and":[                                                           
            {"TXNDATA.Transaction Date":{
                "$gte":start_date,
                "$lte":start_date_30_days
            }},
            {"TXNDATA.Transaction Currency":"INR"},
            {"TXNDATA.Transaction Category":"Withdrawals"},
            {"TXNDATA.Transaction Type":"Cash"}
        ]
        }} ])
        df_each_month = pd.DataFrame(data_from)
        df_each_month['Transaction Amount'] = df_each_month['TXNDATA'].apply(lambda x: x.get('Transaction Amount') if x else None)
        if not df_each_month.empty:
            h = df_each_month.groupby('Account Number')['Transaction Amount'].agg(['sum', 'size']).reset_index()
            h = h.rename(columns={'sum': 'Transaction_Amount_Month', 'size': 'num_transactions_in_month'})

            v = pd.DataFrame(h)
            v = v[v['Transaction_Amount_Month']>current_values['X']]
            merged_df_outer =  pd.merge(f, v, on='Account Number', how='inner')
            merged_df_outer['percentage'] = ((merged_df_outer["num_transactions_in_month"].astype(int) - 
            merged_df_outer["Avg No of transactions in preceeding quarter"].astype(int)) /merged_df_outer["Avg No of transactions in preceeding quarter"].astype(int)) * 100
            # Round the 'percentage' column to 2 decimal places
            merged_df_outer["percentage"] = merged_df_outer["percentage"].round(2)

        # based on the condition
        i = merged_df_outer[merged_df_outer['percentage'] > current_values['Z']]

        # Select columns of interest
        i = i[['Transaction_Amount_Month',"Transaction_Amount_quarter",'percentage','Account Number']]
        i=i.dropna(axis=1)
        if not i.empty:
            def generate_indicative_rule(row):
                return (
                f"Cash withdrawls in client accounts aggregating to more than {current_values['X']} in a month aggregated has {row['Transaction_Amount_Month']} exceeds in a monthly average of cash withdrawls aggregated has {row['Transaction_Amount_quarter']} in the preceding quarter by {current_values['Z']} percent or more aggregated has {row['percentage']} triggered one of the RFI and raised an alert with Account Number {row['Account Number']}"
            )
            i['Indicative_rule'] = i.apply(generate_indicative_rule, axis=1)
        if 'download' in request.form:
           
                excel_buffer = io.BytesIO()

                # Create an ExcelWriter object to write multiple DataFrames to different sheets
                with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                    i.to_excel(writer, sheet_name='totaldata', index=False)
                    # total_df_non.to_excel(writer, sheet_name='Non-Individuals', index=False)

                # Set the position of the BytesIO object to the beginning
                excel_buffer.seek(0)

                # Generate the response to download the Excel file
                response = make_response(excel_buffer.read())
                response.headers["Content-Disposition"] = "attachment filename=TM_3_6_data.xlsx"
                response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                return response
                
        document =TM_collection.find_one({"code":"TM_3_6"})
        tm_heading = document.get("Alert_title","")
        tm_sub_hedding="TM 3.6"
        if returning_data_enabled:

            return [i]
        else:
            if session["user_role"]=="DGM/PO":
        
                return render_template("display_data.html",notify=notify,i=i,
                                  tm_heading=tm_heading,
                                   tm_sub_hedding=tm_sub_hedding,dgmuser=image(),type='dashbord',role='DGM/PO')
            
# CHANGES           
@app.route('/TM_4_1', methods=['GET', 'POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def TM_4_1():
    if request.method == "POST":
        userEmail = session['email_id']
        notify = notification(userEmail) 
        try:
            if 'download' in request.form:
                user_input_date_str = '2021-01-01'  
            elif 'user_input_date_str' in request.form:
                user_input_date_str = request.form.get('user_input_date_str')
            else:
                # user_date = request.form.get("user_entered_date_tm4_1") 
                user_input_date_str = '2021-01-01'  
            individual_df = pd.DataFrame()
            end_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')
            current_values = threshold_values_from_col(TM_collection,'TM_4_1')

            start_date = end_date - timedelta(days=90)

            previously_created_accounts = []
            pipeline = [
                {
                    "$unwind":"$TXNDATA"
                },
                {
                    "$match":{
                        "TXNDATA.Acc_Opening_Date": {"$gte": start_date, "$lte": end_date}
                    }
                },
                {
                    "$group":{
                        "_id":"$TXNDATA.Account Number",
                        "data":{"$push":"$TXNDATA"}
                    }
                }
            ]

            agg_result = list(txn_collection.aggregate(pipeline))
            data_from_col=pd.DataFrame()
            for doc in agg_result:
                data_from_col = pd.DataFrame(doc['data'])

                if not data_from_col.empty:
                    acc_open_date = pd.to_datetime(data_from_col["Acc_Opening_Date"].unique()[0])
                    end_transaction_date = acc_open_date+timedelta(days=current_values['Y'])
                    transaction_conditions = [
                        {
                            "$unwind":"$TXNDATA"
                        },
                        {
                            "$match":{
                                "TXNDATA.Acc_Opening_Date": acc_open_date,
                                "TXNDATA.Transaction Date": {"$gte": acc_open_date, "$lte": end_transaction_date},
                                "TXNDATA.Transaction Currency": "INR",
                                "TXNDATA.Account Number":doc['_id']
                            }
                        },
                        {
                            "$group":{
                                "_id":"$TXNDATA.Account Number",
                                "data":{"$push":"$TXNDATA"}
                            }
                        }
                    ]
                    agg_result1 = list(txn_collection.aggregate(transaction_conditions))
                    df_=pd.DataFrame()
                    for d in agg_result1:
                        df_ = pd.concat([df_, pd.DataFrame(d['data'])])
                    if not df_.empty:
                        total_transaction_amount = df_['Transaction Amount'].sum()
                        if total_transaction_amount >= current_values['X']:
                            previously_created_accounts.append({
                                'Transaction Amount': total_transaction_amount,
                                'Account Number': doc['_id'],
                                'Account opening date': acc_open_date,
                                'Transactions till': end_date
                            })
            # # Create a DataFrame from the results
            if previously_created_accounts:
                individual_df = pd.DataFrame(previously_created_accounts).drop_duplicates()
            else:
                individual_df = pd.DataFrame()
            individual_df=individual_df.dropna(axis=1)
            if not individual_df.empty:
                def generate_indicative_rule(row):
                    return f"Transactions greater than INR {current_values['X']} in newly opened account with Account Number {row['Account Number']} has triggered one of the RFI and raised an alert within {current_values['Y']} days starting from Account Opening Date {row['Account opening date']} untill {row['Transactions till']} with Transaction Amount of {row['Transaction Amount']}"
                individual_df['Indicative_rule'] = individual_df.apply(generate_indicative_rule, axis=1)
            # print("previously_created_accounts",previously_created_accounts)
            if 'download' in request.form:
           
                excel_buffer = io.BytesIO()

                # Create an ExcelWriter object to write multiple DataFrames to different sheets
                with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                    individual_df.to_excel(writer, sheet_name='totaldata', index=False)
                    # total_df_non.to_excel(writer, sheet_name='Non-Individuals', index=False)

                # Set the position of the BytesIO object to the beginning
                excel_buffer.seek(0)

                # Generate the response to download the Excel file
                response = make_response(excel_buffer.read())
                response.headers["Content-Disposition"] = "attachment filename=TM_4_1_data.xlsx"
                response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                return response
            
            tm_sub_hedding="TM.4.1"
            tm_heading=" New Account Transactions greater than INR [x] in newly opened account within [y] months "
            print("individual_df:")
            print(individual_df)
            # return render_template('tm4_data.html', individual_df_4_1=individual_df, tm_sub_hedding=tm_sub_hedding,
            #                tm_heading=tm_heading)
        

        except Exception as e:
           pass
        document =TM_collection.find_one({"code":"TM_4_1"})
        tm_heading = document.get("Alert_title","")
        tm_sub_hedding="TM 4.1"
        if returning_data_enabled:
            return [individual_df]
        else:
            if session["user_role"]=="DGM/PO":
        
                return render_template("display_data.html",notify=notify,total_df=individual_df,
                                  tm_heading=tm_heading,
                                   tm_sub_hedding=tm_sub_hedding,dgmuser=image(),type='dashbord',role='DGM/PO')
            

@app.route('/TM_4_2', methods=['GET', 'POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def TM_4_2():
    if request.method == "POST":
        userEmail = session['email_id']
        notify = notification(userEmail)
        if 'download' in request.form:
            user_input_date_str = '2021-01-01'
        elif 'user_input_date_str' in request.form:
            user_input_date_str = request.form.get('user_input_date_str')
        else:
            user_input_date_str = '2021-01-01'
        end_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')
        current_values = threshold_values_from_col(TM_collection,'TM_4_2')
        # Calculate start date (90 days before end date)
        start_date = end_date - timedelta(days=90)
        # Initialize a list to store results
        previously_created_accounts = []
        pipeline = [
            {
                "$unwind":"$TXNDATA"
            },
            {
                "$match":{
                    "TXNDATA.Acc_Opening_Date": {"$gte": start_date, "$lte": end_date}
                }
            },
            {
                "$group":{
                    "_id":"$TXNDATA.Account Number",
                    "data":{"$push":"$TXNDATA"}
                }
            }
        ]
        agg_result = list(txn_collection.aggregate(pipeline))
        data_from_col=pd.DataFrame()
        for doc in agg_result:
            data_from_col = pd.DataFrame(doc['data'])
            if not data_from_col.empty:
                acc_open_date = pd.to_datetime(data_from_col["Acc_Opening_Date"].unique()[0])
                end_transaction_date = acc_open_date+timedelta(days=current_values['Y'])
                transaction_conditions = [
                    {
                        "$unwind":"$TXNDATA"
                    },
                    {
                        "$match":{
                            "TXNDATA.Acc_Opening_Date": acc_open_date,
                            "TXNDATA.Transaction Date": {"$gte": acc_open_date, "$lte": end_transaction_date},
                            "TXNDATA.Transaction Currency": "INR",
                            "TXNDATA.Account Number":doc['_id']
                        }
                    },
                    {
                        "$group":{
                            "_id":"$TXNDATA.Account Number",
                            "data":{"$push":"$TXNDATA"}
                        }
                    }
                ]
                agg_result1 = list(txn_collection.aggregate(transaction_conditions))
                df_=pd.DataFrame()
                for d in agg_result1:
                    df_ = pd.concat([df_, pd.DataFrame(d['data'])])
                if not df_.empty:
                    if len(df_)>current_values['N']:
                        previously_created_accounts.append({
                            'Transaction Count': len(df_),
                            'Account Number': doc['_id'],
                            'Account Opening Date':acc_open_date
                        })
        # # Create a DataFrame from the results
        if previously_created_accounts:
            individual_df = pd.DataFrame(previously_created_accounts).drop_duplicates()
        else:
            individual_df = pd.DataFrame()
        individual_df=individual_df.dropna(axis=1)
        if not individual_df.empty:
            def generate_indicative_rule(row):
                return f"No.of Transactions which are more than {current_values['N']} in newly opened account with Account Number {row['Account Number']} has triggered one of the RFI and raised an alert  within {current_values['Y']} days starting from the Account Opening Date {row['Account Opening Date']}  have a Transaction count of {row['Transaction Count']}."
            individual_df['Indicative_rule'] = individual_df.apply(generate_indicative_rule, axis=1)
        if 'download' in request.form:
            excel_buffer = io.BytesIO()
            # Create an ExcelWriter object to write multiple DataFrames to different sheets
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                individual_df.to_excel(writer, sheet_name='totaldata', index=False)
                # total_df_non.to_excel(writer, sheet_name='Non-Individuals', index=False)
            # Set the position of the BytesIO object to the beginning
            excel_buffer.seek(0)
            # Generate the response to download the Excel file
            response = make_response(excel_buffer.read())
            response.headers["Content-Disposition"] = "attachment filename=TM_4_2_data.xlsx"
            response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            return response
        tm_sub_hedding="TM 4.2"
        document =TM_collection.find_one({"code":"TM_4_2"})
        tm_heading = document.get("Alert_title","")
        if returning_data_enabled:
            return [individual_df]
        else:
            if session["user_role"]=="DGM/PO":
                return render_template("display_data.html",notify=notify,total_df=individual_df,
                                  tm_heading=tm_heading,
                                   tm_sub_hedding=tm_sub_hedding,dgmuser=image(),type='dashbord',role='DGM/PO')

@app.route('/TM_6_1', methods=['GET', 'POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def TM_6_1():
    if request.method == "POST":
        userEmail = session['email_id']
        notify = notification(userEmail)
        if 'download' in request.form:
            user_input_date_str = '2021-10-20'  
        elif 'user_input_date_str' in request.form:
            user_input_date_str = request.form.get('user_input_date_str')
        else:
            user_input_date_str = "2021-10-20"
        current_values = threshold_values_from_col(TM_collection,'TM_6_1')
        total_df = pd.DataFrame()
        total_df_non = pd.DataFrame()
        end_date = datetime.strptime(user_input_date_str,  '%Y-%m-%d')
        current_values = threshold_values_from_col(TM_collection,'TM_6_1')

        start_date = end_date-timedelta(days=30)
        pipeline = [
            {
                "$unwind": "$TXNDATA"
            },
            {
                "$match": {
                    "TXNDATA.Transaction Type": "Cash",
                    "TXNDATA.Transaction Date": {"$gte": start_date,"$lte":end_date},
                    "TXNDATA.Transaction Currency": "INR",
                    "TXNDATA.Customer Profile": {
                        "$in": ["Student", "Pensioner", "Housewife", "Wages", "Salary Person", "Minor"]
                    }
                }
            },
            {
                "$group": {
                    "_id": "$TXNDATA.Account Number",
                    "data": {"$push": "$TXNDATA"}
                }
            }
        ]

        agg_result = list(txn_collection.aggregate(pipeline))

        data_from_col_df = pd.DataFrame()
        for doc in agg_result:
            data_from_col_df = pd.concat([data_from_col_df, pd.DataFrame(doc['data'])])

        if not data_from_col_df.empty:
            grpedata = data_from_col_df.groupby('Account Number')
            for gname,gdata in grpedata:
                ind_category_data = gdata[gdata['Nature of account'] == "Individual"]
                if not ind_category_data.empty:
                    sum_df = pd.DataFrame({
                        'Transaction Amount': [ind_category_data['Transaction Amount'].sum()],
                        'Account Number': [gname],
                        'Customer Profile': [ind_category_data.loc[0, 'Customer Profile']],
                        'Month': [calendar.month_name[ind_category_data['Transaction Date'].dt.month.unique()[0]]]
                    })
                    filtered_df = sum_df[sum_df['Transaction Amount'] >= current_values['IND']]
                    if not filtered_df.empty:
                        total_df = pd.concat([total_df, filtered_df])
                ind_category_data = gdata[gdata['Nature of account'] == "Non Ind"]
                if not ind_category_data.empty:
                    sum_df = pd.DataFrame({
                        'Transaction Amount': [ind_category_data['Transaction Amount'].sum()],
                        'Account Number': [gname],
                        'Customer Profile': [ind_category_data.loc[0, 'Customer Profile']],
                        'Month': [calendar.month_name[ind_category_data['Transaction Date'].dt.month.unique()[0]]]
                    })
                    filtered_df = sum_df[sum_df['Transaction Amount'] >= current_values['NON_IND']]
                    if not filtered_df.empty:
                        total_df_non = pd.concat([total_df_non, filtered_df])

        if not total_df.empty:
            # Pivot for 'Individual' accounts with 'Customer Profile'
            pivot_df = total_df.pivot(index='Account Number', columns='Month', values='Transaction Amount').reset_index()
            pivot_df['Sum'] = pivot_df[pivot_df.columns[1:]].sum(axis=1)
            pivot_df = pivot_df.fillna(int(0))

            # Add 'Customer Profile' column to the pivot DataFrame
        #     pivot_df['Customer Profile'] = total_df['Customer Profile'].iloc[0]

        #     print(pivot_df['Sum'].sum())
        else:
            pivot_df = pd.DataFrame()

        if not total_df_non.empty:
            # Pivot for 'Non Individual' accounts with 'Customer Profile'
            pivot_df_non = total_df_non.pivot(index='Account Number', columns='Month', values='Transaction Amount').reset_index()
            pivot_df_non['Sum'] = pivot_df_non[pivot_df_non.columns[1:]].sum(axis=1)
            pivot_df_non = pivot_df_non.fillna(int(0))

            # Add 'Customer Profile' column to the pivot DataFrame
        #     print(pivot_df_non['Sum'].sum())
        else:
            pivot_df_non = pd.DataFrame()
        
        if 'download' in request.form:
                
                excel_buffer = io.BytesIO()

                # Create an ExcelWriter object to write multiple DataFrames to different sheets
                with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                    pivot_df.to_excel(writer, sheet_name='totaldata', index=False)
                    pivot_df_non.to_excel(writer, sheet_name='Non-Individuals', index=False)

                # Set the position of the BytesIO object to the beginning
                excel_buffer.seek(0)

                # Generate the response to download the Excel file
                response = make_response(excel_buffer.read())
                response.headers["Content-Disposition"] = "attachment filename=TM_6_1_data.xlsx"
                response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                return response
    
        
        tm_sub_hedding="TM 6.1"
        document =TM_collection.find_one({"code":"TM_6_1"})
        tm_heading = document.get("Alert_title","")
        if returning_data_enabled:
                return [pivot_df,pivot_df_non]
        else:
            if session["user_role"]=="DGM/PO":

                return render_template("display_data.html",notify=notify,pivot_df=pivot_df,
                                    pivot_df_non=pivot_df_non,
                                    tm_heading=tm_heading,
                                tm_sub_hedding=tm_sub_hedding,dgmuser=image(),type='dashbord',role='DGM/PO')

# CHANGES
@app.route("/TM_6_2",methods=['GET','POST'])
def TM_6_2():
    if request.method == 'POST':
        userEmail = session['email_id']
        notify = notification(userEmail)
        if 'download' in request.form:
            user_input_date_str = '2021-10-10'  
        elif 'user_input_date_str' in request.form:
            user_input_date_str = request.form.get('user_input_date_str')
        else:
            user_input_date_str ="2021-10-10"

        total_df = pd.DataFrame()
        total_df_non = pd.DataFrame()

        end_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')
        current_values = threshold_values_from_col(TM_collection,'TM_6_2')


        start_date = end_date-timedelta(days=30)
        pipeline = [
            {
                "$unwind": "$TXNDATA"
            },
            {
                "$match": {
                    "TXNDATA.Transaction Type": "Cash",
                    "TXNDATA.Transaction Date": {"$gte": start_date,"$lte":end_date},
                    "TXNDATA.Transaction Currency": "INR",
                    "TXNDATA.Customer Profile": {
                        "$in": ["Student", "Pensioner", "Housewife", "Wages", "Salary Person", "Minor"]
                    }
                }
            },
            {
                "$group": {
                    "_id": "$TXNDATA.Account Number",
                    "data": {"$push": "$TXNDATA"}
                }
            }
        ]

        agg_result = list(txn_collection.aggregate(pipeline))

        data_from_col_df = pd.DataFrame()
        for doc in agg_result:
            data_from_col_df = pd.concat([data_from_col_df, pd.DataFrame(doc['data'])])

        if not data_from_col_df.empty:
            grpedata = data_from_col_df.groupby('Account Number')
            for gname,gdata in grpedata:
                ind_category_data = gdata[gdata['Nature of account'] == "Individual"]
                if not ind_category_data.empty and len(ind_category_data)>current_values['N']:
                    sum_df = pd.DataFrame({
                        'Transaction Amount': [ind_category_data['Transaction Amount'].sum()],
                        'Account Number': [gname],
                        'Customer Profile': [ind_category_data.loc[0, 'Customer Profile']],
                        'Transaction Count':[len(ind_category_data)],
                        'Month': [calendar.month_name[ind_category_data['Transaction Date'].dt.month.unique()[0]]]
                    })
                    filtered_df = sum_df[sum_df['Transaction Amount'] >= current_values['X']]
                    if not filtered_df.empty:
                        total_df = pd.concat([total_df, filtered_df])
        if not total_df.empty:
            def generate_indicative_rule(row):
                return (
                f"cash transactions with greater than or equal to {current_values['N']},aggregated has {row['Transaction Count']} and transaction amount greater than INR {current_values['X']},aggregated has {row['Transaction Amount']} has triggered one of the RFI and raised an alert in a month of {row['Month']} with customer profile has {row['Customer Profile']} with Account Number {row['Account Number']}"
            )
            total_df['Indicative_rule']= total_df.apply(generate_indicative_rule,axis=1)
                
        if 'download' in request.form:
           
                excel_buffer = io.BytesIO()

                # Create an ExcelWriter object to write multiple DataFrames to different sheets
                with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                    total_df.to_excel(writer, sheet_name='totaldata', index=False)
                    # total_df_non.to_excel(writer, sheet_name='Non-Individuals', index=False)

                # Set the position of the BytesIO object to the beginning
                excel_buffer.seek(0)

                # Generate the response to download the Excel file
                response = make_response(excel_buffer.read())
                response.headers["Content-Disposition"] = "attachment filename=TM_6_2_data.xlsx"
                response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                return response

        tm_sub_hedding="TM 6.2"
        document =TM_collection.find_one({"code":"TM_6_2"})
        tm_heading = document.get("Alert_title","")
        if returning_data_enabled:

                return [total_df]
        
        else:
            if session["user_role"]=="DGM/PO":
        
                return render_template("display_data.html",notify=notify,Individual_df=total_df,
                                    tm_heading=tm_heading,
                                tm_sub_hedding=tm_sub_hedding,dgmuser=image(),type='dashbord',role='DGM/PO')

# CHANGES
@app.route('/TM_8_1', methods=['GET', 'POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def TM_8_1():
   if request.method == 'POST':
        userEmail = session['email_id']
        notify = notification(userEmail)
        if 'download' in request.form:
            user_input_date_str = '2021-01-10'  
        elif 'user_input_date_str' in request.form:
            user_input_date_str = request.form.get('user_input_date_str')
        else:
            user_input_date_str = '2021-01-12'  
        end_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')
        current_values = threshold_values_from_col(TM_collection,'TM_8_1')


        start_date = end_date - timedelta(days=90)

        # Initialize lists to store results
        result_data = []

        # Set of excluded customer profiles
        pipeline = [
            {
                "$unwind":"$TXNDATA"
            },
            {
                "$match":{
                    "TXNDATA.Acc_Opening_Date": {"$gte": start_date, "$lte": end_date}
                }
            },
            {
                "$group":{
                    "_id":"$TXNDATA.Account Number",
                    "data":{"$push":"$TXNDATA"}
                }
            }
        ]

        agg_result = list(txn_collection.aggregate(pipeline))
        data_from_col_df=pd.DataFrame()
        for doc in agg_result:
            data_from_col_df = pd.DataFrame(doc['data'])
            if not data_from_col_df.empty:
                acc_open_date = pd.to_datetime(data_from_col_df["Acc_Opening_Date"].unique()[0])
                end_transaction_date = acc_open_date + timedelta(days=current_values['Y'])

                # Query conditions for transactions
                transaction_conditions = [
                    {
                        "$unwind":"$TXNDATA"
                    },
                    {
                        "$match":{
                            "TXNDATA.Acc_Opening_Date": acc_open_date,
                            "TXNDATA.Transaction Type":"Non-cash",
                            "TXNDATA.Transaction Date": {"$gte": acc_open_date, "$lte": end_transaction_date},
                            "TXNDATA.Transaction Currency": "Foreign Currency",
                            "TXNDATA.Transaction Category": "Withdrawals",
                            "TXNDATA.Account Number":doc['_id']
                        }
                    },
                    {
                        "$group":{
                            "_id":"$TXNDATA.Account Number",
                            "data":{"$push":"$TXNDATA"}
                        }
                    }
                ]
                agg_result1 = list(txn_collection.aggregate(transaction_conditions))
                transactions=pd.DataFrame()
                for d in agg_result1:
                    transactions = pd.concat([transactions, pd.DataFrame(d['data'])])

                if not transactions.empty:
                    total_transaction_amount = transactions['Transaction Amount'].sum()
                    if total_transaction_amount >= current_values['X']:
                        result_data.append({
                            "Transaction Amount gte 20k, 100 days account opening date": total_transaction_amount,
                            "Account Number": doc['_id'],
                            "Transaction Type":transactions["Transaction Type"].unique()[0],
                            "Transaction Currency": "Foreign Currency",
                            "Transaction Category": "Withdrawals"
                        })

        # Create a DataFrame from the collected data
        total_df = pd.DataFrame(result_data)

        # Drop duplicates based on all columns
        total_df = total_df.drop_duplicates()
        if not total_df.empty:
            def generate_indicative_rule(row):
                return f"{row['Transaction Type']} {row['Transaction Currency']} transactions greater than {current_values['X']}, {row['Transaction Amount gte 20k, 100 days account opening date']} after {current_values['Y']} days of account opening has triggered one of the RFI, and an alert has been raised with Account Number {row['Account Number']}."
            
            total_df['Indicative_rule'] = total_df.apply(generate_indicative_rule, axis=1)

        
        print(total_df)

        if 'download' in request.form:
           
                excel_buffer = io.BytesIO()

                # Create an ExcelWriter object to write multiple DataFrames to different sheets
                with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                    total_df.to_excel(writer, sheet_name='totaldata', index=False)
                    # total_df_non.to_excel(writer, sheet_name='Non-Individuals', index=False)

                # Set the position of the BytesIO object to the beginning
                excel_buffer.seek(0)

                # Generate the response to download the Excel file
                response = make_response(excel_buffer.read())
                response.headers["Content-Disposition"] = "attachment filename=TM_8_1_data.xlsx"
                response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                return response
            
        tm_sub_hedding="TM 8.1"
        document =TM_collection.find_one({"code":"TM_8_1"})
        tm_heading = document.get("Alert_title","")
        if returning_data_enabled:
                return [total_df]
        else:
            if session["user_role"]=="DGM/PO":
        
                return render_template("display_data.html",notify=notify,total_df=total_df,
                                    tm_heading=tm_heading,
                                tm_sub_hedding=tm_sub_hedding,dgmuser=image(),type='dashbord',role='DGM/PO')
            
# CHANGES
@app.route('/TM_8_2', methods=['GET', 'POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def TM_8_2():
   if request.method == 'POST':
        userEmail = session['email_id']
        notify = notification(userEmail)
        if 'download' in request.form:
            user_input_date_str = '2021-10-20'  
        elif 'user_input_date_str' in request.form:
            user_input_date_str = request.form.get('user_input_date_str')
        else:
            # user_input_date_str = request.form['user_entered_date_tm_8_2']
            user_input_date_str = '2021-10-20'  
        end_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')
        current_values = threshold_values_from_col(TM_collection,'TM_8_2')


        # Calculate start date (15 days before end date)
        start_date = end_date - timedelta(current_values['Y'])
        total_df = pd.DataFrame()
        
        print("start_date : ",start_date,"end_date : ",end_date)
        data_from_col = txn_collection.aggregate([
        {
            "$unwind": "$TXNDATA"
        },
        {
            "$match": {
            "TXNDATA.Transaction Type":"Non-cash",
            "TXNDATA.Transaction Currency":"Foreign Currency",
            "TXNDATA.Transaction Category":"Withdrawals",
            "TXNDATA.Transaction Date":{
                "$gte":start_date,
                "$lte":end_date
            }
        }}])
        df = pd.DataFrame(data_from_col)
        print(" df : ",df)
        df['Transaction Amount'] = df['TXNDATA'].apply(lambda x: x.get('Transaction Amount') if x else None)
        if not df.empty:
            g = df.groupby('Account Number')['Transaction Amount'].sum()
            h = pd.DataFrame(g)
            h = h.reset_index()
            b = h[h['Transaction Amount']>current_values['X']]
            if not b.empty:
                total_df = pd.concat([total_df,b])
            
        if not total_df.empty:
            def generate_indicative_rule(row):
                return (f"Outward foreign remittance greater than {current_values['X']} aggregated has,{row['Transaction Amount']} has triggered one of the RFI and raised an alert in {current_values['Y']} days with Account Number {row['Account Number']}")
            total_df['Indicative_rule'] = total_df.apply(generate_indicative_rule, axis=1)

        if 'download' in request.form:
           
                excel_buffer = io.BytesIO()

                # Create an ExcelWriter object to write multiple DataFrames to different sheets
                with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                    total_df.to_excel(writer, sheet_name='totaldata', index=False)
                    # total_df_non.to_excel(writer, sheet_name='Non-Individuals', index=False)

                # Set the position of the BytesIO object to the beginning
                excel_buffer.seek(0)

                # Generate the response to download the Excel file
                response = make_response(excel_buffer.read())
                response.headers["Content-Disposition"] = "attachment filename=TM_8_2_data.xlsx"
                response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                return response
            
        tm_sub_hedding="TM 8.2"
        document =TM_collection.find_one({"code":"TM_8_2"})
        tm_heading = document.get("Alert_title","")
        if returning_data_enabled:
            return [total_df]
        else:
            if session["user_role"]=="DGM/PO":
        
                return render_template("display_data.html",notify=notify,Individual_df=total_df,
                                 tm_heading=tm_heading,
                            tm_sub_hedding=tm_sub_hedding,dgmuser=image(),type='dashbord',role='DGM/PO')
            
# CHANGES
@app.route('/TM_8_3', methods=['GET', 'POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def TM_8_3():
    if request.method == 'POST':
        userEmail = session['email_id']
        notify = notification(userEmail)
        total_df = pd.DataFrame()
        total_result_df = pd.DataFrame()

        pipeline_deposit = [
        {"$unwind": "$TXNDATA"},
        {"$match": {"TXNDATA.Transaction Type": "Cash", "TXNDATA.Transaction Category": "Deposits"}},
        {"$group": {"_id": "$TXNDATA.Account Number", "data": {"$push": "$TXNDATA"}}}
    ]

        total_result_df=pd.DataFrame()
        total_df = pd.DataFrame()
        agg_result_deposit = list(txn_collection.aggregate(pipeline_deposit))
        data_from_col_df = pd.concat([pd.DataFrame(doc['data']) for doc in agg_result_deposit], ignore_index=True)

        if not data_from_col_df.empty:
            result_df = data_from_col_df.groupby(['Account Number', 'Transaction Date'])['Transaction Amount'].sum().reset_index()
            result_df = result_df[result_df['Transaction Amount'] > 200000]

            for index, row in result_df.iterrows():
                date = pd.to_datetime(row['Transaction Date'])
                new_date = date + timedelta(days=6)

                pipeline_withdrawal = [
                    {"$unwind": "$TXNDATA"},
                    {"$match": {
                        "TXNDATA.Transaction Type": "Non-cash",
                        "TXNDATA.Transaction Currency": "Foreign Currency",
                        "TXNDATA.Transaction Category": "Withdrawals",
                        "TXNDATA.Transaction Date": {"$gte": date, "$lte": new_date},
                        "TXNDATA.Account Number": row['Account Number']
                    }},
                    {"$group": {"_id": "$TXNDATA.Account Number", "data": {"$push": "$TXNDATA"}}}
                ]

                agg_result_withdrawal = list(txn_collection.aggregate(pipeline_withdrawal))
                if agg_result_withdrawal:
                    df_data_for_foreign_or = pd.concat([pd.DataFrame(doc['data']) for doc in agg_result_withdrawal], ignore_index=True)

                    if not df_data_for_foreign_or.empty:
                        per_value = (row['Transaction Amount'] * 30) / 100
                        df_filtered = result_df[(result_df['Transaction Date'] == row['Transaction Date']) & (result_df['Account Number'] == row['Account Number'])]

                        if not df_filtered.empty and df_data_for_foreign_or['Transaction Amount'].sum() > per_value:
                            total_result_df = pd.concat([total_result_df, df_filtered])
                            total_df = pd.concat([total_df, df_data_for_foreign_or])


        total_df = total_df[['Account Number', 'Transaction Date', 'Transaction Amount', 'Transaction Currency', 'Transaction Category']]
    
        print("total_df",total_df)
        print("total_result_df",total_result_df)
        if 'download' in request.form:
           
                excel_buffer = io.BytesIO()

                # Create an ExcelWriter object to write multiple DataFrames to different sheets
                with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                    total_df.to_excel(writer, sheet_name='totaldata', index=False)
                    total_result_df.to_excel(writer, sheet_name='total_result_df', index=False)
                    # total_df_non.to_excel(writer, sheet_name='Non-Individuals', index=False)

                # Set the position of the BytesIO object to the beginning
                excel_buffer.seek(0)

                # Generate the response to download the Excel file
                response = make_response(excel_buffer.read())
                response.headers["Content-Disposition"] = "attachment filename=TM_8_3_data.xlsx"
                response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                return response

        tm_sub_hedding="TM 8.3"
        document =TM_collection.find_one({"code":"TM_8_3"})
        tm_heading = document.get("Alert_title","")
        if returning_data_enabled:
        
            return [total_df,total_result_df]
        else:
            if session["user_role"]=="DGM/PO":
        
                return render_template("display_data.html",notify=notify,total_df=total_df,total_result_df=total_result_df,
                                    tm_heading=tm_heading,
                            tm_sub_hedding=tm_sub_hedding,dgmuser=image(),type='dashbord',role='DGM/PO')


                
        # return render_template('display_data.html', total_df_8_3=total_df,total_result_df_8_3=total_result_df,
        #                                 tm_heading=tm_heading,
        #                                 tm_sub_hedding=tm_sub_hedding,
        #                             )

# CHANGES
@app.route("/TM_9_1",methods=["GET","POST"])
def TM_9_1(): 
        if request.method == 'POST':
            userEmail = session['email_id']
            notify = notification(userEmail)
            if 'download' in request.form:
                user_input_date_str = '2022-01-30'  
            elif 'user_input_date_str' in request.form:
                user_input_date_str = request.form.get('user_input_date_str')
            else:
                user_input_date_str = '2022-01-30'
            current_values = threshold_values_from_col(TM_collection,'TM_9_1')         

            total_df = pd.DataFrame()

            end_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')

            start_date= end_date-timedelta(days=current_values['Y'])

            pipeline = [
                {
                    "$unwind": "$TXNDATA"
                },
                {
                    "$match": {
                        "TXNDATA.Transaction Currency":"INR",
                        "TXNDATA.Account Holder Type":"Non Account Holder",
                        "TXNDATA.Currency Pair":{"$regex":"INR to "},
                        "TXNDATA.Transaction Category":"Foreign Currency Exchange",
                        "TXNDATA.Transaction Date": {
                            "$gte":start_date,
                            "$lte":end_date
                        }
                    }
                },
                {
                    "$group": {
                        "_id": "$TXNDATA.Identification/Aadhar Number",
                        "data": {"$push": "$TXNDATA"}
                    }
                }
            ]

            agg_result = list(txn_collection.aggregate(pipeline))
            data_from_col_df = pd.DataFrame()

            for doc in agg_result:
                data_from_col_df = pd.concat([data_from_col_df,pd.DataFrame(doc['data'])])
            if not data_from_col_df.empty:
                grouped_data = data_from_col_df.groupby('Identification/Aadhar Number')
                for grpname, grpdata in grouped_data:
                    if (grpdata['Amount Exchanged'].sum() > current_values['X']):
                        total_df= pd.concat([total_df,grpdata])
                    if not total_df.empty:
                        def generate_indicative_rule(row):
                            return f"{row['Transaction Category']} transactions of more than {row['Transaction Currency']} {current_values['X']} were conducted for a {row['Account Holder Type']} in a month has triggered one of the RFI and raised an alert for the aggregation of Amount Exchanged,which is {row['Transaction Currency']}  {row['Amount Exchanged']}, and the Identification/Aadhar Number is {row['Identification/Aadhar Number']} at {row['Bank Location/Address']}."
    
                        total_df['Indicative_rule'] = total_df.apply(generate_indicative_rule, axis=1)
            if 'download' in request.form:
           
                excel_buffer = io.BytesIO()

                # Create an ExcelWriter object to write multiple DataFrames to different sheets
                with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                    total_df.to_excel(writer, sheet_name='totaldata', index=False)
                    # total_df_non.to_excel(writer, sheet_name='Non-Individuals', index=False)

                # Set the position of the BytesIO object to the beginning
                excel_buffer.seek(0)

                # Generate the response to download the Excel file
                response = make_response(excel_buffer.read())
                response.headers["Content-Disposition"] = "attachment filename=TM_9_1_data.xlsx"
                response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                return response
            

            tm_sub_hedding="TM 9.1"
            document =TM_collection.find_one({"code":"TM_9_1"})
            tm_heading = document.get("Alert_title","")
            if returning_data_enabled:
                return [total_df]
            else:
                if session["user_role"]=="DGM/PO":
            
                    return render_template('ty1.html',notify=notify, total_df=total_df,
                                                    tm_heading=tm_heading,
                                                    tm_sub_hedding=tm_sub_hedding,dgmuser=image(),type='dashbord',role='DGM/PO')

# CHANGES
@app.route("/TM_9_2",methods=["GET","POST"])
def TM_9_2():
        
        if request.method =='POST':
 
            userEmail = session['email_id']     
            notify = notification(userEmail) 
            if 'download' in request.form:
                user_input_date_str = '2022-01-30'  
            elif 'user_input_date_str' in request.form:
                user_input_date_str = request.form.get('user_input_date_str')
            else:
                user_input_date_str = "2022-01-30"
            current_values = threshold_values_from_col(TM_collection,'TM_9_2')


            total_df = pd.DataFrame()
            end_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')

            start_date= end_date-timedelta(days=current_values['Y'])
            print(start_date)
            print(end_date)
            pipeline = [
                {
                    "$unwind": "$TXNDATA"
                },
                {
                    "$match": {
                        "TXNDATA.Account Holder Type":"Non Account Holder",
                        "TXNDATA.Transaction Category":"Foreign Currency Exchange",
                        "TXNDATA.Currency Pair":{"$regex":" to INR"},
                        "TXNDATA.Transaction Date": {
                            "$gte":start_date,
                            "$lte":end_date
                        }
                    }
                },
                {
                    "$group": {
                        "_id": "$TXNDATA.Identification/Aadhar Number",
                        "data": {"$push": "$TXNDATA"}
                    }
                }
            ]

            agg_result = list(txn_collection.aggregate(pipeline))
            data_from_col_df = pd.DataFrame()

            for doc in agg_result:
                data_from_col_df = pd.concat([data_from_col_df,pd.DataFrame(doc['data'])])
            if not data_from_col_df.empty:
                grouped_data = data_from_col_df.groupby('Identification/Aadhar Number')
                for grpname, grpdata in grouped_data:
                    if (grpdata['Amount Exchanged'].sum() > current_values['X']):
                        total_df= pd.concat([total_df,grpdata])
                    if not total_df.empty:
                        def generate_indicative_rule(row):
                            return f"{row['Transaction Category']} transactions of more than {row['Currency Pair']} to INR {current_values['X']} were conducted for a {row['Account Holder Type']} in a month has triggered one of the RFI and raised an alert for The Amount Exchanged,which is {row['Amount Exchanged']} {row['Currency Pair']} and the Identification/Aadhar Number is {row['Identification/Aadhar Number']} at {row['Bank Location/Address']}."

                        total_df['Indicative_rule'] = total_df.apply(generate_indicative_rule, axis=1)


            if 'download' in request.form:
           
                excel_buffer = io.BytesIO()

                # Create an ExcelWriter object to write multiple DataFrames to different sheets
                with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                    total_df.to_excel(writer, sheet_name='totaldata', index=False)
                    # total_df_non.to_excel(writer, sheet_name='Non-Individuals', index=False)

                # Set the position of the BytesIO object to the beginning
                excel_buffer.seek(0)

                # Generate the response to download the Excel file
                response = make_response(excel_buffer.read())
                response.headers["Content-Disposition"] = "attachment filename=TM_9_2_data.xlsx"
                response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                return response
            tm_sub_hedding="TM 9.2"
            document =TM_collection.find_one({"code":"TM_9_2"})
            tm_heading = document.get("Alert_title","")
            if returning_data_enabled:
                return [total_df]
            else:
                if session["user_role"]=="DGM/PO":
            
                    return render_template('ty1.html',notify=notify, total_df=total_df,
                                                    tm_heading=tm_heading,
                                                    tm_sub_hedding=tm_sub_hedding,dgmuser=image(),type='dashbord',role='DGM/PO')



@app.route('/typology', methods=['GET', 'POST'])
@secure_route(required_role=['DGM/PO'])
def typology():
    crumbs_data = for_tm_ty_rm(TY_collection,"TY")
    user = users_collection.find_one({'role': 'DGM/PO'})
    notify = notification(user.get('emailid'))

    ituser = {'image': None}
    if user:
        ituser = users_collection.find_one({'emailid': user.get('emailid')})
        if ituser and 'image' in ituser:
            ituser['image'] = base64.b64encode(ituser['image']).decode('utf-8')
    return render_template('typology.html',crumbs_data=crumbs_data,type='dashbord',dgmuser=ituser,role='DGM/PO',notify=notify)

# CHANGES
@app.route('/TY_1_1',  methods=['GET', 'POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def TY_1_1():
    if request.method == 'POST':
        userEmail = session['email_id']
        notify = notification(userEmail)
        if 'download' in request.form:
            user_input_date_str = '2021-10-20'  
        elif 'user_input_date_str' in request.form:
            user_input_date_str = request.form.get('user_input_date_str')
        else:
            user_input_date_str = '2021-10-20'
        current_values = threshold_values_from_col(TY_collection,'TY_1_1')
        end_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')
        start_date = end_date - timedelta(days=30)

        print("start_date : ",start_date," : ",end_date)

        total_df = pd.DataFrame()
        pipeline = [
            {
                "$unwind": "$TXNDATA"
            },
            {
                "$match": {
                    "TXNDATA.Transaction Type": "Cash",
                    "TXNDATA.Transaction Date": {"$gte": start_date,"$lte": end_date},
                    "TXNDATA.Transaction Category": "Deposits",
                    "TXNDATA.Transaction Currency": "INR",
                    "TXNDATA.Transaction Amount":{
                        "$gte":current_values['X1'],
                        "$lte":current_values['X2']
                    }
                }
            },
            {
                "$group": {
                    "_id": "$TXNDATA.Account Number",
                    "data": {"$push": "$TXNDATA"}
                }
            }
        ]

        agg_result = list(txn_collection.aggregate(pipeline))


        for pf in agg_result:
            print('pf : ',pf['data'])

        data_from_col_df = pd.DataFrame(pf['data'])
        for doc in agg_result:
            data_from_col_df = pd.concat([data_from_col_df, pd.DataFrame(doc['data'])])
        print("data_from_col_df : ",data_from_col_df)

        customer_dict = {}
        if not data_from_col_df.empty:
            for index, row in data_from_col_df.iterrows():
                customer_id = row['Customer ID']
                account_number = row['Account Number']
                transaction_amount = row['Transaction Amount']
                if customer_id not in list(customer_dict.keys()):
                    customer_dict[customer_id]=[]
                    customer_dict[customer_id].append({
                        'Account Number': account_number,
                        'Transaction Amount': transaction_amount
                    })
                else:
                    customer_dict[customer_id].append({
                        'Account Number': account_number,
                        'Transaction Amount': transaction_amount
                    })
            
            account_counts = {}
            print("customer_dict : ",customer_dict)

            # Loop through total_df to count rows based on Account number
            for cust_id in list(customer_dict.keys()):
                count = len(customer_dict[cust_id])
                account_counts[cust_id] = count
            count_df = pd.DataFrame(list(account_counts.items()), columns=["Customer ID", "Number of transactions"]) 
            count_df_gt_1 = count_df[count_df['Number of transactions']>current_values['N']]
            filtered_df_total = data_from_col_df.groupby('Customer ID').filter(lambda x: len(x) > 1) 
            filtered_dfs= filtered_df_total[['Customer ID', 'Nature of account', 'Customer Profile', 'Customer Name', 'Account Number', 'Transaction Amount', 'Transaction Date',"DOB","Mobile Number","Address","Pincode","Acc_Opening_Date"]]
            merged_df = pd.merge(count_df_gt_1, filtered_dfs, on='Customer ID', how='inner')
        if not merged_df.empty:
            def generate_indicative_rule(row):
                return f"Cash deposits made by Customer Name {row['Customer Name']} with Customer ID {row['Customer ID']}, Account Number {row['Account Number']} being an {row['Nature of account']} and {row['Customer Profile']} triggered one of the RFI and raised an alert, in amounts ranging between INR {current_values['X1']} and {current_values['X2']} on date {row['Transaction Date']}.The customer has made transactions which aggregated to a total of  {int(row['Transaction Amount'])} ,in single/multiple accounts of the customer greater than once aggregated as {row['Number of transactions']} transactions in a month."

            merged_df['Indicative_rule'] = merged_df.apply(generate_indicative_rule, axis=1)
            

        if 'download' in request.form:
            excel_buffer = io.BytesIO()

            # Create an ExcelWriter object to write multiple DataFrames to different sheets
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                count_df.to_excel(writer, sheet_name='All', index=False)
                filtered_df_total.to_excel(writer, sheet_name='Daywise greaterthan 1', index=False)
                count_df_gt_1.to_excel(writer, sheet_name='greater than 1', index=False)

            # Set the position of the BytesIO object to the beginning
            excel_buffer.seek(0)

            # Generate the response to download the Excel file
            response = make_response(excel_buffer.read())
            response.headers["Content-Disposition"] = "attachment filename=TY_1_1_data.xlsx"
            response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            return response
        document =TY_collection.find_one({"code":"TY_1_1"})
        tm_heading = document.get("Alert_title","")
        tm_sub_hedding="TY 1.1"
        if returning_data_enabled:
            return [merged_df]
        else:
            if session["user_role"]=="DGM/PO":
                return render_template('ty1.html',notify=notify,count_df=count_df,
                                       filtered_df_total=filtered_df_total,count_df_gt_1=count_df_gt_1,tm_heading=tm_heading,
                                               tm_sub_hedding=tm_sub_hedding,dgmuser=image(),type='dashbord',role='DGM/PO')


# CHANGES
@app.route('/TY_1_2',  methods=['GET', 'POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def TY_1_2():
    if request.method == 'POST':
        userEmail = session['email_id']
        notify = notification(userEmail)
        if 'download' in request.form:
            user_input_date_str = '2021-10-20'  
        elif 'user_input_date_str' in request.form:
            user_input_date_str = request.form.get('user_input_date_str')
        else:
            # user_input_date_str = request.form['user_entered_date_ty_1_2']
            user_input_date_str = '2021-10-20'  
        end_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')
        current_values = threshold_values_from_col(TY_collection,'TY_1_2')
        start_date = end_date - timedelta(days=30)
        total_df = pd.DataFrame()

        print("start_date : ",start_date,"end_date : ",end_date)

        
        pipeline = [
            {
                "$unwind": "$TXNDATA"
            },
            {
                "$match": {
                    "TXNDATA.Transaction Type": "Cash",
                    "TXNDATA.Transaction Date": {"$gte": start_date,"$lte": end_date},
                    "TXNDATA.Transaction Category": "Deposits",
                    "TXNDATA.Transaction Currency": "INR",
                    "TXNDATA.Transaction Amount":{
                        "$gte":current_values['X1'],
                        "$lte":current_values['X2']
                    }
                }
            },
            {
                "$group": {
                    "_id": "$TXNDATA.Account Number",
                    "data": {"$push": "$TXNDATA"}
                }
            }
        ]

        agg_result = list(txn_collection.aggregate(pipeline))

       

        data_from_col_df = pd.DataFrame()
        for doc in agg_result:
            data_from_col_df = pd.concat([data_from_col_df, pd.DataFrame(doc['data'])])

        customer_dict = {}
        if not data_from_col_df.empty:
            for index, row in data_from_col_df.iterrows():
                customer_id = row['Customer ID']
                account_number = row['Account Number']
                transaction_amount = row['Transaction Amount']
                if customer_id not in list(customer_dict.keys()):
                    customer_dict[customer_id]=[]
                    customer_dict[customer_id].append({
                        'Account Number': account_number,
                        'Transaction Amount': transaction_amount
                    })
                else:
                    customer_dict[customer_id].append({
                        'Account Number': account_number,
                        'Transaction Amount': transaction_amount
                    })
            
            account_counts = {}

            # Loop through total_df to count rows based on Account number
            for cust_id in list(customer_dict.keys()):
                count = len(customer_dict[cust_id])
                account_counts[cust_id] = count

            count_df = pd.DataFrame(list(account_counts.items()), columns=["Customer ID", "Number of transactions"])
            filtered_df_total = data_from_col_df.groupby('Customer ID').filter(lambda x: len(x) > 1)
            filtered_df_total = filtered_df_total.sort_values(by='Transaction Date', ascending=True)
            count_df_gt_1 = count_df[count_df['Number of transactions']>current_values['N']]
                                                                            
            filtered_dfs= filtered_df_total[['Customer ID', 'Nature of account', 'Customer Profile', 'Customer Name', 'Account Number', 'Transaction Amount', 'Transaction Date',"Mobile Number","Address","Pincode","Acc_Opening_Date"]]
            merged_df = pd.merge(count_df_gt_1, filtered_dfs, on='Customer ID', how='inner')
        if not merged_df.empty:
            def generate_indicative_rule(row):
                return f"Cash deposits made by {row['Customer Name']} with Customer Id {row['Customer ID']},Account Number {row['Account Number']} being an {row['Nature of account']} and {row['Customer Profile']} triggered one of the RFI and raised an alert,in amounts ranging between INR {current_values['X1']} and {current_values['X2']} aggregated has {row['Transaction Amount']} in single/multiple accounts of the customer greater than once aggregated as {row['Number of transactions']} in a month on {row['Transaction Date']}"
            merged_df['Indicative_rule'] = merged_df.apply(generate_indicative_rule, axis=1)


            
        if 'download' in request.form:
            excel_buffer = io.BytesIO()

            # Create an ExcelWriter object to write multiple DataFrames to different sheets
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                count_df.to_excel(writer, sheet_name='All', index=False)
                filtered_df_total.to_excel(writer, sheet_name='Daywise greaterthan 1', index=False)
                count_df_gt_1.to_excel(writer, sheet_name='greater than 1', index=False)

            # Set the position of the BytesIO object to the beginning
            excel_buffer.seek(0)

            # Generate the response to download the Excel file
            response = make_response(excel_buffer.read())
            response.headers["Content-Disposition"] = "attachment filename=TY_1_2_data.xlsx"
            response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            return response
        document =TY_collection.find_one({"code":"TY_1_2"})
        tm_heading = document.get("Alert_title","")
        tm_sub_hedding="TY 1.2"
        if returning_data_enabled:

            return [merged_df]
        else:
            if session["user_role"]=="DGM/PO":
                return render_template('ty1.html',notify=notify,count_df=count_df,
                                   filtered_df_total=filtered_df_total,
                                               count_df_gt_1=count_df_gt_1,
                                               tm_heading=tm_heading,
                                               tm_sub_hedding=tm_sub_hedding,dgmuser=image(),type='dashbord',role='DGM/PO')


# CHANGES
@app.route('/TY_1_3',  methods=['GET', 'POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def TY_1_3():
    if request.method == 'POST':
        userEmail = session['email_id']
        notify = notification(userEmail)
        if 'download' in request.form:
            user_input_date_str = '2021-10-03'  
        elif 'user_input_date_str' in request.form:
            user_input_date_str = request.form.get('user_input_date_str')
        else:
            # user_input_date_str = request.form['user_entered_date_ty_1_3']
            user_input_date_str = '2021-10-03'  
        current_values = threshold_values_from_col(TY_collection,'TY_1_3')
        end_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')
        start_date = end_date - timedelta(days=current_values['Y'])

        total_df = pd.DataFrame()

        pipeline = [
            {
                "$unwind": "$TXNDATA"
            },
            {
                "$match": {
                    "TXNDATA.Transaction Type": "Cash",
                    "TXNDATA.Transaction Date": {"$gte": start_date,"$lte": end_date},
                    "TXNDATA.Transaction Category": "Deposits",
                    "TXNDATA.Transaction Currency": "INR",
                    "TXNDATA.Transaction Amount":{
                        "$gte":current_values['X1'],
                        "$lte":current_values['X2']
                    }
                }
            },
            {
                "$group": {
                    "_id": "$TXNDATA.Account Number",
                    "data": {"$push": "$TXNDATA"}
                }
            }
        ]

        agg_result = list(txn_collection.aggregate(pipeline))

        

        data_from_col_df = pd.DataFrame()
        for doc in agg_result:
            data_from_col_df = pd.concat([data_from_col_df, pd.DataFrame(doc['data'])])

        customer_dict = {}
        if not data_from_col_df.empty:
            for index, row in data_from_col_df.iterrows():
                customer_id = row['Customer ID']
                account_number = row['Account Number']
                transaction_amount = row['Transaction Amount']
                if customer_id not in list(customer_dict.keys()):
                    customer_dict[customer_id]=[]
                    customer_dict[customer_id].append({
                        'Account Number': account_number,
                        'Transaction Amount': transaction_amount
                    })
                else:
                    customer_dict[customer_id].append({
                        'Account Number': account_number,
                        'Transaction Amount': transaction_amount
                    })
            
            account_counts = {}

            # Loop through total_df to count rows based on Account number
            for cust_id in list(customer_dict.keys()):
                count = len(customer_dict[cust_id])
                account_counts[cust_id] = count

            # Convert the dictionary into a DataFrame
            count_df = pd.DataFrame(list(account_counts.items()), columns=["Customer ID", "Number of transactions"])
            count_df_gt_1 = count_df[count_df['Number of transactions']>current_values['N']]
            # print(count_df)
        
            filtered_df_total = data_from_col_df.groupby('Customer ID').filter(lambda x: len(x) > 1)
            filtered_df_total = filtered_df_total.sort_values(by='Transaction Date', ascending=True)
            
            filtered_dfs= filtered_df_total[['Customer ID', 'Nature of account', 'Customer Profile', 'Customer Name', 'Account Number', 'Transaction Amount', 'Transaction Date',"Mobile Number","Address","Pincode","Acc_Opening_Date"]]
            merged_df = pd.merge(count_df_gt_1, filtered_dfs, on='Customer ID', how='inner')
            if not merged_df.empty:
                def generate_indicative_rule(row):
                    return f"Cash deposits of {row['Customer Name']} with Customer Id {row['Customer ID']},Account Number {row['Account Number']} being an {row['Nature of account']} and {row['Customer Profile']} has triggered one of the RFI and raised an alert,in amounts ranging between INR {current_values['X1']} and {current_values['X2']} aggregated has {row['Transaction Amount']} in single/multiple accounts of the customer greater than once aggregated as {row['Number of transactions']} within {current_values['Y']} days on {row['Transaction Date']}."
                
                
                
                merged_df['Indicative_rule'] = merged_df.apply(generate_indicative_rule, axis=1)
                

        
        if 'download' in request.form:
            excel_buffer = io.BytesIO()

            # Create an ExcelWriter object to write multiple DataFrames to different sheets
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                count_df.to_excel(writer, sheet_name='All', index=False)
                filtered_df_total.to_excel(writer, sheet_name='Daywise greaterthan 1', index=False)
                count_df_gt_1.to_excel(writer, sheet_name='greater than 1', index=False)

            # Set the position of the BytesIO object to the beginning
            excel_buffer.seek(0)

            # Generate the response to download the Excel file
            response = make_response(excel_buffer.read())
            response.headers["Content-Disposition"] = "attachment filename=TY_1_3_data.xlsx"
            response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            return response
        
        document =TY_collection.find_one({"code":"TY_1_3"})
        tm_heading = document.get("Alert_title","")
        tm_sub_hedding="TY 1.3"

        if returning_data_enabled:
            return [merged_df]
        else:
            if session["user_role"]=="DGM/PO":

        
                return render_template('ty1.html',notify=notify, count_df_gt_1=count_df_gt_1,
                                                filtered_df_total=filtered_df_total,
                                                count_df=count_df,
                                                tm_heading=tm_heading,
                                                tm_sub_hedding=tm_sub_hedding,dgmuser=image(),type='dashbord',role='DGM/PO')


# CHANGES
@app.route('/TY_1_4',  methods=['GET', 'POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def TY_1_4():
    if request.method == 'POST':
        userEmail = session['email_id']
        notify = notification(userEmail)
        if 'download' in request.form:
            user_input_date_str = '2021-10-20'  
        elif 'user_input_date_str' in request.form:
            user_input_date_str = request.form.get('user_input_date_str')
        else:
            # user_input_date_str = request.form['user_entered_date_ty_1_4']
            user_input_date_str = '2021-10-20'  
        current_values = threshold_values_from_col(TY_collection,'TY_1_4')
        end_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')
        start_date = end_date - timedelta(days=current_values['Y'])

        total_df = pd.DataFrame()

        pipeline = [
            {
                "$unwind": "$TXNDATA"
            },
            {
                "$match": {
                    "TXNDATA.Transaction Type": "Cash",
                    "TXNDATA.Transaction Date": {"$gte": start_date,"$lte": end_date},
                    "TXNDATA.Transaction Category": "Deposits",
                    "TXNDATA.Transaction Currency": "INR",
                    "TXNDATA.Transaction Amount":{
                        "$gte":current_values['X1'],
                        "$lte":current_values['X2']
                    }
                }
            },
            {
                "$group": {
                    "_id": "$TXNDATA.Account Number",
                    "data": {"$push": "$TXNDATA"}
                }
            }
        ]

        agg_result = list(txn_collection.aggregate(pipeline))
        

        data_from_col_df = pd.DataFrame()
        for doc in agg_result:
            data_from_col_df = pd.concat([data_from_col_df, pd.DataFrame(doc['data'])])

        customer_dict = {}
        if not data_from_col_df.empty:
            for index, row in data_from_col_df.iterrows():
                customer_id = row['Customer ID']
                account_number = row['Account Number']
                transaction_amount = row['Transaction Amount']
                if customer_id not in list(customer_dict.keys()):
                    customer_dict[customer_id]=[]
                    customer_dict[customer_id].append({
                        'Account Number': account_number,
                        'Transaction Amount': transaction_amount
                    })
                else:
                    customer_dict[customer_id].append({
                        'Account Number': account_number,
                        'Transaction Amount': transaction_amount
                    })
            
            account_counts = {}

            # Loop through total_df to count rows based on Account number
            for cust_id in list(customer_dict.keys()):
                count = len(customer_dict[cust_id])
                account_counts[cust_id] = count

            # Convert the dictionary into a DataFrame
            count_df = pd.DataFrame(list(account_counts.items()), columns=["Customer ID", "Number of transactions"])
            count_df_gt_1 = count_df[count_df['Number of transactions']>current_values['N']]

            # print(count_df)

            filtered_df_total = data_from_col_df.groupby('Customer ID').filter(lambda x: len(x) > 1)
            filtered_df_total = filtered_df_total.sort_values(by='Transaction Date', ascending=True)
            
            filtered_dfs= filtered_df_total[['Customer ID', 'Nature of account', 'Customer Profile', 'Customer Name', 'Account Number', 'Transaction Amount', 'Transaction Date',"Mobile Number","Address","Pincode","Acc_Opening_Date"]]
            merged_df = pd.merge(count_df_gt_1, filtered_dfs, on='Customer ID', how='inner')
        if not merged_df.empty:
            def generate_indicative_rule(row):
            
                return f"Cash deposits of {row['Customer Name']} with Customer Id {row['Customer ID']}, Account Number {row['Account Number']} being an {row['Nature of account']} and {row['Customer Profile']} has triggered one of the RFI and raised an alert,in amounts ranging between INR {current_values['X1']} and {current_values['X2']} aggregated has {row['Transaction Amount']} in single/multiple accounts of the customer greater than once aggregated as {row['Number of transactions']} within {current_values['Y']} days on {row['Transaction Date']} ."
            
            
            merged_df['Indicative_rule'] = merged_df.apply(generate_indicative_rule, axis=1)


        if 'download' in request.form:
            excel_buffer = io.BytesIO()

            # Create an ExcelWriter object to write multiple DataFrames to different sheets
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                count_df.to_excel(writer, sheet_name='All', index=False)
                filtered_df_total.to_excel(writer, sheet_name='Daywise greaterthan 1', index=False)
                count_df_gt_1.to_excel(writer, sheet_name='greater than 1', index=False)

            # Set the position of the BytesIO object to the beginning
            excel_buffer.seek(0)

            # Generate the response to download the Excel file
            response = make_response(excel_buffer.read())
            response.headers["Content-Disposition"] = "attachment filename=TY_1_4_data.xlsx"
            response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            return response
        document =TY_collection.find_one({"code":"TY_1_4"})
        tm_heading = document.get("Alert_title","")
        tm_sub_hedding="TY 1.4"
        if returning_data_enabled:
            return [merged_df]
        else:
            if session["user_role"]=="DGM/PO":
        
                return render_template('ty1.html',notify=notify, count_df_gt_1=count_df_gt_1,
                                                filtered_df_total=filtered_df_total,
                                                count_df=count_df,
                                                tm_heading=tm_heading,
                                               tm_sub_hedding=tm_sub_hedding,dgmuser=image(),type='dashbord',role='DGM/PO')

# CHANGES
@app.route('/TY_1_5',  methods=['GET', 'POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def TY_1_5():
    if request.method == 'POST':
        userEmail = session['email_id']
        notify = notification(userEmail)
        if 'download' in request.form:
            user_input_date_str = '2021-10-20'  
        elif 'user_input_date_str' in request.form:
            user_input_date_str = request.form.get('user_input_date_str')
        else:
            user_input_date_str = '2021-10-20'  
        current_values = threshold_values_from_col(TY_collection,'TY_1_5')
        end_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')
        start_date = end_date - timedelta(days=current_values['Y'])

        total_df = pd.DataFrame()

        pipeline = [
            {
                "$unwind": "$TXNDATA"
            },
            {
                "$match": {
                    "TXNDATA.Transaction Type": "Cash",
                    "TXNDATA.Transaction Date": {"$gte": start_date,"$lte": end_date},
                    "TXNDATA.Transaction Category": "Withdrawals",
                    "TXNDATA.Transaction Currency": "INR",
                    "TXNDATA.Transaction Amount":{
                        "$gte":current_values['X1'],
                        "$lte":current_values['X2']
                    }
                }
            },
            {
                "$group": {
                    "_id": "$TXNDATA.Account Number",
                    "data": {"$push": "$TXNDATA"}
                }
            }
        ]

        agg_result = list(txn_collection.aggregate(pipeline))
      

        data_from_col_df = pd.DataFrame()
        for doc in agg_result:
            data_from_col_df = pd.concat([data_from_col_df, pd.DataFrame(doc['data'])])

        customer_dict = {}
        if not data_from_col_df.empty:
            for index, row in data_from_col_df.iterrows():
                customer_id = row['Customer ID']
                account_number = row['Account Number']
                transaction_amount = row['Transaction Amount']
                if customer_id not in list(customer_dict.keys()):
                    customer_dict[customer_id]=[]
                    customer_dict[customer_id].append({
                        'Account Number': account_number,
                        'Transaction Amount': transaction_amount
                    })
                else:
                    customer_dict[customer_id].append({
                        'Account Number': account_number,
                        'Transaction Amount': transaction_amount
                    })
            
            account_counts = {}

            # Loop through total_df to count rows based on Account number
            for cust_id in list(customer_dict.keys()):
                count = len(customer_dict[cust_id])
                account_counts[cust_id] = count

            # Convert the dictionary into a DataFrame
            count_df = pd.DataFrame(list(account_counts.items()), columns=["Customer ID", "Number of transactions"])
            count_df_gt_1 = count_df[count_df['Number of transactions']>1]
            # print(count_df)
            filtered_df_total = data_from_col_df.groupby('Customer ID').filter(lambda x: len(x) > 1)
            filtered_df_total = filtered_df_total.sort_values(by='Transaction Date', ascending=True)

            filtered_dfs= filtered_df_total[['Customer ID', 'Nature of account', 'Customer Profile', 'Customer Name', 'Account Number', 'Transaction Amount', 'Transaction Date',"Mobile Number","Address","Pincode","Acc_Opening_Date"]]
            merged_df = pd.merge(count_df_gt_1, filtered_dfs, on='Customer ID', how='inner')
            

        if not merged_df.empty:
            def generate_indicative_rule(row):
                return f"Cash Withdrawal of {row['Customer Name']} with Customer Id {row['Customer ID']},Account Number {row['Account Number']} being an {row['Nature of account']} and {row['Customer Profile']} has triggered one of the RFI and raised an alert,in amounts ranging between INR {current_values['X1']} and {current_values['X2']} aggregated has {row['Transaction Amount']} in single/multiple accounts of the customer greater than once aggregated as {row['Number of transactions']} within {current_values['Y']} days on {row['Transaction Date']}."
            merged_df['Indicative_rule'] = merged_df.apply(generate_indicative_rule, axis=1)
            
            # excel_writer = pd.ExcelWriter('TY_1_5_.xlsx', engine='openpyxl')
            # sheet_name_date = end_date.strftime("%Y-%m-%d").replace(":", "_")
            # merged_df.to_excel(excel_writer,sheet_name='Gt 1 time',index=False)
            

            # Save the Excel file
            # excel_writer.save()

            # print("DataFrame saved to 'TY_1_5.xlsx'")
        if 'download' in request.form:
            excel_buffer = io.BytesIO()

            # Create an ExcelWriter object to write multiple DataFrames to different sheets
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                data_from_col_df.to_excel(writer, sheet_name='All', index=False)
                filtered_df_total.to_excel(writer, sheet_name='Daywise greaterthan 1', index=False)
                count_df_gt_1.to_excel(writer, sheet_name='greater than 1', index=False)

            # Set the position of the BytesIO object to the beginning
            excel_buffer.seek(0)

            # Generate the response to download the Excel file
            response = make_response(excel_buffer.read())
            response.headers["Content-Disposition"] = "attachment filename=TY_1_5_data.xlsx"
            response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            return response    
        document =TY_collection.find_one({"code":"TY_1_5"})
        tm_heading = document.get("Alert_title","")
        tm_sub_hedding="TY 1.5"
        if returning_data_enabled:
            return [merged_df]
        else:
            if session["user_role"]=="DGM/PO":
        
                return render_template('ty1.html',notify=notify, count_df_gt_1=count_df_gt_1,
                                                filtered_df_total=filtered_df_total,
                                                count_df=data_from_col_df,
                                                tm_heading=tm_heading,
                                                tm_sub_hedding=tm_sub_hedding,dgmuser=image(),type='dashbord',role='DGM/PO')

@app.route("/TY_2_2",methods=['GET','POST'])
def TY_2_2():
    if request.method == 'POST':
        userEmail = session['email_id']
        notify = notification(userEmail)
        if 'download' in request.form:
            user_input_date_str = '2021-01-30'
        elif 'user_input_date_str' in request.form:
            user_input_date_str = request.form.get('user_input_date_str')
        else:
            user_input_date_str = "2021-01-30"
        end_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')
        start_date = end_date-timedelta(days=30)
        total_df = pd.DataFrame()
        print("start_date : ",start_date,"end_date : ",end_date)
        data_from_col = txn_collection.aggregate([
            { "$unwind" : "$TXNDATA"},
            {
                "$match":{
                    "TXNDATA.Transaction Date":{
                        "$gte":start_date,
                        "$lte":end_date
                    },
                    "TXNDATA.B Party Account number":{"$exists": True, "$ne": None},
                    "TXNDATA.C Party Account number":{"$exists": True, "$ne": None},
                    "TXNDATA.D Party Account number":{"$exists": True, "$ne": None}
                }
            },{
                "$group": {
                    "_id": "$TXNDATA.Account Number",
                    "data": {"$push": "$TXNDATA"}
                }
            }
        ])
        agg_result = list(data_from_col)
        print("agg_result : ",agg_result)
        data_from_col_df = pd.DataFrame()
        for doc in agg_result:
            data_from_col_df = pd.concat([data_from_col_df, pd.DataFrame(doc.get('data', []))])
        if not data_from_col_df.empty:
            grouped_data = data_from_col_df.groupby(["Customer ID", "Account Number"])
            for gdata, gname in grouped_data:
                gname['Combined_Parties'] = gname.apply(lambda row: [str(row['B Party Account number']), str(int(row['C Party Account number'])), str(int(row['D Party Account number']))], axis=1)
                gname['Transactions'] = gname.apply(lambda row: [int(row['Transaction Amount']),int(row['B Party Transaction Amount']), int(row['C Party Transaction Amount'])], axis=1)
                temp_df = gname[['Account Number', 'Customer ID']].drop_duplicates()
                temp_df['Transaction Amount'] =gname['Transaction Amount'].sum()
                temp_df['Connections'] = [gname['Combined_Parties'].tolist()]
                temp_df['Transactions']=[gname['Transactions'].tolist()]
                temp_df['Count']=len(gname)
                total_df = pd.concat([total_df, temp_df])
        transactions_list = total_df['Transactions'].tolist()
        connections_list = total_df['Connections'].tolist()
        result_dict = {}
        for key, group in total_df.groupby('Customer ID'):
            values_dict = {
                'Connections': group['Connections'].tolist(),
                'Transactions': group['Transactions'].tolist(),
                'Account Numbers':group['Account Number'].tolist()
            }
            result_dict[key] = values_dict
        document =TY_collection.find_one({"code":"TY_2_2"})
        # tm_heading = document.get("Alert_title","")
        # tm_sub_hedding="TY 2.2"
        if returning_data_enabled:
            return [total_df]
        # else:
        #     if session["user_role"]=="DGM/PO":
                # return render_template('ty1.html',notify=notify, total_df=total_df,
                #                                 tm_heading=tm_heading,
                #                                tm_sub_hedding=tm_sub_hedding)





        
   
# CHANGES
@app.route("/TY_3_1",methods=['GET','POST'])
def TY_3_1():
        if request.method == 'POST':
 
            userEmail = session['email_id']          
            notify = notification(userEmail)
            if 'download' in request.form:
                user_input_date_str = '2022-01-01'
            elif 'user_input_date_str' in request.form:
                user_input_date_str = request.form.get('user_input_date_str')
            else:
                user_input_date_str = "2022-01-01"
            start_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')

            total_df = pd.DataFrame()

            data_from_col_df_total = pd.DataFrame()

            
            
            current_values = threshold_values_from_col(TY_collection,'TY_3_1')

            end_date = start_date+timedelta(days=current_values['Y'])


            pipeline = [
                {
                    "$unwind":"$TXNDATA"
                },
                {
                    "$match":{
                        "TXNDATA.Transaction Category":"Deposits",
                        "TXNDATA.Transaction Date":{
                            "$gte":start_date,
                            "$lte":end_date
                        },
                        "TXNDATA.Transaction Amount":{
                        "$gte":current_values['x1'],
                        "$lte":current_values['x2']
                    }
                    }
                },
                {
                    "$group":{
                        "_id":"$TXNDATA.Account Number",
                        "data":{"$push":"$TXNDATA"}
                    }
                }
            ]
            agg_result = list(txn_collection.aggregate(pipeline))
          
            data_from_col_df = pd.DataFrame()

            for doc in agg_result:
                data_from_col_df = pd.concat([data_from_col_df,pd.DataFrame(doc['data'])])

            if not data_from_col_df.empty:
                grped_data = data_from_col_df.groupby('Account Number')
                for gname,gdata in grped_data:
                    if len(gdata)>current_values['N']:
                        data_from_col_df_sum = gdata['Transaction Amount'].sum()
                        last_dep_date =gdata['Transaction Date'].unique()[-1]
                        last_dep_date = pd.to_datetime(last_dep_date)
                        pipeline=[
                            {
                                "$unwind":"$TXNDATA"
                            },
                            {
                                "$match":{
                                    "TXNDATA.Transaction Category":"Withdrawals",
                                    "TXNDATA.Transaction Type":"Cash",
                                    "TXNDATA.Transaction Date":{
                                        "$gte":last_dep_date,
                                        "$lte":last_dep_date+timedelta(days=6)
                                    },
                                    "TXNDATA.Account Number":gname
                                }
                            },
                            {
                                "$group":{
                                    "_id":"$TXNDATA.Account Number",
                                    "data":{"$push":"$TXNDATA"}
                                }
                            }
                        ]
                        agg_result = list(txn_collection.aggregate(pipeline))
                        data_from_col_for_wd_df = pd.DataFrame()

                        for doc in agg_result:
                            data_from_col_for_wd_df = pd.concat([data_from_col_for_wd_df,pd.DataFrame(doc['data'])])
                        if not data_from_col_for_wd_df.empty:
                            if data_from_col_for_wd_df['Transaction Amount'].sum()>(data_from_col_df_sum*current_values['Z'])/100:
                                total_df = pd.concat([total_df,data_from_col_for_wd_df])
                                data_from_col_df_total = pd.concat([data_from_col_df_total,gdata])
            data_from_col_df_total = data_from_col_df_total.dropna(axis=1)
            total_df = total_df.dropna(axis=1)
            total_df = total_df.drop_duplicates()

            

            if not total_df.empty:
                def generate_indicative_rule(row):
                    return f"Cash deposits with Account number {row['Account Number']} and Customer Id {row['Customer ID']} being an {row['Nature of account']} and {row['Customer Profile']} has triggered one of the RFI and raised an alert in amounts ranging between INR {current_values['x1']} to {current_values['x2']} aggregated has {row['Transaction Amount']} greater than {current_values['N']} times in {current_values['Y']} days followed as by immediate cash withdrawls of {current_values['Z']} percent or more of total cash deposits from different locations on {row['Transaction Date']}."
                total_df['Indicative_rule'] = total_df.apply(generate_indicative_rule, axis=1)


            if 'download' in request.form:
                excel_buffer = io.BytesIO()

                # Create an ExcelWriter object to write multiple DataFrames to different sheets
                with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                    total_df.to_excel(writer, sheet_name='All', index=False)
                    data_from_col_df_total.to_excel(writer, sheet_name='Daywise greaterthan 1', index=False)
                    
                # Set the position of the BytesIO object to the beginning
                excel_buffer.seek(0)

                # Generate the response to download the Excel file
                response = make_response(excel_buffer.read())
                response.headers["Content-Disposition"] = "attachment filename=TY_3_1_data.xlsx"
                response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                return response

           
            document =TY_collection.find_one({"code":"TY_3_1"})
            tm_heading = document.get("Alert_title","")
            tm_sub_hedding="TY 3.1"

            if returning_data_enabled:

                return [total_df]
            else:
                if session["user_role"]=="DGM/PO":
            
                    return render_template('ty3.html',notify=notify, total_df=total_df,
                                                    data_from_col_df_total=data_from_col_df_total,
                                                    t1_heading="Repeated small value cash deposits",
                                                    t2_heading="Immediate cash withdrawls from different locations",
                                                    tm_heading=tm_heading,
                                                    tm_sub_hedding=tm_sub_hedding,dgmuser=image(),type='dashbord',role='DGM/PO')


# CHANGES
@app.route("/TY_3_2",methods=['GET','POST'])
def TY_3_2():
        if request.method == 'POST':
 
            userEmail = session['email_id']          
            notify = notification(userEmail)
            if 'download' in request.form:
                user_input_date_str = '2022-01-01'  
            elif 'user_input_date_str' in request.form:
                user_input_date_str = request.form.get('user_input_date_str')
            else:
                user_input_date_str = "2022-01-01"

            total_df = pd.DataFrame()
            data_from_col_df_total = pd.DataFrame()

            start_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')
            current_values = threshold_values_from_col(TY_collection,'TY_3_2')

            end_date = start_date + timedelta(days=current_values['Y'])
            

            pipeline = [
                {"$unwind": "$TXNDATA"},
                {"$match": {
                    "TXNDATA.Transaction Category": {"$in": ["Transfer - NEFT", "Transfer - IMPS", "Transfer - RTGS", "Transfer - UPI"]},
                    "TXNDATA.Transaction Date": {"$gte": start_date, "$lte": end_date},
                    "TXNDATA.Transaction Amount": {"$gte": current_values['x1'], "$lte": current_values['x2']}
                }},
                {"$group": {"_id": "$TXNDATA.Account Number", "data": {"$push": "$TXNDATA"}}}
            ]

            agg_result = list(txn_collection.aggregate(pipeline))
           

            data_from_col_df = pd.DataFrame()
            for doc in agg_result:
                data_from_col_df = pd.concat([data_from_col_df, pd.DataFrame(doc['data'])])

            if not data_from_col_df.empty:
                grped_data = data_from_col_df.groupby('Account Number')

                for gname, gdata in grped_data:
                    gdata =gdata.drop_duplicates()
                    if len(gdata) > current_values['N']:
                        data_from_col_df_sum = gdata['Transaction Amount'].sum()
                        last_dep_date = gdata['Transaction Date'].unique()[-1]
                        last_dep_date = pd.to_datetime(last_dep_date)

                        pipeline = [
                            {"$unwind": "$TXNDATA"},
                            {"$match": {
                                "TXNDATA.Transaction Category": {"$in": ["Withdrawals", "Withdrawls"]},
                                "TXNDATA.Transaction Date": {"$gte": last_dep_date, "$lte": last_dep_date + timedelta(days=6)},
                                "TXNDATA.Account Number": gname
                            }},
                            {"$group": {"_id": "$TXNDATA.Account Number", "data": {"$push": "$TXNDATA"}}}
                        ]

                        agg_result = list(txn_collection.aggregate(pipeline))
                        data_from_col_for_wd_df = pd.DataFrame()

                        for doc in agg_result:
                            data_from_col_for_wd_df = pd.concat([data_from_col_for_wd_df, pd.DataFrame(doc['data'])])
                        
                        if not data_from_col_for_wd_df.empty:
                            if data_from_col_for_wd_df['Transaction Amount'].sum() > (data_from_col_df_sum * current_values['Z']) / 100:
                                total_df = pd.concat([total_df, data_from_col_for_wd_df])
                                data_from_col_df_total = pd.concat([data_from_col_df_total, gdata])
            data_from_col_df_total = data_from_col_df_total.dropna(axis=1)
            total_df = total_df.dropna(axis=1)
            print(total_df)
            if not total_df.empty:
                def generate_indicative_rule(row):
                    return f"Receipt of account-to-account transfers (RTGS/NEFT/IMPS/transfer, etc.) with Account Number {row['Account Number']}, Customer ID {row['Customer ID']},being an {row['Nature of account']} and {row['Customer Profile']} from multiple parties in amounts ranging between INR {current_values['x1']} to {current_values['x2']} Transaction Amount aggregated has {row['Transaction Amount']} INR,has triggered one of the RFI and raised an alert, greater than {current_values['N']} times in {current_values['Y']} days. Subsequently, there have been immediate cash/non-cash withdrawals of {current_values['Z']} percent or more of such deposits on {row['Transaction Date']}."
                total_df['Indicative_rule'] = total_df.apply(generate_indicative_rule, axis=1)
            if 'download' in request.form:
                excel_buffer = io.BytesIO()

                # Create an ExcelWriter object to write multiple DataFrames to different sheets
                with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                    total_df.to_excel(writer, sheet_name='All', index=False)
                    data_from_col_df_total.to_excel(writer, sheet_name='Daywise greaterthan 1', index=False)
                    
                # Set the position of the BytesIO object to the beginning
                excel_buffer.seek(0)

                # Generate the response to download the Excel file
                response = make_response(excel_buffer.read())
                response.headers["Content-Disposition"] = "attachment filename=TY_3_2_data.xlsx"
                response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                return response


            document =TY_collection.find_one({"code":"TY_3_2"})
            tm_heading = document.get("Alert_title","")
            tm_sub_hedding="TY 3.2"
            if returning_data_enabled:

            
                return [total_df]
            else:
                if session["user_role"]=="DGM/PO":
                    return render_template('ty3.html',notify=notify, total_df=total_df,
                                                    data_from_col_df_total=data_from_col_df_total,
                                                    t1_heading="Repeated small value transfers",
                                                    t2_heading="Immediate cash/non-cash withdrawls",
                                                    tm_heading=tm_heading,
                                                    tm_sub_hedding=tm_sub_hedding,dgmuser=image(),type='dashbord',role='DGM/PO')


# CHANGES
@app.route("/TY_3_3",methods=['GET','POST'])
def TY_3_3():
        if request.method == 'POST':
 
            userEmail = session['email_id']  
            notify = notification(userEmail)
            if 'download' in request.form:
                user_input_date_str = '2022-01-01'  
            elif 'user_input_date_str' in request.form:
                user_input_date_str = request.form.get('user_input_date_str')
            else:
                user_input_date_str = "2022-01-01"

            total_df = pd.DataFrame()

            data_from_col_df_total = pd.DataFrame()

            

            start_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')
            current_values = threshold_values_from_col(TY_collection,'TY_3_3')


            end_date = start_date+timedelta(days=current_values['Y'])

            pipeline = [
                {"$unwind": "$TXNDATA"},
                {"$match": {
                    "TXNDATA.Transaction Category": "Deposits",
                    "TXNDATA.Transaction Date": {"$gte": start_date, "$lte": end_date},
                    "TXNDATA.Transaction Currency":{"$ne":"INR"}
                }},
                {"$group": {"_id": "$TXNDATA.Account Number", "data": {"$push": "$TXNDATA"}}}
            ]

            agg_result = list(txn_collection.aggregate(pipeline))
            for doc in agg_result:
                data_from_col_df=pd.DataFrame()
                data_from_col_df = pd.DataFrame(doc['data'])

                if not data_from_col_df.empty:
                    data_from_col_df=data_from_col_df.drop_duplicates()
                    # Converting 'transaction_date' to datetime if it's not already in datetime format
                    # data_from_col_df['Transaction Date'] = pd.to_datetime(data_from_col_df['Transaction Date'])

                    # Grouping by 'transaction_date' and summing 'transaction_amount'
                    new_df = data_from_col_df.groupby('Transaction Date')['Transaction Amount'].sum().reset_index()
                    new_df_filtered = new_df[(new_df['Transaction Amount'] >= current_values['x1']) & (new_df['Transaction Amount'] <= current_values['x2'])]
                    if len(new_df_filtered)>current_values['N']:
                        data_from_col_df_sum = new_df_filtered['Transaction Amount'].sum()
                        last_dep_date = new_df_filtered['Transaction Date'].unique()[-1]
                        last_dep_date = pd.to_datetime(last_dep_date)
                        pipeline = [
                            {"$unwind": "$TXNDATA"},
                            {"$match": {
                                "TXNDATA.Transaction Category": {"$in": ["Withdrawals", "Withdrawls"]},
                                "TXNDATA.Transaction Date": {"$gte": last_dep_date, "$lte": last_dep_date + timedelta(days=6)},
                                "TXNDATA.Account Number": doc['_id'],
                                "TXNDATA.Transaction Type":"Cash"
                            }},
                            {"$group": {"_id": "$TXNDATA.Account Number", "data": {"$push": "$TXNDATA"}}}
                        ]

                        agg_result = list(txn_collection.aggregate(pipeline))
                        data_from_col_for_wd_df = pd.DataFrame()

                        for doc in agg_result:
                            data_from_col_for_wd_df = pd.concat([data_from_col_for_wd_df, pd.DataFrame(doc['data'])])
                        
                        if not data_from_col_for_wd_df.empty:
                            if data_from_col_for_wd_df['Transaction Amount'].sum()>(data_from_col_df_sum*current_values['Z'])/100:
                                total_df = pd.concat([total_df,data_from_col_for_wd_df])
                                data_from_col_df_total = pd.concat([data_from_col_df_total,new_df_filtered])
            data_from_col_df_total = data_from_col_df_total.dropna(axis=1)
            total_df = total_df.dropna(axis=1)
            total_df = total_df.drop_duplicates()
            total_df = total_df[['Customer ID','Account Number','Transaction Amount',"Nature of account","Customer Profile","Transaction Date","ATM Withdrawl Location","Transaction Type","Transaction Category"]]            
            if not total_df.empty:
                def generate_indicative_rule(row):
                    return f"Inward foreign remittances with Account number {row['Account Number']} and Customer Id {row['Customer ID']} being an {row['Nature of account']} and {row['Customer Profile']} in amounts ranging between INR {current_values['x1']} to {current_values['x2']} aggregated has {row['Transaction Amount']} has triggered one of the RFI and raised an alert greater than {current_values['N']} times in {current_values['Y']} days followed by immediate cash withdrawals (through ATM, especially other bank ATMs, or other modes) of {current_values['Z']} percent or more of such remittances on {row['Transaction Date']}."
                total_df['Indicative_rule'] = total_df.apply(generate_indicative_rule, axis=1)
            if 'download' in request.form:
                excel_buffer = io.BytesIO()

                # Create an ExcelWriter object to write multiple DataFrames to different sheets
                with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                    total_df.to_excel(writer, sheet_name='All', index=False)
                    data_from_col_df_total.to_excel(writer, sheet_name='greater than 1', index=False)

                # Set the position of the BytesIO object to the beginning
                excel_buffer.seek(0)

                # Generate the response to download the Excel file
                response = make_response(excel_buffer.read())
                response.headers["Content-Disposition"] = "attachment filename=TY_3_3_data.xlsx"
                response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                return response
            document =TY_collection.find_one({"code":"TY_3_3"})
            tm_heading = document.get("Alert_title","")
            tm_sub_hedding="TY 3.3"
            
            if returning_data_enabled:
                return [total_df]
            else:
                if session["user_role"]=="DGM/PO":
            
                    return render_template('ty3.html',notify=notify, total_df=total_df,
                                                    data_from_col_df_total=data_from_col_df_total,
                                                    t1_heading="Repeated small value inward remittances from unrelated parties",
                                                    t2_heading="Immediate cash withdrawls",
                                                    tm_heading=tm_heading,
                                                    tm_sub_hedding=tm_sub_hedding,dgmuser=image(),type='dashbord',role='DGM/PO')


# CHANGES
@app.route("/TY_3_5",methods=['GET','POST'])
def TY_3_5():

    if request.method == 'POST':
 
        userEmail = session['email_id']       
        notify = notification(userEmail)
        if 'download' in request.form:
            user_input_date_str = '2022-01-30'  
        elif 'user_input_date_str' in request.form:
            user_input_date_str = request.form.get('user_input_date_str')
        else:
            user_input_date_str = "2022-01-30"

            
            
        total_df = pd.DataFrame()

        data_from_col_df_total = pd.DataFrame()


        end_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')
        current_values = threshold_values_from_col(TY_collection,'TY_3_5')

        start_date = end_date-timedelta(days=29)
            
        pipeline = [
            {"$unwind": "$TXNDATA"},
            {"$match": {
                "TXNDATA.Transaction Category": "Deposits",
                "TXNDATA.Transaction Date": {"$gte": start_date, "$lte": end_date},
                "TXNDATA.Transaction Currency":"USD"
            }},
            {"$group": {"_id": "$TXNDATA.Account Number", "data": {"$push": "$TXNDATA"}}}
        ]

        agg_result = list(txn_collection.aggregate(pipeline))
        for doc in agg_result:
            data_from_col_df=pd.DataFrame()
            data_from_col_df = pd.DataFrame(doc['data'])

            if not data_from_col_df.empty:
                data_from_col_df= data_from_col_df.drop_duplicates()
                existing_df = pd.DataFrame(data_from_col_df)
                existing_df['Transaction Date'] = pd.to_datetime(existing_df['Transaction Date'])
                new_df = existing_df.groupby('Transaction Date')['Transaction Amount'].sum().reset_index()
                new_df_filtered = new_df[(new_df['Transaction Amount'] >=current_values['x1']) & (new_df['Transaction Amount'] <= current_values['x2'])]
                if len(new_df_filtered)>current_values['N']:
                    data_from_col_df_sum = new_df_filtered['Transaction Amount'].sum()
                    last_dep_date = new_df_filtered['Transaction Date'].unique()[-1]
                    last_dep_date = pd.to_datetime(last_dep_date)
                    pipeline = [
                        {"$unwind": "$TXNDATA"},
                        {"$match": {
                            "TXNDATA.Transaction Category": {"$in": ["Transfer - UPI"]},
                            "TXNDATA.Transaction Date": {"$gte": last_dep_date, "$lte": last_dep_date + timedelta(days=current_values['Y'])},
                            "TXNDATA.Account Number": doc['_id']
                        }},
                        {"$group": {"_id": "$TXNDATA.Account Number", "data": {"$push": "$TXNDATA"}}}
                    ]

                    agg_result = list(txn_collection.aggregate(pipeline))
                    data_from_col_for_wd_df = pd.DataFrame()

                    for doc in agg_result:
                        data_from_col_for_wd_df = pd.concat([data_from_col_for_wd_df, pd.DataFrame(doc['data'])])

                    if not data_from_col_for_wd_df.empty:
                        if data_from_col_for_wd_df['Transaction Amount'].sum()>(data_from_col_df_sum*current_values['Z'])/100:
                            total_df = pd.concat([total_df,data_from_col_for_wd_df])
                            data_from_col_df_total = pd.concat([data_from_col_df_total,new_df_filtered])
            
                            data_from_col_df_total = data_from_col_df_total.dropna(axis=1)
                            total_df = total_df.dropna(axis=1)
            if not total_df.empty:
                def generate_indicative_rule(row):
                    return f"Inward foreign remittances with Account number {row['Account Number']} and Customer Id {row['Customer ID']} being an {row['Nature of account']} and {row['Customer Profile']} in amounts ranging between INR {current_values['x1']} to {current_values['x2']} aggregated has {row['Transaction Amount']}  has triggered one of the RFI and raised an alert aggregated has {row['Transaction Amount']},has triggered one of the RFI and raised an alert, greater than {current_values['N']} times in a month on {row['Transaction Date']} followed by expenditure on specified activities such as purchase of ticket, hotel bookingetc"

                total_df['Indicative_rule'] = total_df.apply(generate_indicative_rule, axis=1)

            if 'download' in request.form:
                excel_buffer = io.BytesIO()

                # Create an ExcelWriter object to write multiple DataFrames to different sheets
                with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                    total_df.to_excel(writer, sheet_name='All', index=False)
                    data_from_col_df_total.to_excel(writer, sheet_name='greater than 1', index=False)

                # Set the position of the BytesIO object to the beginning
                excel_buffer.seek(0)

                # Generate the response to download the Excel file
                response = make_response(excel_buffer.read())
                response.headers["Content-Disposition"] = "attachment filename=TY_3_5_data.xlsx"
                response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                return response

            document =TY_collection.find_one({"code":"TY_3_5"})
            tm_heading = document.get("Alert_title","")
            tm_sub_hedding="TY 3.5"
        
            if returning_data_enabled:
                return [total_df]
            else:
                if session["user_role"]=="DGM/PO":

                    return render_template('ty3.html',notify=notify, total_df=total_df,
                                                    data_from_col_df_total=data_from_col_df_total,
                                                    t1_heading="Repeated small value inward remittances from unrelated parties",
                                                    t2_heading="Expenditure on specified activities such as purchase of tickets, hotel bookings etc",
                                                    tm_heading=tm_heading,
                                                    tm_sub_hedding=tm_sub_hedding,dgmuser=image(),type='dashbord',role='DGM/PO')



# CHANGES
@app.route("/TY_6_1",methods=['GET','POST'])
def TY_6_1():
        if request.method == 'POST':
 
            userEmail = session['email_id']      
            notify = notification(userEmail)
            if 'download' in request.form:
                user_input_date_str = '2022-03-01'  
            elif 'user_input_date_str' in request.form:
                user_input_date_str = request.form.get('user_input_date_str')
            else:
                user_input_date_str = "2022-03-01"

            total_df = pd.DataFrame()
            end_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')
            current_values = threshold_values_from_col(TY_collection,'TY_6_1')
            start_date= end_date-timedelta(days=current_values['N'])
            print(start_date)
            print(end_date)
            pipeline = [
                {
                    "$unwind": "$TXNDATA"
                },
                {
                    "$match": {
                        "TXNDATA.Transaction Currency":"INR",
                        "TXNDATA.Transaction Type":"Cash",
                        "TXNDATA.Loan Amount":{"$gte":current_values['X1']},
                        "TXNDATA.Transaction Date": {
                            "$gte":start_date,
                            "$lte":end_date
                        },
                        "TXNDATA.Transaction Category":{"$nin":["Loan Repayment"]}
                    }
                },
                {
                    "$group": {
                        "_id": "$TXNDATA.Loan Account Number",
                        "data": {"$push": "$TXNDATA"}
                    }
                }
            ]

            agg_result = list(txn_collection.aggregate(pipeline))
            data_from_col_df = pd.DataFrame()

            for doc in agg_result:
                data_from_col_df = pd.concat([data_from_col_df,pd.DataFrame(doc['data'])])
            if not data_from_col_df.empty:
                grouped_data = data_from_col_df.groupby('Loan Account Number')
                for grpname, grpdata in grouped_data:
                    if (grpdata['Repayment Amount'] > current_values['X']).any():
                        total_df= pd.concat([total_df,grpdata])
            total_df=total_df.dropna(axis=1)
            if not total_df.empty:
                def generate_indicative_rule(row):
                    return f"Loan repayment made by {row['Loan Account Number']} has triggered one of the RFI,{row['Loan Account Number']} made repayments with total loan amount of {row['Loan Amount']} in cash is {row['Repayment Amount']} which is greather than {current_values['X']} in 2 months with a minimun loan disbursement value of {current_values['X1']} on {row['Transaction Date']}"    
                total_df['Indicative_rule'] = total_df.apply(generate_indicative_rule, axis=1)
            if 'download' in request.form:
                excel_buffer = io.BytesIO()

                # Create an ExcelWriter object to write multiple DataFrames to different sheets
                with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                    total_df.to_excel(writer, sheet_name='All', index=False)
                    

                # Set the position of the BytesIO object to the beginning
                excel_buffer.seek(0)

                # Generate the response to download the Excel file
                response = make_response(excel_buffer.read())
                response.headers["Content-Disposition"] = "attachment filename=TY_6_1_data.xlsx"
                response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                return response
            

            document =TY_collection.find_one({"code":"TY_6_1"})
            tm_heading = document.get("Alert_title","")
            tm_sub_hedding="TY 6.1"
            if returning_data_enabled:
                return [total_df]
            else:
                if session["user_role"]=="DGM/PO":
                    return render_template('ty6.html',notify=notify, total_df=total_df,
                                                    tm_heading=tm_heading,
                                                    t2_heading="Repayments of loan in cash",
                                                    tm_sub_hedding=tm_sub_hedding,dgmuser=image(),type='dashbord',role='DGM/PO')

# CHANGES
@app.route('/TY_6_3',methods=['GET', 'POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def TY_6_3():
        if request.method == 'POST':
 
            userEmail = session['email_id']   
            notify = notification(userEmail)
            if 'download' in request.form:
                user_input_date_str = '2022-03-02'  
            elif 'user_input_date_str' in request.form:
                user_input_date_str = request.form.get('user_input_date_str')
            else:
                user_input_date_str = "2022-03-02"
           
            total_df = pd.DataFrame()


            end_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')
            current_values = threshold_values_from_col(TY_collection,'TY_6_3')

            start_date= end_date-timedelta(days=current_values['N'])

            # Create an aggregation pipeline to filter data within MongoDB
            pipeline = [
                {
                    "$unwind": "$TXNDATA"
                },
                {
                    "$match": {
                        "TXNDATA.Transaction Category":"Loan Repayment",
                        "TXNDATA.Transaction Currency":"INR",
                        "TXNDATA.Loan Amount":{"$gte":current_values['X1']},
                        "TXNDATA.Transaction Date": {
                            "$gte":start_date,
                            "$lte":end_date
                        },
                        "TXNDATA.Transaction Category":{"$nin":["Loan Repayment"]}
                    }
                },
                {
                    "$group": {
                        "_id": "$TXNDATA.Loan Account Number",
                        "data": {"$push": "$TXNDATA"}
                    }
                }
            ]

            agg_result = list(txn_collection.aggregate(pipeline))

            data_from_col_df = pd.DataFrame()

            for doc in agg_result:
                data_from_col_df = pd.concat([data_from_col_df,pd.DataFrame(doc['data'])])
            if not data_from_col_df.empty:
                grouped_data = data_from_col_df.groupby('Loan Account Number')
                for grpname, grpdata in grouped_data:
                    total_loan_repayment = (grpdata['Repayment Amount'].sum() * current_values['Z']) / 100
                    condition = grpdata['Transaction Type'] == 'Cash'
                    filtered_data = grpdata[condition]
                    if not filtered_data.empty:
                        filtered_data_sum = filtered_data['Repayment Amount'].sum()
                        if filtered_data_sum>total_loan_repayment:
                            total_df = pd.concat([total_df,filtered_data])
            
            total_df=total_df.dropna(axis=1)
            if not total_df.empty:
                def generate_indicative_rule(row):
                    return f"Loan repayments made by {row['Loan Account Number']} has triggered one of the RFI,{row['Loan Account Number']} made repayments with total loan amount of {row['Loan Amount']} in cash is {row['Repayment Amount']} which is greather than {current_values['Z']} percent of total repayments in {current_values['N']/30} months with a minimun loan disbursement value of INR {current_values['X1']} on {row['Transaction Date']}"    
                total_df['Indicative_rule'] = total_df.apply(generate_indicative_rule, axis=1)
            if 'download' in request.form:
                excel_buffer = io.BytesIO()

                # Create an ExcelWriter object to write multiple DataFrames to different sheets
                with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                    total_df.to_excel(writer, sheet_name='All', index=False)

                # Set the position of the BytesIO object to the beginning
                excel_buffer.seek(0)

                # Generate the response to download the Excel file
                response = make_response(excel_buffer.read())
                response.headers["Content-Disposition"] = "attachment filename=TY_6_3_data.xlsx"
                response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                return response

            document =TY_collection.find_one({"code":"TY_6_3"})
            tm_heading = document.get("Alert_title","")
            tm_sub_hedding="TY 6.3"
            if returning_data_enabled:

                return [total_df]
            else:
                if session["user_role"]=="DGM/PO":
            
                    return render_template('ty6.html',notify=notify,total_df=total_df,
                                                    tm_heading=tm_heading,
                                                    t2_heading=tm_heading,
                                                    tm_sub_hedding=tm_sub_hedding,dgmuser=image(),type='dashbord',role='DGM/PO')

# CHANGES
@app.route('/TY_8_2',methods=['GET', 'POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def TY_8_2():
    if request.method == 'POST':
        userEmail = session['email_id']
        notify = notification(userEmail)
        if 'download' in request.form:
            user_input_date_str = '2022-01-07'  
        elif 'user_input_date_str' in request.form:
            user_input_date_str = request.form.get('user_input_date_str')
        else:
            user_input_date_str = "2022-01-07"
        
        total_df = pd.DataFrame()
        result_df =pd.DataFrame()

        end_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')
        current_values = threshold_values_from_col(TY_collection,'TY_8_2')




        start_date = end_date - timedelta(days=current_values['Y'])

        pipeline = [
            {
                "$unwind": "$TXNDATA"
            },
            {
                "$match": {
                    "TXNDATA.Transaction Date": {
                        "$gte": start_date,
                        "$lte": end_date
                    },
                    "TXNDATA.Transaction Category": "Deposit",
                    "TXNDATA.Transaction Type": "Cash",
                    "TXNDATA.Transaction Amount": {"$gte": current_values['x1'], "$lte": current_values['x2']}
                }
            },
            {
                "$group": {
                    "_id": "$TXNDATA.Customer ID",
                    "data": {"$push": "$TXNDATA"}
                }
            }
        ]

        agg_result = list(txn_collection.aggregate(pipeline))

        data_from_col_df_withdrawal = pd.DataFrame()
        for doc in agg_result:
            result_df = pd.concat([result_df, pd.DataFrame(doc['data'])])
        if not result_df.empty:
            deposits_dates = result_df['Transaction Date'].unique()
            for dt in deposits_dates:
                dt = pd.to_datetime(dt)
                withdrawal_pipeline = [
                    {
                        "$unwind": "$TXNDATA"
                    },
                    {
                        "$match": {
                            "TXNDATA.Transaction Category": "Withdrawls",
                            "TXNDATA.Transaction Type": "Cash",
                            "TXNDATA.Country Code": {"$in": ["PAK", "AFG"]},
                            "TXNDATA.Transaction Date": {"$gte": dt, "$lte": dt + timedelta(days=current_values['Y'])}
                        }
                    },
                    {
                        "$group": {
                            "_id": "$TXNDATA.Customer ID",
                            "data": {"$push": "$TXNDATA"}
                        }
                    }
                ]

                agg_result = list(txn_collection.aggregate(withdrawal_pipeline))

                for doc in agg_result:
                    data_from_col_df_withdrawal = pd.concat([data_from_col_df_withdrawal, pd.DataFrame(doc['data'])])


        if len(result_df)>current_values['N']:
            total_df=pd.concat([total_df,result_df])
        total_df=total_df.dropna(axis=1)
        data_from_col_df_withdrawals = data_from_col_df_withdrawal[['Customer ID','Nature of account','Customer Profile', 'Account Number', 'Transaction Amount', 'Transaction Date',"ATM Withdrawl Location"]]
        data_from_col_df_withdrawals = data_from_col_df_withdrawals.drop_duplicates()


        if not data_from_col_df_withdrawals.empty:
            def generate_indicative_rule(row):
                return f"Deposit of cash in the account with Account Number {row['Account Number']} and Customer ID {row ['Customer ID']} in amounts ranging between INR {current_values['x1']} to INR {current_values['x2']} aggreated has {row['Transaction Amount']} greater than once in {current_values['Y']} days has triggered one of the RFI and raised an alert, followed by ATM withdrawal in Afghanistan or Pakistan located at{row['ATM Withdrawl Location']}."               
            data_from_col_df_withdrawals['Indicative_rule'] = data_from_col_df_withdrawals.apply(generate_indicative_rule, axis=1)
        if 'download' in request.form:
        
            excel_buffer = io.BytesIO()

            # Create an ExcelWriter object to write multiple DataFrames to different sheets
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                total_df.to_excel(writer, sheet_name='Deposits', index=False)
                data_from_col_df_withdrawals.to_excel(writer, sheet_name='withdrawals', index=False)

            # Set the position of the BytesIO object to the beginning
            excel_buffer.seek(0)

            # Generate the response to download the Excel file
            response = make_response(excel_buffer.read())
            response.headers["Content-Disposition"] = "attachment filename=TY_8_2_data.xlsx"
            response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            return response
        

        document =TY_collection.find_one({"code":"TY_8_2"})
        tm_heading = document.get("Alert_title","")
        tm_sub_hedding="TY 8.2"
        if returning_data_enabled:
            return [data_from_col_df_withdrawals]
        else:
            if session["user_role"]=="DGM/PO":
                
                return render_template('ty7.html',notify=notify, total_df=total_df,data_from_col_df_withdrawal=data_from_col_df_withdrawal,
                                        t1_title="cash deposits below threshold reporting limits",
                                        t2_title="Immediate ATM withdrawal Afghanistan/Pakistan",
                                        tm_heading=tm_heading,
                                        tm_sub_hedding=tm_sub_hedding,dgmuser=image(),type='dashbord',role='DGM/PO'
                                    )


# CHANGES
@app.route('/TY_10_2',  methods=['GET', 'POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def TY_10_2():
        if request.method == 'POST':
 
            userEmail = session['email_id']
            notify = notification(userEmail)
            if 'download' in request.form:
                pass
    
            current_values = threshold_values_from_col(TY_collection,'TY_10_2')
            # Define constants
            NON_CASH_CONDITION = {"TXNDATA.Transaction Type": "Non-cash",
                                "TXNDATA.Transaction Category": "Deposits",
                                "TXNDATA.Transaction Currency": "Foreign Currency"}

            # Initialize DataFrames
            total_df = pd.DataFrame()
            total_result_df = pd.DataFrame()

            # Aggregate data from MongoDB
            pipeline = [
                {"$unwind": "$TXNDATA"},
                {"$match": NON_CASH_CONDITION},
                {"$group": {
                    "_id": {"Account Number": "$TXNDATA.Account Number", "Transaction Date": "$TXNDATA.Transaction Date"},
                    "TransactionAmountSum": {"$sum": "$TXNDATA.Transaction Amount"},
                    "data": {"$push": "$TXNDATA"}
                }},
                {"$match": {"TransactionAmountSum": {"$gt": current_values['X1']}}}
            ]
            agg_result = list(txn_collection.aggregate(pipeline))

            data_from_col_df = pd.concat([pd.DataFrame(doc['data']) for doc in agg_result])

            if not data_from_col_df.empty:
                # Convert 'Transaction Date' to datetime
                data_from_col_df['Transaction Date'] = pd.to_datetime(data_from_col_df['Transaction Date'], errors='coerce')

                # Handle NaT values
                data_from_col_df = data_from_col_df.dropna(subset=['Transaction Date'])
                grpdata = data_from_col_df.groupby('Account Number')
                for gname,gdata in grpdata:
                    for date in gdata['Transaction Date'].unique():
                        date = pd.to_datetime(date)
                        new_date = date + timedelta(days=current_values['Y'])
                        # Aggregate withdrawal data from MongoDB
                        withdrawal_pipeline = [
                            {"$unwind": "$TXNDATA"},
                            {"$match": {
                                "TXNDATA.Transaction Category": "Withdrawals",
                                "TXNDATA.Account Number":gname,
                                "TXNDATA.Transaction Date": {"$gte": date, "$lte": new_date}
                                }
                            },
                            {"$group": {"_id": "$TXNDATA.Account Number", "data": {"$push": "$TXNDATA"}}}
                        ]

                        agg_result = list(txn_collection.aggregate(withdrawal_pipeline))
                        df_data_for_foreign_or = pd.DataFrame()
                        for doc in agg_result:
                            df_data_for_foreign_or = pd.concat([df_data_for_foreign_or, pd.DataFrame(doc['data'])])

                        if not df_data_for_foreign_or.empty:
                            val = df_data_for_foreign_or['Transaction Amount'].sum()
                            per_value = (gdata[gdata['Transaction Date'] == date]['Transaction Amount'].sum() * current_values['Z']) / 100

                            if val > per_value:
                                filtered_result_df = gdata[
                                    (gdata['Transaction Date'] == date) & (gdata['Account Number'].isin(df_data_for_foreign_or['Account Number']))]
                                total_result_df = pd.concat([total_result_df, filtered_result_df])
                                total_df = pd.concat([total_df, df_data_for_foreign_or.reset_index(drop=True)])

            # Select relevant columns in the final DataFrame
            total_df = total_df[['Account Number', 'Transaction Date', 'Transaction Amount', 'Transaction Type', 'Transaction Currency', 'Transaction Category']]
            total_result_df=total_result_df[['Account Number', 'Transaction Date', 'Transaction Amount', 'Transaction Type', 'Transaction Currency', 'Transaction Category']]
            total_result_df = total_result_df.drop_duplicates()

            # Fill NaN values with 0
            total_df = total_df.fillna(0)
            total_result_df = total_result_df.fillna(0)
            if 'download' in request.form:
                excel_buffer = io.BytesIO()

                # Create an ExcelWriter object to write multiple DataFrames to different sheets
                with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                    total_df.to_excel(writer, sheet_name='All', index=False)
                    total_result_df.to_excel(writer, sheet_name='Daywise greaterthan 1', index=False)
                    data_from_col_df.to_excel(writer, sheet_name='greater than 1', index=False)

                # Set the position of the BytesIO object to the beginning
                excel_buffer.seek(0)

                # Generate the response to download the Excel file
                response = make_response(excel_buffer.read())
                response.headers["Content-Disposition"] = "attachment filename=TY_10_2_data.xlsx"
                response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                return response


            tm_sub_hedding="TY 10.2"
            document =TY_collection.find_one({"code":"TY_10_2"})
            tm_heading = document.get("Alert_title","")
            if returning_data_enabled:
                return [total_df,total_result_df,data_from_col_df]
            else:
                if session["user_role"]=="DGM/PO":           
                    return render_template('ty1.html',notify=notify, total_df=total_df,
                                                        total_result_df=total_result_df,
                                                        data_from_col_df=data_from_col_df,
                                                        tm_heading=tm_heading,
                                                        tm_sub_hedding=tm_sub_hedding,dgmuser=image(),type='dashbord',role='DGM/PO')




    # # Save the Excel file
    # excel_writer = pd.ExcelWriter('TY_10_2_.xlsx', engine='openpyxl')
    # total_result_df = total_result_df.drop_duplicates()
    # total_df.to_excel(excel_writer, sheet_name="sheet1", index=False)
    # total_result_df.to_excel(excel_writer, sheet_name="sheet2", index=False)
    # excel_writer._save()

    # print("DataFrame saved to 'TY_10_2.xlsx'")

# CHANGES
@app.route('/TY_10_4',  methods=['GET', 'POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def TY_10_4():
        if request.method == 'POST':
 
            userEmail = session['email_id']
            notify = notification(userEmail)
            if 'download' in request.form:
                user_input_date_str = "2022-01-30"  
            elif 'user_input_date_str' in request.form:
                user_input_date_str = request.form.get('user_input_date_str')
            else:
                user_input_date_str ="2022-01-30"

            end_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')
            current_values = threshold_values_from_col(TY_collection,'TY_10_4')
            start_date = end_date-timedelta(days=29)
            
            
            pipeline = [
                {
                    "$unwind": "$TXNDATA"
                },
                {
                    "$match": {
                        "TXNDATA.Transaction Date":{
                            "$gte":start_date,
                            "$lte":end_date
                        }
                    }
                },
                {
                    "$group": {
                        "_id": "$TXNDATA.Account Number",
                        "data": {"$push": "$TXNDATA"}
                    }
                }
            ]
            
            agg_result = list(txn_collection.aggregate(pipeline))
            data_from_col_df = pd.DataFrame()
            
            for doc in agg_result:
                data_from_col_df = pd.concat([data_from_col_df,pd.DataFrame(doc['data'])])
            
            main_df = pd.DataFrame()
            if not data_from_col_df.empty:
                grouped_data = data_from_col_df.groupby('Customer ID')
            
                transaction_currency = {"USD":83.23,"Euro":89.39}     

                def convert_amount(row):
                    currency = row['Transaction Currency']
                    amount = row['Transaction Amount']
                    conversion_rate = transaction_currency.get(currency, 1.0)  # If currency not found, default 1.0 
                    return amount * conversion_rate
            
                for groupname, groupdata in grouped_data:
                    groupdata["Transaction Amount"] = groupdata.apply(convert_amount, axis=1)
                    filtered_group = groupdata[(groupdata["Transaction Amount"] >= 400000) & (groupdata["Transaction Amount"] <= 500000)]
                    if len(filtered_group)>current_values['N']:
                        main_df= pd.concat([main_df,filtered_group])
            main_df = main_df.dropna(axis=1)
            print(main_df)
            if 'download' in request.form:
                excel_buffer = io.BytesIO()

                # Create an ExcelWriter object to write multiple DataFrames to different sheets
                with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                    main_df.to_excel(writer, sheet_name='All', index=False)

                # Set the position of the BytesIO object to the beginning
                excel_buffer.seek(0)

                # Generate the response to download the Excel file
                response = make_response(excel_buffer.read())
                response.headers["Content-Disposition"] = "attachment filename=TY_10_4_data.xlsx"
                response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                return response
            document =TY_collection.find_one({"code":"TY_10_4"})
            tm_heading = document.get("Alert_title","")
            tm_sub_hedding="TY 10.4"
            if returning_data_enabled:
                return [main_df]
            else:
                if session["user_role"]=="DGM/PO":
                    return render_template('ty10.html',notify=notify ,ty_10_4_df=main_df,ty_10_4_df_true=True,
                                                        tm_heading=tm_heading,
                                                        tm_sub_hedding=tm_sub_hedding,dgmuser=image(),type='dashbord',role='DGM/PO')


# @app.route('/TY_10_5',  methods=['GET', 'POST'])
# @secure_route(required_role=['IT Officer','DGM/PO'])
# def TY_10_5():
#     total_df = pd.DataFrame()
    # userEmail = session['email_id']
    # notify = notification(userEmail)

#     total_result_df = pd.DataFrame()

#     for col in db.list_collection_names():
#         collection = db[col]
#         data_from_col = collection.find({
#             "Transaction Type":"Non-cash",
#             "Transaction Category":"Deposits"
#         })
#         df_data_from_col = pd.DataFrame(list(data_from_col))
#         if not df_data_from_col.empty:
#             result_df = df_data_from_col.groupby('Transaction Date')['Transaction Amount'].sum().reset_index()
#             result_df = result_df[result_df['Transaction Amount']>200000]
#             result_df["Account Number"] = col
#             if not result_df.empty:
#                 for date in result_df['Transaction Date'].unique():
#                     date = pd.to_datetime(date)
#                     new_date = date + timedelta(days=6)
#                     data_for_foreign_or = collection.find({
#                         "Transaction Type":"Non-cash",
#                         "Transaction Currency":"Foreign Currency",
#                         "Transaction Category":"Withdrawals",
#                         "Transaction Date":{
#                             "$gte":date,
#                             "$lte":new_date
#                         }
#                     })
#                     df_data_for_foreign_or = pd.DataFrame(list(data_for_foreign_or))
#                     if not df_data_for_foreign_or.empty:
#                         for index, row in df_data_for_foreign_or.iterrows():
#                             val = row['Transaction Amount']

#                             # Calculate the sum of 'Transaction Amount' in 'result_df' for a specific 'Transaction Date' (assuming 'date' is defined)
#                             per_value = (result_df[result_df['Transaction Date'] == date]['Transaction Amount'].sum() * 30) / 100

#                             # Check if 'val' is greater than 'per_value'
#                             if val > per_value:
#                                 # Filter 'result_df' based on 'Transaction Date' and 'Account Number' (assuming 'col' is defined)
#                                 filtered_result_df = result_df[(result_df['Transaction Date'] == date) & (result_df['Account Number'] == col)]

#                                 # Concatenate 'filtered_result_df' to 'total_result_df' and select the row from 'df_data_for_foreign_or' by index
#                                 total_result_df = pd.concat([total_result_df, filtered_result_df])
#                                 selected_row = df_data_for_foreign_or.loc[index]
#                                 total_df = pd.concat([total_df, pd.DataFrame(selected_row).T])

#     total_df= total_df[['Account Number','Transaction Date','Transaction Amount','Transaction Currency','Transaction Category']]            
#     print("total_df",total_df)
#     print("total_result_df",total_df)
        
#     tm_heading ="Non-cash deposits followed by immediate outward remittance transactions, Non-cash deposits greater than [x] value followed by immediate outward foreign remittance of [z] percent or more within [y] days"
#     tm_sub_hedding="TY 10.5"
        
#     return total_result_df, total_df, tm_sub_hedding
#     # return render_template('ty10.html',notify=notify , total_result_df_10_5=total_result_df,
#     #                        total_df_10_5=total_df,
#     #                        tm_heading=tm_heading,
#     #                        tm_sub_hedding=tm_sub_hedding
#     #                        )

# CHANGES
@app.route('/TY_11_1',  methods=['GET', 'POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def TY_11_1():
        if request.method == 'POST':
 
            userEmail = session['email_id']
            notify = notification(userEmail)
            if 'download' in request.form:
                user_input_date_str = '2022-01-31'
            elif 'user_input_date_str' in request.form:
                user_input_date_str = request.form.get('user_input_date_str')

            else:
                user_input_date_str = "2022-01-31"
            # total_df = pd.DataFrame()
            result_df =pd.DataFrame()
            end_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')
            current_values = threshold_values_from_col(TY_collection,'TY_11_1')
            start_date = end_date - timedelta(days=30)
            pipeline = [
                {
                    "$unwind": "$TXNDATA"
                },
                {
                    "$match": {
                        "TXNDATA.Transaction Date": {
                            "$gte": start_date,
                            "$lte": end_date
                        },
                        "TXNDATA.Transaction Category": "Deposit",
                        "TXNDATA.Transaction Type": "Cash",
                        "TXNDATA.State":"Bihar",
                        "TXNDATA.District":{
                            "$in":["West Champaran","East Champaran"]
                        },
                        # Optional to take these values
                        "TXNDATA.Transaction Amount": {"$gte": current_values['x1'], "$lte": current_values['x2']}
                    }
                },
                {
                    "$group": {
                        "_id": "$TXNDATA.Customer ID",
                        "data": {"$push": "$TXNDATA"}
                    }
                }
            ]
            agg_result = list(txn_collection.aggregate(pipeline))
            data_from_col_df_withdrawal = pd.DataFrame()
            for doc in agg_result:
                result_df = pd.concat([result_df, pd.DataFrame(doc['data'])])
            if not result_df.empty:
                deposits_dates = result_df['Transaction Date'].unique()
                for dt in deposits_dates:
                    dt = pd.to_datetime(dt)
                    withdrawal_pipeline = [
                        {
                            "$unwind": "$TXNDATA"
                        },
                        {
                            "$match": {
                                "TXNDATA.Transaction Category": "Withdrawls",
                                "TXNDATA.Transaction Type":{
                                    "$in":["Cash","ATM"]
                                },
                                "TXNDATA.B Party State":"West Bengal",
                                "TXNDATA.B Party District":"Malda",
                                "TXNDATA.State":"Bihar",
                                "TXNDATA.District":{
                                    "$in":["West Champaran","East Champaran","Champaran"]
                                },
                                "TXNDATA.Transaction Date": {"$gte": dt, "$lte": dt + timedelta(days=current_values['N'])}
                            }
                        },
                        {
                            "$group": {
                                "_id": "$TXNDATA.Customer ID",
                                "data": {"$push": "$TXNDATA"}
                            }
                        }
                    ]
                    agg_result = list(txn_collection.aggregate(withdrawal_pipeline))
                    for doc in agg_result:
                        data_from_col_df_withdrawal = pd.concat([data_from_col_df_withdrawal, pd.DataFrame(doc['data'])])
            
            result_df=result_df.dropna(axis=1)
            data_from_col_df_withdrawal=data_from_col_df_withdrawal.dropna(axis=1)
            data_from_col_df_withdrawal = data_from_col_df_withdrawal.drop_duplicates()
            if not data_from_col_df_withdrawal.empty:
                def generate_indicative_rule(row):
                    return f"Cash deposits made in home bank accounts with Account Number {row['Account Number']}, Customer ID {row['Customer ID']}, being an {row['Nature of account']} and {row['Customer Profile']} located on Indo-Nepal border areas in Bihar with quick ATM or cash withdrawals from branches (within {current_values['N']} days) in Malda (West Bengal) area has triggered one of the RFI and raised an alert on {row['Transaction Date']} and ranging between Transaction Amount of {current_values['x1']} to {current_values['x2']} amount is aggregated has {row['Transaction Amount']}"
                data_from_col_df_withdrawal['Indicative_rule'] = data_from_col_df_withdrawal.apply(generate_indicative_rule, axis=1)       
        
            if 'download' in request.form:
                excel_buffer = io.BytesIO()
                # Create an ExcelWriter object to write multiple DataFrames to different sheets
                with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                    result_df.to_excel(writer, sheet_name='sheet1', index=False)
                    data_from_col_df_withdrawal.to_excel(writer, sheet_name='sheet2', index=False)
                # Set the position of the BytesIO object to the beginning
                excel_buffer.seek(0)
                # Generate the response to download the Excel file
                response = make_response(excel_buffer.read())
                response.headers["Content-Disposition"] = "attachment filename=TY_11_1_data.xlsx"
                response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                return response
            document =TY_collection.find_one({"code":"TY_11_1"})
            tm_heading = document.get("Alert_title","")
            tm_sub_hedding="TY 11.1"
            if returning_data_enabled:
                return [data_from_col_df_withdrawal]
            else:
                if session["user_role"]=="DGM/PO":
                    return render_template('ty7.html',notify=notify, total_df=result_df,
                                                        data_from_col_df_withdrawal=data_from_col_df_withdrawal,
                                                        t1_title="Cash deposits made in home bank accounts located on Indo-Nepal border areas in Bihar",t2_title=" ATM withdrawals or cash withdrawal from branches.",
                                                        tm_heading=tm_heading,
                                                        tm_sub_hedding=tm_sub_hedding,dgmuser=image(),type='dashbord',role='DGM/PO')



@app.route('/risk_management', methods=['GET', 'POST'])
@secure_route(required_role=['DGM/PO'])
def risk_management():
    crumbs_data = for_tm_ty_rm(RM_collection,"RM")
    user = users_collection.find_one({'role': 'DGM/PO'})
    notify = notification(user.get('emailid'))

    ituser = {'image': None}
    if user:
        ituser = users_collection.find_one({'emailid': user.get('emailid')})
        if ituser and 'image' in ituser:
            ituser['image'] = base64.b64encode(ituser['image']).decode('utf-8')

    return render_template('risk_management.html',notify=notify,crumbs_data=crumbs_data,type='dashbord',dgmuser=ituser,role='DGM/PO')


@app.route('/RM_1_1',  methods=['GET', 'POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def RM_1_1():
    if request.method == 'POST':
        userEmail = session['email_id']
        notify = notification(userEmail) 
        if'download' in request.form:
            user_input_date_str = '2021-10-10'  
        elif 'user_input_date_str' in request.form:
                user_input_date_str = request.form.get('user_input_date_str')
        else:
            user_input_date_str = '2021-10-10'
        current_values = threshold_values_from_col(RM_collection,'RM_1_1')
        end_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')
        start_date = end_date - timedelta(days=current_values['Y'])
        print(start_date)
        print(end_date)
        total_df = pd.DataFrame()
        pipeline = [
            {
                "$unwind": "$TXNDATA"
            },
            {
                "$match": {
                    "TXNDATA.Transaction Type": "Cash",
                    "TXNDATA.NPO/Charity":"Yes",
                    "TXNDATA.Transaction Date": {"$gte": start_date,
                                                "$lte":end_date},
                    "TXNDATA.Transaction Currency": "INR"
                }
            },
            {
                "$group": {
                    "_id": "$TXNDATA.Account Number",
                    "data": {"$push": "$TXNDATA"}
                }
            }
        ]

        agg_result = list(txn_collection.aggregate(pipeline))

        data_from_col_df = pd.DataFrame()
        for doc in agg_result:
            data_from_col_df = pd.concat([data_from_col_df, pd.DataFrame(doc['data'])])

        if not data_from_col_df.empty:
            groupeddf = data_from_col_df.groupby('Account Number')
            for gpname, gpdf in groupeddf:
                if gpdf["Transaction Amount"].sum()>=500000:
                    new_df = pd.DataFrame({
                        "Transaction Amount":[gpdf["Transaction Amount"].sum()],
                        "Account Number":[gpname],
                        'Customer Profile':[gpdf['Customer Profile'].unique()[0]],
                        'Nature of account':[gpdf['Nature of account'].unique()[0]],
                        "Transaction Currency":gpdf["Transaction Currency"].unique()
                    })
                    if not new_df.empty:
                        total_df = pd.concat([total_df,new_df])  

        if not total_df.empty:
            def generate_indicative_rule(row):
                return f"Cash transactions both deposits & withdrawls made by {row['Account Number']} has triggered one of the RFI, {row['Account Number']} being an {row['Customer Profile']} and {row['Nature of account']} is {row['Transaction Currency']} {row['Transaction Amount']} which is greater than INR  {current_values['X']} in trust/NGO/NPO in between dates {start_date} and {end_date} which are of total {current_values['Y']} days" 
            total_df['Indicative_rule'] = total_df.apply(generate_indicative_rule, axis=1)


        if 'download' in request.form:
            
                    excel_buffer = io.BytesIO()

                    # Create an ExcelWriter object to write multiple DataFrames to different sheets
                    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                        total_df.to_excel(writer, sheet_name='totaldata', index=False)
                        # total_df_non.to_excel(writer, sheet_name='Non-Individuals', index=False)

                    # Set the position of the BytesIO object to the beginning
                    excel_buffer.seek(0)

                    # Generate the response to download the Excel file
                    response = make_response(excel_buffer.read())
                    response.headers["Content-Disposition"] = "attachment filename=RM_1_1_data.xlsx"
                    response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    return response
        tm_heading ="High value cash transactions in NPOs, Cash transactions (Deposits & withdrawls) greater than INR [X] in trust/NGO/NPO in [Y] days"
        tm_sub_hedding="RM 1.1"
        if session["user_role"]=="IT Officer":
            return [total_df] 
        elif session["user_role"]=="DGM/PO":
            return render_template('rm1.html',notify=notify, total_df=total_df,
                                        tm_heading=tm_heading,
                                        tm_sub_hedding=tm_sub_hedding,
                                      )

@app.route('/RM_1_3',  methods=['GET', 'POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def RM_1_3():
    if request.method == 'POST':
        userEmail = session['email_id']
        notify = notification(userEmail) 
        if'download' in request.form:
            user_input_date_str = '2021-10-10'  
        elif 'user_input_date_str' in request.form:
                user_input_date_str = request.form.get('user_input_date_str')
        else:
            user_input_date_str = '2021-10-10'
        current_values = threshold_values_from_col(RM_collection,'RM_1_3')
        end_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')
        start_date = end_date - timedelta(days=current_values['Y'])

        total_df = pd.DataFrame()

        pipeline = [
            {
                "$unwind": "$TXNDATA"
            },
            {
                "$match": {
                    "TXNDATA.Transaction Type": "Cash",
                    "TXNDATA.Real estate agent/dealer":"Yes",
                    "TXNDATA.Transaction Date": {"$gte": start_date,
                                                "$lte":end_date},
                    "TXNDATA.Transaction Currency": "INR"
                }
            },
            {
                "$group": {
                    "_id": "$TXNDATA.Account Number",
                    "data": {"$push": "$TXNDATA"}
                }
            }
        ]

        agg_result = list(txn_collection.aggregate(pipeline))

        data_from_col_df = pd.DataFrame()
        for doc in agg_result:
            data_from_col_df = pd.concat([data_from_col_df, pd.DataFrame(doc['data'])])

        if not data_from_col_df.empty:
            groupeddf = data_from_col_df.groupby('Account Number')
            for gpname, gpdf in groupeddf:
                if gpdf["Transaction Amount"].sum()>=50000:
                    new_df = pd.DataFrame({
                        "Transaction Amount":[gpdf["Transaction Amount"].sum()],
                        "Account Number":[gpname],
                        'Customer Profile':[gpdf['Customer Profile'].unique()[0]],
                        'Nature of account':[gpdf['Nature of account'].unique()[0]],
                        "Transaction Currency":gpdf["Transaction Currency"].unique()
                    })
                    if not new_df.empty:
                        total_df = pd.concat([total_df,new_df])  

        # print(total_df)
        if not total_df.empty:
            def generate_indicative_rule(row):
                return f"Cash transactions both deposits & withdrawls made by {row['Account Number']} triggered one of the RFI, {row['Account Number']} being an {row['Customer Profile']} and {row['Nature of account']} is {row['Transaction Currency']} {row['Transaction Amount']} which is greater than INR {current_values['X']} in real estate agents and dealers in between dates {start_date} and {end_date} which are of total {current_values['Y']} days"    
            total_df['Indicative_rule'] = total_df.apply(generate_indicative_rule, axis=1)

        if 'download' in request.form:
            
                    excel_buffer = io.BytesIO()

                    # Create an ExcelWriter object to write multiple DataFrames to different sheets
                    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                        total_df.to_excel(writer, sheet_name='totaldata', index=False)
                        # total_df_non.to_excel(writer, sheet_name='Non-Individuals', index=False)

                    # Set the position of the BytesIO object to the beginning
                    excel_buffer.seek(0)

                    # Generate the response to download the Excel file
                    response = make_response(excel_buffer.read())
                    response.headers["Content-Disposition"] = "attachment filename=RM_1_3_data.xlsx"
                    response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    return response
            
        document =RM_collection.find_one({"code":"RM_1_3"})
        tm_heading = document.get("Alert_title","")  
        tm_sub_hedding="RM 1.3"
        if returning_data_enabled:


            return [total_df] 
        else:
            if session["user_role"]=="DGM/PO":
                return render_template('rm1.html',notify=notify, total_df=total_df,
                                        tm_heading=tm_heading,
                                        tm_sub_hedding=tm_sub_hedding,
                                      )

# CHANGES
@app.route('/RM_1_4',  methods=['GET', 'POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def RM_1_4():
    if request.method == 'POST':
        userEmail = session['email_id']
        notify = notification(userEmail) 
        if'download' in request.form:
            user_input_date_str = '2021-10-10'  
        elif 'user_input_date_str' in request.form:
                user_input_date_str = request.form.get('user_input_date_str')
        else:
            user_input_date_str = '2021-10-10'
        current_values = threshold_values_from_col(RM_collection,'RM_1_4')
        end_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')
        start_date = end_date - timedelta(days=current_values['Y'])

        total_df = pd.DataFrame()

        pipeline = [
            {
                "$unwind": "$TXNDATA"
            },
            {
                "$match": {
                    "TXNDATA.Transaction Type": "Cash",
                    "TXNDATA.Precious Metal Dealer":"Yes",
                    "TXNDATA.Transaction Date": {"$gte": start_date,
                                                "$lte":end_date},
                    "TXNDATA.Transaction Currency": "INR"
                }
            },
            {
                "$group": {
                    "_id": "$TXNDATA.Account Number",
                    "data": {"$push": "$TXNDATA"}
                }
            }
        ]

        agg_result = list(txn_collection.aggregate(pipeline))

        data_from_col_df = pd.DataFrame()
        for doc in agg_result:
            data_from_col_df = pd.concat([data_from_col_df, pd.DataFrame(doc['data'])])

        if not data_from_col_df.empty:
            groupeddf = data_from_col_df.groupby('Account Number')
            for gpname, gpdf in groupeddf:
                if gpdf["Transaction Amount"].sum()>=50000:
                    new_df = pd.DataFrame({
                        "Transaction Amount":[gpdf["Transaction Amount"].sum()],
                        "Account Number":[gpname],
                        'Customer Profile':[gpdf['Customer Profile'].unique()[0]],
                        'Nature of account':[gpdf['Nature of account'].unique()[0]],
                        "Transaction Currency":gpdf["Transaction Currency"].unique()
                    })
                    if not new_df.empty:
                        total_df = pd.concat([total_df,new_df])  

        # print(total_df)
        if not total_df.empty:
            def generate_indicative_rule(row):
                return f"Cash transactions both deposits & withdrawls made by {row['Account Number']} triggered one of the RFI, {row['Account Number']} being an {row['Customer Profile']} and {row['Nature of account']} is {row['Transaction Currency']} {row['Transaction Amount']} which is greater than INR {current_values['X']} in precious metal, precious stone and gems & jewellery in between dates {start_date} and {end_date} which are of total {current_values['Y']} days"    
            total_df['Indicative_rule'] = total_df.apply(generate_indicative_rule, axis=1)


        if 'download' in request.form:
            
                    excel_buffer = io.BytesIO()

                    # Create an ExcelWriter object to write multiple DataFrames to different sheets
                    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                        total_df.to_excel(writer, sheet_name='totaldata', index=False)
                        # total_df_non.to_excel(writer, sheet_name='Non-Individuals', index=False)

                    # Set the position of the BytesIO object to the beginning
                    excel_buffer.seek(0)

                    # Generate the response to download the Excel file
                    response = make_response(excel_buffer.read())
                    response.headers["Content-Disposition"] = "attachment filename=RM_1_4_data.xlsx"
                    response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    return response
            
        document =RM_collection.find_one({"code":"RM_1_4"})
        tm_heading = document.get("Alert_title","")  
        tm_sub_hedding="RM 1.4"

        if returning_data_enabled:
    
            return [total_df] 
        else:
            if session["user_role"]=="DGM/PO":
        
                return render_template('rm1.html',notify=notify, total_df=total_df,
                                        tm_heading=tm_heading,
                                        tm_sub_hedding=tm_sub_hedding)

                
# CHANGES
@app.route('/RM_2_1',  methods=['GET', 'POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def RM_2_1():
    if request.method == 'POST':
        userEmail = session['email_id']
        notify = notification(userEmail)
        if 'download' in request.form:
            user_input_date_str = '2021-10-20'  
        elif 'user_input_date_str' in request.form:
                user_input_date_str = request.form.get('user_input_date_str')
        else:
            # user_input_date_str = request.form['user_entered_date_rms_2_1']
            user_input_date_str = '2021-10-20'
        current_values = threshold_values_from_col(RM_collection,'RM_2_1')  
        end_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')
        start_date = end_date - timedelta(days=current_values['Y'])
        total_df = pd.DataFrame()

        pipeline = [
            {
                "$unwind": "$TXNDATA"
            },
            {
                "$match": {
                    "TXNDATA.Transaction Type":"Non-cash",
                    "TXNDATA.Transaction Currency":"Foreign Currency",
                    "TXNDATA.Transaction Date": {"$gte": start_date,
                                                "$lte":end_date},
                    "TXNDATA.Transaction Category":"Deposits"
                }
            },
            {
                "$group": {
                    "_id": "$TXNDATA.Account Number",
                    "data": {"$push": "$TXNDATA"}
                }
            }
        ]

        agg_result = list(txn_collection.aggregate(pipeline))

        data_from_col_df = pd.DataFrame()
        for doc in agg_result:
            data_from_col_df = pd.concat([data_from_col_df, pd.DataFrame(doc['data'])])

        if not data_from_col_df.empty:
            groupeddf = data_from_col_df.groupby('Account Number')
            for gname, gdf in groupeddf:
                if gdf["Transaction Amount"].sum()>=500000:
                    new_df = pd.DataFrame({
                        "Transaction Amount":[gdf["Transaction Amount"].sum()],
                        "Account Number":[gname],
                        'Customer Profile':[gdf['Customer Profile'].unique()[0]],
                        'Nature of account':[gdf['Nature of account'].unique()[0]],
                        "Transaction Type":gdf["Transaction Type"].unique(),
                        "Transaction Currency":gdf["Transaction Currency"].unique(),
                        "Transaction Category":gdf["Transaction Category"].unique()
                    })
                    if not new_df.empty:
                        total_df = pd.concat([total_df,new_df])  

        if not total_df.empty:
            def generate_indicative_rule(row):
                return f"Inward foreign remittance made by {row['Account Number']} being an {row['Customer Profile']} and {row['Nature of account']} has triggered one of the RFI, {row['Account Number']} made the inward foreign remittance which is {row['Transaction Category']} of amount {row['Transaction Amount']} in {row['Transaction Currency']} greater than {current_values['X']} value aggregated in between dates {start_date} and {end_date} which are of total {current_values['Y']} days"    
            total_df['Indicative_rule'] = total_df.apply(generate_indicative_rule, axis=1)  
       
        if 'download' in request.form:
            
                    excel_buffer = io.BytesIO()

                    # Create an ExcelWriter object to write multiple DataFrames to different sheets
                    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                        total_df.to_excel(writer, sheet_name='totaldata', index=False)
                        # total_df_non.to_excel(writer, sheet_name='Non-Individuals', index=False)

                    # Set the position of the BytesIO object to the beginning
                    excel_buffer.seek(0)

                    # Generate the response to download the Excel file
                    response = make_response(excel_buffer.read())
                    response.headers["Content-Disposition"] = "attachment filename=RM_2_1_data.xlsx"
                    response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    return response
            
        document =RM_collection.find_one({"code":"RM_2_1"})
        tm_heading = document.get("Alert_title","")   
        tm_sub_hedding="RM 2.1"
            
        if returning_data_enabled:
            return [total_df]
        else:
            if session["user_role"]=="DGM/PO":
         
                return render_template('rm1.html',notify=notify, total_df_2_1=total_df,
                                        tm_heading=tm_heading,
                                        tm_sub_hedding=tm_sub_hedding,
                                    )



# CHANGES
@app.route('/RM_2_2', methods=['GET', 'POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def RM_2_2():
    if request.method == 'POST':
        userEmail = session['email_id']
        notify = notification(userEmail)
        if 'download' in request.form:
            user_input_date_str = '2021-03-10'
        elif 'user_input_date_str' in request.form:
                user_input_date_str = request.form.get('user_input_date_str')
        else:
            user_input_date_str = '2021-03-10'
        current_values = threshold_values_from_col(RM_collection,'RM_2_2')
        end_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')
        start_date = end_date - timedelta(days=90)

        # Initialize lists to store results
        result_data = []

        pipeline = [
            {
                "$unwind": "$TXNDATA"
            },
            {
                "$match": {
                    "TXNDATA.Acc_Opening_Date": {"$gte": start_date, "$lte": end_date}
                }
            },
            {
                "$group": {
                    "_id": "$TXNDATA.Account Number",
                    "data": {"$push": "$TXNDATA"}
                }
            }
        ]

        agg_result = list(txn_collection.aggregate(pipeline))

        data_from_col_df = pd.DataFrame()
        for doc in agg_result:
            data_from_col_df = pd.concat([data_from_col_df, pd.DataFrame(doc['data'])])

        if not data_from_col_df.empty:
            groupeddf = data_from_col_df.groupby('Account Number')
            for gname, gdf in groupeddf:
                acc_open_date = pd.to_datetime(gdf["Acc_Opening_Date"].unique()[0])
                end_transaction_date = acc_open_date + timedelta(days=current_values['Y'])
                transaction_conditions_pipeline = [
                    {
                        "$unwind": "$TXNDATA"
                    },
                    {
                        "$match": {
                            "TXNDATA.Acc_Opening_Date": acc_open_date,
                            "TXNDATA.Account Number": gname,
                            "TXNDATA.Transaction Type": "Non-cash",
                            "TXNDATA.Transaction Date": {"$gte": acc_open_date, "$lte": end_transaction_date},
                            "TXNDATA.Transaction Currency": "Foreign Currency",
                            "TXNDATA.Transaction Category": "Deposits"
                        }
                    },
                    {
                        "$group": {
                            "_id": "$TXNDATA.Account Number",
                            "total_amount": {"$sum": "$TXNDATA.Transaction Amount"}
                        }
                    }]
                transactions = list(txn_collection.aggregate(transaction_conditions_pipeline))
                if transactions and transactions[0]["total_amount"] >= current_values['X']:
                    result_data.append({
                         "Transaction Amount gte 20k, 100 days account opening date": float(transactions[0]["total_amount"]),
                        "Account Number": gname,
                        "Transaction Type": "Non-cash",
                        "Transaction Currency": "Foreign Currency",
                        "Transaction Category": "Deposits"
                    })
        total_df = pd.DataFrame(result_data)
        total_df = total_df.drop_duplicates()

        if not total_df.empty:
            def generate_indicative_rule(row):
                return f"Transaction type of {row['Transaction Type']} and Transaction Category of {row['Transaction Category']} in which transaction currency is {row['Transaction Currency']} triggered one of the RFI and raised an alert where transaction amount is greater than {current_values['X']} aggregated has,{row['Transaction Amount gte 20k, 100 days account opening date']} with new accounts in which account opening date is being from {current_values['Y']} days with Account Number {row['Account Number']}"
            total_df['Indicative_rule'] = total_df.apply(generate_indicative_rule, axis=1)
        

        if 'download' in request.form:
            
                    excel_buffer = io.BytesIO()

                    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                        total_df.to_excel(writer, sheet_name='totaldata', index=False)
                        # total_df_non.to_excel(writer, sheet_name='Non-Individuals', index=False)

                    # Set the position of the BytesIO object to the beginning
                    excel_buffer.seek(0)

                    # Generate the response to download the Excel file
                    response = make_response(excel_buffer.read())
                    response.headers["Content-Disposition"] = "attachment filename=RM_2_2_data.xlsx"
                    response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    return response
            
        tm_sub_hedding="RM 2.2"
        document =RM_collection.find_one({"code":"RM_2_2"})
        tm_heading = document.get("Alert_title","")
        total_df = total_df.drop_duplicates()
        
        if returning_data_enabled:
            return [total_df]
        else:
            if session["user_role"]=="DGM/PO": 
        
                return render_template('rm1.html',notify=notify, total_df_2_2=total_df,
                                        tm_heading=tm_heading,
                                        tm_sub_hedding=tm_sub_hedding,
                                      )
            
        

# CHANGES
@app.route('/RM_2_3',  methods=['GET', 'POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def RM_2_3():
    if request.method == 'POST':
        userEmail = session['email_id']
        notify = notification(userEmail)
        if 'download' in request.form:
            user_input_date_str = '2021-10-10'  
        elif 'user_input_date_str' in request.form:
                user_input_date_str = request.form.get('user_input_date_str')
        else:
            # user_input_date_str = request.form['user_entered_date_rms_2_3']
            user_input_date_str = '2021-10-20'  
        current_values = threshold_values_from_col(RM_collection,'RM_2_3')
        end_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')
        start_date = end_date - timedelta(days=90)
        # Initialize lists to store results
        result_data = []

        # Set of included customer profiles
        included_profiles = {"Student", "Pensioner", "Housewife", "Wages", "Salary Person", "Minor"}

                
        pipeline = [
            {
                "$unwind": "$TXNDATA"
            },
            {
                "$match": {
                    "TXNDATA.Acc_Opening_Date":{"$gte": start_date, "$lte": end_date},
                    "TXNDATA.Customer Profile": {"$in": list(included_profiles)}
                }
            },
            {
                "$group": {
                    "_id": "$TXNDATA.Account Number",
                    "data": {"$push": "$TXNDATA"}
                }
            }
        ]


        agg_result = list(txn_collection.aggregate(pipeline))

        data_from_col_df = pd.DataFrame()
        for doc in agg_result:
            data_from_col_df = pd.concat([data_from_col_df, pd.DataFrame(doc['data'])])

        if not data_from_col_df.empty:
            groupeddf = data_from_col_df.groupby('Account Number')
            for gname, gdf in groupeddf:
                acc_open_date = pd.to_datetime(gdf["Acc_Opening_Date"].unique()[0])
                end_transaction_date = acc_open_date + timedelta(days=current_values['Y'])
                transaction_conditions_pipeline = [
                    {
                        "$unwind": "$TXNDATA"
                    },
                    {
                        "$match": {
                            "TXNDATA.Acc_Opening_Date":acc_open_date,
                            "TXNDATA.Account Number":gname,
                            "TXNDATA.Transaction Type":"Non-cash",
                            "TXNDATA.Transaction Date": {"$gte": acc_open_date, "$lte": end_transaction_date},
                            "TXNDATA.Transaction Currency": "Foreign Currency",
                            "TXNDATA.Transaction Category": "Deposits",
                            "TXNDATA.Customer Profile": {"$in": list(included_profiles)}
                        }
                    },
                    {
                        "$group": {
                            "_id": "$TXNDATA.Account Number",
                            "total_amount": {"$sum": "$TXNDATA.Transaction Amount"}
                        }
                    }]
                transactions = list(txn_collection.aggregate(transaction_conditions_pipeline))
                if transactions and transactions[0]["total_amount"] >= 20000:
                        result_data.append({
                            "Transaction Amount gte 20k, 100 days account opening date": transactions[0]["total_amount"],
                            "Account Number": gname,
                            'Customer Profile':gdf['Customer Profile'].unique()[0],
                            'Nature of account':gdf['Nature of account'].unique()[0],
                            "Transaction Type": "Non-cash",
                            "Transaction Currency": "Foreign Currency",
                            "Transaction Category": "Deposits"
                        })
        total_df = pd.DataFrame(result_data)

        if not total_df.empty:
            def generate_indicative_rule(row):
                return f"Inward foreign remittance made by {row['Account Number']} being an {row['Customer Profile']} and {row['Nature of account']} has ttriggered one of the RFI, {row['Account Number']} made the inward foreign remittance which is {row['Transaction Category']} of amount {row['Transaction Amount']} in {row['Transaction Currency']} greater than {current_values['X']} value in a new account aggregated in between dates {start_date} and {end_date} which are of total {current_values['Y']} days"    
            total_df['Indicative_rule'] = total_df.apply(generate_indicative_rule, axis=1)

        # Drop duplicates based on all columns
        total_df = total_df.drop_duplicates()


        if 'download' in request.form:
            
                    excel_buffer = io.BytesIO()

                    # Create an ExcelWriter object to write multiple DataFrames to different sheets
                    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                        total_df.to_excel(writer, sheet_name='totaldata', index=False)
                        # total_df_non.to_excel(writer, sheet_name='Non-Individuals', index=False)

                    # Set the position of the BytesIO object to the beginning
                    excel_buffer.seek(0)

                    # Generate the response to download the Excel file
                    response = make_response(excel_buffer.read())
                    response.headers["Content-Disposition"] = "attachment filename=RM_2_3_data.xlsx"
                    response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    return response
            
        tm_sub_hedding="RM 2.3"
        document =RM_collection.find_one({"code":"RM_2_3"})
        tm_heading = document.get("Alert_title","")
        if returning_data_enabled:
            return [total_df] 
        else:
            if session["user_role"]=="DGM/PO":
        
                return render_template('rm1.html',notify=notify, total_df_2_3=total_df,
                                        tm_heading=tm_heading,
                                        tm_sub_hedding=tm_sub_hedding,
                                      )

# CHANGES
@app.route("/RM_3_1",methods=['GET','POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def RM_3_1():
        if request.method == 'POST':
            userEmail = session['email_id']
            notify = notification(userEmail)
            if 'download' in request.form:
                user_input_date_str = '2022-01-02'  
            elif 'user_input_date_str' in request.form:
                user_input_date_str = request.form.get('user_input_date_str')
            else:
                user_input_date_str = "2022-01-02"



            empty_df = pd.DataFrame()

            user_input_date_str = "2022-01-02"
            user_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')
            current_values = threshold_values_from_col(RM_collection,'RM_3_1')


            

            has_data_meeting_condition = False


            pipeline = [
                {
                    "$unwind": "$TXNDATA"
                },
                {
                    "$match": {
                        "TXNDATA.Transaction Date":user_date,
                        "TXNDATA.Country Code":
                        {
                            "$in":["IRN","MMR"]
                        },
                        "TXNDATA.Cross Currency":"Yes"
                    }
                },
                {
                    "$group": {
                        "_id": "$TXNDATA.Account Number",
                        "data": {"$push": "$TXNDATA"}
                    }
                }
            ]

            agg_result = list(txn_collection.aggregate(pipeline))
            data_from_col_df = pd.DataFrame()

            for doc in agg_result:
                data_from_col_df = pd.concat([data_from_col_df,pd.DataFrame(doc['data'])])

            if not data_from_col_df.empty:
                grouped_df = data_from_col_df.groupby('Country Code')
                for gp_name,gp_data in grouped_df:
                    if not gp_data.empty:
                        if gp_data['Transaction Amount'].sum()>=current_values['X']:
                            total_df = data_from_col_df
            total_df = total_df.dropna(axis=1)
            if 'download' in request.form:
                excel_buffer = io.BytesIO()

                # Create an ExcelWriter object to write multiple DataFrames to different sheets
                with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                    total_df.to_excel(writer, sheet_name='All', index=False)



                # Set the position of the BytesIO object to the beginning
                excel_buffer.seek(0)

                # Generate the response to download the Excel file
                response = make_response(excel_buffer.read())
                response.headers["Content-Disposition"] = "attachment filename=TY_1_4_data.xlsx"
                response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                return response

            
            document =RM_collection.find_one({"code":"RM_3_1"})
            tm_heading = document.get("Alert_title","")
            tm_sub_hedding="RM 3.1"
            if returning_data_enabled:
                return [data_from_col_df] 
            else:
                if session["user_role"]=="DGM/PO":
            
                    return render_template('rm1.html',notify=notify, total_df_3_1=total_df,
                                            tm_heading=tm_heading,
                                            tm_sub_hedding=tm_sub_hedding)
# CHANGES
@app.route("/RM_3_2",methods=['GET','POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def RM_3_2():
        if request.method == 'POST':
            userEmail = session['email_id']
            notify = notification(userEmail)
            if 'download' in request.form:
                user_input_date_str = '2022-01-01'
            elif 'user_input_date_str' in request.form:
                user_input_date_str = request.form.get('user_input_date_str')
                  

            else:
                user_input_date_str =  "2022-01-01"




            total_df = pd.DataFrame()


            user_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')

            # excel_writer = pd.ExcelWriter('RM_3_2_.xlsx', engine='openpyxl')


            pipeline = [
                {
                    "$unwind": "$TXNDATA"
                },
                {
                    "$match": {
                        "TXNDATA.Transaction Date":user_date,
                        "TXNDATA.Country Code":
                        {
                            "$in":["ALB","HTI"]
                        },
                        "TXNDATA.Cross Currency":"Yes"
                    }
                },
                {
                    "$group": {
                        "_id": "$TXNDATA.Account Number",
                        "data": {"$push": "$TXNDATA"}
                    }
                }
            ]

            agg_result = list(txn_collection.aggregate(pipeline))
            data_from_col_df = pd.DataFrame()

            for doc in agg_result:
                data_from_col_df = pd.concat([data_from_col_df,pd.DataFrame(doc['data'])])

            if not data_from_col_df.empty:
                total_df = pd.concat([total_df,data_from_col_df])
            
            if not total_df.empty:
                def generate_indicative_rule(row):
                    return f"Transaction made by {row['Account Number']} involving a {row['Country Code']} which is considered to be high risk from terrorist financing perspective triggered one of the RFI, {row['Account Number']} made the {row['Transaction Category']} transaction of amount {row['Transaction Amount']} in {row['Transaction Currency']}."    
                total_df['Indicative_rule'] = total_df.apply(generate_indicative_rule, axis=1)
            
            total_df=total_df.dropna(axis=1)
            
            if 'download' in request.form:
                excel_buffer = io.BytesIO()

                # Create an ExcelWriter object to write multiple DataFrames to different sheets
                with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                    total_df.to_excel(writer, sheet_name='All', index=False)



                # Set the position of the BytesIO object to the beginning
                excel_buffer.seek(0)

                # Generate the response to download the Excel file
                response = make_response(excel_buffer.read())
                response.headers["Content-Disposition"] = "attachment filename=TY_3_2_data.xlsx"
                response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                return response
            

            document =RM_collection.find_one({"code":"RM_3_2"})
            tm_heading = document.get("Alert_title","")
            tm_sub_hedding="RM 3.2"
            if returning_data_enabled:                
                return [total_df]
            else:
                if session["user_role"]=="DGM/PO": 
            
                    return render_template('rm1.html',notify=notify, total_df_rm_3_2=total_df,
                                            tm_heading=tm_heading,
                                            tm_sub_hedding=tm_sub_hedding,
                                        )

@app.route("/credit_card_monitoring",methods=["GET","POST"])
@secure_route(required_role=['DGM/PO'])
def credit_card_monitoring():
    crumbs_data = for_tm_ty_rm(TY_collection,"TY")
    user = users_collection.find_one({'role': 'DGM/PO'})
    notify = notification(user.get('emailid'))

    ituser = {'image': None}
    if user:
        ituser = users_collection.find_one({'emailid': user.get('emailid')})
        if ituser and 'image' in ituser:
            ituser['image'] = base64.b64encode(ituser['image']).decode('utf-8')

    return render_template('credit_card_monitoring.html',notify=notify,crumbs_data=crumbs_data,type='dashbord',dgmuser=ituser,role='DGM/PO')

@app.route('/TY_5_1',  methods=['GET', 'POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def TY_5_1():
    if request.method == 'POST':
        userEmail = session['email_id']
        notify = notification(userEmail)
        if 'download' in request.form:
            user_input_date_str = '2023-04-30'
        elif 'user_input_date_str' in request.form:
            user_input_date_str = request.form.get('user_input_date_str')
        else:
            user_input_date_str = '2023-04-30'
        end_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')
        current_values = threshold_values_from_col(TY_collection,'TY_5_1')
        start_date = end_date - timedelta(days=current_values['Y'])
        total_df=pd.DataFrame()
        pipeline = [
            {
                "$unwind":"$TXNDATA"
            },
            {
                "$match":{
                    "TXNDATA.Transaction Type":"Repayment",
                    "TXNDATA.Transaction Date":{
                        "$gte":start_date,
                        "$lt":end_date
                    }
                }
            },
            {
                "$group":{
                    "_id":"$TXNDATA.Card Number",
                    "data":{"$push":"$TXNDATA"}
                }
            }
        ]
        agg_result = list(txn_collection.aggregate(pipeline))
        for doc in agg_result:
            print(doc['_id'])
            df_data_from_col=pd.DataFrame()
            df_data_from_col = pd.DataFrame(doc['data'])
            if not df_data_from_col.empty:
                if df_data_from_col['Transaction Amount'].sum()>=current_values['x']:
                    temp_df = pd.DataFrame({
                        'Transaction Amount': [df_data_from_col['Transaction Amount'].sum()],
                        "Customer ID": [df_data_from_col['Customer ID'].unique()[0]],
                        "Nature of account": [df_data_from_col['Nature of account'].unique()[0]],
                        "Customer Profile": [df_data_from_col['Customer Profile'].unique()[0]],
                        "Customer Name": [df_data_from_col['Customer Name'].unique()[0]],
                        "Account Number": [df_data_from_col['Account Number'].unique()[0]],
                        'Card Number': [doc['_id']]
                    })
                    total_df = pd.concat([total_df, temp_df])
        total_df = total_df[['Card Number'] + [col for col in total_df.columns if col != 'Card Number']]
        if not total_df.empty:
            def generate_indicative_rule(row):
                return f"Credit card repayments of {row['Customer Name']} with Account Number {row['Account Number']}, Customer Id {row['Customer ID']} being an {row['Nature of account']} and {row['Customer Profile']} has triggered one of the RFI and raised an alert, greater than INR {current_values['x']} aggregated has {row['Transaction Amount']} in cash in {current_values['Y']} days."
            total_df['Indicative_rule'] = total_df.apply(generate_indicative_rule, axis=1)

        if 'download' in request.form:
            # Generate the CSV content and send it as a file download
            # csv_content = total_df.to_csv(index=False)
            # response = make_response(csv_content)
            # response.headers["Content-Disposition"] = "attachment filename=TM_1_1_Individual_data.csv"
            # response.headers["Content-Type"] = "text/csv"
            # return response
             # Create a BytesIO object to store the Excel file in memory
            excel_buffer = io.BytesIO()
            # Create an ExcelWriter object to write multiple DataFrames to different sheets
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                total_df.to_excel(writer, sheet_name='Individuals', index=False)
            # Set the position of the BytesIO object to the beginning
            excel_buffer.seek(0)
            # Generate the response to download the Excel file
            response = make_response(excel_buffer.read())
            response.headers["Content-Disposition"] = "attachment filename=TM_5_1_data.xlsx"
            response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            return response
        document =TY_collection.find_one({"code":"TY_5_1"})
        tm_heading = document.get("Alert_title","")
        tm_sub_hedding="TY 5.1"
        if returning_data_enabled:
            return [total_df]
        else:
            if session["user_role"]=="DGM/PO":
                return render_template("creaditcard.html",notify=notify,total_df=total_df,column_names=total_df.columns,
                            tm_heading=tm_heading,
                            t2_heading="Credit card repayments in cash",
                            tm_sub_hedding=tm_sub_hedding)


@app.route('/TY_5_3',  methods=['GET', 'POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def TY_5_3():
    if request.method == 'POST':
        userEmail = session['email_id']
        notify = notification(userEmail)
        mccode=""
        if 'download' in request.form:
            user_input_date_str = '2023-04-20'
        elif 'user_input_date_str' in request.form:
            user_input_date_str = request.form.get('user_input_date_str')
            mccode = request.form.get('mccode')
        else:
            user_input_date_str = '2023-04-20'
        
        if mccode is None or mccode == "":
            mccode = 5944
        
        end_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')
        current_values = threshold_values_from_col(TY_collection,'TY_5_3')
        start_date = end_date - timedelta(days=current_values['Y'])
        total_df=pd.DataFrame()

        pipeline = [
            {
                "$unwind": "$TXNDATA"
            },
            {
                "$match": {
                        "TXNDATA.MCC": mccode ,
                    "TXNDATA.Transaction Date": {
                        "$gte": start_date,
                        "$lt": end_date
                    }
                }
            },
            {
                "$group": {
                    "_id": "$TXNDATA.Card Number",
                    "data": {"$push": "$TXNDATA"}
                }
            }
        ]
        agg_result = list(txn_collection.aggregate(pipeline))
        for doc in agg_result:
            data_from_col_df = pd.DataFrame(doc['data'])
            if not data_from_col_df.empty:
                if data_from_col_df['Transaction Amount'].sum() > current_values['X']:
                    temp_df = pd.DataFrame({
                        "Transaction Amount": [data_from_col_df['Transaction Amount'].sum()],
                        "Customer ID": [data_from_col_df['Customer ID'].unique()[0]],
                        "Nature of account": [data_from_col_df['Nature of account'].unique()[0]],
                        'Transactions Count': [len(data_from_col_df)],
                        "Customer Name": [data_from_col_df['Customer Name'].unique()[0]],
                        "Account Number": [data_from_col_df['Account Number'].unique()[0]],
                        'Card Number': [int(doc['_id'])],
                        "Customer Profile": [data_from_col_df['Customer Profile'].unique()[0]],
                        'MCC code': [mccode],
                    })
                    total_df = pd.concat([total_df, temp_df])      
        if not total_df.empty:
            total_df = total_df[['Card Number'] + [col for col in total_df.columns if col != 'Card Number']]
            def generate_indicative_rule(row):
                return f"Credit card of {row['Customer Name']} with Account Number {row['Account Number']} ,Customer Id {row['Customer ID']} being an {row['Nature of account']} and {row['Customer Profile']} has triggered one of the RFI and raised an alert, greater than INR {current_values['X']} aggregated has {row['Transaction Amount']} for merchant category code (MCC {row['MCC code']}) for example: Jewellery, etc., in {current_values['Y']} days."
            total_df['Indicative_rule'] = total_df.apply(generate_indicative_rule, axis=1)
        if 'download' in request.form:
            excel_buffer = io.BytesIO()

            # Create an ExcelWriter object to write multiple DataFrames to different sheets
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                total_df.to_excel(writer, sheet_name='greaterthan4l', index=False)
                
            # Set the position of the BytesIO object to the beginning
            excel_buffer.seek(0)

            # Generate the response to download the Excel file
            response = make_response(excel_buffer.read())
            response.headers["Content-Disposition"] = "attachment filename=TY_1_1_data.xlsx"
            response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            return response
        document =TY_collection.find_one({"code":"TY_5_3"})
        tm_heading = document.get("Alert_title","")
        tm_sub_hedding="TY 5.3"
        if returning_data_enabled:
            return [total_df]
        else:
            if session["user_role"]=="DGM/PO":
                return render_template("creaditcard.html",notify=notify,total_df=total_df,column_names = total_df.columns,
                            t2_heading="Credit card repayments in cash",
                            tm_heading=tm_heading,
                            tm_sub_hedding=tm_sub_hedding)

@app.route('/TY_5_6',  methods=['GET', 'POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def TY_5_6():
    if request.method == 'POST':
 
        userEmail = session['email_id']
        notify = notification(userEmail)
        
        if 'download' in request.form:
            user_input_date_str = '2023-04-20'
        elif 'user_input_date_str' in request.form:
            user_input_date_str = request.form.get('user_input_date_str')
            mccode = request.form.get("mccode")
        else:
            user_input_date_str = '2023-04-20'
        current_values = threshold_values_from_col(TY_collection,'TY_5_6')
        mccode=""
        if mccode=="":
            mccode=5944
        else:
            mccode = int(mccode)

        end_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')
        start_date = end_date - timedelta(days=current_values['Y'])
        total_df=pd.DataFrame()
        pipeline = [
            {
                "$unwind": "$TXNDATA"
            },
            {
                "$match": {
                    "TXNDATA.MCC": mccode,
                    "TXNDATA.Transaction Date": {"$gte": start_date, "$lte": end_date}
                }
            },
            {
                "$group": {
                    "_id": "$TXNDATA.Card Number",
                    "data": {"$push": "$TXNDATA"}
                }
            }
        ]
        agg_result = list(txn_collection.aggregate(pipeline))
        for doc in agg_result:
            data_from_col_df = pd.DataFrame(doc['data'])
            if not data_from_col_df.empty:
                if data_from_col_df['Transaction Amount'].sum() > current_values['X'] and len(data_from_col_df) > current_values['N']:
                    temp_df = pd.DataFrame({
                        "Transaction Amount": [data_from_col_df['Transaction Amount'].sum()],
                        "Customer ID": data_from_col_df['Customer ID'].unique(),
                        "Nature of account": [data_from_col_df['Nature of account'].unique()[0]],
                        'Transactions Count': [len(data_from_col_df)],
                        "Customer Name": [data_from_col_df['Customer Name'].unique()[0]],
                        "Account Number": [data_from_col_df['Account Number'].unique()[0]],
                        'Card Number': [int(doc['_id'])],
                        "Customer Profile": [data_from_col_df['Customer Profile'].unique()[0]],
                        'MCC code': [mccode],
                    })
                    total_df = pd.concat([total_df, temp_df])
        if not total_df.empty:
            def generate_indicative_rule(row):
                return f"Credit card of {row['Customer Name']} with Account Number {row['Account Number']} ,Customer Id {row['Customer ID']} being an {row['Nature of account']} and {row['Customer Profile']} has triggered one of the RFI and raised an alert, WHERE {row['Card Number']} has made {row['Transactions Count']} transactions, which is more than {current_values['N']} credit card transaction at the same merchant aggregating to more than INR {current_values['X']} has Transaction Amount {row['Transaction Amount']}, spanning a period of {current_values['Y']} days."
            total_df['Indicative_rule'] = total_df.apply(generate_indicative_rule, axis=1)
        if 'download' in request.form:
            excel_buffer = io.BytesIO()

            # Create an ExcelWriter object to write multiple DataFrames to different sheets
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                total_df.to_excel(writer, sheet_name='greaterthan4L', index=False)
                
            # Set the position of the BytesIO object to the beginning
            excel_buffer.seek(0)

            # Generate the response to download the Excel file
            response = make_response(excel_buffer.read())
            response.headers["Content-Disposition"] = "attachment filename=TY_1_1_data.xlsx"
            response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            return response
        tm_sub_hedding="TY 5.6"
        document =TY_collection.find_one({"code":"TY_5_6"})
        tm_heading = document.get("Alert_title","")
        if returning_data_enabled:
            return [total_df]
        else:
            if session["user_role"]=="DGM/PO":
                return render_template("creaditcard.html",notify=notify,total_df=total_df,column_names = total_df.columns,
                            tm_heading=tm_heading,
                            tm_sub_hedding=tm_sub_hedding)

@app.route('/TY_5_7',  methods=['GET', 'POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def TY_5_7():
    if request.method == 'POST':
        userEmail = session['email_id']
        notify = notification(userEmail)
        # user_input_date_str = request.form['credit_card_5_1']
        user_input_date_str = '2023-04-20'  
        print(user_input_date_str)
        
        end_date = datetime.strptime(user_input_date_str, '%Y-%m-%d')
        current_values = threshold_values_from_col(TY_collection,'TY_5_7')

        start_date = end_date - timedelta(days=current_values['Y'])
        total_df=pd.DataFrame()
        percentage = current_values['Z']

        pipeline = [
    {
        "$unwind": "$TXNDATA"
    },
    {
        "$match": {
            "TXNDATA.Transaction Type":"Repayment",
            "TXNDATA.Transaction Date": {
                "$gte": start_date,
                "$lt": end_date
            }
        }
    },{
        "$group": {
            "_id": "$TXNDATA.Card Number",
            "data": {"$push": "$TXNDATA"}
        }
    }
]
        agg_result = list(txn_collection.aggregate(pipeline))
        data_from_col_df = pd.DataFrame(list(agg_result))
        for doc in agg_result:
            data_from_col_df = pd.DataFrame(doc['data'])
            if not data_from_col_df.empty:
                total_repayments = data_from_col_df['Transaction Amount'].sum()
                cash_df = data_from_col_df[data_from_col_df['Purchase Activity']=='cash']
                if not cash_df.empty:
                    cash_repayments = cash_df['Transaction Amount'].sum()
                    if cash_repayments>((total_repayments*50)/100):
                        if cash_repayments>=50000:
                                temp_df = pd.DataFrame({
                                    'Card Number': [int(doc['_id'])],
                                    'Transaction Type':cash_df['Transaction Type'].unique(),
                                    'Total Repayments':[total_repayments],
                                    'Cash Percentage in Total Repayments':(cash_repayments*100)/total_repayments,
                                    'Cash Repayments': [cash_repayments],
                                    "Account Number": [cash_df['Account Number'].unique()[0]],
                                    "Customer Name": [cash_df['Customer Name'].unique()[0]],
                                    "Customer ID": cash_df['Customer ID'].unique(),
                                    "Nature of account": [cash_df['Nature of account'].unique()[0]],
                                    "Customer Profile": [cash_df['Customer Profile'].unique()[0]],

                                })
                                total_df = pd.concat([total_df, temp_df])
        if not total_df.empty:
            def generate_indicative_rule(row):
                return f"Credit card of {row['Customer Name']} with Account Number {row['Account Number']},Customer Id {row['Customer ID']} being an {row['Nature of account']} and {row['Customer Profile']} has trigerred one of the RFI and raised an alert,Where {row['Card Number']}  has made the repayments greater than {current_values['Z']} percent of repayments totalling to INR {current_values['X']} or more in {current_values['Y']} days."    

            total_df['Indicative_rule'] = total_df.apply(generate_indicative_rule, axis=1)
                        
        tm_sub_hedding="TY 5.7"
        document =TY_collection.find_one({"code":"TY_5_7"})
        tm_heading = document.get("Alert_title","")


        if returning_data_enabled:
            return [total_df]
        else:
            if session["user_role"]=="DGM/PO":
                return render_template("creaditcard.html",notify=notify,total_df=total_df,column_names = total_df.columns,
                                       tm_heading=tm_heading,
                            tm_sub_hedding=tm_sub_hedding)



@app.route("/TY_7_2", methods=['GET', 'POST'])
def TY_7_2():
    current_values = threshold_values_from_col(TY_collection,'TY_7_2')
 
    userEmail = session['email_id']       
    notify = notification(userEmail)
    # Create an aggregation pipeline to filter data within MongoDB
    pipeline = [
        {
            "$unwind": "$TXNDATA"
        },
        {
            "$match": {
                "TXNDATA.Transaction Date": {"$exists": True},
                "TXNDATA.Acc_Opening_Date": {"$exists": True},
                "$expr": {
                    "$lte": [
                        { "$subtract": ["$TXNDATA.Transaction Date", "$TXNDATA.Acc_Opening_Date"] },
                        current_values['newly_opened'] * 24 * 60 * 60 * 1000  #3 months in milliseconds
                    ]
                }
            }
        },
        {
            "$group": {
                "_id": "$TXNDATA.Customer ID",
                "data": {"$push": "$TXNDATA"}
            }
        }
    ]

    agg_result = list(txn_collection.aggregate(pipeline))

    data_from_col_df = pd.DataFrame()

    for doc in agg_result:
        data_from_col_df = pd.concat([data_from_col_df,pd.DataFrame(doc['data'])])

    # print(data_from_col_df)
    data_from_col_df['Transaction Date'] = pd.to_datetime(data_from_col_df['Transaction Date'])

    data_from_col_df['YearMonth'] = data_from_col_df['Transaction Date'].dt.to_period('M').astype(str)

    monthly_turnover = data_from_col_df.groupby('Customer ID') 
    data_from_col_df_post_inactivity = pd.DataFrame()
    data_from_col_gt_40l = pd.DataFrame()
    for gpname,gpdata in monthly_turnover:
        if gpdata['Transaction Amount'].sum()>current_values['x1']:
            data_from_col_gt_40l = pd.concat([data_from_col_gt_40l,gpdata])
            gp_last_date = gpdata['Transaction Date'].unique()[-1]
            gp_last_date = pd.to_datetime(gp_last_date)
            pipeline = [
                {
                    "$unwind": "$TXNDATA"
                },
                {
                    "$match": {
                        "TXNDATA.Customer ID":gpname,
                        "TXNDATA.Transaction Date": {
                            "$gte":gp_last_date + timedelta(days=current_values['N'])
                        }
                    }
                },
                {
                    "$group": {
                        "_id": "$TXNDATA.Customer ID",
                        "data": {"$push": "$TXNDATA"}
                    }
                }
            ]
            agg_result = list(txn_collection.aggregate(pipeline))
            
            for doc in agg_result:
                data_from_col_df_post_inactivity = pd.concat([data_from_col_df_post_inactivity,pd.DataFrame(doc['data'])])
    data_from_col_df_post_inactivity = data_from_col_df_post_inactivity.dropna(axis=1)
    data_from_col_gt_40l = data_from_col_gt_40l.dropna(axis=1)
    data_from_col_gt_40l = data_from_col_gt_40l.drop_duplicates()
    if not data_from_col_gt_40l.empty:
        def generate_indicative_rule(row):
            return f"Monthly account turnover with Account Number {row['Account Number']}, Customer Id {row['Customer ID']} being an {row['Nature of account']} and {row['Customer Profile']} of more than INR {current_values['x1']} aggregated has {row['Transaction Amount']} in a newly opened operative account has triggered one of the RFI and raised an alert On Transaction Date {row['Transaction Date']} followed by a period of inactivity in the account."
        data_from_col_gt_40l['Indicative_rule'] = data_from_col_gt_40l.apply(generate_indicative_rule, axis=1)



    document =TY_collection.find_one({"code":"TY_7_2"})
    tm_heading = document.get("Alert_title","")
    tm_sub_hedding="TY 7.2"
    if 'download' in request.form:
            
                    excel_buffer = io.BytesIO()

                    # Create an ExcelWriter object to write multiple DataFrames to different sheets
                    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                        data_from_col_df_post_inactivity.to_excel(writer, sheet_name='sheet1', index=False)
                        data_from_col_gt_40l.to_excel(writer, sheet_name='sheet2', index=False)

                    # Set the position of the BytesIO object to the beginning
                    excel_buffer.seek(0)

                    # Generate the response to download the Excel file
                    response = make_response(excel_buffer.read())
                    response.headers["Content-Disposition"] = "attachment filename=TY_7_2_data.xlsx"
                    response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    return response

    if returning_data_enabled:
        return [data_from_col_gt_40l]
    else:
        if session["user_role"]=="DGM/PO":
            return render_template('ty7.html',notify=notify, total_df=data_from_col_df_post_inactivity,data_from_col_gt_40l=data_from_col_gt_40l,
                                   t1_title="All Transactions Post inactivity",t2_title="Accounts who made Transactions greater than 40L",
                                    tm_heading=tm_heading,
                                    tm_sub_hedding=tm_sub_hedding,dgmuser=image(),type='dashbord',role='DGM/PO'
                                )

@app.route('/revenue', methods=['GET', 'POST'])
@secure_route(required_role=['DGM/PO'])
def revenue():
    target_year = 2021
    total_df = pd.DataFrame()
    total_withdrawals_df = pd.DataFrame()

    pipeline = [
        {
            "$unwind": "$TXNDATA"
        },
        {
            "$match": {
                "TXNDATA.Transaction Currency": "INR",
                "TXNDATA.Transaction Category": {"$in": ["Withdrawals", "Deposits"]}
            }
        },
        {
            "$group": {
                "_id": {
                    "Account Number": "$Account Number",
                    "Transaction Category": "$TXNDATA.Transaction Category",
                    "Month": {"$month": "$TXNDATA.Transaction Date"}
                },
                "total_amount": {"$sum": "$TXNDATA.Transaction Amount"}
            }
        },
        {
            "$match": {
                "total_amount": {"$gte": 200000}
            }
        }
    ]

    agg_result = list(txn_collection.aggregate(pipeline))

    for doc in agg_result:
        account_number = doc['_id']['Account Number']
        category = doc['_id']['Transaction Category']
        month = doc['_id']['Month']
        total_amount = int(doc['total_amount'])

        if category == 'Deposits':
            total_df = pd.concat([total_df, pd.DataFrame([{'Account Number': account_number, 'Month': month, 'Transaction Amount': total_amount}])])
        elif category == 'Withdrawals':
            total_withdrawals_df = pd.concat([total_withdrawals_df, pd.DataFrame([{'Account Number': account_number, 'Month': month, 'Transaction Amount': total_amount}])])

    # Convert 'Month' column to strings
    total_df['Month'] = total_df['Month'].apply(lambda x: calendar.month_name[x])
    total_withdrawals_df['Month'] = total_withdrawals_df['Month'].apply(lambda x: calendar.month_name[x])


    deposits_data_by_month = total_df.groupby('Month')['Transaction Amount'].sum().reset_index()
    withdrawals_data_by_month = total_withdrawals_df.groupby('Month')['Transaction Amount'].sum().reset_index()

    # Fill missing months with zero transaction amounts
    all_months = [calendar.month_name[i] for i in range(1, 13)]
    missing_months_deposits = list(set(all_months) - set(deposits_data_by_month['Month']))
    missing_months_withdrawals = list(set(all_months) - set(withdrawals_data_by_month['Month']))

    for month in missing_months_deposits:
        deposits_data_by_month = deposits_data_by_month.append({'Month': month, 'Transaction Amount': 0}, ignore_index=True)

    for month in missing_months_withdrawals:
        withdrawals_data_by_month = withdrawals_data_by_month.append({'Month': month, 'Transaction Amount': 0}, ignore_index=True)

    # Convert 'Month' column to strings
    deposits_data_by_month['Month'] = deposits_data_by_month['Month'].apply(lambda x: str(x))
    withdrawals_data_by_month['Month'] = withdrawals_data_by_month['Month'].apply(lambda x: str(x))

    deposit_data = deposits_data_by_month.sort_values(by='Month')['Transaction Amount'].tolist()
    withdrawal_data = withdrawals_data_by_month.sort_values(by='Month')['Transaction Amount'].tolist()

    # deposit_data = total_df['Transaction Amount'].tolist()
    # withdrawal_data = total_withdrawals_df['Transaction Amount'].tolist()
    
    return jsonify(deposit_data=deposit_data,withdrawal_data=withdrawal_data)

@app.route('/no_accouts', methods=['GET', 'POST'])
@secure_route(required_role=['DGM/PO'])
def no_accouts():
    # Doneee with new schema
    total_savings_count = 0
    total_current_count = 0


    savings_count = txn_collection.count_documents({"TXNDATA.Type of account": "Savings Account"})
    current_count = txn_collection.count_documents({"TXNDATA.Type of account": "Current Account"})

    # Update the total counts
    total_savings_count += savings_count
    total_current_count += current_count

    # Return the total counts as JSON
    counts = [
    total_savings_count,
    total_current_count, 120
    ]

    return jsonify(counts=counts)



@app.route('/hightes_amount_yearly', methods=['GET', 'POST'])
@secure_route(required_role=['DGM/PO'])
def hightes_amount_yearly():
    # Extract the desired year from user_input_date --> Doneee with new schema
    desired_year = '2021'
    desired_year = int(desired_year.split('-')[0])
    # desired_year = user_input_date.year

    # Initialize a list to store the top 7 transactions
    top_transactions = []


    # Calculate the sum of deposits and withdrawals in the current collection for the last 3 months
    pipeline = [
        {
            "$unwind": "$TXNDATA"
        },
        {
            "$match": {
                "TXNDATA.Transaction Date": {"$gte": datetime(desired_year, 1, 1), "$lt": datetime(desired_year + 1, 1, 1)}
                }

        },
        {
            "$group": {
                "_id": "$TXNDATA.Account Number",
                "total": {"$sum": "$TXNDATA.Transaction Amount"}
                # "opening_date":"$Acc_Opening_Date"
            }
        }
    ]

    agg_result = list(txn_collection.aggregate(pipeline))

    for doc in agg_result:
        sum_df = pd.DataFrame({
        'Transaction Amount': [int(doc['total'])],
        'Account Number': [doc['_id']],
        })
        top_transactions.append(sum_df)

    # Combine all the filtered data into a single DataFrame
    total_df = pd.concat(top_transactions)

    # Sort the DataFrame by 'Transaction Amount' in descending order and get the top 7 transactions
    top_7_transactions = total_df.sort_values(by='Transaction Amount', ascending=False).head(7)
    account_numbers = top_7_transactions['Account Number'].tolist()
    transaction_amounts = top_7_transactions['Transaction Amount'].tolist()


    return jsonify(account_numbers=account_numbers,transaction_amounts=transaction_amounts)

@app.route('/lowest_amount_yearly', methods=['GET', 'POST'])
@secure_route(required_role=['DGM/PO'])
def lowest_amount_yearly():
    # Extract the desired year from user_input_date --> Doneee with new schema
    desired_year = '2021'
    desired_year = int(desired_year.split('-')[0])
    # desired_year = user_input_date.year

    # Initialize a list to store the top 7 transactions
    lowest_transactions = []


    pipeline = [
        {
            "$unwind": "$TXNDATA"
        },
        {
            "$match": {
                "TXNDATA.Transaction Date": {"$gte": datetime(desired_year, 1, 1), "$lt": datetime(desired_year + 1, 1, 1)}
                }

        },
        {
            "$group": {
                "_id": "$TXNDATA.Account Number",
                "minimum_amount": {"$min": "$TXNDATA.Transaction Amount"}
            }
        }
    ]

    agg_result = list(txn_collection.aggregate(pipeline))

    for doc in agg_result:
        min_df = pd.DataFrame({
            'Transaction Amount': [int(doc['minimum_amount'])],
            'Account Number': [doc['_id']],
        })
        lowest_transactions.append(min_df)

    # Combine all the filtered data into a single DataFrame
    total_df = pd.concat(lowest_transactions)

    # Sort the DataFrame by 'Transaction Amount' in descending order and get the top 7 transactions
    lowest_7_transactions = total_df.sort_values(by='Transaction Amount').head(7)
    account_numbers = lowest_7_transactions['Account Number'].tolist()
    transaction_amounts = lowest_7_transactions['Transaction Amount'].tolist()



    return jsonify(account_numbers=account_numbers, transaction_amounts=transaction_amounts)
   
@app.route('/accounts_created_count', methods=['GET', 'POST']) 
@secure_route(required_role=['DGM/PO'])
def accounts_created_count():
    target_year = 2015
    # Doneeee with new schemaa
    account_openings = {} 

    for target_month in range(1, 13):
        name_of_month = calendar.month_name[target_month]
        # Start date to get the starting date of the month
        start_date = datetime(target_year, target_month, 1)
        if target_month == 12:
            end_date = datetime(target_year + 1, 1, 1)
        else:
            end_date = datetime(target_year, target_month + 1, 1)
        count = txn_collection.count_documents({
            "TXNDATA.Acc_Opening_Date": {
                "$gte": start_date,
                "$lt": end_date
            }
        })
        # Count the number of account openings in the current month
        account_openings[name_of_month] = account_openings.get(name_of_month, 0) + count
    months = list(account_openings.keys())
    counts = list(account_openings.values())
    for month, count in account_openings.items():
        print(f"Account openings in {month}: {count}")

    return jsonify(months=months,counts=counts)



# @app.route('/reports')
# def reports():
#      return render_template('reports.html')


@app.route('/FINnetReports', methods=['GET', 'POST'])
@secure_route(required_role='IT Officer')
def FINnetReports():
    user = users_collection.find_one({'role': 'IT Officer'})

    ituser = {'image': ""}
    if user:
        ituser = users_collection.find_one({'emailid': user.get('emailid')})

        if ituser and 'image' in ituser:
            ituser['image'] = base64.b64encode(ituser['image']).decode('utf-8')

    return render_template('FINnet_report.html',ituser=ituser,type='FINnetReports',role='IT Officer')

def flatten_data(data, prefix=""):
    flattened_data = {}
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                flattened_data.update(flatten_data(value, f"{prefix}_{key}" if prefix else key))
            else:
                flattened_data[f"{prefix}_{key}" if prefix else key] = value
    elif isinstance(data, list):
        for index, item in enumerate(data):
            flattened_data.update(flatten_data(item, f"{prefix}_{index}" if prefix else str(index)))
    return flattened_data

def find_all_approved_objects(data, approved_objects, parent_data=None):
    # Traverse the nested structure and filter out approved objects
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'finalReport' and value == 'Approved':
                if parent_data is not None:
                    # Flatten the data from both parent and Case_Details
                    flattened_data = flatten_data(parent_data)
                    flattened_data.update(flatten_data(data))
                    approved_objects.append(flattened_data)
                    flattened_data = flatten_data(parent_data)
                    print("Flattened data before update:", flattened_data)

            elif isinstance(value, (dict, list)):
                find_all_approved_objects(value, approved_objects, parent_data=data)
    elif isinstance(data, list):
        for item in data:
            find_all_approved_objects(item, approved_objects, parent_data=parent_data)

@app.route('/online_STR_download_page',methods=['POST','GET'])
@secure_route(required_role='IT Officer')
def online_STR_download_page():
    
        data = []
        all_collections = [CASE_collection]
        array_names = ["output_data1", "output_data2", "output_data3"]
        for collection, array_name in product(all_collections, array_names):
            pipeline = [
                {
                    "$unwind": f"${array_name}"
                },
                {
                    "$match": {
                        f"{array_name}.finalReport":"Approved",
                        f"{array_name}.finalReport_Submited_on":{"$exists":True}
                    }
                },
                {
                    "$group": {
                "_id": "code",
                "data":{"$push":{
                    "AccountNumber": f"${array_name}.Account Number",
                    "Date": f"${array_name}.finalReport_Submited_on",
                    "TicketId": f"${array_name}.ticket_id",
                }},

            }
                }
            ]
            data_from_collection = collection.aggregate(pipeline)
            for doc in data_from_collection:
                data = (doc['data'])
        user = users_collection.find_one({'role': 'IT Officer'})

        ituser = {'image': ""}
        if user:
            ituser = users_collection.find_one({'emailid': user.get('emailid')})

            if ituser and 'image' in ituser:
                ituser['image'] = base64.b64encode(ituser['image']).decode('utf-8')  

        return render_template('online_STR_Downloads.html',data=data,type='FINnetReports',ituser=ituser,role='IT Officer')

@app.route('/download_pdf_str', methods=['POST'])
@secure_route(required_role=['IT Officer'])
def download_pdf_str():

    accNo = request.form.get('accNumber')
    dateSubmited = request.form.get('date')
    TicketId = request.form.get('TicketId')
    formate = request.form.get('formate')

    date_object = datetime.strptime(dateSubmited, "%Y-%m-%d %H:%M:%S")


    all_collections = [CASE_collection]
    array_names = ["output_data1", "output_data2", "output_data3"]
    for collection, array_name in product(all_collections, array_names):
        query = {f"{array_name}.ticket_id": TicketId,f"{array_name}.finalReport": "Approved"}
        cursor = collection.find(query)
        for document in cursor:
            # Process the matched document as needed
            matching_object = document.get(array_name, {})
    if matching_object:
            for obj in matching_object:
                print("his is obj : ",obj)
                if obj["ticket_id"] == TicketId:
                    temp_dir = tempfile.mkdtemp()
                    temp_csv_filename = os.path.join(temp_dir, "str_data.csv")
                    temp_pdf_filename = os.path.join(temp_dir, "str_data.pdf")
                    flattened_data_list = [flatten_data(obj) ]
                    required_columns = [ 'Account Number','Customer ID', 'Nature of account', 'Customer Profile',
                                        'PAN', 'Type of account',
                                        'Transaction Amount', 'Transaction Date', 'Transaction Type', 'Transaction Category',
                                        'SuspeciousDuoCrime', 'Classification',
                                        'SuspeciousDuoComplexTr', 'SuspeciousDuoNoeco', 'terrorisumFunding',
                                        'LEAinformed' , 'reportCase',
                                        'additionalInfo', 'priorityRAG', 'cumulativeCrtTurnover',
                                        'cumulativeDTTurnover', 'cumulativeDepositTurnover', 'cumulativeWithdrawalTurnover',
                                        'NumTransactionReport', 'Raise_STR']    
                    df = pd.DataFrame(flattened_data_list)
                    print("DataFrame content:", df)
                    df.to_csv(temp_csv_filename, index=False)
                    list_of_dicts = df.to_dict(orient='records')
                    # Convert CSV to PDF using reportlab
                    generate_pdf_from_csv(temp_csv_filename, temp_pdf_filename, list_of_dicts)
                    if os.path.exists(temp_pdf_filename):
                        if formate == "PDF":
                           return send_from_directory(temp_dir, "str_data.pdf", as_attachment=True)
                        if formate == "CSV":
                           return send_from_directory(temp_dir, "str_data.csv", as_attachment=True)

    return render_template('FINnet_report.html', message='No approved cases found',type='FINnetReports',role='IT Officer')



def generate_pdf_from_csv(csv_filename, pdf_filename, approved_objects):
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter, bottomMargin=20)
    styles = getSampleStyleSheet()

    story = []

    for obj in approved_objects:
        obj_data = []

        for key, value in obj.items():
            # Wrap the text in each column
            if value is not None:
                wrapper = textwrap.TextWrapper(width=70)
                wrapped_lines = wrapper.wrap(text=str(value))
                wrapped_text = "\n".join(wrapped_lines)  # Merge wrapped lines into a single string
                obj_data.append([key, wrapped_text]) 

        # Create a table with the object's data
        obj_table = Table(obj_data, colWidths=[200, 400],  # Adjust the column widths as needed
                          style=[
                              ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Add grid lines
                              ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Add background color to header row
                              ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Set text color in header row
                              ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Center align all cells
                              ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Middle align all cells
                              ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),  # Inner grid lines
                              ('BOX', (0, 0), (-1, -1), 0.25, colors.black),  # Add box around the table
                          ])
        
       
       

        story.append(obj_table)
        story.append(Spacer(1, 70))

        # Add a page break after each object's data (limit to 2 pages)

        all_names = ["MLRO","CM/PO", "AGM"]
        names_table_data = [[all_names[0], all_names[1],all_names[2]]]
        names_table = Table(names_table_data, colWidths=[180, 180, 180],
                    style=[
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
                        ('ALIGN', (2, 0), (-1, -1), 'RIGHT')
                        
                    ])
        story.append(names_table)

        story.append(Spacer(1, 50))

        dgm_names = ["DGM \n (Approved)"]
        dgm_table_data = [[dgm_names[0]]]

        
        dgm_table = Table(dgm_table_data,   # Adjust column widths as needed
                            style=[
                        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),

                            ])
        story.append(dgm_table)


        story.append(PageBreak())
        

    # Add the main story to the PDF
    pdf.build(story)

    buffer.seek(0)
    with open(pdf_filename, 'wb') as f:
        f.write(buffer.read())


        



# def generate_pdf_from_csv(csv_filename, pdf_filename, approved_objects,caseComments,caseDetails,type):
#     buffer = BytesIO()
#     pdf = SimpleDocTemplate(buffer, pagesize=letter, bottomMargin=20)
#     styles = getSampleStyleSheet()

#     story = []

#     for obj in approved_objects:

#         if type == 'online':

#             obj_data = "(1)Full name and address of the account holder:"f"{obj.get('Customer Name', 'None')}",f"{obj.get('Address', 'None')}","Pincode-", f"{obj.get('Pincode', 'None')}",f"{obj.get('City', 'None')}""(2) Date of Birth (for Individual)/date of Incorporation for the company):"f"{obj.get('DOB', 'None')}""(3)Pan No:"f"{obj.get('PAN', 'None')}""(4) Passport No:""None""(5)Other Identification documents:" "None""(6) IEC Code:""None""(7)GSTIN:" "None""(8)Mobile Number/Landline No:-" f"{obj.get('Mobile Number', 'None')}","e-mail id:" "None""(9)Other facilities availed:" "None""(10) Risk category:" f"{obj.get('priorityRAG', 'None')}""(11) Name of the authorized signing Authorities:" "None""(12)KYC Compliance status:" "None""(13) Date of last KYC updation:" "None""(14)Profile/nature of business:" "None""(15)Annual Income as declared in KYC(Amount in Rs. in Lacs):""None""(16)Annual Turnover of business as declared in KYC(Amount in Rs in Lacs):" "None""(17) Beneficial owner is determined under Rule 9(3) of PMLA Rulest:" "None""(18) Bank and Branch details:" f"{obj.get('Bank Name', 'None')}","Branch", f"{obj.get('Bank Location/Address', 'None')}",f"{obj.get('Bank State', 'None')}""(19) Bank Account No:"f"{obj.get('Account Number', 'None')}""(20) Bank Account Type:" f"{obj.get('Type of account', 'None')}""(21) Bank A/c opened on:" f"{obj.get('Acc_Opening_Date', 'None')}""(22)Bank Account Status:""None""(23)Quantum of transactions for current year:""None""(24)Debit Turnover: Rs." f"{obj.get('cumulativeWithdrawalTurnover', 'None')}""Lacs (in cash Rs.0.00 Lacs)and Credit Turnover: Rs." f"{obj.get('cumulativeDepositTurnover', 'None')}""Lacs(in cash Rs.0.00 Lacs)""(24)Quantum of transactions for previous years:" "None"," Debit Turnover: Rs.", "0.00", "Lacs tin cash Rs 0.00 Lacs) and Credit Turnover:Rs", "0.00","Lacs(in cash Rs.0.00 LacsIFY 2021-22: Debit Turnover: Rs. 0.00 Lacs (in cash Rs. 0:00 Lacsjand Credit Turnover: Rs.0.00 Lacs(in cash Rs.0.00 Lacs), FY 2020-21:Debit Turnover: Rs 0.00 Lacs (in cash Rs.0.00 Lacs)and Credit Turnover: Rs.0.00 Lacs(in cash Rs.0.00 Lacs).","(25)Balance in account on date of filing STR:", "None","(26) Details of earlier STRs filed on account or account holders/related persons:", "None","(27) Reactive STRs:", "None","(28)Adverse Media Report:", f"{obj.get('reportCase', 'None')}","(29) Ground of Suspicion: (a)"f"{obj.get('Customer Name', 'None')} whose date of birth is {obj.get('DOB', 'None')} opend an {obj.get('Type of account' , 'None')} on {obj.get('Acc_Opening_Date',)} (b) Declared profile is WHETHER EMPLOYED OR UNEMPLOYYED & income as SOME RUPEES to less then SOME LEMMITED AMOUNT RUPEES (c) The reported customer also having {obj.get('Type of account','None')} with a/c.no:{obj.get('Account Number','None')} opened on {obj.get('Acc_Opening_Date','None')} where in Rs.{obj.get('cumulativeCrtTurnover','None')} of tturnover within 5 montths is observed through huge UPI/IMPS transactions (d) on observing transactions in both the accounts(CA & SB A/c),we noticed that regularlyy amountt are comming from a/c:{obj.get('Account Number')} (a/c of the reported a/c holder maintained with other bank-same mobile no)through IMPS (e)The reported CA and SB a/c's are maintained with SOME BANK NAME WITH THERE ADDRESS ANDDETAILS OF WHICH TTHERE ARE ANY FLOCKED DEVOTEES every day (f) Huge UPI/IMPS( SOME NUMBER OF DEBIS AND SOME NUMBER OF CREDITS-many to many ) transactions to the tune of Rs. {obj.get('cumulativeDTTurnover','None')} within the span period of SOME months is observed (g) Huge turnover and huge UPI/IMPS transaction in the reported a/c and also in other SB a/c which are opend throungh online,within period below SOME months not matching with declared profile(graduate) & annual income is looking suspicious.Hence,STR is filed (30) Details of Investigation :", *[f"{key}:{value}" for key,value in caseDetails.items()], "(a)"f"{caseComments['mlrocomment']}""(b)"f"{caseComments['cmcomment']}""(c)"f"{caseComments['agmcomment']}""(d)"f"{caseComments['dgmcomment']}"
#         if type == 'offline':

#             obj_data = "(1)Full name and address of the account holder:"f"{obj.get('personname', 'None')}",f"{obj.get('Address', 'None')}","Pincode-", f"{obj.get('Pincode', 'None')}",f"{obj.get('City', 'None')}""(2) Date of Birth (for Individual)/date of Incorporation for the company):"f"{obj.get('DOB', 'None')}""(3)Pan No:"f"{obj.get('PAN', 'None')}""(4) Passport No:""None""(5)Other Identification documents:" "None""(6) IEC Code:""None""(7)GSTIN:" "None""(8)Mobile Number/Landline No:-" f"{obj.get('Mobile Number', 'None')}","e-mail id:" "None""(9)Other facilities availed:" "None""(10) Risk category:" f"{obj.get('scenario', 'None')}""(11) Name of the authorized signing Authorities:" "None""(12)KYC Compliance status:" "None""(13) Date of last KYC updation:" "None""(14)Profile/nature of business:" "None""(15)Annual Income as declared in KYC(Amount in Rs. in Lacs):""None""(16)Annual Turnover of business as declared in KYC(Amount in Rs in Lacs):" "None""(17) Beneficial owner is determined under Rule 9(3) of PMLA Rulest:" "None""(18) Bank and Branch details:" f"{obj.get('Bank Name', 'None')}","Branch", f"{obj.get('Bank Location/Address', 'None')}",f"{obj.get('Bank State', 'None')}""(19) Bank Account No:"f"{obj.get('AccountNumber', 'None')}""(20) Bank Account Type:" f"{obj.get('AccountType', 'None')}""(21) Bank A/c opened on:" f"{obj.get('DateofOpening', 'None')}""(22)Bank Account Status: "f"{obj.get('AccountStatus','None')}""(23)Quantum of transactions for current year:""None""(24)Debit Turnover: Rs." f"{obj.get('CummulativeCashDepositTurnover', 'None')}""Lacs (in cash Rs.0.00 Lacs)and Credit Turnover: Rs." f"{obj.get('CummulativeCerditTurnover', 'None')}""Lacs(in cash Rs.0.00 Lacs)""(24)Quantum of transactions for previous years:" "None"," Debit Turnover: Rs.", "0.00", "Lacs tin cash Rs 0.00 Lacs) and Credit Turnover:Rs", "0.00","Lacs(in cash Rs.0.00 LacsIFY 2021-22: Debit Turnover: Rs. 0.00 Lacs (in cash Rs. 0:00 Lacsjand Credit Turnover: Rs.0.00 Lacs(in cash Rs.0.00 Lacs), FY 2020-21:Debit Turnover: Rs 0.00 Lacs (in cash Rs.0.00 Lacs)and Credit Turnover: Rs.0.00 Lacs(in cash Rs.0.00 Lacs).","(25)Balance in account on date of filing STR:"f"{obj.get('amount', 'None')}""(26) Details of earlier STRs filed on account or account holders/related persons:"f"{obj.get('amount', 'None')}""(27) Reactive STRs:", "None","(28)Adverse Media Report:", f"{obj.get('RuleScenario', 'None')}","(29) Ground of Suspicion: (a)"f"{obj.get('personname', 'None')} whose date of birth is {obj.get('DOB', 'None')} opend an {obj.get('AccountType' , 'None')} on {obj.get('DateofOpening',)} (b) Declared profile is WHETHER EMPLOYED OR UNEMPLOYYED & income as SOME RUPEES to less then SOME LEMMITED AMOUNT RUPEES (c) The reported customer also having {obj.get('AccountType','None')} with a/c.no:{obj.get('RelatedAccountNumber','None')} opened on {obj.get('DateofOpening','None')} where in Rs.{obj.get('DispositionOfFunds','None')} of turnover within 5 montths is observed through huge UPI/IMPS transactions (d) on observing transactions in both the accounts(CA & SB A/c),we noticed that regularlyy amountt are comming from a/c:{obj.get('AccountNumber')} (a/c of the reported a/c holder maintained with other bank-same mobile no)through IMPS (e)The reported CA and SB a/c's are maintained with SOME BANK NAME WITH THERE ADDRESS ANDDETAILS OF WHICH TTHERE ARE ANY FLOCKED DEVOTEES every day (f) Huge UPI/IMPS( SOME NUMBER OF DEBIS AND SOME NUMBER OF CREDITS-many to many ) transactions to the tune of Rs. {obj.get('CummulativeDebitTurnover','None')} within the span period of SOME months is observed (g) Huge turnover and huge UPI/IMPS transaction in the reported a/c and also in other SB a/c which are opend throungh online,within period below SOME months not matching with declared profile(graduate) & annual income is looking suspicious.Hence,STR is filed (30) Details of Investigation :" "(a)"f"{obj.get('scenario')}" f"{obj.get('RuleScenario')}" f"{obj.get('Guidance')}" "(b)"f"{caseComments['Ros_comments']}""(c)"f"{caseComments['AGM_comments']}""(d)"f"{caseComments['DGM_comments']}""(e)"f"{obj.get('Remark')}"



#         obj_text = str(obj_data)[1:-1]
        

#         # Create a Paragraph for the object's text
#         obj_paragraph = Paragraph(obj_text.replace("'"," "), styles['Normal'])

#         story.append(obj_paragraph)
#         # story.append(Spacer(1, 12))

#         # Add a page break after each object's data (limit to 2 pages)
#         story.append(PageBreak())

# # Add the main story to the PDF
#     pdf.build(story)

#     buffer.seek(0)
#     with open(pdf_filename, 'wb') as f:
#        f.write(buffer.read())


# offline pdf str download

def filter_and_flatten_data():
    query = {"data.comment.Final_Approval": "Approve"}
    projection = {
        "_id": 0,
        "data.$": 1 
    }
    approved_data = list(offline_collection.find(query, projection))

    # Extract only the relevant object from the array
    flattened_data = [entry["data"][0] for entry in approved_data if entry.get("data")]

    return flattened_data if flattened_data else None

# Route to handle PDF download
@app.route('/download_pdf_offline_str', methods=['POST'])
@secure_route(required_role=['IT Officer'])
def download_pdf_offline_str():
    
    accNo = request.form.get('accNumber')
    dateSubmited = request.form.get('date')
    TicketId = request.form.get('TicketId')
    formate = request.form.get('formate')
    date_object = datetime.strptime(dateSubmited, "%Y-%m-%d %H:%M:%S")

    all_collections = [offline_collection]
    array_names = ["data"]
    for collection, array_name in product(all_collections, array_names):
        query = {f"{array_name}.ticket_id": TicketId,f"{array_name}.finalReport": "Approved"}
        cursor = collection.find(query)
        for document in cursor:
            # Process the matched document as needed
            matching_object = document.get(array_name, {})
    if matching_object:
            for obj in matching_object:
                print("his is obj : ",obj)
                if obj["ticket_id"] == TicketId:
                    temp_dir = tempfile.mkdtemp()
                    temp_csv_filename = os.path.join(temp_dir, "str_offline_data.csv")
                    temp_pdf_filename = os.path.join(temp_dir, "str_offline_data.pdf")
                    flattened_data_list = [flatten_data(obj) ]
                    print("flattened_data_list : ",flattened_data_list)
                    required_columns = [ 'Account Number','Customer ID', 'Nature of account', 'Customer Profile',
                                        'PAN', 'Type of account',
                                        'Transaction Amount', 'Transaction Date', 'Transaction Type', 'Transaction Category',
                                        'SuspeciousDuoCrime', 'Classification',
                                        'SuspeciousDuoComplexTr', 'SuspeciousDuoNoeco', 'terrorisumFunding',
                                        'LEAinformed' , 'reportCase',
                                        'additionalInfo', 'priorityRAG', 'cumulativeCrtTurnover',
                                        'cumulativeDTTurnover', 'cumulativeDepositTurnover', 'cumulativeWithdrawalTurnover',
                                        'NumTransactionReport', 'Raise_STR']
                    df = pd.DataFrame(flattened_data_list)
                    print("DataFrame content:", df)
                    df.to_csv(temp_csv_filename, index=False)
                    list_of_dicts = df.to_dict(orient='records')
                    # Convert CSV to PDF using reportlab
                    generate_pdf_from_csv(temp_csv_filename, temp_pdf_filename, list_of_dicts)

                    if os.path.exists(temp_pdf_filename):
                        if formate == "PDF":
                           return send_from_directory(temp_dir, "str_offline_data.pdf", as_attachment=True)
                        if formate == "CSV":
                           return send_from_directory(temp_dir, "str_offline_data.csv", as_attachment=True)
                        
                        # print("hogayaaa.............")

    return render_template('FINnet_report.html', message='No approved cases found',type='FINnetReports',role='IT Officer')




@app.route('/download_csv_str', methods=['GET'])
@secure_route(required_role=['IT Officer'])
def download_csv_str():
    data = CASE_collection.find_one()
    if data:
        approved_objects = []
        find_all_approved_objects(data, approved_objects)
        if approved_objects:
            temp_dir = tempfile.mkdtemp()
            temp_filename = os.path.join(temp_dir, "approved_data.csv")
            flattened_data_list = [flatten_data(obj) for obj in approved_objects]
            # Extract only the required columns
            required_columns = ['Customer ID', 'Nature of account', 'Customer Profile', 'NPO/Charity', 'Real estate agent/dealer',
                                'Precious Metal Dealer', 'PAN', 'Type of account', 'Account Number', 'Acc_Opening_Date',
                                'Transaction Amount', 'Transaction Date', 'Transaction Type', 'Transaction Category',
                                'Transaction Currency','sentTo', 'SuspeciousDuoCrime', 'Classification',
                                'SuspeciousDuoComplexTr', 'SuspeciousDuoNoeco', 'terrorisumFunding',
                                'Investigation', 'LEAinformed', 'LEADetails', 'reportCase',
                                'additionalInfo', 'priorityRAG', 'cumulativeCrtTurnover',
                                'cumulativeDTTurnover', 'cumulativeDepositTurnover', 'cumulativeWithdrawalTurnover',
                                'NumTransactionReport', 'remark', 'fileName']
            df = pd.DataFrame(flattened_data_list)[required_columns]
            df.to_csv(temp_filename, index=False)
            return send_file(temp_filename, as_attachment=True)
    return render_template('FINnet_report.html', message='No approved cases found',type='FINnetReports',role='IT Officer')

@app.route('/download_csv/<filename>', methods=['GET'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def download_csv(filename):
    # Fetch data from MongoDB based on the filename
    data = Finnet_collection.find_one({'name': filename.replace('.csv', '')})
    if data is not None:
        csv_data = data.get('data', [])
        if csv_data:
            temp_dir = tempfile.mkdtemp()
            # Create a temporary CSV file
            temp_filename = os.path.join(temp_dir, filename)
            with open(temp_filename, 'w', newline='') as csvfile:
                fieldnames = csv_data[0].keys() if csv_data else []
                csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                csv_writer.writeheader()
                csv_writer.writerows(csv_data)
            def remove_temp_dir(response):
                # Delete the temporary directory and its contents
                shutil.rmtree(temp_dir)
                return response
            return send_file(temp_filename, as_attachment=True)
    return render_template('404.html'), 404

@app.route('/<report_type>')
@secure_route(required_role=['IT Officer','DGM/PO'])
def display_report(report_type):
    email = session['email_id']
    user = users_collection.find_one({'emailid':email})
    notify = notification(email)

    ituser = {'image': None}
    if user:
        ituser = users_collection.find_one({'emailid': user.get('emailid')})
        if ituser and "image" in ituser:
            ituser['image'] = base64.b64encode(ituser['image']).decode('utf-8')

    if report_type == 'NTR':
        reports_list_heading = "NTR"
        reports_list_data = ["Account Details", "Account Personal Relation", "GT 1", "KC 2", "TC 1", "TC 2", "TS 1", "TS 2", "TS 3"]
    elif report_type == 'CRT':
        reports_list_heading = "CTR"
        reports_list_data = ["Account Details", "Account Personal Relation", "KC 1", "KC 2", "TC 1", "TC 2"]
    elif report_type == 'CWTR':
        reports_list_heading = "CWTR"
        reports_list_data = ["Account Details", "Account Personal Relation", "KC 1", "KC 2", "CB 1"]
    else:
        # Handle other cases or invalid report types here
        return "Invalid report type"

    return render_template('ntr.html', reports_list_data=reports_list_data, reports_list_heading=reports_list_heading,notify=notify,type='dashbord',dgmuser=ituser,role='DGM/PO')



# ==============Dashboard Section====================
# def count_documents_with_empty_allocate_to(collection, field_name):
#     count = 0
#     for doc in collection:
#         if doc.get(field_name) is None:
#             count += 1
#     return count

@app.route('/ITdashboard', methods=['GET'])
@secure_route(required_role='IT Officer')
def ITdashboard():
            user = users_collection.find_one({'role': 'IT Officer'})
            email = session.get('email_id')
            print('emailidddd:',email)
            if 'email_id' not in session:
                return redirect(url_for('post_login'))
            ituser = {'image': None}
            if user:
                ituser = users_collection.find_one({'emailid': user.get('emailid')})

                if ituser and 'image' in ituser:
                    ituser['image'] = base64.b64encode(ituser['image']).decode('utf-8')    
            
            dayData = user.get('dayData', [])
            dayData = list(dayData)

            # print("daaaaaaa",dayData)


            count = 0
            countSubmited = 0

    # Query the first MongoDB collection
            documents1 = TY_collection.find()
            
            for document in documents1:
                for array_name in ["output_data1", "output_data2", "output_data3"]:  # Replace with your actual array names
                    if array_name in document:
                        for obj in document[array_name]:
                            if "allocate_to" in obj and obj["allocate_to"] is None:
                                count += 1
                            else:
                                countSubmited +=1

            # Query the second MongoDB collection
            documents2 = TM_collection.find()
            
            for document in documents2:
                for array_name in ["output_data1", "output_data2", "output_data3"]:  # Replace with your actual array names
                    if array_name in document:
                        for obj in document[array_name]:
                            if "allocate_to" in obj and obj["allocate_to"] is None:
                                count += 1
                            else:
                                countSubmited +=1
            # Query the second MongoDB collection
            documents3 = RM_collection.find()
            
            for document in documents3:
                for array_name in ["output_data1", "output_data2", "output_data3"]:  # Replace with your actual array names
                    if array_name in document:
                        for obj in document[array_name]:
                            if "allocate_to" in obj and obj["allocate_to"] is None:
                                count += 1
                            else:
                                countSubmited +=1
            # print("count11111",count)
            # print("countsubbb222",countSubmited)
            # print("Before Update: ", user)
            

            current_datetime = datetime.now()
            # Extract only the date and set the time to midnight
            current_date = str(current_datetime.date())
            # current_date = '2024-01-10'
            update_perday_data(user, current_date, count)

            # print('done storing.............. ')
            dashboardCount = users_collection.find_one({'emailid': user["emailid"],"status":'Approved'})
            perdayData = dashboardCount.get('perdayData', [])
            perday_Data = []
            for perdayDatait in perdayData:
                perday_Data.append(perdayDatait)
            # print("ppppiiittt",perday_Data)
            
            


            numUsers = users_collection.count_documents({'role':'MLRO','status':'Approved','leaveStatus':'Working'})

            mlrosinfo = users_collection.find({'role':'MLRO','status':'Approved','leaveStatus':'Working'},
                                              {'name': 1, 'emailid': 1, 'image': 1})

            mlroDetails = {}
            
            for doc in mlrosinfo:
                name = doc.get('name', '')
                emailid = doc.get('emailid', '')
                image = doc.get('image', '')
                if image:
                    image_base64 = base64.b64encode(image).decode('utf-8')
                else:
                    image_base64 = None
                
                mlroDetails[doc['name']] = {'emailid': emailid,'image_base64': image_base64}
                    
            cm_users_count = users_collection.count_documents({'role': {'$in': ['AGM', 'CM/SM']}, 'status': 'Approved', 'leaveStatus': 'Working'})

            cm_and_agm_info = users_collection.find(
                {'role': {'$in': ['AGM', 'CM/SM']}, 'status': 'Approved', 'leaveStatus': 'Working'},
                {'name': 1, 'emailid': 1, 'role': 1, 'image': 1})            
            cmDetails = {}

            for cmdoc in cm_and_agm_info:
                name = cmdoc.get('name', '')
                emailid = cmdoc.get('emailid', '')
                role = cmdoc.get('role', '')
                image = cmdoc.get('image', '')
                if image:
                    image_base64 = base64.b64encode(image).decode('utf-8')
                else:
                    image_base64 = None
                

                # Add details to the dictionary with name, emailid, and role
                cmDetails[cmdoc['name']] = {'emailid': emailid, 'role': role,'image_base64': image_base64}

            if 'success_message' in session:
                msg = session['success_message']
                session.pop('success_message')
            else:
                msg=None
            return render_template("IT Officer.html", count=count,countSubmited=countSubmited,numUsers=numUsers,mlroDetails=mlroDetails,cmUsers=cm_users_count,cmDetails=cmDetails,ituser=ituser,perdayDatait=perday_Data,role='IT Officer',type='ITdashboard',msg=msg)

def update_perday_data(user, current_date, count):
    day_data = user.get('perdayData', [])
    # print("countttttts", count)
    # print("ppppp", day_data)

    for data in day_data:
        if data.get(current_date) is not None:
            return

    new_entry = {current_date: count}
    day_data.append(new_entry)
    
    users_collection.update_one({'_id': user['_id']}, {'$set': {'perdayData': day_data}})

@app.route('/allocate', methods=['GET','POST'])
@secure_route(required_role='IT Officer')
def allocate():
    success_message = ""
    if request.method == "POST":
        current_datetime = datetime.now() 
        # Extract only the date and set the time to midnight
        current_date = current_datetime.date()
        midnight_datetime = datetime.combine(current_date, datetime.min.time())

        user = users_collection.find_one({'role': 'IT Officer'})

        ituser = {'image': None}
        if user:
            ituser = users_collection.find_one({'emailid': user.get('emailid')})

            if ituser and 'image' in ituser:
                ituser['image'] = base64.b64encode(ituser['image']).decode('utf-8') 

        # Step 1: Fetch all Mlros email IDs from the "authentication" collection
        mlros_emails = [mlro["emailid"] for mlro in users_collection.find({"role": "MLRO","status":"Approved","leaveStatus":"Working"})]

        print("mlros_emails",mlros_emails)

        try:
            # Step 2: Query objects with a null "allocate_to" field
            collections = [TM_collection,TY_collection,RM_collection]
            for collection in collections:
                for document in collection.find():
                    for array_name in ["output_data1", "output_data2", "output_data3"]:
                        if array_name in document:
                            for obj in document[array_name]:
                                if "allocate_to" in obj and obj["allocate_to"] is None:
                                    random_mlro_email = random.choice(mlros_emails)  # Implement logic to get random MLRO email
                                    obj["allocate_to"] = random_mlro_email
                                    collection.update_one(
                                        {"_id": document["_id"]},
                                        {"$set": {f"{array_name}.$[elem].allocate_to": random_mlro_email,f"{array_name}.$[elem].alert_allocated_on": midnight_datetime}},
                                        array_filters=[{"elem.ticket_id": obj["ticket_id"]}]
                                    )
                                    # Add the ticket_id to the "authentication" collection
                                    users_collection.update_one(
                                        {"emailid": random_mlro_email},
                                        {"$push": {"allocated_tickets": obj["ticket_id"]}}
                                    )
                                    update_perdaydata(random_mlro_email, current_date)

            count = 0
            countSubmited = 0
            collections = [TM_collection,TY_collection,RM_collection]
            # Query the first MongoDB collection
            for collection in collections:
                for document in collection.find():
                    for array_name in ["output_data1", "output_data2", "output_data3"]:
                        if array_name in document:
                            for obj in document[array_name]:
                                if "allocate_to" in obj and obj["allocate_to"] is None:
                                    count += 1
                                else:
                                    countSubmited +=1
                                    

            # update_perday_data(user, current_date, count)
            numUsers = users_collection.count_documents({'role':'MLRO','status':'Approved','leaveStatus':'Working'})

            # mlrosinfo = users_collection.find({'role':'MLRO','status':'Approved','leaveStatus':'Working'})
            # mlroDetails = {}

            # for doc in mlrosinfo:
            #     mlroDetails[doc['name']] = doc['emailid']

            mlrosinfo = users_collection.find({'role':'MLRO','status':'Approved','leaveStatus':'Working'},
                                                {'name': 1, 'emailid': 1, 'image': 1})

            mlroDetails = {}
                
            for doc in mlrosinfo:
                    name = doc.get('name', '')
                    emailid = doc.get('emailid', '')
                    image = doc.get('image', '')
                    if image:
                        image_base64 = base64.b64encode(image).decode('utf-8')
                    else:
                        image_base64 = None
                    
                    mlroDetails[doc['name']] = {'emailid': emailid,'image_base64': image_base64}
                        
            cm_users_count = users_collection.count_documents({'role': {'$in': ['AGM', 'CM/SM']}, 'status': 'Approved', 'leaveStatus': 'Working'})

            cm_and_agm_info = users_collection.find(
                    {'role': {'$in': ['AGM', 'CM/SM']}, 'status': 'Approved', 'leaveStatus': 'Working'},
                    {'name': 1, 'emailid': 1, 'role': 1, 'image': 1})            
            cmDetails = {}

            for cmdoc in cm_and_agm_info:
                    name = cmdoc.get('name', '')
                    emailid = cmdoc.get('emailid', '')
                    role = cmdoc.get('role', '')
                    image = cmdoc.get('image', '')
                    if image:
                        image_base64 = base64.b64encode(image).decode('utf-8')
                    else:
                        image_base64 = None
                    

                    # Add details to the dictionary with name, emailid, and role
                    cmDetails[cmdoc['name']] = {'emailid': emailid, 'role': role,'image_base64': image_base64}     
        
            success_message = "Alerts have been allocated to MLROs successfully."
            session['success_message'] = success_message
        except:
            success_message = "MLROS are Not Approved Yet....."
            session['success_message'] = success_message
    return redirect(url_for('ITdashboard'))
    

def update_perdaydata(mlro_email, current_date):
    current_date_str = current_date.strftime('%Y-%m-%d')
    # Check if the MLRO document with the given email exists
    existing_document = users_collection.find_one({"emailid": mlro_email})
    if existing_document:
        # Ensure "perdaydata" field exists and is a list
        perday_data = existing_document.get("perdaydata", [])
        if not isinstance(perday_data, list):
            perday_data = []
        # Check if an entry for the current date already exists in "perdaydata"
        date_entry = next((entry for entry in perday_data if entry and entry.get("date") == current_date_str), None)
        if date_entry:
            # If the entry exists, increment the count
            users_collection.update_one(
                {"emailid": mlro_email, "perdaydata.date": current_date_str},
                {"$inc": {"perdaydata.$.count": 1}}
            )
        else:
            # If the entry doesn't exist, create a new entry
            users_collection.update_one(
                {"emailid": mlro_email},
                {"$push": {"perdaydata": {"date": current_date_str, "count": 1}}}
            )
    else:
        # If the document doesn't exist, create a new one with "perdaydata" field
        users_collection.insert_one({
            "emailid": mlro_email,
            "perdaydata": [{"date": current_date_str, "count": 1}]
        })

@app.route('/MLROdashboard', methods=['GET', 'POST'])
@secure_route(required_role='MLRO')
def MLROdashboard():

            if 'email_id' not in session:
                return redirect(url_for('post_login'))
            mlro_email = session['email_id']

            user = users_collection.find_one({'emailid':mlro_email})
            notify = notification(mlro_email)

            if 'image' in user:
                user['image'] = base64.b64encode(user['image']).decode('utf-8')

            dashboardCount = users_collection.find_one({'emailid':mlro_email,"status":'Approved'})
            if "allocated_tickets" in dashboardCount :
             count = len(dashboardCount['allocated_tickets'])
             if 'Sent_Back_Alerts' in dashboardCount:
                 count += len(dashboardCount['Sent_Back_Alerts'])
            else:
                count = 0
            if "case_tickets" in dashboardCount :
              print(dashboardCount['case_tickets'])
              countSubmited = len(dashboardCount['case_tickets'])
            else:
                countSubmited=0
            if 'Sent_Back_Case_Alerts' in dashboardCount:
                countSentBackCaseAlerts= len(dashboardCount['Sent_Back_Case_Alerts'])
            else:
                countSentBackCaseAlerts=0
            if 'commented_tickets' in dashboardCount:
                countcommentedtickets= len(dashboardCount['commented_tickets'])
            else:
                countcommentedtickets=0

            #======================== Per Day graph =======================
            perdaydata = dashboardCount.get('perdaydata')
            # Check if perdaydata is not None and is a list
            result_list = []
            if perdaydata is not None and isinstance(perdaydata, list):
                for dataa in perdaydata:
                    # Check if dataa is not None and has 'date' and 'count' keys
                    if dataa and 'date' in dataa and 'count' in dataa:
                        result_list.append({dataa['date']: dataa['count']})
                    else:
                        # Handle the case where dataa is None or does not have the expected keys
                        print("Invalid data format in perdaydata:", dataa)
            else:
                # Handle the case where perdaydata is None or not a list
                print("Invalid perdaydata format:", perdaydata)
            commented_perday = dashboardCount.get('commented_perday', [])
            commented_data = []
            for commenteddata in commented_perday:
                commented_data.append(commenteddata)
               
            case_tickets_perday = dashboardCount.get('case_tickets_perday',[])
            casetickets_perday = []
            for caseticketsperday in case_tickets_perday:
                casetickets_perday.append(caseticketsperday)
            
            return render_template('MLRO Officer.html',count=count,countSubmited=countSubmited,mlrouser=user,type='MLROdashboard',role='MLRO',countSentBackCaseAlerts=countSentBackCaseAlerts,countcommentedtickets=countcommentedtickets,resultlist=result_list,commentdata=commented_data,caseperday=casetickets_perday,notify=notify)

@app.route('/AGMdashboard', methods=['GET', 'POST'])
@secure_route(required_role='AGM')
def AGMdashboard():
    if 'email_id' not in session:
        return redirect(url_for('post_login'))
    agm_email = session['email_id']
    notify = notification(agm_email)
   
    agmuser = users_collection.find_one({"emailid": agm_email})
    if 'image' in agmuser:
        # Encode the image data as a base64 string
        agmuser['image'] = base64.b64encode(agmuser['image']).decode('utf-8')
    print("login agm mail", agm_email)
   
    dashboardCount = users_collection.find_one({'emailid': agm_email, "status": 'Approved'})
    if "allocated_tickets" in dashboardCount :
        count = len(dashboardCount['allocated_tickets'])
    else:
        count = 0
    if "case_tickets" in dashboardCount:
        countSubmited = len(dashboardCount['case_tickets'])
    else:
        countSubmited = 0
    if 'Sent_Back_Case_Alerts' in dashboardCount:
        countSentBackCaseAlerts = len(dashboardCount['Sent_Back_Case_Alerts'])
    else:
        countSentBackCaseAlerts=0
    if "cms_assigned" in dashboardCount:
        cmscount = (dashboardCount['cms_assigned'])
        # print("rosss",roscount)
    #========================= Per Day count ========================= 
    allocated_perday = dashboardCount.get('allocated_perday',[])
    allocated_ticket_perday = []
    for allocatedticketperday in allocated_perday:
        allocated_ticket_perday.append(allocatedticketperday)
    case_tickets_perday = dashboardCount.get('case_tickets_perday',[])
    casetickets_perday = []
    for caseticketsperday in case_tickets_perday:
        casetickets_perday.append(caseticketsperday)

    CM_COUNT = users_collection.find({"emailid": {"$in": cmscount},"status":'Approved'})
    # CM_COUNT = users_collection.find({"role": "CM/SM"})
    print("CM_COUNTtt", CM_COUNT)
    # Initialize empty lists to store data
    cm_data = []
    mlro_data = []
    for cm_emailid in CM_COUNT:
        email_id = cm_emailid.get("emailid", "")
        mlros_assigned = cm_emailid.get("mlros_assigned", [])
        # Initialize lists for MLRO data
        mlro_email_ids = []
        mlro_empids = []
        count_mlro_tickets = []
        mlro_commented_tickets = []
        mlro_case_tickets = []
        for mlro_emailid in mlros_assigned:
            user_data = users_collection.find_one({"emailid": mlro_emailid})

            if user_data and "allocated_tickets" in user_data:
                mlro_email_ids.append(user_data['emailid'])
                mlro_empids.append(user_data['empid'])
                count_mlro_ticket = len(user_data['allocated_tickets'])
                count_mlro_tickets.append(count_mlro_ticket)
                if "commented_tickets" in user_data:
                    mlro_commented_tickets.append(len(user_data['commented_tickets']))
                else:
                    mlro_commented_tickets.append(0)
                if "case_tickets" in user_data:
                    mlro_case_tickets.append(len(user_data['case_tickets']))
                else:
                    mlro_case_tickets.append(0)
            else:
                mlro_email_ids.append(mlro_emailid)
                # mlro_empids.append(user_data['empid'])
                count_mlro_tickets.append(0)
                mlro_commented_tickets.append(0)
                mlro_case_tickets.append(0)
        # Append CM data along with MLRO data
        cm_data.append({
            "cm_email_id": email_id,
            "cm_empids":cm_emailid.get("empid"),
            "count_cm_tickets": len(cm_emailid.get("allocated_tickets", [])),
            "cm_commented_tickets": len(cm_emailid.get("commented_tickets", [])),
            "cm_case_tickets": len(cm_emailid.get("case_tickets", [])),
            "mlro_data": list(zip(mlro_email_ids, count_mlro_tickets, mlro_case_tickets, mlro_commented_tickets,mlro_empids))
        })
    # Print or use the resulting data as needed
    print("cm_data", cm_data)
    return render_template('AGMdashboard.html',count=count,countSubmited=countSubmited,cm_data=cm_data,agmuser=agmuser,type='AGMdashboard',role='AGM',countSentBackCaseAlerts=countSentBackCaseAlerts,allocatedperday=allocated_ticket_perday,caseticketsperday=casetickets_perday,notify=notify)



@app.route('/CM_SM_dashboard', methods=['GET', 'POST'])
@secure_route(required_role='CM/SM')
def CM_SM_dashboard():
       
            if 'email_id' not in session:
                return redirect(url_for('post_login'))
            cm_email = session['email_id']
            notify = notification(cm_email)

            cm = users_collection.find_one({"emailid": cm_email})
            if 'image' in cm:
                # Encode the image data as a base64 string
                cm['image'] = base64.b64encode(cm['image']).decode('utf-8')
                
            mlros_assigned = cm.get("mlros_assigned", [])
            print("mlros_assigned", mlros_assigned)

            # Initialize empty arrays to store email IDs and counts
            mlro_email_ids = []
            mlro_emp_ids = []
            count_mlro_tickets = []
            mlro_commented_tickets = []  # Use a different name for the list
            mlro_case_tickets = []

            for email in mlros_assigned:
                # Find and print all data for the current email
                user_data = users_collection.find_one({"emailid": email})

                if user_data and "allocated_tickets" in user_data:
                    mlro_emailid = user_data['emailid']
                    mlro_empid = user_data['empid']
                    count_mlro_ticket = len(user_data['allocated_tickets'])

                    # Append the values to the arrays
                    mlro_email_ids.append(mlro_emailid)
                    mlro_emp_ids.append(mlro_empid)
                    count_mlro_tickets.append(count_mlro_ticket)

                    # Check if "commented_tickets" is present in user_data
                    if "commented_tickets" in user_data:
                        mlro_commented_tickets.append(len(user_data['commented_tickets']))
                    else:
                        mlro_commented_tickets.append(0)
                    if "case_tickets" in user_data:
                        mlro_case_tickets.append(len(user_data['case_tickets']))
                    else:
                        mlro_case_tickets.append(0)
                        
                        

                else:
                    # If no data or no allocated_tickets, append default values
                    
                    mlro_email_ids.append(email)
                    mlro_emp_ids.append(user_data['empid'])
                    count_mlro_tickets.append(0)
                    mlro_commented_tickets.append(0)  # Assign 0 for commented_tickets
                    mlro_case_tickets.append(0)

                 
            dashboardCount = users_collection.find_one({'emailid':cm_email,"status":'Approved'})
            if  "allocated_tickets" in dashboardCount:
             count = len(dashboardCount['allocated_tickets'])
            else:
                count = 0
            if "case_tickets" in dashboardCount :
              countSubmited = len(dashboardCount['case_tickets'])
            else:
                countSubmited=0
            if 'Sent_Back_Case_Alerts' in dashboardCount:
                countSentBackCaseAlerts = len(dashboardCount['Sent_Back_Case_Alerts'])
            else:
                countSentBackCaseAlerts=0
            if 'commented_tickets' in dashboardCount:
                countcommentedtickets= len(dashboardCount['commented_tickets'])
            else:
                countcommentedtickets=0
            
            # ===================== Per Day Count ==========================
            allocated_perday = dashboardCount.get('allocated_perday')
            # Check if perdaydata is not None and is a list
            result_list = []
            if allocated_perday is not None and isinstance(allocated_perday, list):
                for dataa in allocated_perday:
                    # Check if dataa is not None and has 'date' and 'count' keys
                    if dataa and 'date' in dataa and 'count' in dataa:
                        result_list.append({dataa['date']: dataa['count']})
                    else:
                        # Handle the case where dataa is None or does not have the expected keys
                        print("Invalid data format in perdaydata:", dataa)
            else:
                # Handle the case where perdaydata is None or not a list
                print("Invalid perdaydata format:", allocated_perday)
            case_tickets_perday = dashboardCount.get('case_tickets_perday',[])
            casetickets_perday = []
            for caseticketsperday in case_tickets_perday:
                casetickets_perday.append(caseticketsperday)

            zipped_data = list(zip(mlro_email_ids, count_mlro_tickets,mlro_case_tickets, mlro_commented_tickets,mlro_emp_ids))

            return render_template('CM_SM_dashboard.html',count=count,countSubmited=countSubmited,zipped_data=zipped_data,cmuser=cm,type='CM_SM_dashboard',role='CM/SM',countSentBackCaseAlerts=countSentBackCaseAlerts,countcommentedtickets=countcommentedtickets,allocateresultlist=result_list,caseresultlist=casetickets_perday,notify=notify)

def itCountToDgm():
            count = 0
            countSubmited = 0

    # Query the first MongoDB collection
            documents1 = TY_collection.find()
            
            for document in documents1:
                for array_name in ["output_data1", "output_data2", "output_data3"]:  # Replace with your actual array names
                    if array_name in document:
                        for obj in document[array_name]:
                            if "allocate_to" in obj and obj["allocate_to"] is None:
                                count += 1
                            else:
                                countSubmited +=1

            # Query the second MongoDB collection
            documents2 = TM_collection.find()
            
            for document in documents2:
                for array_name in ["output_data1", "output_data2", "output_data3"]:  # Replace with your actual array names
                    if array_name in document:
                        for obj in document[array_name]:
                            if "allocate_to" in obj and obj["allocate_to"] is None:
                                count += 1
                            else:
                                countSubmited +=1
            # Query the second MongoDB collection
            documents3 = RM_collection.find()
            
            for document in documents3:
                for array_name in ["output_data1", "output_data2", "output_data3"]:  # Replace with your actual array names
                    if array_name in document:
                        for obj in document[array_name]:
                            if "allocate_to" in obj and obj["allocate_to"] is None:
                                count += 1
                            else:
                                countSubmited +=1 
            return countSubmited

def mlroCountToDgm():
            coutAcceptedSTR = 0
            coutAcceptedNONSTR10 = 0

    # Query the first MongoDB collection
            documents1 = TY_collection.find()
            
            for document in documents1:
                for array_name in ["output_data1", "output_data2", "output_data3"]:  # Replace with your actual array names
                    if array_name in document:
                        for obj in document[array_name]:
                                 if "levels" in obj and obj["levels"]["mlro_level"] == "Accepted":
                                    if "status" in obj and obj["status"]["mlro_officer"] == "Accept as STR":
                                      coutAcceptedSTR +=1 
                                    else:
                                      coutAcceptedNONSTR10 +=1

            # Query the second MongoDB collection
            documents2 = TM_collection.find()
            
            for document in documents2:
                for array_name in ["output_data1", "output_data2", "output_data3"]:  # Replace with your actual array names
                    if array_name in document:
                        for obj in document[array_name]:
                                 if "levels" in obj and obj["levels"]["mlro_level"] == "Accepted":
                                    if "status" in obj and obj["status"]["mlro_officer"] == "Accept as STR":
                                      coutAcceptedSTR +=1 
                                    else:
                                      coutAcceptedNONSTR10 +=1
            # Query the second MongoDB collection
            documents3 = RM_collection.find()
            
            for document in documents3:
                for array_name in ["output_data1", "output_data2", "output_data3"]:  # Replace with your actual array names
                    if array_name in document:
                        for obj in document[array_name]:
                                 if "levels" in obj and obj["levels"]["mlro_level"] == "Accepted":
                                    if "status" in obj and obj["status"]["mlro_officer"] == "Accept as STR":
                                      coutAcceptedSTR +=1 
                                    else:
                                      coutAcceptedNONSTR10 +=1
            return coutAcceptedSTR,coutAcceptedNONSTR10

def cmCountToDgm():
            coutAcceptedSTR = 0
            coutAcceptedNONSTR10 = 0

    # Query the first MongoDB collection
            documents1 = TY_collection.find()
            
            for document in documents1:
                for array_name in ["output_data1", "output_data2", "output_data3"]:  # Replace with your actual array names
                    if array_name in document:
                        for obj in document[array_name]:
                                 if "levels" in obj and obj["levels"]["cm_level"] == "Accepted":
                                    if "status" in obj and obj["status"]["cm_officer"] == "Accept as STR":
                                      coutAcceptedSTR +=1 
                                    else:
                                      coutAcceptedNONSTR10 +=1

            # Query the second MongoDB collection
            documents2 = TM_collection.find()
            
            for document in documents2:
                for array_name in ["output_data1", "output_data2", "output_data3"]:  # Replace with your actual array names
                    if array_name in document:
                        for obj in document[array_name]:
                                 if "levels" in obj and obj["levels"]["cm_level"] == "Accepted":
                                    if "status" in obj and obj["status"]["cm_officer"] == "Accept as STR":
                                      coutAcceptedSTR +=1 
                                    else:
                                      coutAcceptedNONSTR10 +=1
            # Query the second MongoDB collection
            documents3 = RM_collection.find()
            
            for document in documents3:
                for array_name in ["output_data1", "output_data2", "output_data3"]:  # Replace with your actual array names
                    if array_name in document:
                        for obj in document[array_name]:
                                 if "levels" in obj and obj["levels"]["cm_level"] == "Accepted":
                                    if "status" in obj and obj["status"]["cm_officer"] == "Accept as STR":
                                      coutAcceptedSTR +=1 
                                    else:
                                      coutAcceptedNONSTR10 +=1
            return coutAcceptedSTR,coutAcceptedNONSTR10

def agmCountToDgm():
            coutAcceptedSTR = 0
            coutAcceptedNONSTR10 = 0

    # Query the first MongoDB collection
            documents1 = TY_collection.find()
            
            for document in documents1:
                for array_name in ["output_data1", "output_data2", "output_data3"]:  # Replace with your actual array names
                    if array_name in document:
                        for obj in document[array_name]:
                                 if "levels" in obj and obj["levels"]["agm_level"] == "Accepted":
                                    if "status" in obj and obj["status"]["agm_officer"] == "Accept as STR":
                                      coutAcceptedSTR +=1 
                                    else:
                                      coutAcceptedNONSTR10 +=1

            # Query the second MongoDB collection
            documents2 = TM_collection.find()
            
            for document in documents2:
                for array_name in ["output_data1", "output_data2", "output_data3"]:  # Replace with your actual array names
                    if array_name in document:
                        for obj in document[array_name]:
                                 if "levels" in obj and obj["levels"]["agm_level"] == "Accepted":
                                    if "status" in obj and obj["status"]["agm_officer"] == "Accept as STR":
                                      coutAcceptedSTR +=1 
                                    else:
                                      coutAcceptedNONSTR10 +=1
            # Query the second MongoDB collection
            documents3 = RM_collection.find()
            
            for document in documents3:
                for array_name in ["output_data1", "output_data2", "output_data3"]:  # Replace with your actual array names
                    if array_name in document:
                        for obj in document[array_name]:
                                 if "levels" in obj and obj["levels"]["agm_level"] == "Accepted":
                                    if "status" in obj and obj["status"]["agm_officer"] == "Accept as STR":
                                      coutAcceptedSTR +=1 
                                    else:
                                      coutAcceptedNONSTR10 +=1 
            return  coutAcceptedSTR,coutAcceptedNONSTR10

            



def get_user_ticket_data(user_data):
    if user_data and "allocated_tickets" in user_data:
        return {
            "email_id": user_data['emailid'],
            "empid": user_data['empid'],
            "count_tickets": len(user_data['allocated_tickets']),
            "commented_tickets": len(user_data.get('commented_tickets', [])),
            "case_tickets": len(user_data.get('case_tickets', [])),
        }
    else:
        return {
            "email_id": user_data['emailid'] if user_data else "",
            "empid": user_data['empid'] if user_data else "",
            "count_tickets": 0,
            "commented_tickets": 0,
            "case_tickets": 0,
        }

@app.route('/DGMdashboard', methods=['GET', 'POST'])
@secure_route(required_role='DGM/PO')
def DGMdashboard():
            if 'email_id' not in session:
                print("holaa.........")
                return redirect(url_for('post_login'))
            dgm_email = session['email_id']
            notify = notification(dgm_email)

            dgmuser = users_collection.find_one({"emailid": dgm_email})
            if 'image' in dgmuser:
                # Encode the image data as a base64 string
                dgmuser['image'] = base64.b64encode(dgmuser['image']).decode('utf-8')
            dashboardCount = users_collection.find_one({'emailid':dgm_email,"status":'Approved'})
            finalReportdata = CASE_collection.find()
            # Initialize counters
            approved_count = 0
            rejected_count = 0
            for finaldata in finalReportdata:
                if 'output_data3' in finaldata:
                    for data_entry in finaldata['output_data3']:
                        if 'finalReport' in data_entry:
                            final_report_value = data_entry['finalReport']
                            if final_report_value.lower() == 'approved':
                                approved_count += 1
                            elif final_report_value.lower() == 'rejected':
                                rejected_count += 1
            
            # print(len(dashboardCount['allocated_tickets']))
            if "allocated_tickets" in dashboardCount and dashboardCount['allocated_tickets'] is not None and dashboardCount['allocated_tickets'] != []:
            # Your code here
             count = len(dashboardCount['allocated_tickets'])
            else:
                count = 0
            if "case_tickets" in dashboardCount :
              case_tickets = len(dashboardCount['case_tickets'])
            else:
                case_tickets=0
            CM_COUNT = users_collection.find({"role": "CM/SM"})
            # Initialize empty list to store data
            cm_data = []
            for cm_emailid in CM_COUNT:
                email_id = cm_emailid.get("emailid", "")
                mlros_assigned = cm_emailid.get("mlros_assigned", [])
                # Initialize lists for MLRO data
                mlro_data = []
                # Collect MLRO data
                for mlro_emailid in mlros_assigned:
                    user_data = users_collection.find_one({"emailid": mlro_emailid})
                    mlro_data.append(get_user_ticket_data(user_data))
                # Collect AGM data
                agm_data = []
                assigned_to_agm = cm_emailid.get("assigned_to_agm", "")
                # Convert the string to a list of email IDs
                assigned_to_agm_list = [email.strip() for email in assigned_to_agm.split(',')]
                for agm_emailid in assigned_to_agm_list:
                    agm_data.append(get_user_ticket_data(users_collection.find_one({"emailid": agm_emailid})))
                # Append CM data along with MLRO and AGM data
                cm_data.append({
                    "cm_email_id": email_id,
                    "cm_empid": cm_emailid.get("empid"),
                    "count_cm_tickets": len(cm_emailid.get("allocated_tickets", [])),
                    "cm_commented_tickets": len(cm_emailid.get("commented_tickets", [])),
                    "cm_case_tickets": len(cm_emailid.get("case_tickets", [])),
                    "mlro_data": mlro_data,
                    "agm_data": agm_data,
                })
            # ====================== Per Day Count ==============================
            allocated_perday = dashboardCount.get('allocated_perday',[])
            allocated_ticket_perday = []
            for allocatedticketperday in allocated_perday:
                allocated_ticket_perday.append(allocatedticketperday)
            DGMApproved_perDay = dashboardCount.get('DGMApproved_perDay',[])
            DGMApprovedperDay = []
            for DGMApproved_ticket_perDay in DGMApproved_perDay:
                DGMApprovedperDay.append(DGMApproved_ticket_perDay)
            DGMRejected_perDay = dashboardCount.get('DGMRejected_perDay',[])
            DGMRejectedperDay = []
            for DGMRejected_ticket_perDay in DGMRejected_perDay:
                DGMRejectedperDay.append(DGMRejected_ticket_perDay)
            # Print or use the resulting data as needed
            # print("cm_data", cm_data)
            return render_template('DGMdashboard.html', count=count, commented_tickets=case_tickets, cm_data=cm_data,approved_count=approved_count,rejected_count=rejected_count,dgmuser=dgmuser,type='DGMdashboard',role='DGM/PO',allocatedperday=allocated_ticket_perday,DGMApprovedperDay=DGMApprovedperDay,DGMRejectedperDay=DGMRejectedperDay,notify=notify)


# ==============Next Level Section====================


@app.route('/MLRONextLevel', methods=['GET', 'POST'])
@secure_route(required_role='MLRO')
def MLRONextLevel():
    success_message = session.pop('success_message', None)
    # Check user login
    if 'email_id' not in session:
        return redirect(url_for('post_login'))
    mlro_email = session['email_id']
    print('mlro email:',mlro_email)
    notify = clearnotification(mlro_email,'nextLevel')

    mlro = users_collection.find_one({"emailid": mlro_email})
    
    if mlro is None:
        return "User data not found. Please log in again."
    
    if 'image' in mlro:
                # Encode the image data as a base64 string
                mlro['image'] = base64.b64encode(mlro['image']).decode('utf-8')
    if 'ACC_Num' in session and 'ticket_id' in session and 'CUST_ID' in session:
        session.pop('ACC_Num')
        session.pop('ticket_id')
        session.pop('CUST_ID')
    ticket_numbers = mlro.get("allocated_tickets", [])
    data = {}
    all_collections = [TY_collection, TM_collection, RM_collection]
    array_names = ["output_data1", "output_data2", "output_data3"]
    for collection, array_name in product(all_collections, array_names):
        pipeline = [
            {
                "$unwind": f"${array_name}"
            },
            {
                "$match": {
                    f"{array_name}.allocate_to":mlro_email,
                    f"{array_name}.ticket_id":{"$in":ticket_numbers}
                }
            },
            {
                "$group": {
                    "_id": "$code",
                    "data": {"$push": f"${array_name}"}
                }
            }
        ]
        data_from_collection = collection.aggregate(pipeline)
        for doc in data_from_collection:
            if doc['_id'] not in list(data.keys()):
                data[doc['_id']] = []
                data[doc['_id']].extend(doc['data'])
            else:
                data[doc['_id']].extend(doc['data'])
        # print('dataa:',data)
    return render_template('alertOperationMLRO (1).html', data=data, success_message=success_message,mlrouser=mlro,type='MLRONextLevel',role='MLRO',notify=notify)

@app.route('/mlro_comments', methods=['GET', 'POST']) 
@secure_route(required_role='MLRO')
def mlro_comments():
    if request.method == "POST":
        print("hiiiiiiiiiiii")
        # action = request.form.get('action')
        # print("action", action)
        ticket_id = request.form.get('ticket_id')
        print("ticket_id", ticket_id)
        comment_text = request.form.get('comments')
        # comments_added_date = datetime.now()
        comments_added_date=datetime.now()
        # Update in the first collection (TM_collection)
        for document in TM_collection.find():
            for array_name in ["output_data1", "output_data2", "output_data3"]:
                if array_name in document:
                    for obj in document[array_name]:
                        if "ticket_id" in obj and obj["ticket_id"] == ticket_id:
                            TM_collection.update_one(
                                {"_id": document["_id"], f"{array_name}.ticket_id": ticket_id},
                                {"$set": 
                                {f"{array_name}.$[elem].Comments": comment_text,
                                  f"{array_name}.$[elem].Comments_status": "pending"
                                # f"{array_name}.$[elem].Comments_added_date": comments_added_date
                                          }
                                          },
                                array_filters=[{"elem.ticket_id": ticket_id}]
                            )
        # Update in the second collection (TY_collection)
        for document in TY_collection.find():
            for array_name in ["output_data1", "output_data2", "output_data3"]:
                if array_name in document:
                    for obj in document[array_name]:
                        if "ticket_id" in obj and obj["ticket_id"] == ticket_id:
                            TY_collection.update_one(
                                {"_id": document["_id"], f"{array_name}.ticket_id": ticket_id},
                                {"$set": {f"{array_name}.$[elem].Comments": comment_text,
                                        #   f"{array_name}.$[elem].Comments_added_date": comments_added_date
                                         f"{array_name}.$[elem].Comments_status": "pending"
                                          }},
                                array_filters=[{"elem.ticket_id": ticket_id}]
                            )
                   
        # Update in the third collection (RM_collection)
        for document in RM_collection.find():
            for array_name in ["output_data1", "output_data2", "output_data3"]:
                if array_name in document:
                    for obj in document[array_name]:
                        if "ticket_id" in obj and obj["ticket_id"] == ticket_id:
                            RM_collection.update_one(
                                {"_id": document["_id"], f"{array_name}.ticket_id": ticket_id},
                                {"$set": {f"{array_name}.$[elem].Comments": comment_text,
                                        #   f"{array_name}.$[elem].Comments_added_date": comments_added_date
                                         f"{array_name}.$[elem].Comments_status": "pending"
                                          }
                                          },
                                array_filters=[{"elem.ticket_id": ticket_id}]
                            )
        

           
        session['success_message'] = 'Comments saved successfully.'
        mlro_email = session['email_id']
        users_collection.update_one(
                {'emailid': mlro_email, 'allocated_tickets': ticket_id},
                {
                    '$pull': {'allocated_tickets': ticket_id},
                    '$push': {'commented_tickets': ticket_id}
                }
            )

        return redirect(url_for("MLRONextLevel"))


 

@app.route('/caseFormPage', methods=['GET', 'POST'])
@secure_route(required_role='MLRO')
def caseFormPage():
    
    msgg = session.pop('msgg', None)  
    mlro_email = session.get('email_id')  # Retrieve email from session safely
    if mlro_email is None:
        return redirect(url_for('login'))

    user = users_collection.find_one({"emailid": mlro_email})
    notify = notification(mlro_email)

    if 'image' in user:
        user['image'] = base64.b64encode(user['image']).decode('utf-8')

    allocatedCM = user.get("assigned_to")
    data = {}
    all_collections = [TY_collection, TM_collection, RM_collection]
    array_names = ["output_data1", "output_data2", "output_data3"]
    CustomerName = None

    if request.method == 'POST':
        ticket_id_from_form = request.form.get('ticket_id')  # Use .get() to safely retrieve form data
        CustomerId = request.form.get('custId')
        

        for collection, array_name in product(all_collections, array_names):
            pipeline = [
                {"$unwind": f"${array_name}"},
                {"$match": {f"{array_name}.allocate_to": mlro_email, f"{array_name}.ticket_id": ticket_id_from_form}},
                {"$group": {"_id": "$code", "data": {"$push": f"${array_name}"}}}
            ]
            data_from_collection = collection.aggregate(pipeline)
            for doc in data_from_collection:
                result = doc['data']
                CustomerName = result[0].get('Customer Name')
                if doc['_id'] not in data:
                    data[doc['_id']] = []
                data[doc['_id']].extend(doc['data'])

        return render_template('Form_Page.html', ticket_id=ticket_id_from_form, CustomerId=CustomerId,
                               allocatedCM=allocatedCM, data=data, role='MLRO', type='MLRONextLevel',
                               mlrouser=user, notify=notify, CustomerName=CustomerName, msgg=msgg)
    
    ticket_id_from_session = session.get('ticket_id')
    CustomerId = session.get('custid')
    print('ticket_id:', ticket_id_from_session)
    print('custid:', CustomerId)

    for collection, array_name in product(all_collections, array_names):
        pipeline = [
            {"$unwind": f"${array_name}"},
            {"$match": {f"{array_name}.allocate_to": mlro_email, f"{array_name}.ticket_id": ticket_id_from_session}},
            {"$group": {"_id": "$code", "data": {"$push": f"${array_name}"}}}
        ]
        data_from_collection = collection.aggregate(pipeline)
        for doc in data_from_collection:
            result = doc['data']
            CustomerName = result[0].get('Customer Name')
            if doc['_id'] not in data:
                data[doc['_id']] = []
            data[doc['_id']].extend(doc['data'])

    return render_template('Form_Page.html', ticket_id=ticket_id_from_session, CustomerId=CustomerId,
                           allocatedCM=allocatedCM, data=data, role='MLRO', type='MLRONextLevel',
                           mlrouser=user, notify=notify, CustomerName=CustomerName, msgg=msgg)




ALLOWED_EXTENSIONSS = {'pdf', 'xls', 'xlsx', 'csv'}  

@app.route('/submetCaseForm', methods=['GET', 'POST'])
@secure_route(required_role=['MLRO', 'AGM', 'CM/SM', 'DGM/PO'])
def submetCaseForm():
    if request.method == 'POST':
        
        user = session.get('email_id') 
        if user is None:
            return redirect(url_for('login'))

        info = users_collection.find_one({"emailid": user})
        if info is None:
            return redirect(url_for('login'))
        
        type=request.form['type']
        print('type:',type)
        ticket_id_from_form = request.form['ticket_id']
        customerNo = request.form['customerNo']
        print('custid:',customerNo)
        sentTo = request.form['sentTo']
        crime = request.form['crime']
        Classification = request.form['caseAllocation']
        SuspeciousDuo = request.form['SuspeciousDuo']
        SuspeciousDuoeco = request.form['SuspeciousDuoeco']
        SuspeciousDuofinancing = request.form['SuspeciousDuofinancing']
        Investigation = request.form['Investigation']
        LEAinformed = request.form['LEAinformed']
        LEADetails = request.form['LEADetails']
        reportCase = request.form['reportCase']
        additionalInfo = request.form['additionalInfo']
        priorityRAG = request.form['priorityRAG']
        cumulativeCrtTurnover = request.form['cumulativeCrtTurnover']
        cumulativeDTTurnover = request.form['cumulativeDTTurnover']
        cumulativeDepositTurnover = request.form['cumulativeDepositTurnover']
        cumulativeWithdrawalTurnover = request.form['cumulativeWithdrawalTurnover']
        NumTransactionReport = request.form['NumTransactionReport']
        remark = request.form['remark']
        Raise_STR = request.form['strraising']
        comment = request.form['comments']
        finalReport = request.form['finalReport']
        prefilled = request.form['prefilled']
        accountNoSearch = request.form['accountNoSearch']
        

        session['ticket_id'] = ticket_id_from_form
        session['custid'] = customerNo

        

        file = request.files['file']
        print(f"Uploaded file: '{file.filename}'")
        
        # Trim any extra spaces from the filename
        filename = file.filename.strip()
        print(f"Trimmed filename: '{filename}'")

        formData = {
            "sentTo": sentTo,
            "SuspeciousDuoCrime": crime,
            "accountNoSearch": accountNoSearch,
            "Classification": Classification,
            "SuspeciousDuoComplexTr": SuspeciousDuo,
            "SuspeciousDuoNoeco": SuspeciousDuoeco,
            "terrorisumFunding": SuspeciousDuofinancing,
            "Investigation": Investigation,
            "LEAinformed": LEAinformed,
            "LEADetails": LEADetails,
            "reportCase": reportCase,
            "additionalInfo": additionalInfo,
            "priorityRAG": priorityRAG,
            "cumulativeCrtTurnover": cumulativeCrtTurnover,
            "cumulativeDTTurnover": cumulativeDTTurnover,
            "cumulativeDepositTurnover": cumulativeDepositTurnover,
            "cumulativeWithdrawalTurnover": cumulativeWithdrawalTurnover,
            "NumTransactionReport": NumTransactionReport,
            "remark": remark,
            "Raise_STR": Raise_STR,
            "comment": comment,
            "finalReport": finalReport,
            "prefilled": prefilled,
            "fileName": filename
        }
        
            
        if info["role"] == "MLRO":
            if type=='MLRONextLevel':
                form_data = {field: request.form.get(field) for field in request.form}
                cumulativeCrtTurnover=form_data.get('cumulativeCrtTurnover')
                cumulativeDTTurnover=form_data.get('cumulativeDTTurnover')
                cumulativeDepositTurnover=form_data.get('cumulativeDepositTurnover')
                cumulativeWithdrawalTurnover=form_data.get('cumulativeWithdrawalTurnover')
                if not cumulativeCrtTurnover:  
                    print(cumulativeCrtTurnover)
                    session['msgg'] = "cumulativeCrtTurnover is required"
                    return redirect(url_for('caseFormPage'))

                elif not re.match(r'^[0-9.]*$', cumulativeCrtTurnover):
                    session['msgg'] = "cumulativeCrtTurnover should only contain  numbers and decimal points are allowed."
                    return redirect(url_for('caseFormPage'))
                elif len(cumulativeCrtTurnover) > 15:

                    session['msgg'] = "cumulativeCrtTurnover should not exceed 15 digits."
                    return redirect(url_for('caseFormPage'))
                
                if not cumulativeDTTurnover:  
                    print(cumulativeDTTurnover)
                    session['msgg'] = "cumulativeDTTurnover is required"
                    return redirect(url_for('caseFormPage'))

                elif not re.match(r'^[0-9.]*$', cumulativeDTTurnover):
                    session['msgg'] = "cumulativeDTTurnover should only contain  numbers and decimal points are allowed."
                    return redirect(url_for('caseFormPage'))
                elif len(cumulativeDTTurnover) > 15:

                    session['msgg'] = "cumulativeDTTurnover should not exceed 15 digits."
                    return redirect(url_for('caseFormPage'))
                
                if not cumulativeDepositTurnover:  
                    print(cumulativeDepositTurnover)
                    session['msgg'] = "cumulativeDepositTurnover is required"
                    return redirect(url_for('caseFormPage'))
                
                elif not re.match(r'^[0-9.]*$', cumulativeDepositTurnover):
                    session['msgg'] = "cumulativeDepositTurnover should only contain  numbers and decimal points are allowed."
                    return redirect(url_for('caseFormPage'))
                
                elif len(cumulativeDepositTurnover) > 15:

                    session['msgg'] = "cumulativeDepositTurnover should not exceed 15 digits."
                    return redirect(url_for('caseFormPage'))
                
                if not cumulativeWithdrawalTurnover:  
                    print(cumulativeWithdrawalTurnover)
                    session['msgg'] = "cumulativeWithdrawalTurnover is required"
                    return redirect(url_for('caseFormPage'))
                
                elif not re.match(r'^[0-9.]*$', cumulativeWithdrawalTurnover):
                    session['msgg'] = "cumulativeWithdrawalTurnover should only contain  numbers and decimal points are allowed."
                    return redirect(url_for('caseFormPage'))
                
                elif len(cumulativeWithdrawalTurnover) > 15:

                    session['msgg'] = "cumulativeWithdrawalTurnover should not exceed 15 digits."
                    return redirect(url_for('caseFormPage'))
                
                accountNoSearch = form_data.get('accountNoSearch')
                print(len(accountNoSearch))
                if not accountNoSearch:  
                    print(accountNoSearch)
                    session['msgg'] = "AccountNo is required"
                    return redirect(url_for('caseFormPage'))
                elif not re.match(r'^[0-9.]*$', accountNoSearch):
                    session['msgg'] = "AccountNo should only contain  numbers and decimal points are allowed."
                    return redirect(url_for('caseFormPage'))

                elif len(accountNoSearch) > 15:

                    session['msgg'] = "AccountNo should not exceed 15 digits."
                    return redirect(url_for('caseFormPage'))

            number_pattern = r'^\d+(\.\d+)?$'
            acc_pattern = r'^\d{11,14}$'
            if type=='return_Mlro_Alerts':
                if not re.match(number_pattern, cumulativeCrtTurnover):
                    session['msgg'] = "cumulativeCrtTurnover must contain only numbers and decimals."
                    return redirect(url_for('returnCaseFormEdit'))                
                if not re.match(number_pattern, cumulativeDTTurnover):  
                    session['msgg'] = "cumulativeDTTurnover must contain only numbers and decimals."
                    return redirect(url_for('returnCaseFormEdit'))
                if not re.match(number_pattern, cumulativeDepositTurnover):
                    session['msgg'] = "cumulativeDepositTurnover must contain only numbers and decimals."
                    return redirect(url_for('returnCaseFormEdit'))
                if not re.match(number_pattern, cumulativeWithdrawalTurnover):
                    session['msgg'] = "cumulativeWithdrawalTurnover must contain only numbers and decimals."
                    return redirect(url_for('returnCaseFormEdit'))
                if 'file' not in request.files:
                    session['msgg'] = 'No file part'
                    return redirect(url_for('returnCaseFormEdit'))
                if filename == '':
                        session['msgg'] = 'No selected file'
                        return redirect(url_for('returnCaseFormEdit'))

                if not allowed_files(filename):
                    session['msgg'] = 'Invalid file extension. Allowed extensions are .pdf, .xls, .xlsx, .csv.'
                    return redirect(url_for('returnCaseFormEdit'))
                if not re.match(acc_pattern, accountNoSearch):
                    session['msgg'] = "Account Number must contain only numbers and decimals and must be 11 to 14 digits long."
                    return redirect(url_for('returnCaseFormEdit'))
            

            if type=='display_Sent_Back_Alerts':
                if not re.match(number_pattern, cumulativeCrtTurnover):
                    session['msgg'] = "cumulativeCrtTurnover must contain only numbers and decimals."
                    return redirect(url_for('sent_back_case_FormPage'))                
                if not re.match(number_pattern, cumulativeDTTurnover):  
                    session['msgg'] = "cumulativeDTTurnover must contain only numbers and decimals."
                    return redirect(url_for('sent_back_case_FormPage'))
                if not re.match(number_pattern, cumulativeDepositTurnover):
                    session['msgg'] = "cumulativeDepositTurnover must contain only numbers and decimals."
                    return redirect(url_for('sent_back_case_FormPage'))
                if not re.match(number_pattern, cumulativeWithdrawalTurnover):
                    session['msgg'] = "cumulativeWithdrawalTurnover must contain only numbers and decimals."
                    return redirect(url_for('sent_back_case_FormPage'))
                if 'file' not in request.files:
                    session['msgg'] = 'No file part'
                    return redirect(url_for('sent_back_case_FormPage'))
                if filename == '':
                        session['msgg'] = 'No selected file'
                        return redirect(url_for('sent_back_case_FormPage'))

                if not allowed_files(filename):
                    session['msgg'] = 'Invalid file extension. Allowed extensions are .pdf, .xls, .xlsx, .csv.'
                    return redirect(url_for('sent_back_case_FormPage'))
                if not re.match(acc_pattern, accountNoSearch):
                    session['msgg'] = "Account Number must contain only numbers and decimals and must be 11 to 14 digits long."
                    return redirect(url_for('sent_back_case_FormPage'))
                print("Raise_STR: %s", Raise_STR) 
                
            if 'file' not in request.files:
                session['msgg'] = 'No file part'
                return redirect(url_for('caseFormPage'))
            if filename == '':
                    session['msgg'] = 'No selected file'
                    return redirect(url_for('caseFormPage'))

            if not allowed_files(filename):
                session['msgg'] = 'Invalid file extension. Allowed extensions are .pdf, .xls, .xlsx, .csv.'
                return redirect(url_for('caseFormPage'))

            if Raise_STR == "STR":
                redirect_to_endpoint = mlroCaseFormStore(ticket_id_from_form, formData, user)
                db.files.insert_one({'filename': filename, 'ticket_id': ticket_id_from_form, 'data': file.read()})
                return redirect(url_for(redirect_to_endpoint))

            elif Raise_STR == "NON-STR":
                mlroCasecloseFormStore(ticket_id_from_form, formData, user)
                db.files.insert_one({'filename': filename, 'ticket_id': ticket_id_from_form, 'data': file.read()})
                return redirect(url_for('MLRONextLevel'))
        
        else:
            print('^^^^^^^')
            redirect_to_endpoint = CaseFormUpdate(ticket_id_from_form, formData, user)
            # db.files.insert_one({'filename': filename, 'ticket_id': ticket_id_from_form, 'data': file.read()})
            print("Uploaded file...")
            print("redirect_to_endpoint : ",redirect_to_endpoint)
            
            if info["role"] == "CM/SM":
                print('role:',info['role'])
                return redirect(url_for(redirect_to_endpoint))
            elif info["role"] == "AGM":
                return redirect(url_for(redirect_to_endpoint))
            elif info["role"] == "DGM/PO":
                return redirect(url_for('DGMNextLevel'))

    # return redirect(url_for('caseFormPage'))

def allowed_files(filename):
    ALLOWED_EXTENSIONSS = {'pdf', 'xls', 'xlsx', 'csv'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONSS









def mlroCaseFormStore(ticket_id,dataObject,user):      
        # Update in the first collection (TM_collection)
        for document in TM_collection.find():
            for array_name in ["output_data1", "output_data2", "output_data3"]:
                if array_name in document:
                    for obj in document[array_name]:
                        if "ticket_id" in obj and obj["ticket_id"] == ticket_id:
                                        # Remove the document from TM_Collection
                                TM_collection.update_one(
                        {"_id": document["_id"]},
                        {"$pull": {f"{array_name}": {"ticket_id": ticket_id}}}
                    )
                                obj["levels"]["mlro_level"] = user
                                nextOfficer = dataObject["sentTo"]
                                obj["status"]["cm_officer"] = nextOfficer
                                com = dataObject["comment"]
                                prefilled = dataObject["prefilled"]
                                
                                if len(com) != 0 and len(prefilled) != 0:
                                 commentobj ={"mlrocomment":com,
                                                       "cmcomment":None,
                                                       "agmcomment":None,
                                                       "dgmcomment":None
                                                       }
                                 obj["CaseComment"] = commentobj
                                 prefilledComment = {"mlrocomment":prefilled,
                                                       "cmcomment":None,
                                                       "agmcomment":None,
                                                       "dgmcomment":None
                                                       }
                                 obj["prefilledComment"] = prefilledComment
                                 
                                else:
                                 commentobj ={"mlrocomment":"Case Created due to some Suspicious Amount Transaction ",
                                                       "cmcomment":None,
                                                       "agmcomment":None,
                                                       "dgmcomment":None
                                                       }
                                 obj["CaseComment"] = commentobj
                                 prefilledComment = {"mlrocomment":"Others",
                                                       "cmcomment":None,
                                                       "agmcomment":None,
                                                       "dgmcomment":None
                                                       }
                                 obj["prefilledComment"] = prefilledComment
                                 
                                del dataObject['comment']
                                del dataObject["prefilled"]

                                print(dataObject)
                                obj["Case_Details"] = dataObject
                                common_code = document['code']

                                print(common_code)
                                # removing the previous document with ticket id if the ticket got re sent by CM/SM
                                all_collections = [CLOSE_CASE_collection]
                                array_names = ["output_data1", "output_data2", "output_data3"]
                                for collection, array_name in product(all_collections, array_names):
                                        collection.update_one( {f"{array_name}.ticket_id": ticket_id},{"$pull": {f"{array_name}": {"ticket_id": ticket_id}}})

                                # Check if a document with the same code and array_name already exists
                                existing_document = CASE_collection.find_one({
                                    "code": common_code
                                })

                                if existing_document:
                                        # If the document with the same code exists, update or insert into the appropriate array field
                                        if array_name in existing_document:
                                            # If the array_name already exists, push obj into the array
                                            CASE_collection.update_one(
                                                {"code": common_code},
                                                {"$push": {f"{array_name}": obj}}
                                            )
                                        else:
                                            # If the array_name does not exist, create a new array field and insert obj
                                            CASE_collection.update_one(
                                                {"code": common_code},
                                                {"$set": {f"{array_name}": [obj]}}
                                            )
                                else:
                                    # If no document with the same code and array_name exists, create a new document
                                    CASE_collection.insert_one({
                                        "_id": ObjectId(),
                                        "code": common_code,
                                        f"{array_name}": [obj]
                                    })

                                # Optionally, you can break out of the loop once the update/insert is done
                                break
                    session['success_message'] = 'MLRO officer updated successfully.'

        # Update in the second collection (TY_collection)
        for document in TY_collection.find():
            for array_name in ["output_data1", "output_data2", "output_data3"]:
                if array_name in document:
                    for obj in document[array_name]:
                        if "ticket_id" in obj and obj["ticket_id"] == ticket_id:
                            # Remove the document from TM_Collection
                            TY_collection.update_one(
                                   {"_id": document["_id"]},
                                    {"$pull": {f"{array_name}": {"ticket_id": ticket_id}}}
                                )
                            obj["levels"]["mlro_level"] = user

                            nextOfficer = dataObject["sentTo"]
                            obj["status"]["cm_officer"] = nextOfficer
                            com = dataObject["comment"]
                            prefilled = dataObject["prefilled"]
                                
                            if len(com) != 0 and len(prefilled) != 0:
                                 commentobj ={"mlrocomment":com,
                                                       "cmcomment":None,
                                                       "agmcomment":None,
                                                       "dgmcomment":None
                                                       }
                                 obj["CaseComment"] = commentobj
                                 prefilledComment = {"mlrocomment":prefilled,
                                                       "cmcomment":None,
                                                       "agmcomment":None,
                                                       "dgmcomment":None
                                                       }
                                 obj["prefilledComment"] = prefilledComment
                                 
                            else:
                                 commentobj ={"mlrocomment":"Case Created due to some Suspicious Amount Transaction ",
                                                       "cmcomment":None,
                                                       "agmcomment":None,
                                                       "dgmcomment":None
                                                       }
                                 obj["CaseComment"] = commentobj
                                 prefilledComment = {"mlrocomment":"Others",
                                                       "cmcomment":None,
                                                       "agmcomment":None,
                                                       "dgmcomment":None
                                                       }
                                 obj["prefilledComment"] = prefilledComment
                                 
                            del dataObject['comment']
                            del dataObject["prefilled"]

                            obj["Case_Details"] = dataObject

                            common_code = document['code']

                            # removing the previous document with ticket id if the ticket got re sent by CM/SM
                            all_collections = [CLOSE_CASE_collection]
                            array_names = ["output_data1", "output_data2", "output_data3"]
                            for collection, array_name in product(all_collections, array_names):
                                    collection.update_one( {f"{array_name}.ticket_id": ticket_id},{"$pull": {f"{array_name}": {"ticket_id": ticket_id}}})
                            

                            # Check if a document with the same code and array_name already exists
                            existing_document = CASE_collection.find_one({
                                "code": common_code
                            })

                            if existing_document:
                               # If the document with the same code exists, update or insert into the appropriate array field
                                        if array_name in existing_document:
                                            # If the array_name already exists, push obj into the array
                                            CASE_collection.update_one(
                                                {"code": common_code},
                                                {"$push": {f"{array_name}": obj}}
                                            )
                                        else:
                                            # If the array_name does not exist, create a new array field and insert obj
                                            CASE_collection.update_one(
                                                {"code": common_code},
                                                {"$set": {f"{array_name}": [obj]}}
                                            )
                            else:
                                # If no document with the same code and array_name exists, create a new document
                                CASE_collection.insert_one({
                                    "_id": ObjectId(),
                                    "code": common_code,
                                    f"{array_name}": [obj]
                                })

                            # Optionally, you can break out of the loop once the update/insert is done
                            break
    
                    session['success_message'] = 'MLRO officer updated successfully.'
        # Update in the third collection (RM_collection)
        for document in RM_collection.find():
            for array_name in ["output_data1", "output_data2", "output_data3"]:
                if array_name in document:
                    for obj in document[array_name]:
                        if "ticket_id" in obj and obj["ticket_id"] == ticket_id:
                                
                                RM_collection.update_one(
                                    {"_id": document["_id"]},
                                    {"$pull": {f"{array_name}": {"ticket_id": ticket_id}}}
                                )
                                obj["levels"]["mlro_level"] = user

                                nextOfficer = dataObject["sentTo"]
                                obj["status"]["cm_officer"] = nextOfficer

                                com = dataObject["comment"]
                                prefilled = dataObject["prefilled"]
                                
                                if len(com) != 0 and len(prefilled) != 0:
                                 commentobj ={"mlrocomment":com,
                                                       "cmcomment":None,
                                                       "agmcomment":None,
                                                       "dgmcomment":None
                                                       }
                                 obj["CaseComment"] = commentobj
                                 prefilledComment = {"mlrocomment":prefilled,
                                                       "cmcomment":None,
                                                       "agmcomment":None,
                                                       "dgmcomment":None
                                                       }
                                 obj["prefilledComment"] = prefilledComment
                                 
                                else:
                                 commentobj ={"mlrocomment":"Case Created due to some Suspicious Amount Transaction ",
                                                       "cmcomment":None,
                                                       "agmcomment":None,
                                                       "dgmcomment":None
                                                       }
                                 obj["CaseComment"] = commentobj
                                 prefilledComment = {"mlrocomment":"Others",
                                                       "cmcomment":None,
                                                       "agmcomment":None,
                                                       "dgmcomment":None
                                                       }
                                 obj["prefilledComment"] = prefilledComment
                                 
                                del dataObject['comment']
                                del dataObject["prefilled"]
                                obj["Case_Details"] = dataObject

                                common_code = document['code']

                                # removing the previous document with ticket id if the ticket got re sent by CM/SM
                                all_collections = [CLOSE_CASE_collection]
                                array_names = ["output_data1", "output_data2", "output_data3"]
                                for collection, array_name in product(all_collections, array_names):
                                        collection.update_one( {f"{array_name}.ticket_id": ticket_id},{"$pull": {f"{array_name}": {"ticket_id": ticket_id}}})

                                # Check if a document with the same code and array_name already exists
                                existing_document = CASE_collection.find_one({
                                    "code": common_code
                                })

                                if existing_document:
                                    # If the document with the same code exists, update or insert into the appropriate array field
                                        if array_name in existing_document:
                                            # If the array_name already exists, push obj into the array
                                            CASE_collection.update_one(
                                                {"code": common_code},
                                                {"$push": {f"{array_name}": obj}}
                                            )
                                        else:
                                            # If the array_name does not exist, create a new array field and insert obj
                                            CASE_collection.update_one(
                                                {"code": common_code},
                                                {"$set": {f"{array_name}": [obj]}}
                                            )
                                else:
                                    # If no document with the same code and array_name exists, create a new document
                                    CASE_collection.insert_one({
                                        "_id": ObjectId(),
                                        "code": common_code,
                                        f"{array_name}": [obj]
                                    })

                                # Optionally, you can break out of the loop once the update/insert is done
                                break
                    session['success_message'] = 'MLRO officer updated successfully.'
        
        # Update in the fourth collection (CLOSE_CASE_collection)
        for document in CLOSE_CASE_collection.find():
            for array_name in ["output_data1", "output_data2", "output_data3"]:
                if array_name in document:
                    for obj in document[array_name]:
                        if "ticket_id" in obj and obj["ticket_id"] == ticket_id:
                                        # Remove the document from TM_Collection
                                CLOSE_CASE_collection.update_one(
                        {"_id": document["_id"]},
                        {"$pull": {f"{array_name}": {"ticket_id": ticket_id}}}
                    )
                                obj["levels"]["mlro_level"] = user

                                com = dataObject["comment"]
                                prefilled = dataObject["prefilled"]
                                
                                if len(com) != 0 and len(prefilled) != 0:
                                 commentobj ={"mlrocomment":com,
                                                       "cmcomment":None,
                                                       "agmcomment":None,
                                                       "dgmcomment":None
                                                       }
                                 obj["CaseComment"] = commentobj
                                 prefilledComment = {"mlrocomment":prefilled,
                                                       "cmcomment":None,
                                                       "agmcomment":None,
                                                       "dgmcomment":None
                                                       }
                                 obj["prefilledComment"] = prefilledComment
                                 
                                else:
                                 commentobj ={"mlrocomment":"Case Created due to some Suspicious Amount Transaction ",
                                                       "cmcomment":None,
                                                       "agmcomment":None,
                                                       "dgmcomment":None
                                                       }
                                 obj["CaseComment"] = commentobj
                                 prefilledComment = {"mlrocomment":"Others",
                                                       "cmcomment":None,
                                                       "agmcomment":None,
                                                       "dgmcomment":None
                                                       }
                                 obj["prefilledComment"] = prefilledComment
                                 
                                del dataObject['comment']
                                del dataObject["prefilled"]

                                print(dataObject)
                                obj["Case_Details"] = dataObject
                                common_code = document['code']

                                print(common_code)
                                # removing the previous document with ticket id if the ticket got re sent by CM/SM
                                all_collections = [CLOSE_CASE_collection]
                                array_names = ["output_data1", "output_data2", "output_data3"]
                                for collection, array_name in product(all_collections, array_names):
                                        collection.update_one( {f"{array_name}.ticket_id": ticket_id},{"$pull": {f"{array_name}": {"ticket_id": ticket_id}}})

                                # Check if a document with the same code and array_name already exists
                                existing_document = CASE_collection.find_one({
                                    "code": common_code
                                })

                                if existing_document:
                                        # If the document with the same code exists, update or insert into the appropriate array field
                                        if array_name in existing_document:
                                            # If the array_name already exists, push obj into the array
                                            CASE_collection.update_one(
                                                {"code": common_code},
                                                {"$push": {f"{array_name}": obj}}
                                            )
                                        else:
                                            # If the array_name does not exist, create a new array field and insert obj
                                            CASE_collection.update_one(
                                                {"code": common_code},
                                                {"$set": {f"{array_name}": [obj]}}
                                            )
                                else:
                                    # If no document with the same code and array_name exists, create a new document
                                    CASE_collection.insert_one({
                                        "_id": ObjectId(),
                                        "code": common_code,
                                        f"{array_name}": [obj]
                                    })

                                # Optionally, you can break out of the loop once the update/insert is done
                                break
                    session['success_message'] = 'MLRO officer updated successfully.'
       # Update in the fourth collection (CLOSE_CASE_collection)
        for document in CASE_collection.find():
            for array_name in ["output_data1", "output_data2", "output_data3"]:
                if array_name in document:
                    for obj in document[array_name]:
                        if "ticket_id" in obj and obj["ticket_id"] == ticket_id and "comment" in dataObject:
                                com = dataObject["comment"]
                                prefilled = dataObject["prefilled"]
                                obj["levels"]["mlro_level"] = user
                                if len(com) != 0 and len(prefilled) != 0:
                                 commentobj ={"mlrocomment":com,
                                                       "cmcomment":None,
                                                       "agmcomment":None,
                                                       "dgmcomment":None
                                                       }
                                 obj["CaseComment"] = commentobj
                                 prefilledComment = {"mlrocomment":prefilled,
                                                       "cmcomment":None,
                                                       "agmcomment":None,
                                                       "dgmcomment":None
                                                       }
                                 obj["prefilledComment"] = prefilledComment
                                else:
                                 commentobj ={"mlrocomment":"Case Created due to some Suspicious Amount Transaction ",
                                                       "cmcomment":None,
                                                       "agmcomment":None,
                                                       "dgmcomment":None
                                                       }
                                 obj["CaseComment"] = commentobj
                                 prefilledComment = {"mlrocomment":"Others",
                                                       "cmcomment":None,
                                                       "agmcomment":None,
                                                       "dgmcomment":None
                                                       }
                                 obj["prefilledComment"] = prefilledComment
                                del dataObject['comment']
                                del dataObject["prefilled"]
                                print(dataObject)
                                obj["Case_Details"] = dataObject
                                common_code = document['code']
                                print(common_code)
                                # removing the previous document with ticket id if the ticket got re sent by CM/SM
                                all_collections = [CASE_collection]
                                array_names = ["output_data1", "output_data2", "output_data3"]
                                for collection, array_name in product(all_collections, array_names):
                                        collection.update_one( {f"{array_name}.ticket_id": ticket_id},{"$pull": {f"{array_name}": {"ticket_id": ticket_id}}})
                                # Check if a document with the same code and array_name already exists
                                existing_document = CASE_collection.find_one({
                                    "code": common_code
                                })
                                if existing_document:
                                        # If the document with the same code exists, update or insert into the appropriate array field
                                        if array_name in existing_document:
                                            # If the array_name already exists, push obj into the array
                                            CASE_collection.update_one(
                                                {"code": common_code},
                                                {"$push": {f"{array_name}": obj}}
                                            )
                                        else:
                                            # If the array_name does not exist, create a new array field and insert obj
                                            CASE_collection.update_one(
                                                {"code": common_code},
                                                {"$set": {f"{array_name}": [obj]}}
                                            )
                                else:
                                    # If no document with the same code and array_name exists, create a new document
                                    CASE_collection.insert_one({
                                        "_id": ObjectId(),
                                        "code": common_code,
                                        f"{array_name}": [obj]
                                    })
                                # Optionally, you can break out of the loop once the update/insert is done
                                break
                    session['success_message'] = 'MLRO officer updated successfully.'

       
        mlro_email = session['email_id']
        
        time = datetime.now()
        # Extract only the date and set the time to midnight
        
        current_date = str(time.date())  # Get the current date in 'YYYY-MM-DD' format
        # Update query for both commented_perday and case_tickets_perday
        update_query = {
            '$pull': {'allocated_tickets': ticket_id},
            '$push': {'case_tickets': ticket_id}
        }
        # Additional functionality related to case_tickets_perday
        users_collection.update_one(
            {'emailid': mlro_email, 'case_tickets': ticket_id},
            {
                '$pull': {'case_tickets': ticket_id}
            }
        )
        findingTicketLocation = users_collection.find_one({'emailid': mlro_email,'allocated_tickets': ticket_id})
        if findingTicketLocation:
            # Ensure 'case_tickets_perday' is an array, create if it doesn't exist
            case_tickets_perday = findingTicketLocation.get('case_tickets_perday', [])
            # Check if an object with the current date already exists in case_tickets_perday
            existing_index_case = next((index for index, entry in enumerate(case_tickets_perday) if current_date in entry), None)
            if existing_index_case is not None:
                # If the entry exists, increment the count in case_tickets_perday
                users_collection.update_one(
                    {"$or":[{'emailid': mlro_email, 'allocated_tickets': ticket_id},{'emailid': mlro_email, 'Sent_Back_Case_Alerts': ticket_id}]},
                    {'$inc': {'case_tickets_perday.' + str(existing_index_case) + '.' + current_date: 1}}
                )
            else:
                # If the entry doesn't exist, create a new object for the current date in case_tickets_perday
                users_collection.update_one(
                    {'emailid': mlro_email, 'allocated_tickets': ticket_id},
                    {'$push': {'case_tickets_perday': {current_date: 1}}}
                )
            # Update for commented_tickets and case_tickets
            users_collection.update_one(
                {'emailid': mlro_email, 'allocated_tickets': ticket_id},
                update_query
            )
            endPointRedirect = 'MLRONextLevel'
        else:
            users_collection.update_one(
                {'emailid': mlro_email, 'Sent_Back_Case_Alerts': ticket_id},
                {
                    '$pull': {'Sent_Back_Case_Alerts': ticket_id},
                    '$push': {'case_tickets': ticket_id}
                }
            )

            time = datetime.now()
            # Extract only the date and set the time to midnight
            timeDate = str(time.date())
            perDay = users_collection.find_one({"emailid":mlro_email,"case_tickets_perday":{"$exists":True}})
            if perDay:
                                dateExists = users_collection.find_one({"emailid": mlro_email, f'case_tickets_perday.{timeDate}': {"$exists": True}})
                                if dateExists:
                                    users_collection.update_one(
                                            {'emailid': mlro_email, 'case_tickets_perday': { '$elemMatch': { timeDate: { '$exists': True } } }},
                                            {"$inc": {f'case_tickets_perday.$.{timeDate}': 1}}
                                        )
                                else:
                                    users_collection.update_one({"emailid":mlro_email},{"$push":{"case_tickets_perday":{timeDate:1}}})
            else:
                                users_collection.update_one({"emailid":mlro_email},{"$set":{"case_tickets_perday":[{timeDate:1}]}})
            
            
            
            users_collection.update_one(
                {'emailid': mlro_email, 'Sent_Back_Alerts': ticket_id},
                {
                    '$pull': {'Sent_Back_Alerts': ticket_id},
                    '$push': {'case_tickets': ticket_id}
                }
            )
            endPointRedirect = 'display_Sent_Back_Alerts'
        


        # Update 'allocated_tickets' for cmMail
        info = users_collection.find_one({'emailid': mlro_email})
        cmMail = info["assigned_to"]
        # Update 'allocated_tickets' functionality (keep it the same as before)
        update_query_cmmail_tickets = {
            '$push': {'allocated_tickets': ticket_id},
        } 
        users_collection.update_one(
            {'emailid': cmMail},
            update_query_cmmail_tickets
        )
        # Update 'allocated_perday' functionality
        result = users_collection.update_one(
            {'emailid': cmMail, 'allocated_perday.date': current_date},
            {'$inc': {'allocated_perday.$[elem].count': 1}},
            array_filters=[{'elem.date': current_date}]
        )
        # If the document for the current date doesn't exist, insert a new document
        if result.modified_count == 0:
            users_collection.update_one(
                {'emailid': cmMail},
                {'$push': {'allocated_perday': {'date': current_date, 'count': 1}}}
            )
        return endPointRedirect
        
def mlroCasecloseFormStore(ticket_id,dataObject,user):      
        # Update in the first collection (TM_collection)
        current_datetime = datetime.now()
        current_date = current_datetime.date()
        midnight_datetime = datetime.combine(current_date, datetime.min.time())
        
        for document in TM_collection.find():
            for array_name in ["output_data1", "output_data2", "output_data3"]:
                if array_name in document:
                    for obj in document[array_name]:
                        if "ticket_id" in obj and obj["ticket_id"] == ticket_id:
                                        # Remove the document from TM_Collection
                                      
                                TM_collection.update_one(
                                    {"_id": document["_id"]},
                                    {"$pull": {f"{array_name}": {"ticket_id": ticket_id}}}
                                )
                                del dataObject["finalReport"]
                                nextOfficer = dataObject["sentTo"]
                                obj["status"]["cm_officer"] = nextOfficer
                                com = dataObject["comment"]
                                prefilled = dataObject["prefilled"]
                                
                                if len(com) != 0 and len(prefilled) != 0:
                                 commentobj ={"mlrocomment":com,
                                                       "cmcomment":None,
                                                       "agmcomment":None,
                                                       "dgmcomment":None
                                                       }
                                 obj["CaseComment"] = commentobj
                                 prefilledComment = {"mlrocomment":prefilled,
                                                       "cmcomment":None,
                                                       "agmcomment":None,
                                                       "dgmcomment":None
                                                       }
                                 obj["prefilledComment"] = prefilledComment
                                 
                                else:
                                 commentobj ={"mlrocomment":"Case Created due to some Suspicious Amount Transaction ",
                                                       "cmcomment":None,
                                                       "agmcomment":None,
                                                       "dgmcomment":None
                                                       }
                                 obj["CaseComment"] = commentobj
                                 prefilledComment = {"mlrocomment":"Others",
                                                       "cmcomment":None,
                                                       "agmcomment":None,
                                                       "dgmcomment":None
                                                       }
                                 obj["prefilledComment"] = prefilledComment
                                 
                                del dataObject['comment']
                                del dataObject["prefilled"]

                                print(dataObject)

                                obj["Case_Details"] = dataObject
                                obj["updated_on"] = midnight_datetime
                                common_code = document['code']

                                print("this is obj : ",obj)
                                # removing the previous document with ticket id if the ticket got re sent by CM/SM
                                all_collections = [CLOSE_CASE_collection]
                                array_names = ["output_data1", "output_data2", "output_data3"]
                                for collection, array_name in product(all_collections, array_names):
                                        collection.update_one( {f"{array_name}.ticket_id": ticket_id},{"$pull": {f"{array_name}": {"ticket_id": ticket_id}}})

                                # Check if a document with the same code and array_name already exists
                                existing_document = CLOSE_CASE_collection.find_one({
                                    "code": common_code
                                })

                                if existing_document:
                                        # If the document with the same code exists, update or insert into the appropriate array field
                                        if array_name in existing_document:
                                            # If the array_name already exists, push obj into the array
                                            CLOSE_CASE_collection.update_one(
                                                {"code": common_code},
                                                {"$push": {f"{array_name}": obj}}
                                            )
                                        else:
                                            # If the array_name does not exist, create a new array field and insert obj
                                            CLOSE_CASE_collection.update_one(
                                                {"code": common_code},
                                                {"$set": {f"{array_name}": [obj]}}
                                            )
                                else:
                                    # If no document with the same code and array_name exists, create a new document
                                    CLOSE_CASE_collection.insert_one({
                                        "_id": ObjectId(),
                                        "code": common_code,
                                        f"{array_name}": [obj]
                                    })

                                # Optionally, you can break out of the loop once the update/insert is done
                                break
                    session['success_message'] = 'MLRO officer updated successfully.'

        # Update in the second collection (TY_collection)
        for document in TY_collection.find():
            for array_name in ["output_data1", "output_data2", "output_data3"]:
                if array_name in document:
                    for obj in document[array_name]:
                        if "ticket_id" in obj and obj["ticket_id"] == ticket_id:
                            # Remove the document from TM_Collection
                            
                            TY_collection.update_one(
                                   {"_id": document["_id"]},
                                    {"$pull": {f"{array_name}": {"ticket_id": ticket_id}}}
                                )
                            del dataObject["finalReport"]
                            nextOfficer = dataObject["sentTo"]
                            obj["status"]["cm_officer"] = nextOfficer
                            
                            com = dataObject["comment"]
                            prefilled = dataObject["prefilled"]
                                
                            if len(com) != 0 and len(prefilled) != 0:
                                 commentobj ={"mlrocomment":com,
                                                       "cmcomment":None,
                                                       "agmcomment":None,
                                                       "dgmcomment":None
                                                       }
                                 obj["CaseComment"] = commentobj
                                 prefilledComment = {"mlrocomment":prefilled,
                                                       "cmcomment":None,
                                                       "agmcomment":None,
                                                       "dgmcomment":None
                                                       }
                                 obj["prefilledComment"] = prefilledComment
                                 
                            else:
                                 commentobj ={"mlrocomment":"Case Created due to some Suspicious Amount Transaction ",
                                                       "cmcomment":None,
                                                       "agmcomment":None,
                                                       "dgmcomment":None
                                                       }
                                 obj["CaseComment"] = commentobj
                                 prefilledComment = {"mlrocomment":"Others",
                                                       "cmcomment":None,
                                                       "agmcomment":None,
                                                       "dgmcomment":None
                                                       }
                                 obj["prefilledComment"] = prefilledComment
                                 
                            del dataObject['comment']
                            del dataObject["prefilled"]

                            obj["Case_Details"] = dataObject
                            obj["updated_on"] = midnight_datetime


                            common_code = document['code']
                            print("this is obj : ",obj)
                            # removing the previous document with ticket id if the ticket got re sent by CM/SM
                            all_collections = [CLOSE_CASE_collection]
                            array_names = ["output_data1", "output_data2", "output_data3"]
                            for collection, array_name in product(all_collections, array_names):
                                    collection.update_one( {f"{array_name}.ticket_id": ticket_id},{"$pull": {f"{array_name}": {"ticket_id": ticket_id}}})


                            # Check if a document with the same code and array_name already exists
                            existing_document = CLOSE_CASE_collection.find_one({
                                "code": common_code
                            })

                            if existing_document:
                               # If the document with the same code exists, update or insert into the appropriate array field
                                        if array_name in existing_document:
                                            # If the array_name already exists, push obj into the array
                                            CLOSE_CASE_collection.update_one(
                                                {"code": common_code},
                                                {"$push": {f"{array_name}": obj}}
                                            )
                                        else:
                                            # If the array_name does not exist, create a new array field and insert obj
                                            CLOSE_CASE_collection.update_one(
                                                {"code": common_code},
                                                {"$set": {f"{array_name}": [obj]}}
                                            )
                            else:
                                # If no document with the same code and array_name exists, create a new document
                                CLOSE_CASE_collection.insert_one({
                                    "_id": ObjectId(),
                                    "code": common_code,
                                    f"{array_name}": [obj]
                                })

                            # Optionally, you can break out of the loop once the update/insert is done
                            break
    
                    session['success_message'] = 'MLRO officer updated successfully.'
        # Update in the third collection (RM_collection)
        for document in RM_collection.find():
            for array_name in ["output_data1", "output_data2", "output_data3"]:
                if array_name in document:
                    for obj in document[array_name]:
                        if "ticket_id" in obj and obj["ticket_id"] == ticket_id:
                                
                                RM_collection.update_one(
                                    {"_id": document["_id"]},
                                    {"$pull": {f"{array_name}": {"ticket_id": ticket_id}}}
                                )

                                del dataObject["finalReport"]
                                nextOfficer = dataObject["sentTo"]
                                obj["status"]["cm_officer"] = nextOfficer

                                com = dataObject["comment"]
                                prefilled = dataObject["prefilled"]
                                
                                if len(com) != 0 and len(prefilled) != 0:
                                 commentobj ={"mlrocomment":com,
                                                       "cmcomment":None,
                                                       "agmcomment":None,
                                                       "dgmcomment":None
                                                       }
                                 obj["CaseComment"] = commentobj
                                 prefilledComment = {"mlrocomment":prefilled,
                                                       "cmcomment":None,
                                                       "agmcomment":None,
                                                       "dgmcomment":None
                                                       }
                                 obj["prefilledComment"] = prefilledComment
                                 
                                else:
                                 commentobj ={"mlrocomment":"Case Created due to some Suspicious Amount Transaction ",
                                                       "cmcomment":None,
                                                       "agmcomment":None,
                                                       "dgmcomment":None
                                                       }
                                 obj["CaseComment"] = commentobj
                                 prefilledComment = {"mlrocomment":"Others",
                                                       "cmcomment":None,
                                                       "agmcomment":None,
                                                       "dgmcomment":None
                                                       }
                                 obj["prefilledComment"] = prefilledComment
                                 
                                del dataObject['comment']
                                del dataObject["prefilled"]

                                obj["Case_Details"] = dataObject
                                obj["updated_on"] = midnight_datetime


                                common_code = document['code']
                                print("this is obj : ",obj)

                                # removing the previous document with ticket id if the ticket got re sent by CM/SM
                                all_collections = [CLOSE_CASE_collection]
                                array_names = ["output_data1", "output_data2", "output_data3"]
                                for collection, array_name in product(all_collections, array_names):
                                        collection.update_one( {f"{array_name}.ticket_id": ticket_id},{"$pull": {f"{array_name}": {"ticket_id": ticket_id}}})


                                # Check if a document with the same code and array_name already exists
                                existing_document = CLOSE_CASE_collection.find_one({
                                    "code": common_code
                                })

                                if existing_document:
                                    # If the document with the same code exists, update or insert into the appropriate array field
                                        if array_name in existing_document:
                                            # If the array_name already exists, push obj into the array
                                            CLOSE_CASE_collection.update_one(
                                                {"code": common_code},
                                                {"$push": {f"{array_name}": obj}}
                                            )
                                        else:
                                            # If the array_name does not exist, create a new array field and insert obj
                                            CLOSE_CASE_collection.update_one(
                                                {"code": common_code},
                                                {"$set": {f"{array_name}": [obj]}}
                                            )
                                else:
                                    # If no document with the same code and array_name exists, create a new document
                                    CLOSE_CASE_collection.insert_one({
                                        "_id": ObjectId(),
                                        "code": common_code,
                                        f"{array_name}": [obj]
                                    })

                                # Optionally, you can break out of the loop once the update/insert is done
                                break
                    session['success_message'] = 'MLRO officer updated successfully.'
         # Update in the four collection (CLOSE_CASE_collection)
        for document in CLOSE_CASE_collection.find():
            for array_name in ["output_data1", "output_data2", "output_data3"]:
                if array_name in document:
                    for obj in document[array_name]:
                        if "ticket_id" in obj and obj["ticket_id"] == ticket_id and "finalReport" in dataObject:
                                
                                CLOSE_CASE_collection.update_one(
                                    {"_id": document["_id"]},
                                    {"$pull": {f"{array_name}": {"ticket_id": ticket_id}}}
                                )

                                del dataObject["finalReport"]
                                nextOfficer = dataObject["sentTo"]
                                obj["status"]["cm_officer"] = nextOfficer

                                com = dataObject["comment"]
                                prefilled = dataObject["prefilled"]
                                
                                if len(com) != 0 and len(prefilled) != 0:
                                 commentobj ={"mlrocomment":com,
                                                       "cmcomment":None,
                                                       "agmcomment":None,
                                                       "dgmcomment":None
                                                       }
                                 obj["CaseComment"] = commentobj
                                 prefilledComment = {"mlrocomment":prefilled,
                                                       "cmcomment":None,
                                                       "agmcomment":None,
                                                       "dgmcomment":None
                                                       }
                                 obj["prefilledComment"] = prefilledComment
                                 
                                else:
                                 commentobj ={"mlrocomment":"Case Created due to some Suspicious Amount Transaction ",
                                                       "cmcomment":None,
                                                       "agmcomment":None,
                                                       "dgmcomment":None
                                                       }
                                 obj["CaseComment"] = commentobj
                                 prefilledComment = {"mlrocomment":"Others",
                                                       "cmcomment":None,
                                                       "agmcomment":None,
                                                       "dgmcomment":None
                                                       }
                                 obj["prefilledComment"] = prefilledComment
                                 
                                del dataObject['comment']
                                del dataObject["prefilled"]

                                obj["Case_Details"] = dataObject
                                obj["updated_on"] = midnight_datetime


                                common_code = document['code']
                                print("this is obj : ",obj)

                                # removing the previous document with ticket id if the ticket got re sent by CM/SM
                                all_collections = [CLOSE_CASE_collection]
                                array_names = ["output_data1", "output_data2", "output_data3"]
                                for collection, array_name in product(all_collections, array_names):
                                        collection.update_one( {f"{array_name}.ticket_id": ticket_id},{"$pull": {f"{array_name}": {"ticket_id": ticket_id}}})

                                # Check if a document with the same code and array_name already exists
                                existing_document = CLOSE_CASE_collection.find_one({
                                    "code": common_code
                                })

                                if existing_document:
                                    # If the document with the same code exists, update or insert into the appropriate array field
                                        if array_name in existing_document:
                                            # If the array_name already exists, push obj into the array
                                            CLOSE_CASE_collection.update_one(
                                                {"code": common_code},
                                                {"$push": {f"{array_name}": obj}}
                                            )
                                        else:
                                            # If the array_name does not exist, create a new array field and insert obj
                                            CLOSE_CASE_collection.update_one(
                                                {"code": common_code},
                                                {"$set": {f"{array_name}": [obj]}}
                                            )
                                else:
                                    # If no document with the same code and array_name exists, create a new document
                                    CLOSE_CASE_collection.insert_one({
                                        "_id": ObjectId(),
                                        "code": common_code,
                                        f"{array_name}": [obj]
                                    })

                                # Optionally, you can break out of the loop once the update/insert is done
                                break
                    session['success_message'] = 'MLRO officer updated successfully.'
        
        
        mlro_email = session['email_id']
        current_date = datetime.now().strftime('%Y-%m-%d')  # Get the current date in 'YYYY-MM-DD' format
        findingTicketLocation = users_collection.find_one({'emailid': mlro_email, 'allocated_tickets': ticket_id})
        # Prepare the new object for the current date
        new_entry = {current_date: 1}
        update_query = {
            '$pull': {'allocated_tickets': ticket_id},
            '$push': {'commented_tickets': ticket_id}
        }
        # If the document exists
        if findingTicketLocation:
            # Ensure 'commented_perday' is an array, create if it doesn't exist
            commented_perday = findingTicketLocation.get('commented_perday', [])
            # Check if an object with the current date already exists
            existing_index = next((index for index, entry in enumerate(commented_perday) if current_date in entry), None)
            if existing_index is not None:
                # If the entry exists, increment the count
                users_collection.update_one(
                    {'emailid': mlro_email, 'allocated_tickets': ticket_id},
                    {'$inc': {'commented_perday.' + str(existing_index) + '.' + current_date: 1}}
                )
            else:
                # If the entry doesn't exist, create a new object for the current date
                users_collection.update_one(
                    {'emailid': mlro_email, 'allocated_tickets': ticket_id},
                    {'$push': {'commented_perday': new_entry}}
                )
            # Update the original functionality
            users_collection.update_one(
                {'emailid': mlro_email, 'allocated_tickets': ticket_id},
                update_query
            )
        else:
            # If the document doesn't exist, create it with 'commented_perday' as an array
            users_collection.update_one(
                {'emailid': mlro_email, 'Sent_Back_Alerts': ticket_id},
                {**update_query, '$push': {'commented_perday': new_entry}},
                upsert=True  # Create the document if it doesn't exist
            )
       
    
def CaseFormUpdate(ticket_id,dataObject,user):
        current_datetime = datetime.now()
        current_date = current_datetime.date()
        midnight_datetime = datetime.combine(current_date, datetime.min.time())
        # Update in the first collection (TM_collection)
        mlro_email = session['email_id']
        info = users_collection.find_one({'emailid': mlro_email})
        for document in CASE_collection.find():
            for array_name in ["output_data1", "output_data2", "output_data3"]:
                if array_name in document:
                    for obj in document[array_name]:
                        if "ticket_id" in obj and obj["ticket_id"] == ticket_id:
                                com = dataObject["comment"]
                                prefilled = dataObject["prefilled"]
                                finalReport = dataObject["finalReport"]
                                sentTo = dataObject["sentTo"]

                                if len(com) != 0 and len(prefilled) != 0:
                                    if info["role"] == "CM/SM":
                                        nextOfficer = dataObject["sentTo"]
                                        CASE_collection.update_one(
                                                    {f"{array_name}.ticket_id": ticket_id},
                                                    {"$set": {f"{array_name}.$.CaseComment.cmcomment": com,f"{array_name}.$.prefilledComment.cmcomment": prefilled,f"{array_name}.$.status.agm_officer": nextOfficer,f"{array_name}.$.levels.cm_level": user}}
                                                )
                                    if info["role"] == "AGM":
                                        nextOfficer = dataObject["sentTo"]
                                        CASE_collection.update_one(
                                                    {f"{array_name}.ticket_id": ticket_id},
                                                    {"$set": {f"{array_name}.$.CaseComment.agmcomment": com,f"{array_name}.$.prefilledComment.agmcomment": prefilled,f"{array_name}.$.status.dgm_officer": nextOfficer,f"{array_name}.$.levels.agm_level": user}}
                                                )
                                    if info["role"] == "DGM/PO":
                                        CASE_collection.update_one(
                                                    {f"{array_name}.ticket_id": ticket_id},
                                                    {"$set": {f"{array_name}.$.CaseComment.dgmcomment": com,f"{array_name}.$.prefilledComment.dgmcomment": prefilled,f"{array_name}.$.finalReport": finalReport,f"{array_name}.$.finalReport_Submited_on":midnight_datetime}}
                                            )
                                else:
                                    if info["role"] == "CM/SM":
                                        nextOfficer = dataObject["sentTo"]
                                        CASE_collection.update_one(
                                                    {f"{array_name}.ticket_id": ticket_id},
                                                    {"$set": {f"{array_name}.$.CaseComment.cmcomment": "Case Created due to some Suspicious Amount Transaction happend of Amount rs.500000",f"{array_name}.$.prefilledComment.cmcomment": "Others",f"{array_name}.$.status.agm_officer": nextOfficer,f"{array_name}.$.levels.cm_level": user}}
                                                )
                                    if info["role"] == "AGM":
                                        nextOfficer = dataObject["sentTo"]
                                        CASE_collection.update_one(
                                                    {f"{array_name}.ticket_id": ticket_id},
                                                    {"$set": {f"{array_name}.$.CaseComment.cmcomment": "Case Created due to some Suspicious Amount Transaction happend of Amount rs.500000",f"{array_name}.$.prefilledComment.agmcomment": "Others",f"{array_name}.$.status.dgm_officer": nextOfficer,f"{array_name}.$.levels.agm_level": user}}
                                                )
                                    if info["role"] == "DGM/PO":
                                        nextOfficer = dataObject["sentTo"]
                                        CASE_collection.update_one(
                                                    {f"{array_name}.ticket_id": ticket_id},
                                                    {"$set": {f"{array_name}.$.CaseComment.cmcomment": "Case Created due to some Suspicious Amount Transaction happend of Amount rs.500000",f"{array_name}.$.prefilledComment.dgmcomment": "Others",f"{array_name}.$.finalReport": finalReport,f"{array_name}.$.finalReport_Submited_on":midnight_datetime}}
                                                )
                                del dataObject['comment']
                                del dataObject["finalReport"]
                                print(dataObject)
                                # obj["Case_Details"] = dataObject
                                CASE_collection.update_one(
                                                {f"{array_name}.ticket_id": ticket_id},
                                                {"$set": {f"{array_name}.$.Case_Details": dataObject}}
                                            )
                                common_code = document['code']
                                print(common_code)
                    session['success_message'] = 'form updated successfully.'
        
        users_collection.update_one(
                {'emailid': mlro_email,'case_tickets': ticket_id},
                {
                    '$pull': {'case_tickets': ticket_id}
                }
                )
        endPointRedirect = None
        conformTicketEndPoint = users_collection.find_one({'emailid': mlro_email,'Sent_Back_Case_Alerts': ticket_id})
        if conformTicketEndPoint:
            users_collection.update_one(
                    {'emailid': mlro_email,'Sent_Back_Case_Alerts': ticket_id},
                    {
                        '$pull': {'Sent_Back_Case_Alerts': ticket_id},
                        '$push': {'case_tickets': ticket_id}
                    }
                    )
            endPointRedirect = 'display_Sent_Back_Alerts'
            
        users_collection.update_one(
            {'emailid': mlro_email,'allocated_tickets': ticket_id},
            {
                '$pull': {'allocated_tickets': ticket_id},
                '$push': {'case_tickets': ticket_id}
            }
            )
        if info["role"] == "CM/SM":
            cmMail = users_collection.find_one({"emailid":user,"status":"Approved"})["assigned_to_agm"]
            users_collection.update_one(
            {'emailid': cmMail,"status":"Approved"},
            {
                '$push': {'allocated_tickets': ticket_id}
            }
            )
            if endPointRedirect == "display_Sent_Back_Alerts":
                endPointRedirect = "display_Sent_Back_Alerts"
            else:
                endPointRedirect = 'CM_SM_NextLevel'
        if info["role"] == "AGM":
            cmMail = users_collection.find_one({"role":"DGM/PO"})["emailid"]
            users_collection.update_one(
            {'emailid': cmMail},
            {
                '$push': {'allocated_tickets': ticket_id}
            }
            )
            if endPointRedirect == "display_Sent_Back_Alerts":
                endPointRedirect = "display_Sent_Back_Alerts"
            else:
                endPointRedirect = 'AGMNextLevel'

# ================= Graph Part =========================
            
        time = datetime.now()
        # Extract only the date and set the time to midnight
        timeDate = str(time.date())
        # current_date = '2024-01-23'
        if info['role'] != 'DGM/PO':
                perDay = users_collection.find_one({"emailid":user,"case_tickets_perday":{"$exists":True}})
                if perDay:
                                dateExists = users_collection.find_one({"emailid": user, f'case_tickets_perday.{timeDate}': {"$exists": True}})
                                if dateExists:
                                    users_collection.update_one(
                                            {'emailid': user, 'case_tickets_perday': { '$elemMatch': { timeDate: { '$exists': True } } }},
                                            {"$inc": {f'case_tickets_perday.$.{timeDate}': 1}}
                                        )
                                else:
                                    users_collection.update_one({"emailid":user},{"$push":{"case_tickets_perday":{timeDate:1}}})
                else:
                                users_collection.update_one({"emailid":user},{"$set":{"case_tickets_perday":[{timeDate:1}]}})
                perDay = users_collection.find_one({"emailid":sentTo,"allocated_perday":{"$exists":True}})
                if perDay:
                                dateExists = users_collection.find_one({"emailid": sentTo, f'allocated_perday.{timeDate}': {"$exists": True}})
                                if dateExists:
                                    users_collection.update_one(
                                            {'emailid': sentTo, 'allocated_perday': { '$elemMatch': { timeDate: { '$exists': True } } }},
                                            {"$inc": {f'allocated_perday.$.{timeDate}': 1}}
                                        )
                                else:
                                    users_collection.update_one({"emailid":sentTo},{"$push":{"allocated_perday":{timeDate:1}}})
                else:
                                users_collection.update_one({"emailid":sentTo},{"$set":{"allocated_perday":[{timeDate:1}]}})
        else:
                if finalReport == 'Approved':
                    perDay = users_collection.find_one({"emailid":user,"DGMApproved_perDay":{"$exists":True}})
                    if perDay:
                                    dateExists = users_collection.find_one({"emailid": user, f'DGMApproved_perDay.{timeDate}': {"$exists": True}})
                                    if dateExists:
                                        users_collection.update_one(
                                                {'emailid': user, 'DGMApproved_perDay': { '$elemMatch': { timeDate: { '$exists': True } } }},
                                                {"$inc": {f'DGMApproved_perDay.$.{timeDate}': 1}}
                                            )
                                    else:
                                        users_collection.update_one({"emailid":user},{"$push":{"DGMApproved_perDay":{timeDate:1}}})
                    else:
                                    users_collection.update_one({"emailid":user},{"$set":{"DGMApproved_perDay":[{timeDate:1}]}})
                if finalReport == 'Rejected':
                    perDay = users_collection.find_one({"emailid":user,"DGMRejected_perDay":{"$exists":True}})
                    if perDay:
                                    dateExists = users_collection.find_one({"emailid": user, f'DGMRejected_perDay.{timeDate}': {"$exists": True}})
                                    if dateExists:
                                        users_collection.update_one(
                                                {'emailid': user, 'DGMRejected_perDay': { '$elemMatch': { timeDate: { '$exists': True } } }},
                                                {"$inc": {f'DGMRejected_perDay.$.{timeDate}': 1}}
                                            )
                                    else:
                                        users_collection.update_one({"emailid":user},{"$push":{"DGMRejected_perDay":{timeDate:1}}})
                    else:
                                    users_collection.update_one({"emailid":user},{"$set":{"DGMRejected_perDay":[{timeDate:1}]}})              
        
        return endPointRedirect;
   


@app.route('/caseFormPageEdit',methods=['POST'])
@secure_route(required_role=['AGM','CM/SM','DGM/PO'])
def caseFormPageEdit():
    msgg = session.pop('msgg', None)
    if request.method == 'POST':
        
        ticket_id_from_form = request.form['ticket_id']
        CustomerId = request.form['custId']
        # formDAta = mlroCaseForm(ticket_id_from_form)
        email = session['email_id']
        notify = clearnotification(email,'nextLevel')

        user = users_collection.find_one({"emailid":email})

        email = session['email_id']
        mailInfo = users_collection.find_one({"emailid": email})
        
        if 'image' in mailInfo:
                    # Encode the image data as a base64 string
                    mailInfo['image'] = base64.b64encode(mailInfo['image']).decode('utf-8')

        # allocatedCM = user["assigned_to"]
        data = {}
        # TY_collection, TM_collection, RM_collection,
        all_collections = [CASE_collection]
        array_names = ["output_data1", "output_data2", "output_data3"]
        CustomerName = None
        for collection, array_name in product(all_collections, array_names):
            pipeline = [
                {
                    "$unwind": f"${array_name}"
                },
                {
                    "$match": {
                        f"{array_name}.ticket_id":ticket_id_from_form
                    }
                },
                {
                    "$group": {
                        "_id": "$code",
                        "data": {"$push": f"${array_name}"}
                    }
                }
            ]
            data_from_collection = collection.aggregate(pipeline)
            for doc in data_from_collection:
                result = doc['data']
                CustomerName = result[0].get('Customer Name')
                if doc['_id'] not in list(data.keys()):
                    data[doc['_id']] = []
                    data[doc['_id']].extend(doc['data'])
                else:
                    data[doc['_id']].extend(doc['data'])
        print(email)
        if user["role"] == "CM/SM":
            allocated = users_collection.find_one({"emailid":email})["assigned_to_agm"]
            endpo = 'CM_SM_NextLevel'
        if user["role"] == "AGM":
            allocated = users_collection.find_one({"role":"DGM/PO"})["emailid"]
            endpo = 'AGMNextLevel'

        if user["role"] == "DGM/PO":
            allocated = None
            endpo = 'DGMNextLevel'

        return render_template('Form_PageEdit.html',ticket_id=ticket_id_from_form,CustomerId=CustomerId,role=user["role"],allocated=allocated,data=data,type=endpo,allImages=mailInfo,notify=notify,CustomerName=CustomerName,msgg=msgg)
    


@app.route('/leavePenddingDistribution',methods=['POST','GET'])
@secure_route(required_role='IT Officer')
def leavePenddingDistribution():
    user = users_collection.find_one({'role': 'IT Officer'})

    ituser = {'image': ""}
    if user:
        ituser = users_collection.find_one({'emailid': user.get('emailid')})

        if ituser and 'image' in ituser:
            ituser['image'] = base64.b64encode(ituser['image']).decode('utf-8')


    on_leave_info = users_collection.find({
                        '$and': [
                            {'leaveStatus': 'On Leave', 'status': 'Approved','allocated_tickets': {'$ne': None},'allocated_tickets':{'$ne': []}},
                            {'$or': [{'role': 'MLRO'}, {'role': 'CM/SM'}]},
                        ]
                    },{"_id": 0 })
    data = {}
    countMLRO = 0
    countCM = 0
    mlroOnLeaveName = []
    cmOnLeaveName = []
    for user in on_leave_info:
        print(user)
        if user["role"] == "MLRO":
            mlroOnLeaveName.append(user["name"])
            countMLRO +=1
        if user["role"] == "CM/SM":
            cmOnLeaveName.append(user["name"])
            countCM +=1
        if "allocated_tickets" in user:
            token = user["allocated_tickets"]
            for da in token:
                date_pattern = r'\d{4}-\d{2}-\d{2}'

                # Use re.search to find the first occurrence of the pattern in the token
                match = re.search(date_pattern, da)
                
                # Check if a match was found
                if match:
                    extracted_date = match.group()
                    # Check if the extracted_date is already a key in the dictionary
                    if extracted_date in data:
                        if 'permisionFormCount' in user:
                            user_info = {"name": user["name"], "role": user["role"],"emailid": user["emailid"],"count":user['permisionFormCount']}
                        else:
                            user_info = {"name": user["name"], "role": user["role"],"emailid": user["emailid"],"count":0}
                        
                        if user["name"] in data[extracted_date]:
                            data[extracted_date][user["name"]]["tickets"].append(da)
                        else:
                            data[extracted_date][user["name"]] = {"user_info": user_info, "tickets": [da]}
                    else:
                        data[extracted_date] = {user["name"]: {"user_info": {"name": user["name"],"emailid": user["emailid"],"role": user["role"],"count":0}, "tickets": [da]}}


    working_emps = users_collection.find({
                        '$and': [
                            {'leaveStatus': 'Working', 'status': 'Approved'},
                            {'$or': [{'role': 'MLRO'}, {'role': 'CM/SM'}]},
                        ]
                    },{"_id": 0 })
    
    workingMLRO = []
    workingCM = []

    for emp in working_emps:
        if emp["role"] == "MLRO":
            workingMLRO.append(emp["emailid"])
            # countMLRO +=1
        if emp["role"] == "CM/SM":
            workingCM.append(emp["emailid"])
            # countCM +=1
    print(workingMLRO)
    print(workingCM)

    # print("this is data",data)
    return render_template("leavePage.html",data=data,countMLRO=countMLRO,countCM=countCM,mlroOnLeaveName=mlroOnLeaveName,cmOnLeaveName=cmOnLeaveName,workingMLRO=workingMLRO,workingCM=workingCM,ituser=ituser,type='leavePenddingDistribution',role='IT Officer')
    

# ================= Permision Form to AGM ===================== 
@app.route('/permisionForm',methods=['POST','GET'])
@secure_route(required_role=['IT Officer'])
def permisionForm():
    fromMail = request.form.get('from')
    alertsToSend = request.form.get('alertsToSend')
    toMail = request.form.get('to')
    dateAllocated = request.form.get('dateAllocated')
    role = request.form.get('role')
    uniqId = str(uuid.uuid4())


    # print(fromMail," ",alertsToSend," ",toMail)
    alertsToSendNumber = int(alertsToSend)
    permisionFormDetails = {
        "fromMail":fromMail,
        "alertsToSend":alertsToSendNumber,
        "toMail":toMail,
        "dateAllocated":dateAllocated,
        "role":role,
        "id":uniqId
    }

    fromDataTickets = users_collection.find_one({'emailid':fromMail})

    allFromDataTickets = []
    

    for dataTickets in fromDataTickets["allocated_tickets"]:

        # Construct a regular expression pattern using the date
        pattern = re.compile(r'\b{}\b'.format(re.escape(dateAllocated)))

        # Use search to find the pattern in the token
        match = re.search(pattern, dataTickets) 

        if match:
            allFromDataTickets.append(dataTickets)

            
    randomTickets = []
    count = 1
    while count <= alertsToSendNumber:
        choiceTickets = random.choice(allFromDataTickets)
        randomTickets.append(choiceTickets)
        allFromDataTickets.remove(choiceTickets)
        count +=1
    
    for token in randomTickets:
         users_collection.update_one(
                {"emailid":fromMail},
                {"$pull": {"allocated_tickets": token},
                '$push': {'leave_tickets': token}}
                
                )


   
    agmPermision = users_collection.find_one({'role':'AGM','permisionFormDetails':{'$exists':True}})

    if agmPermision:
       users_collection.update_one({'role':'AGM'},{"$push": {'permisionFormDetails': permisionFormDetails}})
    else:
       users_collection.update_one({'role':'AGM'},{"$set":{"permisionFormDetails":[permisionFormDetails]}})
    return redirect(url_for('leavePenddingDistribution'))


# =====================================agm verify user distribution=======================================
@app.route('/leaveVerifyDistribution',methods=['POST','GET'])
@secure_route(required_role='AGM')
def leaveVerifyDistribution():
    agmVerify = users_collection.find_one({"role":'AGM'})
    notify = notification(agmVerify.get('emailid'))

    
    ituser = {'image': None}
    if agmVerify:
        ituser = users_collection.find_one({'emailid': agmVerify.get('emailid')})

        if ituser and 'image' in ituser:
            ituser['image'] = base64.b64encode(ituser['image']).decode('utf-8')    

    
    displaData = []
    if 'permisionFormDetails' in agmVerify:
     for data in agmVerify['permisionFormDetails']:
        displaData.append(data)

    return render_template('leaveVerify.html',data=displaData,ituser=ituser,type='leaveVerifyDistribution',role='AGM',notify=notify)  

# ============================= AGM Accepted permision=======================================

@app.route('/permisionFormVerified',methods=['POST','GET'])
@secure_route(required_role=['AGM'])
def permisionFormVerified():

        fromMail = request.form.get('from')
        alertsToSend = request.form.get('alertsToSend')
        toMail = request.form.get('to')
        dateAllocated = request.form.get('dateAllocated')
        role = request.form.get('role')
        uniqId = request.form.get('id')

        # print(fromMail," ",alertsToSend," ",toMail)
        alertsToSendNumber = int(alertsToSend)

        print(toMail)
      

        fromDataTickets = users_collection.find_one({'emailid':fromMail})

        allFromDataTickets = []
        

        for dataTickets in fromDataTickets["leave_tickets"]:

            # Construct a regular expression pattern using the date
            pattern = re.compile(r'\b{}\b'.format(re.escape(dateAllocated)))

            # Use search to find the pattern in the token
            match = re.search(pattern, dataTickets) 

            if match:
                allFromDataTickets.append(dataTickets)

                
        randomTickets = []
        count = 1
        while count <= alertsToSendNumber:
            choiceTickets = random.choice(allFromDataTickets)
            randomTickets.append(choiceTickets)
            allFromDataTickets.remove(choiceTickets)
            count +=1
        
        # print(randomTickets)
        for token in randomTickets:
            collections = [TM_collection,TY_collection,RM_collection]
            for collection in collections:
                for document in collection.find():
                    for array_name in ["output_data1", "output_data2", "output_data3"]:
                        if array_name in document:
                            for obj in document[array_name]:
                                if "allocate_to" in obj and obj["allocate_to"] is not None and obj["allocate_to"] in fromMail:
                                   
                                    collection.update_one(
                                        {f"{array_name}.ticket_id":token},
                                        {
                                            "$set":{
                                                f"{array_name}.$.allocate_to":toMail
                                            }
                                        }
                                    )

            users_collection.update_one(
                                    {"emailid":fromMail},
                                    {"$pull": {"leave_tickets": token}}
                                    
                                    )
                                    
                                    # Add the ticket_id to the "authentication" collection
            users_collection.update_one(
                                        {"emailid": toMail},
                                        {"$push": {"allocated_tickets": token}}
                                    )

            users_collection.update_one(
                                        {'role':'AGM'},
                                        {"$pull": {"permisionFormDetails": {"id": uniqId}}}
                                    )


        return redirect(url_for('leaveVerifyDistribution'))



@app.route('/permisionFormRejected',methods=['POST','GET'])
@secure_route(required_role=['AGM'])
def permisionFormRejected():
        fromMail = request.form.get('from')
        alertsToSend = request.form.get('alertsToSend')
        toMail = request.form.get('to')
        dateAllocated = request.form.get('dateAllocated')
        role = request.form.get('role')
        uniqId = request.form.get('id')

        # print(fromMail," ",alertsToSend," ",toMail)
        alertsToSendNumber = int(alertsToSend)

        print(toMail)
      

        fromDataTickets = users_collection.find_one({'emailid':fromMail})

        allFromDataTickets = []
        

        for dataTickets in fromDataTickets["leave_tickets"]:

            # Construct a regular expression pattern using the date
            pattern = re.compile(r'\b{}\b'.format(re.escape(dateAllocated)))

            # Use search to find the pattern in the token
            match = re.search(pattern, dataTickets) 

            if match:
                allFromDataTickets.append(dataTickets)

                
        randomTickets = []
        count = 1
        while count <= alertsToSendNumber:
            choiceTickets = random.choice(allFromDataTickets)
            randomTickets.append(choiceTickets)
            allFromDataTickets.remove(choiceTickets)
            count +=1
        
        # print(randomTickets)
        for token in randomTickets:
            users_collection.update_one(
                                    {"emailid":fromMail},
                                    {"$pull": {"leave_tickets": token},"$push": {"allocated_tickets": token}}
                                    
                                    )
                               
            users_collection.update_one(
                                        {'role':'AGM'},
                                        {"$pull": {"permisionFormDetails": {"id": uniqId}}}
                                    )


        return redirect(url_for('leaveVerifyDistribution'))



@app.route('/acc_violation_history', methods=['GET', 'POST'])
@secure_route(required_role=['MLRO','AGM','CM/SM','ROS','DGM/PO'])
def acc_violation_history():
    user = request.form["account_number"]
    mlro_email = session['email_id']
    notify = notification(mlro_email)

    ituser = {'image': None}
    if mlro_email:
        ituser = users_collection.find_one({'emailid': mlro_email})

        if ituser and 'image' in ituser:
            ituser['image'] = base64.b64encode(ituser['image']).decode('utf-8') 

    data = {}
    all_collections = [TY_collection, TM_collection, RM_collection, CASE_collection, CLOSE_CASE_collection]
    array_names = ["output_data1", "output_data2", "output_data3"]
    for collection, array_name in product(all_collections, array_names):
        pipeline = [
            {
                "$unwind": f"${array_name}"
            },
            {
                "$match": {
                    f"{array_name}.allocate_to":mlro_email,
                    f"{array_name}.Account Number":{"$in":[user]}
                }
            },
            {
                "$group": {
                    "_id": "$code",
                    "data": {"$push": f"${array_name}"}
                }
            }
        ]
        data_from_collection = collection.aggregate(pipeline)
        for doc in data_from_collection:
            if doc['_id'] not in list(data.keys()):
                data[doc['_id']] = []
                data[doc['_id']].extend(doc['data'])
            else:
                data[doc['_id']].extend(doc['data'])
    # for k,v in data.items():
    #     print(k)
    #     print(len(v))
    return render_template('acc_voilation_history.html',data=data,role="MLRO",type='MLRONextLevel',mlrouser=ituser,notify=notify)

def get_number_from_value_dict(value_dict):
    account_number = value_dict.get('Account Number', None)
    card_number = value_dict.get('Card Number', None)
    aadhar_number = value_dict.get('Identification/Aadhar Number', None)

    if account_number and account_number != "None":
        return account_number
    elif card_number and card_number != "None":
        return card_number
    elif aadhar_number and aadhar_number != "None":
        return aadhar_number
    else:
        return ""
    
@app.route('/acc_holder_history', methods=['POST','GET'])
@secure_route(required_role=['MLRO','AGM','CM/SM','ROS','DGM/PO'])
def acc_holder_history():
    mlro_email = session['email_id']
    notify = notification(mlro_email)
    mlro = users_collection.find_one({"emailid": mlro_email})
    if mlro is None:
                return "User data not found. Please log in again."
    if 'image' in mlro:
                # Encode the image data as a base64 string
                mlro['image'] = base64.b64encode(mlro['image']).decode('utf-8')
    role = users_collection.find_one({'emailid':mlro_email})['role']
    if role == 'MLRO':
        typeo = request.form.get('typeo')
       
        if typeo:
            if 'closed_Data_To_CM' in session and typeo == None:
                typeEnd = session['closed_Data_To_CM']
                session['comm'] = 'return_Mlro_Alerts'

            elif 'display_Sent_Back_Alerts' in session and typeo == None:
                typeEnd = session['display_Sent_Back_Alerts']
                session['comm'] = 'display_Sent_Back_Alerts'

            elif typeo == 'return_Mlro_Alerts':
                if 'closed_Data_To_CM' not in session:
                    session['closed_Data_To_CM'] = "return_Mlro_Alerts"
                session['comm'] = 'return_Mlro_Alerts'

                typeEnd = "return_Mlro_Alerts"

            elif typeo == 'display_Sent_Back_Alerts':
                if 'display_Sent_Back_Alerts' not in session:
                    session['display_Sent_Back_Alerts'] = "display_Sent_Back_Alerts"
                session['comm'] = 'display_Sent_Back_Alerts'
                typeEnd = "display_Sent_Back_Alerts"
        else: 
            session['comm'] = 'MLRONextLevel'
            typeEnd = 'MLRONextLevel'

    if role == 'CM/SM':
        typeo = request.form.get('typeo')
       
        if typeo:
            if 'closed_Data_To_CM' in session and typeo == None:
                typeEnd = session['closed_Data_To_CM']
                session['comm'] = 'closed_Data_To_CM'

            elif 'display_Sent_Back_Alerts' in session and typeo == None:
                typeEnd = session['display_Sent_Back_Alerts']
                session['comm'] = 'display_Sent_Back_Alerts'

            elif typeo == 'closed_Data_To_CM':
                if 'closed_Data_To_CM' not in session:
                    session['closed_Data_To_CM'] = "closed_Data_To_CM"
                session['comm'] = 'closed_Data_To_CM'

                typeEnd = "closed_Data_To_CM"

            elif typeo == 'display_Sent_Back_Alerts':
                if 'display_Sent_Back_Alerts' not in session:
                    session['display_Sent_Back_Alerts'] = "display_Sent_Back_Alerts"
                session['comm'] = 'display_Sent_Back_Alerts'
                typeEnd = "display_Sent_Back_Alerts"
        else: 
            session['comm'] = 'CM_SM_NextLevel'
            typeEnd = 'CM_SM_NextLevel'
       
    if role == 'AGM':
        typeo = request.form.get('typeo')

       
        if typeo:
            if 'closed_Data_To_CM' in session and typeo == None:
                typeEnd = session['closed_Data_To_CM']
                session['comm'] = 'closed_Data_To_CM'

            elif 'display_Sent_Back_Alerts' in session and typeo == None:
                typeEnd = session['display_Sent_Back_Alerts']
                session['comm'] = 'display_Sent_Back_Alerts'
            
            elif 'offline_agm_Str' in session and typeo == None:
                typeEnd = session['offline_agm_Str']
                session['comm'] = 'offline_agm_Str'

            elif typeo == 'closed_Data_To_CM':
                if 'closed_Data_To_CM' not in session:
                    session['closed_Data_To_CM'] = "closed_Data_To_CM"
                session['comm'] = 'closed_Data_To_CM'

                typeEnd = "closed_Data_To_CM"

            elif typeo == 'display_Sent_Back_Alerts':
                if 'display_Sent_Back_Alerts' not in session:
                    session['display_Sent_Back_Alerts'] = "display_Sent_Back_Alerts"
                session['comm'] = 'display_Sent_Back_Alerts'
                typeEnd = "display_Sent_Back_Alerts"

            elif typeo == 'offline_agm_Str':
                if 'offline_agm_Str' not in session:
                    session['offline_agm_Str'] = "offline_agm_Str"
                session['comm'] = 'offline_agm_Str'
                typeEnd = "offline_agm_Str"
        elif 'closed_Data_To_CM' in session and typeo == None:
                typeEnd = session['closed_Data_To_CM']
                session['comm'] = 'closed_Data_To_CM'

        elif 'display_Sent_Back_Alerts' in session and typeo == None:
                typeEnd = session['display_Sent_Back_Alerts']
                session['comm'] = 'display_Sent_Back_Alerts'
            
        elif 'offline_agm_Str' in session and typeo == None:
                typeEnd = session['offline_agm_Str']
                session['comm'] = 'offline_agm_Str'
        else: 

            session['comm'] = 'AGMNextLevel'
            typeEnd = 'AGMNextLevel'
    if role == 'DGM/PO':
        typeo = request.form.get('typeo')


       
        if typeo:
            
            
            if 'offline_dgm_Str' in session and typeo == None:
                typeEnd = session['offline_dgm_Str']
                session['comm'] = 'offline_dgm_Str'


            elif typeo == 'offline_dgm_Str':
                if 'offline_dgm_Str' not in session:
                    session['offline_dgm_Str'] = "offline_dgm_Str"
                session['comm'] = 'offline_dgm_Str'
                typeEnd = "offline_dgm_Str"
        
            
        elif 'offline_dgm_Str' in session and typeo == None:
                typeEnd = session['offline_dgm_Str']
                session['comm'] = 'offline_dgm_Str'
        else: 

            session['comm'] = 'DGMNextLevel'
            typeEnd = 'DGMNextLevel'
    if role == 'ROS':
        typeEnd = 'ros'

    print("session : ",session)
    if  'ACC_Num' in session and  'ticket_id' in session and 'CUST_ID' in session :
        accnum = session['ACC_Num']
        ticket_id = session['ticket_id']
        custid = session['CUST_ID']
    else:    
        custidSession = request.form.get('custid') 
        accnumSession = request.form.get('accnum')
        ticket_idSession = request.form.get('ticket_id')

        session['ACC_Num'] = accnumSession
        session['ticket_id'] = ticket_idSession
        session['CUST_ID'] = custidSession
        
        accnum = session['ACC_Num']
        ticket_id = session['ticket_id']
        custid = session['CUST_ID']
        
    # custid = request.form.get('custid') 
    # accnum = request.form.get('accnum')
    # ticket_id = request.form.get('ticket_id')    

    collections = [RM_collection]
        # Query the first MongoDB collection
    for collection in collections:
            for document in collection.find():
                for array_name in ["output_data1", "output_data2", "output_data3"]:
                    if array_name in document:
                        for obj in document[array_name]:
                            if obj['ticket_id'] == ticket_id :
                                    mobile_no = obj['MobileNumber']
                                    IP_ADDRESS = obj['IP ADDRESS']
                                    PNR_COUNT = obj['PNR COUNT']
                                    Sub_net = obj['Subnet']
                                    ISP = obj['ISP']
                                    TAGS = obj['TAGS']

                                    print("mobile_no",mobile_no)
                                    print("IP_ADDRESS",IP_ADDRESS)
                                    print("PNR_COUNT",PNR_COUNT)


                                    print("123456789dfghhhhhhhhhhhhhhh0")
                                    print("scenario_code : ",obj['scenario_code'])
    
  
    pipeline = [
        {"$unwind": "$TXNDATA"},
        {"$match": {}}
    ]
    values_present = False
    all_collections = [TY_collection, TM_collection, RM_collection]
    array_names = ["output_data1", "output_data2", "output_data3"]
    Acc_no=""
    formatted_value = ""
    alert_code = ""
    transaction_amount = ""
    cust_profile = ""
    mobile_no =""
    IP_ADDRESS = ""
    PNR_COUNT = ""
    Sub_net = ""
    ISP = ""
    TAGS = ""


    for collection, array_name in product(all_collections, array_names):
        ticket_pipeline = [
            {"$unwind": f"${array_name}"},
            {"$match": {f"{array_name}.ticket_id": ticket_id}},
            {"$group": {"_id": "$code", "data": {"$push": f"${array_name}"}}}
        ]
        data_from_collection = collection.aggregate(ticket_pipeline)
        for d in data_from_collection:
            value_dict = d['data'][0]
            Acc_no = get_number_from_value_dict(value_dict)
    data_from_collection_all={}
    for collection, array_name in product(all_collections, array_names):
        main_pipeline = [
            {"$unwind": f"${array_name}"},
            {
                "$match": {
                    "$or": [
                        {f"{array_name}.Account Number": Acc_no},
                        {f"{array_name}.Card Number": Acc_no},
                        {f"{array_name}.Identification/Aadhar Number": Acc_no}
                    ]
                }
            },
            {"$group": {"_id": "$code", "data": {"$push": f"${array_name}"}}}
        ]
        data_from_collection_da = collection.aggregate(main_pipeline)
        for data in data_from_collection_da:
            data_from_collection_all[data['_id']]=data['data']
    print(data_from_collection_all)
    all_collections = [TY_collection, TM_collection, RM_collection]
    array_names = ["output_data1", "output_data2", "output_data3"]
    for collection, array_name in product(all_collections, array_names):
        ticket_pipeline = [
            {
                "$unwind": f"${array_name}"
            },
            {
                "$match": {
                    f"{array_name}.ticket_id":ticket_id
                }
            },
            {
                "$group": {
                    "_id": "$code",
                    "values":{"$first":"$Current_values"},
                    "data": {"$push": f"${array_name}"}
                }
            }
        ]
        data_from_collection = collection.aggregate(ticket_pipeline)
        for d in data_from_collection:
            value_dict =d['data'][0]
            alert_code = d['_id']
            transaction_amount = int(value_dict['Transaction Amount'])
            if 'Customer Profile' in list(value_dict.keys()):
                cust_profile = value_dict['Customer Profile']
            else:
                cust_profile = ""
            if 'Indicative_rule' in list(value_dict.keys()):
                formatted_value = value_dict['Indicative_rule']
            else:
                formatted_value = ""
    if custid!='' and custid is not None:
        if custid!='None':
            pipeline[1]["$match"]["TXNDATA.Customer ID"] = custid
            values_present=True
    elif accnum!='' and accnum is not None:
        if accnum!='None':
            pipeline[1]["$match"]["Account Number"] = accnum
            values_present=True
    print(values_present)
    if values_present:
        pipeline.extend([
            {
                "$group": {
                    "_id": {
                        "account": "$Account Number",
                        "name": "$TXNDATA.Customer Name",
                        "type": "$TXNDATA.Nature of account"
                    },
                    "data": {"$push": "$TXNDATA"}
                }
            }
        ])
        aggregate_result = list(txn_collection.aggregate(pipeline))
        if len(aggregate_result)==0:
            aggregate_result=[]
        data = {}
        data_from_col_df = pd.DataFrame()
        for doc in aggregate_result:
            account_value = doc['_id']['account']
            for data_item in doc['data']:
                data_item['account'] = account_value
            data_from_col_df = pd.concat([data_from_col_df, pd.DataFrame(doc['data'])])
        columns_to_check_uniqueness = ['Customer ID', 'Customer Name', 'Nature of account','Address','Pincode','City','Mobile Number','account','Acc_Opening_Date']  # Replace with the actual column names
        unique_rows_df = data_from_col_df.drop_duplicates(subset=columns_to_check_uniqueness)
        result_df = unique_rows_df[columns_to_check_uniqueness].copy()
        columns_to_convert_to_int = ['Pincode', 'Mobile Number']
        if alert_code!="TY_2_2":
            result_df[columns_to_convert_to_int] = result_df[columns_to_convert_to_int]
        customer_values ={}
        if not result_df.empty:
            data=result_df.to_dict(orient="records")
            customer_values['id'] = result_df['Customer ID'].unique()[0]
            customer_values['name'] = result_df['Customer Name'].unique()[0]
            customer_values['type'] = result_df['Nature of account'].unique()[0]
            # customer_values[''] = result_df['Account Number'].unique()[0]
    else:
        data={}
        customer_values={}
    return render_template('account_holder_details.html', 
                           data=data,customer_values=customer_values,
                           formatted_value=formatted_value,alert_code=alert_code,
                           amount=transaction_amount,cust_profile=cust_profile,
                           data_from_collection_all=data_from_collection_all,
                           mobile_no=str(mobile_no),
                           IP_ADDRESS=str(IP_ADDRESS),
                           PNR_COUNT=str(PNR_COUNT),
                           Sub_net=str(Sub_net),
                           ISP=str(ISP),notify=notify,
                           TAGS=str(TAGS),accnum=accnum,
                           type=typeEnd,role=role,allImages=mlro
                           )

# @app.route('/CM_SM_ALL', methods=['GET', 'POST'])
# @secure_route(required_role=['MLRO','IT Officer','AGM','BranchMakers','CM/SM','ROS','DGM/PO'])
# def CM_SM_ALL():
#     cm_email = session['email_id']
#     cm = users_collection.find_one({"emailid": cm_email})
#     if 'image' in cm:
#                 # Encode the image data as a base64 string
#                 cm['image'] = base64.b64encode(cm['image']).decode('utf-8')
#     return render_template('CM_SM_ALL.html',type='CM_SM_ALL',role='CM/SM',cmuser=cm)

@app.route('/graph1', methods=['GET', 'POST'])
@secure_route(required_role=['MLRO','AGM','CM/SM','ROS','DGM/PO'])
def graph1():

    mlro_email = session['email_id']
    notify = notification(mlro_email)
    mlro = users_collection.find_one({"emailid": mlro_email})
    if mlro is None:
                return "User data not found. Please log in again."
    if 'image' in mlro:
                # Encode the image data as a base64 string
                mlro['image'] = base64.b64encode(mlro['image']).decode('utf-8')
    role = users_collection.find_one({'emailid':mlro_email})['role']
    if role == 'MLRO':
            typeEnd = session['comm']

    if role == 'CM/SM':
            typeEnd = session['comm']

    if role == 'AGM':
            typeEnd = session['comm']


    if role == 'DGM/PO':
        typeEnd = session['comm']

    if role == 'ROS':
        typeEnd = 'ros'
    
    
    user_date = "2021-01-30"
    end_date = datetime.strptime(user_date, '%Y-%m-%d')
    start_date = end_date-timedelta(days=30)
    total_df = pd.DataFrame()
    data_from_col = txn_collection.aggregate([
        { "$unwind" : "$TXNDATA"},
        {
            "$match":{
                "TXNDATA.Transaction Date":{
                    "$gte":start_date,
                    "$lte":end_date
                },
                "TXNDATA.B Party Account number":{"$exists": True, "$ne": None},
                "TXNDATA.C Party Account number":{"$exists": True, "$ne": None},
                "TXNDATA.D Party Account number":{"$exists": True, "$ne": None}
            }
        },{
            "$group": {
                "_id": "$TXNDATA.Account Number",
                "data": {"$push": "$TXNDATA"}
            }
        }
    ])
    agg_result = list(data_from_col)
    data_from_col_df = pd.DataFrame()
    for doc in agg_result:
        data_from_col_df = pd.concat([data_from_col_df, pd.DataFrame(doc.get('data', []))])
    if not data_from_col_df.empty:
        grouped_data = data_from_col_df.groupby(["Customer ID", "Account Number"])
        for gdata, gname in grouped_data:
            gname['Combined_Parties'] = gname.apply(lambda row: [str(row['B Party Account number']), str(int(row['C Party Account number'])), str(int(row['D Party Account number']))], axis=1)
            gname['Transactions'] = gname.apply(lambda row: [int(row['Transaction Amount']),int(row['B Party Transaction Amount']), int(row['C Party Transaction Amount'])], axis=1)
            temp_df = gname[['Account Number', 'Customer ID']].drop_duplicates()
            temp_df['Connections'] = [gname['Combined_Parties'].tolist()]
            temp_df['Transactions']=[gname['Transactions'].tolist()]
            temp_df['Count']=len(gname)
            total_df = pd.concat([total_df, temp_df])
    result_dict = {}
    for key, group in total_df.groupby('Customer ID'):
        values_dict = {
            'Connections': group['Connections'].tolist(),
            'Transactions': group['Transactions'].tolist(),
            'Account Numbers':group['Account Number'].tolist()
        }
        result_dict[key] = values_dict
    print("typeEnd : ",session)
    return render_template('sample1.html',data=result_dict,notify=notify,type=typeEnd,role=role,allImages=mlro)

@app.route('/graph2', methods=['GET', 'POST'])
@secure_route(required_role=['MLRO','AGM','CM/SM','ROS','DGM/PO'])
def graph2():
    mlro_email = session['email_id']
    notify = notification(mlro_email)
    mlro = users_collection.find_one({"emailid": mlro_email})
    if mlro is None:
                return "User data not found. Please log in again."
    if 'image' in mlro:
                # Encode the image data as a base64 string
                mlro['image'] = base64.b64encode(mlro['image']).decode('utf-8')
    role = users_collection.find_one({'emailid':mlro_email})['role']
    if role == 'MLRO':
            typeEnd = session['comm']


    if role == 'CM/SM':
            typeEnd = session['comm']

    if role == 'AGM':
            typeEnd = session['comm']

            
    if role == 'DGM/PO':
        typeEnd = session['comm']

    if role == 'ROS':
        typeEnd = 'ros'


    Account_Number = request.form.get('Acc_no')
    user_date = "2021-01-30"
    end_date = datetime.strptime(user_date, '%Y-%m-%d')
    start_date = end_date-timedelta(days=30)
    total_df = pd.DataFrame()
    data_from_col = txn_collection.aggregate([
        { "$unwind" : "$TXNDATA"},
        {
            "$match":{
                "TXNDATA.Transaction Date":{
                    "$gte":start_date,
                    "$lte":end_date
                },
                "TXNDATA.B Party Account number":{"$exists": True, "$ne": None},
                "TXNDATA.C Party Account number":{"$exists": True, "$ne": None},
                "TXNDATA.D Party Account number":{"$exists": True, "$ne": None}
            }
        },{
            "$group": {
                "_id": "$TXNDATA.Account Number",
                "data": {"$push": "$TXNDATA"}
            }
        }
    ])
    agg_result = list(data_from_col)
    data_from_col_df = pd.DataFrame()
    for doc in agg_result:
        data_from_col_df = pd.concat([data_from_col_df, pd.DataFrame(doc.get('data', []))])
    if not data_from_col_df.empty:
        grouped_data = data_from_col_df.groupby(["Customer ID", "Account Number"])
        for gdata, gname in grouped_data:
            gname['Combined_Parties'] = gname.apply(lambda row: [str(row['B Party Account number']), str(int(row['C Party Account number'])), str(int(row['D Party Account number']))], axis=1)
            gname['Transactions'] = gname.apply(lambda row: [int(row['Transaction Amount']),int(row['B Party Transaction Amount']), int(row['C Party Transaction Amount'])], axis=1)
            temp_df = gname[['Account Number', 'Customer ID']].drop_duplicates()
            temp_df['Connections'] = [gname['Combined_Parties'].tolist()]
            temp_df['Transactions']=[gname['Transactions'].tolist()]
            temp_df['Count']=len(gname)
            total_df = pd.concat([total_df, temp_df])
    result_dict = {}
    for key, group in total_df.groupby('Customer ID'):
        values_dict = {
            'Connections': group['Connections'].tolist(),
            'Transactions': group['Transactions'].tolist(),
            'Account Numbers':group['Account Number'].tolist()
        }
        result_dict[key] = values_dict

    print("typeEnd : ",typeEnd)
    return render_template('sample3.html',data=result_dict,value=Account_Number,notify=notify,type=typeEnd,role=role,allImages=mlro)


@app.route('/mlro_status', methods=['GET', 'POST'])
@secure_route(required_role=['MLRO'])
def mlro_status():
       if request.method == "POST":
        print("hiiiiiiiiiiii")
        action = request.form.get('action')
        print("action",action)
        ticket_id = request.form.get('ticket_id')
        print("ticket_id",ticket_id)
        
        for document in TM_collection.find():
            for array_name in ["output_data1", "output_data2", "output_data3"]:
                if array_name in document:
                    for obj in document[array_name]:
                        if "ticket_id" in obj and obj["ticket_id"] == ticket_id:
                            obj["status"]["mlro_officer"] = ''
                            TM_collection.update_one(
                                {"_id": document["_id"]},
                                {"$set": {f"{array_name}.$[elem].status.mlro_officer": action}},
                                array_filters=[{"elem.ticket_id": ticket_id}]
                            )

        # Update in the second collection
        for document in TY_collection.find():
            for array_name in ["output_data1", "output_data2", "output_data3"]:
                if array_name in document:
                    for obj in document[array_name]:
                        if "ticket_id" in obj and obj["ticket_id"] == ticket_id:
                            obj["status"]["mlro_officer"] = ''
                            TY_collection.update_one(
                                {"_id": document["_id"]},
                                {"$set": {f"{array_name}.$[elem].status.mlro_officer": action}},
                                array_filters=[{"elem.ticket_id": ticket_id}]
                            )
                    session['success_message'] = 'MLRO officer updated successfully.'
        for document in RM_collection.find():
            for array_name in ["output_data1", "output_data2", "output_data3"]:
                if array_name in document:
                    for obj in document[array_name]:
                        if "ticket_id" in obj and obj["ticket_id"] == ticket_id:
                            obj["status"]["mlro_officer"] = ''
                            TY_collection.update_one(
                                {"_id": document["_id"]},
                                {"$set": {f"{array_name}.$[elem].status.mlro_officer": action}},
                                array_filters=[{"elem.ticket_id": ticket_id}]
                            )
                    session['success_message'] = 'MLRO officer updated successfully.'
        return redirect(url_for("MLRONextLevel"))
       
@app.route('/mlro_submit', methods=['GET', 'POST'])
@secure_route(required_role=['MLRO'])
def mlro_submit():
    dividedData = request.get_json()
    print("dividedData",dividedData)
    if dividedData:
            print("hellooooooooooooooo",dividedData[1])
            count = 0
            updateStatus = ""
            for subData in dividedData:
                if count == 0:
                    updateStatus = "Accepted"
                else:
                    updateStatus = "Rejected"
                count +=1
            
                for activeDate in subData:
                    ticket_id = activeDate["ticket_id"] 
                    print("ticket_id",ticket_id)
                    for document in TM_collection.find():
                        for array_name in ["output_data1", "output_data2", "output_data3"]:
                            if array_name in document:
                                for obj in document[array_name]:
                                    if "ticket_id" in obj and obj["ticket_id"] == ticket_id:
                                        obj["levels"]["mlro_level"] = ''
                                        TM_collection.update_one(
                                            {"_id": document["_id"]},
                                            {"$set": {f"{array_name}.$[elem].levels.mlro_level": updateStatus}},
                                            array_filters=[{"elem.ticket_id": ticket_id}]
                                        )
                        for document in TY_collection.find():
                            for array_name in ["output_data1", "output_data2", "output_data3"]:
                                if array_name in document:
                                    for obj in document[array_name]:
                                        if "ticket_id" in obj and obj["ticket_id"] == ticket_id:
                                            obj["levels"]["mlro_level"] = ''
                                            TY_collection.update_one(
                                                {"_id": document["_id"]},
                                                {"$set": {f"{array_name}.$[elem].levels.mlro_level": updateStatus}},
                                                array_filters=[{"elem.ticket_id": ticket_id}]
                                            )
                    session['success_message'] = 'MLRO officer send to next level successfully.'
                # filter_condition = {"alertsShared.ticket_id": activeDate["ticket_id"]}  # Replace with your actual token value
                # update_query = {"$set": {"alertsShared.$[element].levels": {"MLRO":updateStatus,"CM": None,
                #     "AGM": None,
                #     "DGM": None}}}
                # array_filters = [{"element.Token": activeDate["ticket_id"]}]  # Replace with your actual token value
                # TM_collection.update_many(filter_condition, update_query, array_filters=array_filters)
        
    return redirect(url_for("MLRONextLevel"))

@app.route('/Closed_Mlro_Alerts', methods=['GET', 'POST'])
@secure_route(required_role='MLRO')
def Closed_Mlro_Alerts():
    success_message = session.pop('success_message', None)
    # Check user login
    
    if 'email_id' not in session:
        return redirect(url_for('post_login'))
    mlro_email = session['email_id']
    print('closed cases emailid:',mlro_email)
    notify = notification(mlro_email)

    mlro = users_collection.find_one({"emailid": mlro_email})
    if mlro is None:
        return "User data not found. Please log in again."
    if 'image' in mlro:
                # Encode the image data as a base64 string
                mlro['image'] = base64.b64encode(mlro['image']).decode('utf-8')
    
    ticket_numbers = mlro.get("commented_tickets", [])
    print("all_tickets", ticket_numbers)
    data = {}
    all_collections = [CLOSE_CASE_collection]
    array_names = ["output_data1", "output_data2", "output_data3"]
    for collection, array_name in product(all_collections, array_names):
        pipeline = [
            {
                "$unwind": f"${array_name}"
            },
            {
                "$match": {
                    f"{array_name}.allocate_to":mlro_email,
                    f"{array_name}.ticket_id":{"$in":ticket_numbers}
                }
            },
            {
                "$group": {
                    "_id": "$code",
                    "data": {"$push": f"${array_name}"}
                }
            }
        ]
        data_from_collection = collection.aggregate(pipeline)
        for doc in data_from_collection:
            if doc['_id'] not in list(data.keys()):
                data[doc['_id']] = []
                data[doc['_id']].extend(doc['data'])
            else:
                data[doc['_id']].extend(doc['data'])
    # for k,v in data.items():
    #     print(k)
    #     print(len(v))
    print("final_data", data)
    return render_template('Closed_Mlro_Alerts.html', data=data,success_message=success_message,mlrouser=mlro,role='MLRO',type='Closed_Mlro_Alerts',notify=notify)



@app.route('/CM_SM_NextLevel', methods=['GET', 'POST'])
@secure_route(required_role='CM/SM')
def CM_SM_NextLevel(): 
        success_message = session.pop('success_message', None)
        if 'email_id' not in session:
            return redirect(url_for('post_login'))
        cm_email = session['email_id']
        notify = clearnotification(cm_email,"nextLevel")

        cm = users_collection.find_one({"emailid": cm_email})
        if cm is None:
                    return "User data not found. Please log in again."
        if 'image' in cm:
            # Encode the image data as a base64 string
            cm['image'] = base64.b64encode(cm['image']).decode('utf-8')        
        if 'ACC_Num' in session and 'ticket_id' in session and 'CUST_ID' in session:
                        session.pop('ACC_Num')
                        session.pop('ticket_id')
                        session.pop('CUST_ID')
        if 'closed_Data_To_CM' in session:
            session.pop('closed_Data_To_CM')

        ticket_numbers = cm.get("allocated_tickets", [])
        data = {}
        all_collections = [CASE_collection]
        array_names = ["output_data1", "output_data2", "output_data3"]
        for collection, array_name in product(all_collections, array_names):
                    pipeline = [
                        {
                            "$unwind": f"${array_name}"
                        },
                        {
                            "$match": {
                                f"{array_name}.ticket_id":{"$in":ticket_numbers}
                            }
                        },
                        {
                            "$group": {
                                "_id": "$code",
                                "data": {"$push": f"${array_name}"}
                            }
                        }
                    ]
                    data_from_collection = collection.aggregate(pipeline)
                    for doc in data_from_collection:
                        print(doc)
                        if doc['_id'] not in list(data.keys()):
                            data[doc['_id']] = []
                            data[doc['_id']].extend(doc['data'])
                        else:
                            data[doc['_id']].extend(doc['data'])
        print(data)
        return render_template('alertOperation_CM_SM.html', data=data,success_message=success_message,cmuser=cm,role='CM/SM',type='CM_SM_NextLevel',notify=notify)

@app.route('/acc_violation_history_CM_AGM_DGM', methods=['GET', 'POST'])
@secure_route(required_role=['AGM','CM/SM','DGM/PO'])
def acc_violation_history_CM_AGM_DGM():
    user = request.form["account_number"]
    mlro_email = session['email_id']
    notify = notification(mlro_email)
    data = {}
    ituser = {'image': None}
    if mlro_email:
        ituser = users_collection.find_one({'emailid': mlro_email})

        if ituser and 'image' in ituser:
            ituser['image'] = base64.b64encode(ituser['image']).decode('utf-8') 

    all_collections = [CASE_collection]
    array_names = ["output_data1", "output_data2", "output_data3"]
    for collection, array_name in product(all_collections, array_names):
        pipeline = [
            {
                "$unwind": f"${array_name}"
            },
            {
                "$match": {
                    "$or": [
                        {f"{array_name}.status.cm_officer": mlro_email},
                        {f"{array_name}.status.agm_officer": mlro_email},
                        {f"{array_name}.status.dgm_officer": mlro_email},
                    ],
                    f"{array_name}.Account Number":{"$in":[user]}
                }
            },
            {
                "$group": {
                    "_id": "$code",
                    "data": {"$push": f"${array_name}"}
                }
            }
        ]
        data_from_collection = collection.aggregate(pipeline)
        for doc in data_from_collection:
            if doc['_id'] not in list(data.keys()):
                data[doc['_id']] = []
                data[doc['_id']].extend(doc['data'])
            else:
                data[doc['_id']].extend(doc['data'])
    role = users_collection.find_one({"emailid":mlro_email})["role"]

    if role == 'CM/SM':
        typeEnd = 'CM_SM_NextLevel'

    if role == 'AGM':
        typeEnd = 'AGMNextLevel'

    if role == 'DGM/PO':
        typeEnd = 'DGMNextLevel'

    if role == 'ROS':
        typeEnd = 'ros'

    return render_template('acc_voilation_history.html',data=data,role=role,type=typeEnd,allImages=ituser,notify=notify)

@app.route('/cm_status', methods=['GET', 'POST'])
@secure_route(required_role=['CM/SM'])
def cm_status():
       if request.method == "POST":
        print("hiiiiiiiiiiii")
        action = request.form.get('action')
        print("action",action)
        ticket_id = request.form.get('ticket_id')
        print("ticket_id",ticket_id)
        
        for document in TM_collection.find():
            for array_name in ["output_data1", "output_data2", "output_data3"]:
                if array_name in document:
                    for obj in document[array_name]:
                        if "ticket_id" in obj and obj["ticket_id"] == ticket_id:
                            obj["status"]["cm_officer"] = ''
                            TM_collection.update_one(
                                {"_id": document["_id"]},
                                {"$set": {f"{array_name}.$[elem].status.cm_officer": action}},
                                array_filters=[{"elem.ticket_id": ticket_id}]
                            )

        # Update in the second collection
        for document in TY_collection.find():
            for array_name in ["output_data1", "output_data2", "output_data3"]:
                if array_name in document:
                    for obj in document[array_name]:
                        if "ticket_id" in obj and obj["ticket_id"] == ticket_id:
                            obj["status"]["cm_officer"] = ''
                            TY_collection.update_one(
                                {"_id": document["_id"]},
                                {"$set": {f"{array_name}.$[elem].status.cm_officer": action}},
                                array_filters=[{"elem.ticket_id": ticket_id}]
                            )
                    session['success_message'] = 'CM/SM officer updated successfully.'
        return redirect(url_for("CM_SM_NextLevel"))

@app.route('/cm_submit', methods=['GET', 'POST'])
@secure_route(required_role=['CM/SM'])
def cm_submit():
    dividedData = request.get_json()
    # print("dividedData",dividedData)
    if dividedData:
            print("hellooooooooooooooo",dividedData[1])
            # count = 0
            updateStatus = ""
            for subData in dividedData:
                updateStatus = "Accepted"
                # if count == 0:
                #     updateStatus = "Accepted"
                # else:
                #     updateStatus = "Rejected"
                # count +=1
            
                for activeDate in subData:
                    ticket_id = activeDate["ticket_id"] 
                    print("ticket_id",ticket_id)
                    for document in TM_collection.find():
                        for array_name in ["output_data1", "output_data2", "output_data3"]:
                            if array_name in document:
                                for obj in document[array_name]:
                                    if "ticket_id" in obj and obj["ticket_id"] == ticket_id:
                                        obj["levels"]["cm_level"] = ''
                                        TM_collection.update_one(
                                            {"_id": document["_id"]},
                                            {"$set": {f"{array_name}.$[elem].levels.cm_level": updateStatus}},
                                            array_filters=[{"elem.ticket_id": ticket_id}]
                                        )
                        for document in TY_collection.find():
                            for array_name in ["output_data1", "output_data2", "output_data3"]:
                                if array_name in document:
                                    for obj in document[array_name]:
                                        if "ticket_id" in obj and obj["ticket_id"] == ticket_id:
                                            obj["levels"]["cm_level"] = ''
                                            TY_collection.update_one(
                                                {"_id": document["_id"]},
                                                {"$set": {f"{array_name}.$[elem].levels.cm_level": updateStatus}},
                                                array_filters=[{"elem.ticket_id": ticket_id}]
                                            )
                    session['success_message'] = 'MLRO officer send to next level successfully.'
                # filter_condition = {"alertsShared.ticket_id": activeDate["ticket_id"]}  # Replace with your actual token value
                # update_query = {"$set": {"alertsShared.$[element].levels": {"MLRO":updateStatus,"CM": None,
                #     "AGM": None,
                #     "DGM": None}}}
                # array_filters = [{"element.Token": activeDate["ticket_id"]}]  # Replace with your actual token value
                # TM_collection.update_many(filter_condition, update_query, array_filters=array_filters)
        
    return redirect(url_for("CM_SM_NextLevel"))

@app.route('/AGMNextLevel', methods=['GET', 'POST'])
@secure_route(required_role='AGM')
def AGMNextLevel(): 
        success_message = session.pop('success_message', None)
        if 'email_id' not in session:
            return redirect(url_for('post_login'))
        cm_email = session['email_id']
        notify = clearnotification(cm_email,'nextLevel')

        cm = users_collection.find_one({"emailid": cm_email})
        if cm is None:
            return "User data not found. Please log in again."
        if 'image' in cm:
            # Encode the image data as a base64 string
            cm['image'] = base64.b64encode(cm['image']).decode('utf-8')
                
        if 'ACC_Num' in session and 'ticket_id' in session and 'CUST_ID' in session:
                        session.pop('ACC_Num')
                        session.pop('ticket_id')
                        session.pop('CUST_ID')
        ticket_numbers = cm.get("allocated_tickets", [])
        data = {}
        all_collections = [CASE_collection]
        array_names = ["output_data1", "output_data2", "output_data3"]
        for collection, array_name in product(all_collections, array_names):
                    pipeline = [
                        {
                            "$unwind": f"${array_name}"
                        },
                        {
                            "$match": {
                                f"{array_name}.ticket_id":{"$in":ticket_numbers}
                            }
                        },
                        {
                            "$group": {
                                "_id": "$code",
                                "data": {"$push": f"${array_name}"}
                            }
                        }
                    ]
                    data_from_collection = collection.aggregate(pipeline)
                    for doc in data_from_collection:
                        print(doc)
                        if doc['_id'] not in list(data.keys()):
                            data[doc['_id']] = []
                            data[doc['_id']].extend(doc['data'])
                        else:
                            data[doc['_id']].extend(doc['data'])
        return render_template('alertOperationAGM.html', data=data,success_message=success_message,agmuser=cm,role='AGM',type='AGMNextLevel',notify=notify)
    #    return render_template('alertOperationAGM.html')

@app.route('/agm_status', methods=['GET', 'POST'])
@secure_route(required_role=['AGM'])
def agm_status():
       if request.method == "POST":
        print("hiiiiiiiiiiii")
        action = request.form.get('action')
        print("action",action)
        ticket_id = request.form.get('ticket_id')
        print("ticket_id",ticket_id)
        
        for document in TM_collection.find():
            for array_name in ["output_data1", "output_data2", "output_data3"]:
                if array_name in document:
                    for obj in document[array_name]:
                        if "ticket_id" in obj and obj["ticket_id"] == ticket_id:
                            obj["status"]["agm_officer"] = ''
                            TM_collection.update_one(
                                {"_id": document["_id"]},
                                {"$set": {f"{array_name}.$[elem].status.agm_officer": action}},
                                array_filters=[{"elem.ticket_id": ticket_id}]
                            )

        # Update in the second collection
        for document in TY_collection.find():
            for array_name in ["output_data1", "output_data2", "output_data3"]:
                if array_name in document:
                    for obj in document[array_name]:
                        if "ticket_id" in obj and obj["ticket_id"] == ticket_id:
                            obj["status"]["agm_officer"] = ''
                            TY_collection.update_one(
                                {"_id": document["_id"]},
                                {"$set": {f"{array_name}.$[elem].status.agm_officer": action}},
                                array_filters=[{"elem.ticket_id": ticket_id}]
                            )
                    session['success_message'] = 'AGM officer updated successfully.'
        return redirect(url_for("AGMNextLevel"))

@app.route('/agm_submit', methods=['GET', 'POST'])
@secure_route(required_role=['AGM'])
def agm_submit():
    dividedData = request.get_json()
    # print("dividedData",dividedData)
    if dividedData:
            print("hellooooooooooooooo",dividedData[1])
            # count = 0
            updateStatus = ""
            for subData in dividedData:
                updateStatus = "Accepted"
                # if count == 0:
                #     updateStatus = "Accepted"
                # else:
                #     updateStatus = "Rejected"
                # count +=1
            
                for activeDate in subData:
                    ticket_id = activeDate["ticket_id"] 
                    print("ticket_id",ticket_id)
                    for document in TM_collection.find():
                        for array_name in ["output_data1", "output_data2", "output_data3"]:
                            if array_name in document:
                                for obj in document[array_name]:
                                    if "ticket_id" in obj and obj["ticket_id"] == ticket_id:
                                        obj["levels"]["agm_level"] = ''
                                        TM_collection.update_one(
                                            {"_id": document["_id"]},
                                            {"$set": {f"{array_name}.$[elem].levels.agm_level": updateStatus}},
                                            array_filters=[{"elem.ticket_id": ticket_id}]
                                        )
                        for document in TY_collection.find():
                            for array_name in ["output_data1", "output_data2", "output_data3"]:
                                if array_name in document:
                                    for obj in document[array_name]:
                                        if "ticket_id" in obj and obj["ticket_id"] == ticket_id:
                                            obj["levels"]["agm_level"] = ''
                                            TY_collection.update_one(
                                                {"_id": document["_id"]},
                                                {"$set": {f"{array_name}.$[elem].levels.agm_level": updateStatus}},
                                                array_filters=[{"elem.ticket_id": ticket_id}]
                                            )
                    session['success_message'] = 'MLRO officer send to next level successfully.'
                # filter_condition = {"alertsShared.ticket_id": activeDate["ticket_id"]}  # Replace with your actual token value
                # update_query = {"$set": {"alertsShared.$[element].levels": {"MLRO":updateStatus,"CM": None,
                #     "AGM": None,
                #     "DGM": None}}}
                # array_filters = [{"element.Token": activeDate["ticket_id"]}]  # Replace with your actual token value
                # TM_collection.update_many(filter_condition, update_query, array_filters=array_filters)
        
    return redirect(url_for("AGMNextLevel"))




@app.route('/DGMNextLevel', methods=['GET', 'POST'])
@secure_route(required_role='DGM/PO')
def DGMNextLevel():
        success_message = session.pop('success_message', None)
        if 'email_id' not in session:
            return redirect(url_for('post_login'))
        cm_email = session['email_id']
        notify = clearnotification(cm_email,'nextLevel')

        cm = users_collection.find_one({"emailid": cm_email})
        if cm is None:
                    return "User data not found. Please log in again."
        if 'image' in cm:
            # Encode the image data as a base64 string
            cm['image'] = base64.b64encode(cm['image']).decode('utf-8') 


        if 'ACC_Num' in session and 'ticket_id' in session and 'CUST_ID' in session:
                        session.pop('ACC_Num')
                        session.pop('ticket_id')
                        session.pop('CUST_ID')
        ticket_numbers = cm.get("allocated_tickets", [])
        data = {}
        all_collections = [CASE_collection]
        array_names = ["output_data1", "output_data2", "output_data3"]
        for collection, array_name in product(all_collections, array_names):
                    pipeline = [
                        {
                            "$unwind": f"${array_name}"
                        },
                        {
                            "$match": {
                                f"{array_name}.ticket_id":{"$in":ticket_numbers}
                            }
                        },
                        {
                            "$group": {
                                "_id": "$code",
                                "data": {"$push": f"${array_name}"}
                            }
                        }
                    ]
                    data_from_collection = collection.aggregate(pipeline)
                    for doc in data_from_collection:
                        print(doc)
                        if doc['_id'] not in list(data.keys()):
                            data[doc['_id']] = []
                            data[doc['_id']].extend(doc['data'])
                        else:
                            data[doc['_id']].extend(doc['data'])
        return render_template('alertOperationDGM.html',data=data,success_message=success_message,dgmuser=cm,role='DGM/PO',type='DGMNextLevel',notify=notify)
    #    return render_template('alertOperationDGM.html')


@app.route('/dgm_status', methods=['GET', 'POST'])
@secure_route(required_role=['DGM/PO'])
def dgm_status():
       if request.method == "POST":
        print("hiiiiiiiiiiii")
        action = request.form.get('action')
        print("action",action)
        ticket_id = request.form.get('ticket_id')
        print("ticket_id",ticket_id)
        
        for document in TM_collection.find():
            for array_name in ["output_data1", "output_data2", "output_data3"]:
                if array_name in document:
                    for obj in document[array_name]:
                        if "ticket_id" in obj and obj["ticket_id"] == ticket_id:
                            obj["status"]["dgm_officer"] = ''
                            TM_collection.update_one(
                                {"_id": document["_id"]},
                                {"$set": {f"{array_name}.$[elem].status.dgm_officer": action}},
                                array_filters=[{"elem.ticket_id": ticket_id}]
                            )

        # Update in the second collection
        for document in TY_collection.find():
            for array_name in ["output_data1", "output_data2", "output_data3"]:
                if array_name in document:
                    for obj in document[array_name]:
                        if "ticket_id" in obj and obj["ticket_id"] == ticket_id:
                            obj["status"]["dgm_officer"] = ''
                            TY_collection.update_one(
                                {"_id": document["_id"]},
                                {"$set": {f"{array_name}.$[elem].status.dgm_officer": action}},
                                array_filters=[{"elem.ticket_id": ticket_id}]
                            )
                    session['success_message'] = 'AGM officer updated successfully.'
        return redirect(url_for("DGMNextLevel"))

@app.route('/dgm_submit', methods=['GET', 'POST'])
@secure_route(required_role=['DGM/PO'])
def dgm_submit():
    dividedData = request.get_json()
    # print("dividedData",dividedData)
    if dividedData:
            print("hellooooooooooooooo",dividedData[1])
            # count = 0
            updateStatus = ""
            for subData in dividedData:
                updateStatus = "Accepted"
                # if count == 0:
                #     updateStatus = "Accepted"
                # else:
                #     updateStatus = "Rejected"
                # count +=1
            
                for activeDate in subData:
                    ticket_id = activeDate["ticket_id"] 
                    print("ticket_id",ticket_id)
                    for document in TM_collection.find():
                        for array_name in ["output_data1", "output_data2", "output_data3"]:
                            if array_name in document:
                                for obj in document[array_name]:
                                    if "ticket_id" in obj and obj["ticket_id"] == ticket_id:
                                        obj["levels"]["dgm_level"] = ''
                                        TM_collection.update_one(
                                            {"_id": document["_id"]},
                                            {"$set": {f"{array_name}.$[elem].levels.dgm_level": updateStatus}},
                                            array_filters=[{"elem.ticket_id": ticket_id}]
                                        )
                        for document in TY_collection.find():
                            for array_name in ["output_data1", "output_data2", "output_data3"]:
                                if array_name in document:
                                    for obj in document[array_name]:
                                        if "ticket_id" in obj and obj["ticket_id"] == ticket_id:
                                            obj["levels"]["dgm_level"] = ''
                                            TY_collection.update_one(
                                                {"_id": document["_id"]},
                                                {"$set": {f"{array_name}.$[elem].levels.dgm_level": updateStatus}},
                                                array_filters=[{"elem.ticket_id": ticket_id}]
                                            )
                    session['success_message'] = 'MLRO officer send to next level successfully.'
                # filter_condition = {"alertsShared.ticket_id": activeDate["ticket_id"]}  # Replace with your actual token value
                # update_query = {"$set": {"alertsShared.$[element].levels": {"MLRO":updateStatus,"CM": None,
                #     "AGM": None,
                #     "DGM": None}}}
                # array_filters = [{"element.Token": activeDate["ticket_id"]}]  # Replace with your actual token value
                # TM_collection.update_many(filter_condition, update_query, array_filters=array_filters)
        
    return redirect(url_for("DGMNextLevel"))


# ==============Next Level after Submitting data view Section====================
data = [{'Id': '00112233', 'Date': '20/12/2000', 'ITOfficerName': 'tom', 'ITOfficerMail': 'tom@gmail.com', 'status': 'STR'}, {'Id': '00112233', 'Date': '20/12/2000', 'ITOfficerName': 'JIm', 'ITOfficerMail': 'JIm@gmail.com', 'status': 'Close STR'}, {'Id': '00112233', 'Date': '20/12/2000', 'ITOfficerName': 'tom', 'ITOfficerMail': 'tom@gmail.com', 'status': 'STR'}, {'Id': '00112233', 'Date': '20/12/2000', 'ITOfficerName': 'JIm', 'ITOfficerMail': 'JIm@gmail.com', 'status': 'STR'}, {'Id': '00112233', 'Date': '20/12/2000', 'ITOfficerName': 'tom', 'ITOfficerMail': 'tom@gmail.com', 'status': 'Close STR'}, {'Id': '00112233', 'Date': '20/12/2000', 'ITOfficerName': 'JIm', 'ITOfficerMail': 'JIm@gmail.com', 'status': 'STR'}, {'Id': '00112233', 'Date': '20/12/2000', 'ITOfficerName': 'JIm', 'ITOfficerMail': 'JIm@gmail.com', 'status': 'STR'}]

@app.route('/MLRONextLevelSubmitView', methods=['GET', 'POST'])
@secure_route(required_role='MLRO')
def MLRONextLevelSubmitView(): 
      success_message = session.pop('success_message', None)
      if 'email_id' not in session:
          return redirect(url_for('post_login'))
      mlro_email = session['email_id']
      print('mlro email:',mlro_email)
      notify = notification(mlro_email)

      mlro = users_collection.find_one({"emailid": mlro_email})
      if mlro is None:
                return "User data not found. Please log in again."
            
      if 'image' in mlro:
                # Encode the image data as a base64 string
                mlro['image'] = base64.b64encode(mlro['image']).decode('utf-8')
                  
      ticket_numbers = mlro.get("case_tickets", [])
      data = {}
      all_collections = [CASE_collection]
      array_names = ["output_data1", "output_data2", "output_data3"]
      for collection, array_name in product(all_collections, array_names):
                pipeline = [
                    {
                        "$unwind": f"${array_name}"
                    },
                    {
                        "$match": {
                            f"{array_name}.allocate_to":mlro_email,
                            f"{array_name}.ticket_id":{"$in":ticket_numbers}
                        }
                    },
                    {
                        "$group": {
                            "_id": "$code",
                            "data": {"$push": f"${array_name}"}
                        }
                    }
                ]
                data_from_collection = collection.aggregate(pipeline)
                for doc in data_from_collection:
                    print(doc)
                    if doc['_id'] not in list(data.keys()):
                        data[doc['_id']] = []
                        data[doc['_id']].extend(doc['data'])
                    else:
                        data[doc['_id']].extend(doc['data'])
      return render_template('MLROhigherLevel.html', data=data,mlrouser=mlro,role='MLRO',type='MLRONextLevelSubmitView',notify=notify)
           



@app.route('/AGMNextLevelSubmitView', methods=['GET', 'POST'])
@secure_route(required_role='AGM')
def AGMNextLevelSubmitView(): 
        success_message = session.pop('success_message', None)
        if 'email_id' not in session:
            return redirect(url_for('post_login'))
        mlro_email = session['email_id']
        notify = notification(mlro_email)

        mlro = users_collection.find_one({"emailid": mlro_email})
        if mlro is None:
            return "User data not found. Please log in again."
        if 'image' in mlro:
            # Encode the image data as a base64 string
            mlro['image'] = base64.b64encode(mlro['image']).decode('utf-8')
                
        ticket_numbers = mlro.get("case_tickets", [])
        data = {}
        all_collections = [CASE_collection]
        array_names = ["output_data1", "output_data2", "output_data3"]
        for collection, array_name in product(all_collections, array_names):
                    pipeline = [
                        {
                            "$unwind": f"${array_name}"
                        },
                        {
                            "$match": {
                                f"{array_name}.ticket_id":{"$in":ticket_numbers}
                            }
                        },
                        {
                            "$group": {
                                "_id": "$code",
                                "data": {"$push": f"${array_name}"}
                            }
                        }
                    ]
                    data_from_collection = collection.aggregate(pipeline)
                    for doc in data_from_collection:
                        print(doc)
                        if doc['_id'] not in list(data.keys()):
                            data[doc['_id']] = []
                            data[doc['_id']].extend(doc['data'])
                        else:
                            data[doc['_id']].extend(doc['data'])
        print(data)
        return render_template('AGMhigherLevel.html',data=data,agmuser=mlro,role='AGM',type='AGMNextLevelSubmitView',notify=notify)


@app.route('/CM_SM_NextLevelSubmitView', methods=['GET', 'POST'])
@secure_route(required_role='CM/SM')
def CM_SM_NextLevelSubmitView():
      success_message = session.pop('success_message', None)
      if 'email_id' not in session:
          return redirect(url_for('post_login'))
      cm_email = session['email_id']
      notify = notification(cm_email)

      cm = users_collection.find_one({"emailid": cm_email})
      if 'image' in cm:
                # Encode the image data as a base64 string
                cm['image'] = base64.b64encode(cm['image']).decode('utf-8')
      
            
      ticket_numbers = cm.get("case_tickets", [])
      data = {}
      all_collections = [CASE_collection]
      array_names = ["output_data1", "output_data2", "output_data3"]
      for collection, array_name in product(all_collections, array_names):
                pipeline = [
                    {
                        "$unwind": f"${array_name}"
                    },
                    {
                        "$match": {
                            f"{array_name}.ticket_id":{"$in":ticket_numbers}
                        }
                    },
                    {
                        "$group": {
                            "_id": "$code",
                            "data": {"$push": f"${array_name}"}
                        }
                    }
                ]
                data_from_collection = collection.aggregate(pipeline)
                for doc in data_from_collection:
                    print(doc)
                    if doc['_id'] not in list(data.keys()):
                        data[doc['_id']] = []
                        data[doc['_id']].extend(doc['data'])
                    else:
                        data[doc['_id']].extend(doc['data'])
      return render_template('CM_SM_higherLevel.html',data=data,role='CM/SM',type='CM_SM_NextLevelSubmitView',cmuser=cm,notify=notify)


@app.route('/DGMNextLevelSubmitView', methods=['GET', 'POST'])
@secure_route(required_role='DGM/PO')
def DGMNextLevelSubmitView():
      success_message = session.pop('success_message', None)
      if 'email_id' not in session:
          return redirect(url_for('post_login'))
      mlro_email = session['email_id']
      notify = notification(mlro_email)

      mlro = users_collection.find_one({"emailid": mlro_email})
      if mlro is None:
                return "User data not found. Please log in again."
      if 'image' in mlro:
                # Encode the image data as a base64 string
                mlro['image'] = base64.b64encode(mlro['image']).decode('utf-8')
                      
      ticket_numbers = mlro.get("case_tickets", [])
      data = {}
      all_collections = [CASE_collection]
      array_names = ["output_data1", "output_data2", "output_data3"]
      for collection, array_name in product(all_collections, array_names):
                pipeline = [
                    {
                        "$unwind": f"${array_name}"
                    },
                    {
                        "$match": {
                            f"{array_name}.ticket_id":{"$in":ticket_numbers}
                        }
                    },
                    {
                        "$group": {
                            "_id": "$code",
                            "data": {"$push": f"${array_name}"}
                        }
                    }
                ]
                data_from_collection = collection.aggregate(pipeline)
                for doc in data_from_collection:
                    print(doc)
                    if doc['_id'] not in list(data.keys()):
                        data[doc['_id']] = []
                        data[doc['_id']].extend(doc['data'])
                    else:
                        data[doc['_id']].extend(doc['data'])
      print(data)
      return render_template('DGMhigherLevel.html',data=data,dgmuser=mlro,role='DGM/PO',type='DGMNextLevelSubmitView',notify=notify)


# ===================DGM Side bar cllosed and submited alerts endpoints===========================
# ========================case Created Data End point==============================
@app.route('/all_casecreated_alerts', methods=['GET', 'POST'])
@secure_route(required_role='DGM/PO')
def all_casecreated_alerts():
        data = {}
        all_collections = [CASE_collection]
        email = session['email_id']
        notify = notification(email)
        dgminfo = users_collection.find_one({"emailid": email})
        
        if 'image' in dgminfo:
                    # Encode the image data as a base64 string
                    dgminfo['image'] = base64.b64encode(dgminfo['image']).decode('utf-8')

        array_names = ["output_data1", "output_data2", "output_data3"]
        for collection in all_collections:
            cursor = collection.find()
            for doc in cursor:
                for array_name in array_names:
                    items = doc.get(array_name, [])
                    code = doc.get("code")  # Assuming there is a 'code' field in your documents
                    if code not in data:
                        data[code] = []
                    data[code].extend(items)
        print("Final data:", data)
        return render_template('dgm_casecreate_Alerts.html', notify = notify, data=data,role='DGM/PO',type='all_casecreated_alerts',dgmuser=dgminfo)
# ========================closed Data End point==============================

@app.route('/all_closed_alerts', methods=['GET', 'POST'])
@secure_route(required_role='DGM/PO')
def all_closed_alerts():
        data = {}

        email = session['email_id']
        notify = notification(email)

        dgminfo = users_collection.find_one({"emailid": email})
        
        if 'image' in dgminfo:
                    # Encode the image data as a base64 string
                    dgminfo['image'] = base64.b64encode(dgminfo['image']).decode('utf-8')

        collections = [CLOSE_CASE_collection]
        array_names = ["output_data1", "output_data2", "output_data3"]
        for collection in collections:
            cursor = collection.find()
            for doc in cursor:
                for array_name in array_names:
                    items = doc.get(array_name, [])
                    code = doc.get("code")  # Assuming there is a 'code' field in your documents
                    if code not in data:
                        data[code] = []
                    data[code].extend(items)
        print("ALL closed data : ",data)                        
        return render_template('all_closed_alerts.html',notify=notify, data=data,role='DGM/PO',type='all_closed_alerts',dgmuser=dgminfo)
# ===========================All pendding alerts ENdPoints ====================================

@app.route('/all_pendding_alerts',methods=['GET','POST'])
@secure_route(required_role='DGM/PO')
def all_pendding_alerts():
        data = {}
        email = session['email_id']
        notify = notification(email)

        dgminfo = users_collection.find_one({"emailid": email})
        
        if 'image' in dgminfo:
                    # Encode the image data as a base64 string
                    dgminfo['image'] = base64.b64encode(dgminfo['image']).decode('utf-8')

        collections = [TM_collection, TY_collection, RM_collection]
        array_name = ["output_data1", "output_data2", "output_data3"]
        for collection in collections:
            for document in collection.find():
                for array_name in ["output_data1", "output_data2", "output_data3"]:
                    if array_name in document:
                        for obj in document[array_name]:
                            if "Comments" not in obj :
                                code = document.get("code")
                                if code not in data:
                                    data[code] = []
                                data[code].append(obj)
        return render_template('all_pendding_alerts.html', notify=notify,data=data,role='DGM/PO',type='all_pendding_alerts',dgmuser=dgminfo)
# =========================================================================================================

@app.route('/sendBackCaseCreated',methods=['POST','GET'])
@secure_route(required_role=['MLRO','AGM','CM/SM','DGM/PO'])
def sendBackCaseCreated():
    ticketId = request.form.get('tickId')
    comment = request.form.get('sendBackComment')
    reverseTo = request.form.get('allocateTo')
    typee = request.form.get('typee')
    mailid = session['email_id']

    role = users_collection.find_one({'emailid':mailid,'status':'Approved'})['role']


    time = datetime.now()
    # Extract only the date and set the time to midnight
    timeDate = str(time.date())

    all_collections = [CASE_collection]
    array_names = ["output_data1", "output_data2", "output_data3"]
    for collection, array_name in product(all_collections, array_names):
        collection.update_one( {f"{array_name}.ticket_id": ticketId},{"$set":{f"{array_name}.$.sentBackReason":comment,f"{array_name}.$.sentBackCase":True}})
        if role == 'DGM/PO':
            collection.update_one( {f"{array_name}.ticket_id": ticketId},{"$set":{f"{array_name}.$.status.dgm_officer":None}}) 
        if role == 'AGM':
            collection.update_one( {f"{array_name}.ticket_id": ticketId},{"$set":{f"{array_name}.$.status.agm_officer":None}}) 
        if role == 'CM/SM':
            collection.update_one( {f"{array_name}.ticket_id": ticketId},{"$set":{f"{array_name}.$.status.cm_officer":None}}) 

    if role == 'CM/SM':
            users_collection.update_one({'emailid': mailid, 'allocated_perday.date': timeDate}, 
    # Update operation to decrement the 'count' field
    {"$inc": {'allocated_perday.$.count': -1}})

    findUser = users_collection.find_one({'emailid':reverseTo,'status':'Approved','Sent_Back_Case_Alerts':{'$exists':True}})
    if findUser:
       users_collection.update_one({'emailid':reverseTo,'status':'Approved'},{"$push":{'Sent_Back_Case_Alerts':ticketId}})
    else:
       users_collection.update_one({'emailid':reverseTo,'status':'Approved'},{"$set":{'Sent_Back_Case_Alerts':[ticketId]}})

    casesPerDayUser = users_collection.find_one({'emailid':reverseTo,'status':'Approved',f'case_tickets_perday.{timeDate}':{'$exists':True}})

    if casesPerDayUser:
        users_collection.update_one({'emailid': reverseTo, 'case_tickets_perday': { '$elemMatch': { timeDate: { '$exists': True } } }},{"$inc": {f'case_tickets_perday.$.{timeDate}': -1}})
        users_collection.update_one({'emailid': mailid, 'allocated_perday': { '$elemMatch': { timeDate: { '$exists': True } } }},{"$inc": {f'allocated_perday.$.{timeDate}': -1}})
    else:
        users_collection.update_one({'emailid':reverseTo},{"$push": {'case_tickets_perday':{timeDate:-1}}})
        users_collection.update_one({'emailid': mailid, 'allocated_perday': { '$elemMatch': { timeDate: { '$exists': True } } }},{"$inc": {f'allocated_perday.$.{timeDate}': -1}})


    users_collection.update_one({'emailid': reverseTo, 'case_tickets': ticketId},
                {
                    '$pull': {'case_tickets': ticketId}})   


    users_collection.update_one({'emailid': mailid, 'allocated_tickets': ticketId},
                {
                    '$pull': {'allocated_tickets': ticketId}})
    
    users_collection.update_one({'emailid': mailid, 'Sent_Back_Case_Alerts': ticketId},
                {
                    '$pull': {'Sent_Back_Case_Alerts': ticketId}})
    
    if typee == 'CM_SM_NextLevel' or typee == 'AGMNextLevel':
        redirect_to_endpoint = typee
    else:
        redirect_to_endpoint = 'display_Sent_Back_Alerts'

    if role != 'DGM/PO':
       return redirect(url_for(redirect_to_endpoint))
    else:
       return redirect(url_for("DGMNextLevel"))



@app.route('/display_Sent_Back_Alerts',methods=['POST','GET'])
@secure_route(required_role=['MLRO','AGM','CM/SM','DGM/PO'])
def display_Sent_Back_Alerts():
    success_message = session.pop('success_message', None)
    if 'email_id' not in session:
        return redirect(url_for('post_login'))
    email = session['email_id']
    print('mlro email:',email)
    notify = clearnotification(email,'sentBack')
    mailInfo = users_collection.find_one({"emailid": email})
    if 'image' in mailInfo:
                # Encode the image data as a base64 string
                mailInfo['image'] = base64.b64encode(mailInfo['image']).decode('utf-8')
    role = mailInfo["role"]
    ticket_numbers = mailInfo.get("Sent_Back_Case_Alerts", [])
    print(ticket_numbers)
    data = {}
    all_collections = [CASE_collection]
    array_names = ["output_data1", "output_data2", "output_data3"]
    for collection, array_name in product(all_collections, array_names):
        pipeline = [
            {
                "$unwind": f"${array_name}"
            },
            {
                "$match": {
                    f"{array_name}.sentBackReason":{"$exists":True},
                    f"{array_name}.sentBackCase":{"$exists":True},
                    f"{array_name}.ticket_id":{"$in":ticket_numbers}
                }
            },
            {
                "$group": {
                    "_id": "$code",
                    "data": {"$push": f"${array_name}"}
                }
            }
        ]
        data_from_collection = collection.aggregate(pipeline)
        for doc in data_from_collection:
            if doc['_id'] not in list(data.keys()):
                data[doc['_id']] = []
                data[doc['_id']].extend(doc['data'])
            else:
                data[doc['_id']].extend(doc['data'])
    response = make_response(render_template('case_sent_Back_Alerts.html',data=data,success_message=success_message,role=role,allImages=mailInfo,type='display_Sent_Back_Alerts',notify=notify))
    response.set_cookie('display_Sent_Back_Alerts','I am cookieee',secure=True,samesite='Lax',httponly=True)
    return response


@app.route('/sent_back_case_FormPage',methods=['POST','GET'])
@secure_route(required_role=['MLRO','AGM','CM/SM'])
def sent_back_case_FormPage():
    email = session['email_id']
    notify = notification(email)
    msgg = session.pop('msgg', None)

    user = users_collection.find_one({"emailid":email})
    mailInfo = users_collection.find_one({"emailid": email})
    
    if 'image' in mailInfo:
                # Encode the image data as a base64 string
                mailInfo['image'] = base64.b64encode(mailInfo['image']).decode('utf-8')
    data = {}
    all_collections = [CASE_collection]
    array_names = ["output_data1", "output_data2", "output_data3"]
    if request.method == 'POST':
        ticket_id_from_form = request.form['ticket_id']
        CustomerId = request.form['custId']
        # formDAta = mlroCaseForm(ticket_id_from_form)
        
        # TY_collection, TM_collection, RM_collection,
        
        for collection, array_name in product(all_collections, array_names):
            pipeline = [
                {
                    "$unwind": f"${array_name}"
                },
                {
                    "$match": {
                        f"{array_name}.ticket_id":ticket_id_from_form,
                        f"{array_name}.sentBackCase":{"$exists":True}
                    }
                },
                {
                    "$group": {
                        "_id": "$code",
                        "data": {"$push": f"${array_name}"}
                    }
                }
            ]
            data_from_collection = collection.aggregate(pipeline)
            for doc in data_from_collection:
                if doc['_id'] not in list(data.keys()):
                    data[doc['_id']] = []
                    data[doc['_id']].extend(doc['data'])
                else:
                    data[doc['_id']].extend(doc['data'])
        print(data)

        if user["role"] == "CM/SM":
            allocated = user["assigned_to_agm"]
        if user["role"] == "MLRO":
            allocated = user["assigned_to"]
        if user["role"] == "AGM":
            allocated = users_collection.find_one({"role":"DGM/PO"})["emailid"]
        if user["role"] == "DGM/PO":
            allocated = None
       
        return render_template('sent_back_case_form.html',ticket_id=ticket_id_from_form,CustomerId=CustomerId,role=user["role"],allocated=allocated,data=data,type='display_Sent_Back_Alerts',allImages=mailInfo,notify=notify, msgg=msgg)
    ticket_id_from_session = session.get('ticket_id')
    CustomerId = session.get('custid')
    print('ticket_id:', ticket_id_from_session)
    print('custidddddd:', CustomerId)
    for collection, array_name in product(all_collections, array_names):
        pipeline = [
            {
                "$unwind": f"${array_name}"
            },
            {
                "$match": {
                    f"{array_name}.ticket_id":ticket_id_from_session,
                    f"{array_name}.sentBackCase":{"$exists":True}
                }
            },
            {
                "$group": {
                    "_id": "$code",
                    "data": {"$push": f"${array_name}"}
                }
            }
        ]
        data_from_collection = collection.aggregate(pipeline)
        for doc in data_from_collection:
            if doc['_id'] not in list(data.keys()):
                data[doc['_id']] = []
                data[doc['_id']].extend(doc['data'])
            else:
                data[doc['_id']].extend(doc['data'])
    print(data)

    if user["role"] == "CM/SM":
        allocated = user["assigned_to_agm"]
    if user["role"] == "MLRO":
        allocated = user["assigned_to"]
    if user["role"] == "AGM":
        allocated = users_collection.find_one({"role":"DGM/PO"})["emailid"]
    if user["role"] == "DGM/PO":
        allocated = None
    
    return render_template('sent_back_case_form.html',ticket_id=ticket_id_from_session,CustomerId=CustomerId,role=user["role"],allocated=allocated,data=data,type='display_Sent_Back_Alerts',allImages=mailInfo,notify=notify, msgg=msgg)




# ==============Offline section===============

@app.route('/DGMofflinedashboard', methods=['GET', 'POST'])
@secure_route(required_role='DGM/PO')
def DGMofflinedashboard():
    # Redirect if the user is not logged in
    if 'email_id' not in session:
        return redirect(url_for('post_login'))
    
    dgm_email = session.get('email_id', '')
    notify = notification(dgm_email)

    dgmuser = {}
    dashboardCount = users_collection.find_one({'emailid': dgm_email, 'status': 'Approved'}) or {}

    # Encode image data as a base64 string if it exists
    if 'image' in dashboardCount:
        dgmuser['image'] = base64.b64encode(dashboardCount.get('image')).decode('utf-8')

    offline_assigned_perday = dashboardCount.get('offline_assigned_perday')

    # Check if offline_assigned_perday is not None and is a list
    assigned_perday_dgm = []
    if isinstance(offline_assigned_perday, list):
        
        for dataa in offline_assigned_perday:
            if dataa and all(key in dataa for key in ['date', 'count']):
                assigned_perday_dgm.append({dataa['date']: dataa['count']})
            else:
                print("Invalid data format in offline_assigned_perday:", dataa)
    else:
        print("Invalid offline_assigned_perday format:", offline_assigned_perday)
    
    DGMApproved_perDay_offline = dashboardCount.get('DGMApproved_perDay_offline', [])
    DGMApprovedperDayoffline = list(DGMApproved_perDay_offline)

    DGMRejected_perDay_offline = dashboardCount.get('DGMRejected_perDay_offline', [])
    DGMRejectedperDayoffline = list(DGMRejected_perDay_offline)

    # print("aaaaaaaa111", DGMApprovedperDayoffline)
    # print("bbbbbb2222", DGMRejectedperDayoffline)

    # Count approved and rejected reports
    finalReportdata = offline_collection.find()
    # Initialize counters
    approved_count = 0
    rejected_count = 0
    for finaldata in finalReportdata:
        if 'data' in finaldata:
            for data_entry in finaldata['data']:
                if 'finalReport' in data_entry:
                    final_report_value = data_entry['finalReport']
                    print("FinalReportValue:", final_report_value)
                    if final_report_value.lower() == 'approved':
                        approved_count += 1
                    elif final_report_value.lower() == 'rejected':
                        rejected_count += 1
    # print("Approvedreports:", approved_count)
    # print("Rejectedreports:", rejected_count)
    # Count assigned and submitted tickets
    count = len(dashboardCount.get('Offline_assigned_tickets', []))
    count_submitted = len(dashboardCount.get('Offline_submited_tickets', []))
    # Retrieve ROS and AGM counts
    ROS_COUNT = users_collection.find({"role": "ROS", "status": 'Approved'})
    AGM_COUNT = users_collection.find({"role": "AGM", "status": 'Approved'})
    # Retrieve data for ROS
    ros_data = [
        {
            "ros_email_id": ros_emailid.get("emailid", ""),
            "empid": ros_emailid.get("empid", ""),
            "offline_ticket_count": len(ros_emailid.get('Offline_assigned_tickets', [])),
            "offline_submited_ticket_count": len(ros_emailid.get('Offline_submited_tickets', []))
        }
        for ros_emailid in ROS_COUNT
    ]
    # Retrieve data for AGM
    agm_data = [
        {
            "email_id": agm_emailid.get("emailid", ""),
            "empid": agm_emailid.get("empid", ""),
            "offline_ticket_count": len(agm_emailid.get('Offline_assigned_tickets', [])),
            "offline_submited_ticket_count": len(agm_emailid.get('Offline_submited_tickets', []))
        }
        for agm_emailid in AGM_COUNT
    ]
    return render_template('DGM_offline_dashboard.html', ros_data=ros_data, agm_data=agm_data,
                           count=count, count_submitted=count_submitted, notify=notify,
                           approved_count=approved_count, rejected_count=rejected_count, assignedperdaydgm=assigned_perday_dgm,
                           DGMApprovedperDayoffline=DGMApprovedperDayoffline,DGMRejectedperDayoffline=DGMRejectedperDayoffline,
                           dashboardCount=dashboardCount, dgmuser=dgmuser, role='DGM/PO', type='DGMofflinedashboard')

# AGM OFFLINE DASHBOARD PAGE

@app.route('/AGMofflinedashboard', methods=['GET', 'POST'])
@secure_route(required_role='AGM')
def AGMofflinedashboard():
    # return render_template('AGM_offline_dashboard.html')
    if 'email_id' not in session:
        return redirect(url_for('post_login'))
    agm_email = session['email_id']
    notify = notification(agm_email)

    agmuser = users_collection.find_one({"emailid": agm_email})
    if 'image' in agmuser:
        # Encode the image data as a base64 string
        agmuser['image'] = base64.b64encode(agmuser['image']).decode('utf-8')
    count = 0
    countSubmited = 0
    dashboardCount = users_collection.find_one({'emailid': agm_email, "status": 'Approved'})
    if "Offline_assigned_tickets" in dashboardCount:
       count = len(dashboardCount['Offline_assigned_tickets'])
    else:
        count=0
    if "Offline_submited_tickets" in dashboardCount:
       countSubmited = len(dashboardCount['Offline_submited_tickets'])
    else:
        countSubmited=0

    offline_assigned_perday = dashboardCount.get('offline_assigned_perday')

    # Check if offline_assigned_perday is not None and is a list
    assigned_perday = []
    if isinstance(offline_assigned_perday, list):
        
        for dataa in offline_assigned_perday:
            if dataa and all(key in dataa for key in ['date', 'count']):
                assigned_perday.append({dataa['date']: dataa['count']})
            else:
                print("Invalid data format in offline_assigned_perday:", dataa)
    else:
        print("Invalid offline_assigned_perday format:", offline_assigned_perday)

    Offline_submitted_perday = dashboardCount.get('Offline_submitted_perday')

    # Check if offline_assigned_perday is not None and is a list
    submitted_perday = []
    if isinstance(Offline_submitted_perday, list):
        
        for dataa in Offline_submitted_perday:
            # Check if dataa is not None and has 'date' and 'count' keys
            if dataa and all(key in dataa for key in ['date', 'count']):
                submitted_perday.append({dataa['date']: dataa['count']})
            else:
                print("Invalid data format in offline_assigned_perday:", dataa)
    else:
        print("Invalid offline_assigned_perday format:", Offline_submitted_perday)



    roscount = dashboardCount.get('ros_assigned', [])
    ROS_COUNT = users_collection.find({"emailid": {"$in": roscount}, "status": 'Approved'})
    ros_data = []

    for ros_emailid in ROS_COUNT:
        email_id = ros_emailid.get("emailid", "")
        empid = ros_emailid.get("empid", "")
        if "Offline_assigned_tickets" in ros_emailid:
            offline_ticket = len(ros_emailid['Offline_assigned_tickets'])
        else:
            offline_ticket = 0
        if "Offline_submited_tickets" in ros_emailid:
            offline_submited_ticket = len(ros_emailid['Offline_submited_tickets'])
        else:
            offline_submited_ticket = 0
        # Append data to the ros_data list
        ros_data.append({
            "ros_email_id": email_id,
            "empid" : empid,
            "offline_ticket_count": offline_ticket,
            "offline_submited_ticket_count":offline_submited_ticket
        })
    return render_template('AGM_offline_dashboard.html',count=count,countSubmited=countSubmited,ros_data=ros_data,agmuser=agmuser,role='AGM',type='AGMofflinedashboard',assignedperday=assigned_perday,submittedperday=submitted_perday,notify=notify)

#  ROS dashboard  
@app.route('/ROSDashboard',methods=['GET','POST'])
@secure_route(required_role='ROS')
def ROSDashboard():
    if 'email_id' not in session:
        return redirect(url_for('post_login'))

    ros_email = session['email_id']
    notify = notification(ros_email)

    rosuser = users_collection.find_one({'emailid':ros_email})
    if 'image' in rosuser:
        # Encode the image data as a base64 string
        rosuser['image'] = base64.b64encode(rosuser['image']).decode('utf-8')
        
    dashboardCount = users_collection.find_one({'emailid':ros_email,"status":'Approved'})
    # print(len(dashboardCount['Offline_assigned_tickets']))
    if "Offline_assigned_tickets" in dashboardCount  : 
     count = len(dashboardCount['Offline_assigned_tickets'])
    else:
     count = 0
    if "Offline_submited_tickets" in dashboardCount  : 
     countSubmited = len(dashboardCount['Offline_submited_tickets'])
    else:
     countSubmited = 0

    offline_assigned_perday = dashboardCount.get('offline_assigned_perday')

    # Check if offline_assigned_perday is not None and is a list
    assigned_perday = []
    if isinstance(offline_assigned_perday, list):
        
        for dataa in offline_assigned_perday:
            if dataa and all(key in dataa for key in ['date', 'count']):
                assigned_perday.append({dataa['date']: dataa['count']})
            else:
                print("Invalid data format in offline_assigned_perday:", dataa)
    else:
        print("Invalid offline_assigned_perday format:", offline_assigned_perday)

    Offline_submitted_perday = dashboardCount.get('Offline_submitted_perday')

    # Check if offline_assigned_perday is not None and is a list
    submitted_perday = []
    if isinstance(Offline_submitted_perday, list):
        
        for dataa in Offline_submitted_perday:
            # Check if dataa is not None and has 'date' and 'count' keys
            if dataa and all(key in dataa for key in ['date', 'count']):
                submitted_perday.append({dataa['date']: dataa['count']})
            else:
                print("Invalid data format in offline_assigned_perday:", dataa)
    else:
        print("Invalid offline_assigned_perday format:", Offline_submitted_perday)
    
    
    
    return render_template('ros_dashboard.html',count=count,countSubmited=countSubmited,assignedperday=assigned_perday,submittedperday=submitted_perday,rosuser=rosuser,role='ROS',type='ROSDashboard',notify=notify)

# @app.route('/branchmakers', methods=['GET','POST'])
# @secure_route(required_role='BranchMakers')
# def branchmakers():
#      if 'email_id' not in session:
#         return redirect(url_for('post_login'))
#      email_id = session['email_id']
#      user = users_collection.find_one({'emailid': email_id})

#      branchmakeruser = {}
#      if user and 'image' in user:
#         # Encode the image data as a base64 string
#         branchmakeruser['image'] = base64.b64encode(user['image']).decode('utf-8')
#      success_message = session.pop('success_message', None)
#      error_message = session.pop('ps_error', None)  # Retrieve and clear the error message from session

#      if request.method == 'POST':
#             print('*****')
#             amount = request.form.get('amount')
#             print('amount:',amount)

#             if not amount:  # Check if the amount field is empty
#                 session['ps_error'] = "Amount is required."
#             elif not re.match(r'^[0-9.]*$', amount):
#                 session['ps_error'] = "Only numbers and decimal points are allowed."
#             elif len(amount) > 15:
#                 session['ps_error'] = "Input should not exceed 15 digits."
            
#             if 'ps_error' in session:
#                 return redirect(url_for('branch_makers'))
#             session['success_message'] = "Amount processed successfully."
#      return render_template('Branch_makers.html',success_message=success_message, error_message=error_message,branchmakeruser=branchmakeruser,role='BranchMakers',type='branchmakers')


@app.route('/branchmakers', methods=['GET','POST'])
@secure_route(required_role=['BranchMakers'])
def branchmakers():
    if 'email_id' not in session:
        return redirect(url_for('post_login'))
    email_id = session['email_id']
    user = users_collection.find_one({'emailid': email_id})

    branchmakeruser = {}
    if user and 'image' in user:
        branchmakeruser['image'] = base64.b64encode(user['image']).decode('utf-8')
    success_message = session.pop('success_message', None)
    # error_message = session.pop('ps_error', None)

    # if request.method == 'POST':
    #     print('*****')
    #     amount = request.form.get('amount')
    #     print('amount:',amount)

    #     if not amount:  
    #         session['ps_error'] = "Amount is required."
    #         return redirect(url_for('branchmakers'))  # Redirect immediately after encountering an error

    #     elif not re.match(r'^[0-9.]*$', amount):
    #         session['ps_error'] = "Only numbers and decimal points are allowed."
    #         return redirect(url_for('branchmakers'))  # Redirect immediately after encountering an error

    #     elif len(amount) > 15:
    #         session['ps_error'] = "Input should not exceed 15 digits."
    #         return redirect(url_for('branchmakers'))  # Redirect immediately after encountering an error
        
    #     session['success_message'] = "Amount processed successfully."
    #     return redirect(url_for('branchmakers'))  # Redirect after processing the amount

    return render_template('Branch_makers.html', success_message=success_message, branchmakeruser=branchmakeruser, role='BranchMakers', type='branchmakers')

     
@app.route('/searchUserOffline',methods=['POST'])
@secure_route(required_role='BranchMakers')
def searchUserOffline():
    userInfo = request.get_json()
    user = userInfo["user"] 
    field = userInfo["field"] 
    if field == "Account Number":
       userdetails = txn_collection.find_one({field:user},{"_id":0})
    else:
        userdetails = txn_collection.find_one({"TXNDATA.Customer ID":user},{"_id":0})
    if userdetails:
        info = userdetails['TXNDATA'][0]
        userAllInfo = {
             "personname":info['Customer Name'],
            "custCode":info['Customer ID'],
            "AccNo":info['Account Number'],
            "AccType":info['Type of account'],
            "opingDate":info['Acc_Opening_Date'],
            "AccStatus":"Active",
            "holderType":"Private person",
            "holderName":info['Customer Name'],
            "debitCard": "Credit", #info['Card Type']
            "Address": info['Address'],
            "Pincode": info['Pincode'],
            "City": info['City'],
            "DOB": info['DOB'],
            "MobileNumber": info['Mobile Number'],
            "PAN": info['PAN'],
            "TransactionAmount":info['Transaction Amount'],
            "TransactionType" : info['Transaction Type'],
            "TransactionCategory" : info['Transaction Category'],
            "TransactionCurrency" : info['Transaction Currency'],
            "BankName" : info['Bank Name'],
            "BankState" : info['Bank State'],
        }
        return userAllInfo;
    else:
        return {"none":"no data"}

@app.route('/post_manual_str',  methods=['GET', 'POST'])
@secure_route(required_role=['BranchMakers'])
def post_manual_str():
    branchmaker_email = session['email_id']
    if request.method == 'POST':
        form_data = {field: request.form.get(field) for field in request.form}
        cummulativeCerditTurnover= form_data.get('CummulativeCerditTurnover')
        # print('formdata:',form_data)
        # Validate amount
        # date_pattern = r'^(0[1-9]|[12][0-9]|3[01])[-/](0[1-9]|1[0-2])[-/]\d{4}$'

        # Validate DateofOpening
        # DateofOpening = form_data.get('DateofOpening')
        # if not re.match(date_pattern, DateofOpening):
        #     error_msg = "DateofOpening should not be empty and should be in dd/mm/yyyy or dd-mm-yyyy format."
        #     return render_template('Branch_makers.html', msgg=error_msg , role='BranchMakers', type='branchmakers')
        category_pattern = r'^[a-zA-Z0-9]{1,10}$'
        pincode_pattern = r'^\d{6}$'
        if not cummulativeCerditTurnover:  
            print(cummulativeCerditTurnover)
            error_msg = "cummulativeCerditTurnover is required"
            return render_template('Branch_makers.html', msgg=error_msg , role='BranchMakers', type='branchmakers')

        elif not re.match(r'^[0-9.]*$', cummulativeCerditTurnover):
            error_msg = "cummulativeCerditTurnover should only contain  numbers and decimal points are allowed."
            return render_template('Branch_makers.html', msgg=error_msg , role='BranchMakers', type='branchmakers')

        elif len(cummulativeCerditTurnover) > 15:

            error_msg = "cummulativeCerditTurnover should not exceed 15 digits."
            return render_template('Branch_makers.html', msgg=error_msg , role='BranchMakers', type='branchmakers')
        
        
        cummulativeDebitTurnover=form_data.get('CummulativeDebitTurnover')
        if not cummulativeDebitTurnover:  
            print(cummulativeDebitTurnover)
            error_msg = "cummulativeDebitTurnover is required"
            return render_template('Branch_makers.html', msgg=error_msg , role='BranchMakers', type='branchmakers')

        elif not re.match(r'^[0-9.]*$', cummulativeDebitTurnover):
            error_msg = "cummulativeDebitTurnover should only contain  numbers and decimal points are allowed."
            return render_template('Branch_makers.html', msgg=error_msg , role='BranchMakers', type='branchmakers')

        elif len(cummulativeDebitTurnover) > 15:

            error_msg = "cummulativeDebitTurnover should not exceed 15 digits."
            return render_template('Branch_makers.html', msgg=error_msg , role='BranchMakers', type='branchmakers')
        
        CummulativeCashDepositTurnover=form_data.get('CummulativeCashDepositTurnover')
        if not CummulativeCashDepositTurnover:  
            print(CummulativeCashDepositTurnover)
            error_msg = "CummulativeCashDepositTurnover is required"
            return render_template('Branch_makers.html', msgg=error_msg , role='BranchMakers', type='branchmakers')

        elif not re.match(r'^[0-9.]*$', CummulativeCashDepositTurnover):
            error_msg = "CummulativeCashDepositTurnover should only contain  numbers and decimal points are allowed."
            return render_template('Branch_makers.html', msgg=error_msg , role='BranchMakers', type='branchmakers')

        elif len(CummulativeCashDepositTurnover) > 15:

            error_msg = "CummulativeCashDepositTurnover should not exceed 15 digits."
            return render_template('Branch_makers.html', msgg=error_msg , role='BranchMakers', type='branchmakers')

        CummulativeCashWithdrawalTurnover=form_data.get('CummulativeCashWithdrawalTurnover')
        if not CummulativeCashWithdrawalTurnover:  
            print(CummulativeCashWithdrawalTurnover)
            error_msg = "CummulativeCashWithdrawalTurnover is required"
            return render_template('Branch_makers.html', msgg=error_msg , role='BranchMakers', type='branchmakers')

        elif not re.match(r'^[0-9.]*$', CummulativeCashWithdrawalTurnover):
            error_msg = "CummulativeCashWithdrawalTurnover should only contain  numbers and decimal points are allowed."
            return render_template('Branch_makers.html', msgg=error_msg , role='BranchMakers', type='branchmakers')

        elif len(CummulativeCashWithdrawalTurnover) > 15:

            error_msg = "CummulativeCashWithdrawalTurnover should not exceed 15 digits."
            return render_template('Branch_makers.html', msgg=error_msg , role='BranchMakers', type='branchmakers')


        # Validate Pincode
        pincode = form_data.get('Pincode')
        if not pincode:
            error_msg = "Pincode must not be empty ."
            return render_template('Branch_makers.html', msgg=error_msg, role='BranchMakers', type='branchmakers')

        elif not re.match(pincode_pattern, pincode):
            error_msg = "Pincode must  contain only numbers and must contain only 6 digits ."
            return render_template('Branch_makers.html', msgg=error_msg, role='BranchMakers', type='branchmakers')
        city_pattern=r'^[a-zA-Z]*$'
        city=form_data.get('City')
        if not city:
            error_msg = "city must not be empty ."
            return render_template('Branch_makers.html', msgg=error_msg, role='BranchMakers', type='branchmakers')

        elif not re.match(city_pattern, city):
            error_msg = "City must contain only letters."
            return render_template('Branch_makers.html', msgg=error_msg, role='BranchMakers', type='branchmakers')
        
        mobileno_pattern = r'^(\d{10})?$'
        mobilenum = form_data.get('MobileNumber')
        if not mobilenum:
            error_msg = "mobilenum must not be empty ."
            return render_template('Branch_makers.html', msgg=error_msg, role='BranchMakers', type='branchmakers')

        elif not re.match(mobileno_pattern, mobilenum):
            error_msg = "Mobile number must contain only numbers with 10 digits."
            return render_template('Branch_makers.html', msgg=error_msg, role='BranchMakers', type='branchmakers')
        
        pan_pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'
        pan=form_data.get('PAN')
        if not pan:
            error_msg = "pan is required."
            return render_template('Branch_makers.html', msgg=error_msg , role='BranchMakers', type='branchmakers')

        elif not re.match(pan_pattern, pan):
            error_msg = "pan must contain only  Capital letters and numbers i.e; in a sequence of five letters, four numbers, one letter and must be ten characters long."
            return render_template('Branch_makers.html', msgg=error_msg , role='BranchMakers', type='branchmakers')
        
        transaction_type_pattern=r'^[a-zA-Z]{1,20}$'


        TransactionType = form_data.get('TransactionType')
        if not TransactionType:
            error_msg = "TransactionType must not be empty ."
            return render_template('Branch_makers.html', msgg=error_msg , role='BranchMakers', type='branchmakers')

        elif not re.match(transaction_type_pattern, TransactionType):
            error_msg = "TransactionType must contain only letters and must be twenty charcters long ."
            return render_template('Branch_makers.html', msgg=error_msg , role='BranchMakers', type='branchmakers')

        # Validate TransactionCategory
        transaction_category = form_data.get('TransactionCategory')
        if not transaction_category:
            error_msg = "Transaction Category must not be empty ."
            return render_template('Branch_makers.html', msgg=error_msg , role='BranchMakers', type='branchmakers')

        elif not re.match(transaction_type_pattern, transaction_category):
            error_msg = "TransactionCategory must contain only letters and numbers and be up to 20 characters long."
            return render_template('Branch_makers.html', msgg=error_msg , role='BranchMakers', type='branchmakers')


        amount = form_data.get('amount')
        print(len(amount))
        if not amount:  
            print(amount)
            error_msg = "Amount is required"
            return render_template('Branch_makers.html', msgg=error_msg , role='BranchMakers', type='branchmakers')

        elif not re.match(r'^[0-9.]*$', amount):
            error_msg = "Amount should only contain  numbers and decimal points are allowed."
            return render_template('Branch_makers.html', msgg=error_msg , role='BranchMakers', type='branchmakers')

        elif len(amount) > 15:

            error_msg = "Amount should not exceed 15 digits."
            return render_template('Branch_makers.html', msgg=error_msg , role='BranchMakers', type='branchmakers')

        current_datetime = datetime.now()
        # Extract only the date and set the time to midnight
        current_date = current_datetime.date()
        current_date_str = current_date.isoformat()
        
        midnight_datetime = datetime.combine(current_date, datetime.min.time())

        # record['ticket_id'] = str(uuid.uuid4())  # Assign a unique UUID
        ticket_id = f"ARM-VRV-{str(uuid.uuid4())}"  # Assign a unique ticket ID
    
        print("helooo this is str page")
        # Retrieve form data
        ticket_id = ticket_id
        Created_Date=current_date_str
        customerno = request.form.get('Customerno')
        casename = request.form.get('casename')
        personname = request.form.get('personname')
        RuleScenario = request.form.get('RuleScenario')
        Guidance = request.form.get('Guidance')
        scenario = request.form.get('scenario')
        SourceofAlert = request.form.get('SourceofAlert')
        alertindicator = request.form.get('alertindicator')
        SuspiciousDueToproceedofCrime = request.form.get('SuspiciousDueToproceedofCrime')
        SuspiciousDueToComplexTranscaction = request.form.get('SuspiciousDueToComplexTranscaction')
        SuspiciousDueToNoecoRational = request.form.get('SuspiciousDueToNoecoRational')
        SuspiciousDueToFinancingTerrorism = request.form.get('SuspiciousDueToFinancingTerrorism')
        AttemptedTranscaction = request.form.get('AttemptedTranscaction')
        LEAInformed = request.form.get('LEAInformed')
        PriorityRating = request.form.get('PriorityRating')
        ReportCoverage = request.form.get('ReportCoverage')
        leadetails = request.form.get('leadetails')
        AdditionalDocument = request.form.get('AdditionalDocument')
        Aroundofsuspision = request.form.get('Aroundofsuspision')
        DetailsofInvestigation = request.form.get('DetailsofInvestigation')
        AccountNumber = request.form.get('AccountNumber')
        AccountType = request.form.get('AccountType')
        holdername = request.form.get('holdername')
        AccountHolderType = request.form.get('AccountHolderType')
        AccountStatus = request.form.get('AccountStatus')
        # DateofOpening = request.form.get('DateofOpening')
        RiskRating = request.form.get('RiskRating')
        CummulativeCerditTurnover = request.form.get('CummulativeCerditTurnover')
        CummulativeDebitTurnover = request.form.get('CummulativeDebitTurnover')
        CummulativeCashDepositTurnover = request.form.get('CummulativeCashDepositTurnover')
        CummulativeCashWithdrawalTurnover = request.form.get('CummulativeCashWithdrawalTurnover')
        NoOfTransactionsToBeReported = request.form.get('NoOfTransactionsToBeReported')
        TransactionDate = request.form.get('TransactionDate')
        TransactionsID = request.form.get('TransactionsID')
        TransactionMode = request.form.get('TransactionMode')
        DebitCredit = request.form.get('DebitCredit')
        # amount = request.form.get('amount')
        TransactionsCurrency = request.form.get('TransactionsCurrency')
        ProductType = request.form.get('ProductType')
        DateofOpening = request.form.get('DateofOpening')
        ProductIdentifiers = request.form.get('ProductIdentifiers')
        # TransactionType = request.form.get('TransactionType')
        unit = request.form.get('unit')
        Date = request.form.get('Date')

        DispositionOfFunds = request.form.get('DispositionOfFunds')
        RelatedAccountNumber = request.form.get('RelatedAccountNumber')
        RelatedInstitutionName = request.form.get('RelatedInstitutionName')
        RelatedInstitutionRefNum = request.form.get('RelatedInstitutionRefNum')
        Remark = request.form.get('Remark')
        
        # current_datetime = datetime.now()
        # current_date = current_datetime.date()
        # ticket_id = f"ARM-VRV-{str(i + 1)}-{current_date}"
        existing_document = offline_collection.find_one({'code': scenario})

        if existing_document:
            # Update the existing document by adding a new object to the array
            obj={
                            'ticket_id' :ticket_id,
                            'Created_Date':Created_Date,
                            'Created_By': branchmaker_email,
                            'Customerno': customerno,
                            'casename': casename,
                            'scenario': scenario,
                            'Guidance':Guidance,
                            'RuleScenario':RuleScenario,
                            'personname': personname,
                            'SourceofAlert':SourceofAlert,
                            'alertindicator':alertindicator,
                            'SuspiciousDueToproceedofCrime':SuspiciousDueToproceedofCrime,
                            'SuspiciousDueToComplexTranscaction' : SuspiciousDueToComplexTranscaction,
                            'SuspiciousDueToNoecoRational' : SuspiciousDueToNoecoRational,
                            'SuspiciousDueToFinancingTerrorism' : SuspiciousDueToFinancingTerrorism,
                            'AttemptedTranscaction' : AttemptedTranscaction,
                            'LEAInformed' : LEAInformed,
                            'PriorityRating' : PriorityRating,
                            'ReportCoverage' :ReportCoverage,
                            'leadetails'  :leadetails,
                            'AdditionalDocument' : AdditionalDocument,
                            'Aroundofsuspision' : Aroundofsuspision,
                            'DetailsofInvestigation' : DetailsofInvestigation,
                            'AccountNumber' : AccountNumber,
                            'AccountType' : AccountType,
                            'holdername' : holdername,
                            'AccountHolderType' : AccountHolderType,
                            'AccountStatus' : AccountStatus,
                            'DateofOpening' : DateofOpening,
                            'RiskRating' : RiskRating,
                            'CummulativeCerditTurnover' : CummulativeCerditTurnover,
                            'CummulativeDebitTurnover' : CummulativeDebitTurnover,
                            'CummulativeCashDepositTurnover' : CummulativeCashDepositTurnover,
                            'CummulativeCashWithdrawalTurnover' : CummulativeCashWithdrawalTurnover,
                            'NoOfTransactionsToBeReported' : NoOfTransactionsToBeReported,
                            'TransactionDate' : TransactionDate,
                            'TransactionsID' : TransactionsID,
                            'TransactionMode' : TransactionMode,
                            'DebitCredit' : DebitCredit,
                            'amount' : amount,
                            'TransactionsCurrency' : TransactionsCurrency,
                            'ProductType' : ProductType,
                            'ProductIdentifiers' : ProductIdentifiers,
                            'TransactionType' : TransactionType,
                            'unit' :  unit,
                            'Date':Date,
                            'DispositionOfFunds' : DispositionOfFunds,
                            'RelatedAccountNumber' :RelatedAccountNumber,
                            'RelatedInstitutionName' : RelatedInstitutionName,
                            'RelatedInstitutionRefNum' : RelatedInstitutionRefNum,
                            'Remark' :Remark,
                            "Guidance":Guidance,
                            "RuleScenario":RuleScenario
                            }
        
                    
            # ... include other fields in the document
            offline_collection.update_one(
                {'code': scenario},
                {'$push': {'data': obj}}
            )
            
        else:
            document = {
                'code': scenario,
                'data': [{
                    'ticket_id':ticket_id,
                    'Created_Date':current_date_str,
                    'Created_By': branchmaker_email,
                    'Customerno': customerno,
                    'casename': casename,
                    'scenario': scenario,
                    'personname': personname,
                    'SourceofAlert':SourceofAlert,
                    'alertindicator':alertindicator,
                    'SuspiciousDueToproceedofCrime':SuspiciousDueToproceedofCrime,
                    'SuspiciousDueToComplexTranscaction' : SuspiciousDueToComplexTranscaction,
                    'SuspiciousDueToNoecoRational' : SuspiciousDueToNoecoRational,
                    'SuspiciousDueToFinancingTerrorism' : SuspiciousDueToFinancingTerrorism,
                    'AttemptedTranscaction' : AttemptedTranscaction,
                    'LEAInformed' : LEAInformed,
                    'PriorityRating' : PriorityRating,
                    'ReportCoverage' :ReportCoverage,
                    'leadetails'  :leadetails,
                    'AdditionalDocument' : AdditionalDocument,
                    'Aroundofsuspision' : Aroundofsuspision,
                    'DetailsofInvestigation' : DetailsofInvestigation,
                    'AccountNumber' : AccountNumber,
                    'AccountType' : AccountType,
                    'holdername' : holdername,
                    'AccountHolderType' : AccountHolderType,
                    'AccountStatus' : AccountStatus,
                    'DateofOpening' : DateofOpening,
                    'RiskRating' : RiskRating,
                    'CummulativeCerditTurnover' : CummulativeCerditTurnover,
                    'CummulativeDebitTurnover' : CummulativeDebitTurnover,
                    'CummulativeCashDepositTurnover' : CummulativeCashDepositTurnover,
                    'CummulativeCashWithdrawalTurnover' : CummulativeCashWithdrawalTurnover,
                    'NoOfTransactionsToBeReported' : NoOfTransactionsToBeReported,
                    'TransactionDate' : TransactionDate,
                    'TransactionsID' : TransactionsID,
                    'TransactionMode' : TransactionMode,
                    'DebitCredit' : DebitCredit,
                    'amount' : amount,
                    'TransactionsCurrency' : TransactionsCurrency,
                    'ProductType' : ProductType,
                    'ProductIdentifiers' : ProductIdentifiers,
                    'TransactionType' : TransactionType,
                    'unit' :  unit,
                    'Date':Date,
                    'DispositionOfFunds' : DispositionOfFunds,
                    'RelatedAccountNumber' :RelatedAccountNumber,
                    'RelatedInstitutionName' : RelatedInstitutionName,
                    'RelatedInstitutionRefNum' : RelatedInstitutionRefNum,
                    'Remark' :Remark,
                    "Guidance":Guidance,
                    "RuleScenario":RuleScenario
                     }
                ]
            }

           
            offline_collection.insert_one(document)

        ros = users_collection.find({'role': 'ROS', 'status': 'Approved'})
        ros_documents = list(ros)
        if len(ros_documents) > 0:
            random_ros = random.choice(ros_documents)
            ros_id = random_ros['_id']

            # Update the MLRO's data to include the assigned ticket

            findUser = users_collection.find_one({'_id': ros_id, 'status': 'Approved'})
            current_date = datetime.now().strftime('%Y-%m-%d')
            if findUser:
                update_query = {"$push": {"Offline_assigned_tickets": ticket_id}}
                if "offline_assigned_perday" in findUser:
                    date_index = next((i for i, obj in enumerate(findUser["offline_assigned_perday"]) if obj["date"] == current_date), None)
                    if date_index is not None:
                        findUser["offline_assigned_perday"][date_index]["count"] += 1
                    else:
                        findUser["offline_assigned_perday"].append({"date": current_date, "count": 1})
                    update_query["$set"] = {"offline_assigned_perday": findUser["offline_assigned_perday"]}
                else:
                    update_query["$set"] = {
                        "offline_assigned_perday": [{"date": current_date, "count": 1}]  # Create as an array
                    }
                users_collection.update_one({'_id': ros_id, 'status': 'Approved'}, update_query)
            else:
                users_collection.update_one({'_id': ros_id, 'status': 'Approved'}, {
                    "$set": {
                        "Offline_assigned_tickets": [ticket_id],
                        "Offline_submited_tickets": [],
                        "offline_assigned_perday": [{"date": current_date, "count": 1}]  # Create as an array
                    }
                })


           

        findUser = users_collection.find_one({'emailid':branchmaker_email,'status':'Approved','Offline_submited_tickets':{'$exists':True}})
        if findUser:
             users_collection.update_one({'emailid':branchmaker_email,'status':'Approved'},{"$push":{'Offline_submited_tickets':ticket_id}})
        else:
             users_collection.update_one({'emailid':branchmaker_email,'status':'Approved'},{"$set":{'Offline_submited_tickets':[ticket_id]}})
        session['success_message'] = 'Comments saved successfully.'
        return redirect(url_for("branchmakers"))
        
@app.route('/all_offline_str')
@secure_route(required_role='DGM/PO')
def all_offline_str():
        success_message = session.pop('success_message', None)
        if 'email_id' not in session:
            return redirect(url_for('post_login'))

        mlro_email = session['email_id']
        mlro = users_collection.find_one({"emailid": mlro_email})

        if mlro is None:
            return "User data not found. Please log in again."

        ticket_numbers = mlro.get("Offline_assigned_tickets", [])
        data = {}

        pipeline = [
            {"$match": {"mlro_comments": {"$exists": False}, "_id": {"$in": ticket_numbers}}},
            {
                "$group": {
                    "_id": "$code",
                    "data": {"$push": "$$ROOT"}
                }
            }
        ]

        data_from_collection = offline_collection.aggregate(pipeline)

        print("data_from_collection",data_from_collection)

        for doc in data_from_collection:
            data[doc['_id']] = doc['data']
        print("data",data)
        return render_template('all_offline_str.html', data=data,success_message=success_message)


@app.route('/update_offline_str',  methods=['GET', 'POST'])
@secure_route(required_role=['AGM','ROS','DGM/PO'])
def update_offline_str():
     if request.method == 'POST':
        print("helooo this is str page")
        comments = request.form.get('comments')
        ticket_id = request.form.get('ticket_id')
        print("comments",comments)
        print("ticket_id",ticket_id)
        offline_collection.update_one({'_id': ObjectId(ticket_id)}, {'$set': {'mlro_comments': comments}})

        session['success_message'] = 'Comments Updated successfully.'

        return redirect(url_for("all_offline_str"))
     

# @app.route('/update_offline_str')
# @secure_route(required_role=['MLRO','IT Officer','AGM','BranchMakers','CM/SM','ROS','DGM/PO'])
# def all_offline_str():
#      data_from_db = offline_collection.find()
#      return render_template('all_offline_str.html',data_from_db=data_from_db)

@app.route('/ros', methods=['GET', 'POST'])
@secure_route(required_role='ROS')
def ros():
    success_message = session.pop('success_message', None)

    # Check user login
    if 'email_id' not in session:
        return redirect(url_for('post_login'))

    ros_email = session['email_id']
    notify = clearnotification(ros_email,'offline')

    ros = users_collection.find_one({"emailid": ros_email})

    if ros is None:
        return "User data not found. Please log in again."
    if 'image' in ros:
        # Encode the image data as a base64 string
        ros['image'] = base64.b64encode(ros['image']).decode('utf-8')
    

    ticket_numbers = ros.get("Offline_assigned_tickets", [])

    data = {}

    all_collections = [offline_collection]
    array_names = ["data"]

    for collection, array_name in product(all_collections, array_names):
        pipeline = [
            {
                "$unwind": f"${array_name}"
            }, 
            {
                "$match": { 
                    f"{array_name}.comment.Ros_comments": {"$exists": False},
                    f"{array_name}.ticket_id": {"$in": ticket_numbers} 

                    
                }
            },
            {
                "$group": {
                    "_id": "$code",
                    "data": {"$push": f"${array_name}"}
                }
            }
        ]

        data_from_collection = collection.aggregate(pipeline)

        print("pipeline", pipeline)

        for doc in data_from_collection:
            data[doc['_id']] = doc['data']

    print("data", data)

    return render_template('ros.html', success_message=success_message, data=data,rosuser=ros,role='ROS',type='ros',notify=notify)

@app.route('/offline_Form_Edit',methods=['POST','GET'])
@secure_route(required_role=['AGM','ROS','DGM/PO'])
def offline_Form_Edit():
    mailid = session['email_id']
    notify = notification(mailid)

    role = users_collection.find_one({'emailid':mailid})['role']
     
    ticket_id = request.form.get('ticket_id')
    all_collections = [offline_collection]
    array_names = ["data"]


    for all_collections, array_name in product(all_collections, array_names):
        pipeline = [
            {
                "$unwind": f"${array_name}"
             },
            {
                "$match": {
                    f"{array_name}.ticket_id":ticket_id
                    
                }
            },
            {
                "$group": {
                    "_id": "$code",
                    "data": {"$push": f"${array_name}"}
                }
            }
        ]
    data_agm = offline_collection.aggregate(pipeline)
    for doc in data_agm:
        data = doc['data']

    print("mailid : ",mailid)
    user = users_collection.find_one({'emailid':mailid})

    ituser = {}
    if 'image' in user :
            
            ituser['image'] = base64.b64encode(user['image']).decode('utf-8')   
    
    
    print("ituser : ",ituser )
    if role == 'AGM':
        typeEnd = 'offline_agm_Str'

    if role == 'DGM/PO':
        typeEnd = 'offline_dgm_Str'

    if role == 'ROS':
        typeEnd = 'ros'  
    
    
    return render_template('offline_Form_edit.html',data=data,role=role,type=typeEnd,allImages=ituser,notify=notify)

@app.route('/update_offline_str_ros', methods=['POST'])
@secure_route(required_role=['ROS','AGM','DGM/PO'])
def update_offline_str_ros():
    if request.method == 'POST':
        current_datetime = datetime.now()
        current_date = current_datetime.date()
        midnight_datetime = datetime.combine(current_date, datetime.min.time())


        comments = request.form.get('comments')
        ticket_id = request.form.get('ticket_id')
        approval_status = request.form.get('finalReport')

        print("ticket_id : ",ticket_id)


        mailid = session['email_id']
        rosinfo = users_collection.find_one({'emailid':mailid})
        role = rosinfo['role']

        

        if role == 'ROS':
            offline_collection.update_one(
                {'data.ticket_id': ticket_id},
                {'$set': {'data.$.comment.Ros_comments': comments}}
                
            )
            assigned_to_agm = rosinfo['assigned_to_agm']

            current_date = datetime.now().strftime('%Y-%m-%d')

            findUser = users_collection.find_one({'role': 'AGM', 'emailid': assigned_to_agm, 'status': 'Approved', 'Offline_assigned_tickets': {'$exists': True}, 'Offline_submited_tickets': {'$exists': True}})
            if findUser:
                update_query = {"$push": {"Offline_assigned_tickets": ticket_id}}
                if "offline_assigned_perday" in findUser:
                    date_index = next((i for i, obj in enumerate(findUser["offline_assigned_perday"]) if obj["date"] == current_date), None)
                    if date_index is not None:
                        findUser["offline_assigned_perday"][date_index]["count"] += 1
                    else:
                        findUser["offline_assigned_perday"].append({"date": current_date, "count": 1})
                    update_query["$set"] = {"offline_assigned_perday": findUser["offline_assigned_perday"]}
                else:
                    update_query["$set"] = {"offline_assigned_perday": [{"date": current_date, "count": 1}]}
                users_collection.update_one({'role': 'AGM', 'emailid': assigned_to_agm, 'status': 'Approved'}, update_query)
            else:
                users_collection.update_one({'role': 'AGM', 'emailid': assigned_to_agm, 'status': 'Approved'}, {
                    "$set": {
                        "Offline_assigned_tickets": [ticket_id],
                        "Offline_submited_tickets": [],
                        "offline_assigned_perday": [{"date": current_date, "count": 1}]
                    }
                })
            
            
            current_date_str = datetime.now().strftime('%Y-%m-%d')

            user_query = {'emailid': mailid, 'status': 'Approved', 'Offline_assigned_tickets': ticket_id}
            user_document = users_collection.find_one(user_query)

            if user_document:
                if 'Offline_submitted_perday' not in user_document:
                    user_document['Offline_submitted_perday'] = []

                date_entry = next((entry for entry in user_document['Offline_submitted_perday'] if entry['date'] == current_date_str), None)

                if date_entry:
                    date_entry['count'] += 1
                else:
                    user_document['Offline_submitted_perday'].append({'date': current_date_str, 'count': 1})

                users_collection.update_one(
                    user_query,
                    {
                        '$pull': {'Offline_assigned_tickets': ticket_id},
                        '$push': {'Offline_submited_tickets': ticket_id},
                        '$set': {'Offline_submitted_perday': user_document['Offline_submitted_perday']}
                    },
                    upsert=True
                )
            else:
                print(f"User with emailid {mailid} and status 'Approved' not found.")


            session['success_message'] = 'ROS Commented successfully.'
            return redirect(url_for("ros"))
            
        if role == 'AGM':
            offline_collection.update_one(
                {'data.ticket_id': ticket_id},
                {'$set': {'data.$.comment.AGM_comments': comments}}
                
            )
            current_date = datetime.now().strftime('%Y-%m-%d')

            findUser = users_collection.find_one({'role': 'DGM/PO', 'status': 'Approved', 'Offline_assigned_tickets': {'$exists': True}, 'Offline_submited_tickets': {'$exists': True}})
            if findUser:
                update_query = {"$push": {"Offline_assigned_tickets": ticket_id}}

                if "offline_assigned_perday" in findUser:
                    date_index = next((i for i, obj in enumerate(findUser["offline_assigned_perday"]) if obj["date"] == current_date), None)
                    if date_index is not None:
                        findUser["offline_assigned_perday"][date_index]["count"] += 1
                    else:
                        findUser["offline_assigned_perday"].append({"date": current_date, "count": 1})
                    update_query["$set"] = {"offline_assigned_perday": findUser["offline_assigned_perday"]}
                else:
                    update_query["$set"] = {"offline_assigned_perday": [{"date": current_date, "count": 1}]}

                # date_index = next((i for i, obj in enumerate(findUser["offline_assigned_perday"]) if obj["date"] == current_date), None)
                # if date_index is not None:
                #     findUser["offline_assigned_perday"][date_index]["count"] += 1
                # else:
                #     findUser["offline_assigned_perday"].append({"date": current_date, "count": 1})
                # update_query["$set"] = {"offline_assigned_perday": findUser["offline_assigned_perday"]}

                users_collection.update_one({'role': 'DGM/PO', 'status': 'Approved'}, update_query)
            else:
                users_collection.update_one({'role': 'DGM/PO', 'status': 'Approved'}, {
                    "$set": {
                        "Offline_assigned_tickets": [ticket_id],
                        "Offline_submited_tickets": [],
                        "offline_assigned_perday": [{"date": current_date, "count": 1}]
                    }
                })

            user_query = {'emailid': mailid, 'status': 'Approved', 'Offline_assigned_tickets': ticket_id}
            user_document = users_collection.find_one(user_query)

            if user_document:
                if 'Offline_submitted_perday' not in user_document:
                    user_document['Offline_submitted_perday'] = []

                date_entry = next((entry for entry in user_document['Offline_submitted_perday'] if entry['date'] == current_date), None)

                if date_entry:
                    date_entry['count'] += 1
                else:
                    user_document['Offline_submitted_perday'].append({'date': current_date, 'count': 1})

                users_collection.update_one(
                    user_query,
                    {
                        '$pull': {'Offline_assigned_tickets': ticket_id},
                        '$push': {'Offline_submited_tickets': ticket_id},
                        '$set': {'Offline_submitted_perday': user_document['Offline_submitted_perday']}
                    },
                    upsert=True
                )
            else:
                print(f"User with emailid {mailid} and status 'Approved' not found.")

            session['success_message'] = 'AGM Commented successfully.'
            return redirect(url_for('offline_agm_Str'))
            
        if role == 'DGM/PO':
            time = datetime.now()
            # Extract only the date and set the time to midnight
            timeDate = str(time.date())
            offline_collection.update_one(
                {'data.ticket_id': ticket_id},
                {'$set': {'data.$.comment.DGM_comments': comments,
                          'data.$.finalReport': approval_status,
                          'data.$.finalReport_Submited_on': midnight_datetime}}
            )

            users_collection.update_one(
                {'emailid': mailid, 'status': 'Approved', 'Offline_assigned_tickets': ticket_id},
                {
                    '$pull': {'Offline_assigned_tickets': ticket_id},
                    '$push': {'Offline_submited_tickets': ticket_id}
                }
            )

            offlinereportperday(mailid, approval_status, timeDate, users_collection)

            session['success_message'] = 'DGM Commented successfully.'
            return redirect(url_for("offline_dgm_Str"))

def offlinereportperday(mailid, approval_status, timeDate, users_collection):
    time = datetime.now()
    # Extract only the date and set the time to midnight
    timeDate = str(time.date())
    # Additional Functionality
    if approval_status == 'Approved':
        perDayField = 'DGMApproved_perDay_offline'
    elif approval_status == 'Rejected':
        perDayField = 'DGMRejected_perDay_offline'

    # Update per day counts
    perDay = users_collection.find_one({"emailid": mailid, perDayField: {"$exists": True}})
    if perDay:
        dateExists = users_collection.find_one({"emailid": mailid, f'{perDayField}.{timeDate}': {"$exists": True}})
        if dateExists:
            users_collection.update_one(
                {"emailid": mailid, f'{perDayField}.{timeDate}': {"$exists": True}},
                {"$inc": {f'{perDayField}.$.{timeDate}': 1}}
            )
        else:
            users_collection.update_one({"emailid": mailid}, {"$push": {perDayField: {timeDate: 1}}})
    else:
        users_collection.update_one({"emailid": mailid}, {"$set": {perDayField: [{timeDate: 1}]}})



@app.route('/offline_agm_Str',methods=['POST','GET'])
@secure_route(required_role='AGM')
def offline_agm_Str():
    success_message = session.pop('success_message', None)
    # Check user login
    if 'email_id' not in session:
        return redirect(url_for('post_login'))
    agm_email = session['email_id']
    notify = clearnotification(agm_email,'offline')

    agm = users_collection.find_one({'emailid':agm_email,'status':'Approved'})
    if 'image' in agm:
        # Encode the image data as a base64 string
        agm['image'] = base64.b64encode(agm['image']).decode('utf-8')
    
    ticket_numbers = agm.get("Offline_assigned_tickets", [])


    data={}
    all_collections = [offline_collection]
    array_names = ["data"]

    for all_collections, array_name in product(all_collections, array_names):
        pipeline = [
            {
                "$unwind": f"${array_name}"
            },
            {
                "$match": {
                    f"{array_name}.comment.Ros_comments": {"$exists": True},
                    f"{array_name}.comment.AGM_comments": {"$exists": False},
                    f"{array_name}.ticket_id": {"$in": ticket_numbers} 

                    
                }
            },
            {
                "$group": {
                    "_id": "$code",
                    "data": {"$push": f"${array_name}"}
                }
            }
        ]
    data_agm = offline_collection.aggregate(pipeline)
    for doc in data_agm:
        data[doc['_id']] = doc['data']

    
    return render_template("offline_str_agm.html",success_message=success_message,data=data,agmuser=agm,role='AGM',type='offline_agm_Str',notify=notify)

@app.route('/update_offline_str_agm',  methods=['GET', 'POST'])
@secure_route(required_role=['AGM'])
def update_offline_str_agm():
     if request.method == 'POST':
        print("helooo this is str page")
        comments = request.form.get('comments')
        ticket_id = request.form.get('ticket_id')
        print("comments",comments)
        print("ticket_id",ticket_id)
        result = offline_collection.update_one(
            {'data.ticket_id': ticket_id},
            {'$set': {'data.$.comment.AGM_comments': comments}}
            
        )

        session['success_message'] = 'AGM Comments Updated successfully.'
        return redirect(url_for("offline_agm_Str"))

# dgm route

@app.route('/offline_dgm_Str')
@secure_route(required_role='DGM/PO')
def offline_dgm_Str():
    success_message = session.pop('success_message', None)
    # Check user login
    if 'email_id' not in session:
        return redirect(url_for('post_login'))
    
    dgm_email = session['email_id']
    notify = clearnotification(dgm_email,'offline')

    dgm = users_collection.find_one({'emailid':dgm_email,'status':'Approved'})
    if 'image' in dgm:
        # Encode the image data as a base64 string
        dgm['image'] = base64.b64encode(dgm['image']).decode('utf-8')
    
    

    ticket_numbers = dgm.get("Offline_assigned_tickets", [])

    data={}
    all_collections = [offline_collection]
    array_names = ["data"]

    for all_collections, array_name in product(all_collections, array_names):
        pipeline = [
            {
                "$unwind": f"${array_name}"
             },
            {
                "$match": {
                    f"{array_name}.comment.AGM_comments": {"$exists": True},
                    f"{array_name}.comment.DGM_comments": {"$exists": False},
                    f"{array_name}.ticket_id": {"$in": ticket_numbers} 

                    
                }
            },
            {
                "$group": {
                    "_id": "$code",
                    "data": {"$push": f"${array_name}"}
                }
            }
        ]
    data_agm = offline_collection.aggregate(pipeline)
    print("data agmm", data)
    for doc in data_agm:
        data[doc['_id']] = doc['data']


    # data_dgm = offline_collection.find({"AGM_comments": {"$exists": True}, "DGM_comments": {"$exists": False}})
    return render_template('offline_str_dgm.html',success_message=success_message,data=data,dgmuser=dgm,role='DGM/PO',type='offline_dgm_Str',notify=notify)

@app.route('/offline_submited_Str',methods=['POST','GET'])
@secure_route(required_role=['AGM','BranchMakers','ROS','DGM/PO'])
def offline_submited_Str():
    success_message = session.pop('success_message', None)
    # Check user login
    if 'email_id' not in session:
        return redirect(url_for('post_login'))
    email = session['email_id']
    notify = notification(email)

    info = users_collection.find_one({'emailid':email,'status':'Approved'})
    if 'image' in info:
        # Encode the image data as a base64 string
        info['image'] = base64.b64encode(info['image']).decode('utf-8')
    
    ticket_numbers = info.get("Offline_submited_tickets", [])
    role = info.get("role")


    data={}
    all_collections = [offline_collection]
    array_names = ["data"]

    for all_collections, array_name in product(all_collections, array_names):
        pipeline = [
            {
                "$unwind": f"${array_name}"
            },
            {
                "$match": {
 
                    f"{array_name}.ticket_id": {"$in": ticket_numbers} 

                    
                }
            },
            {
                "$group": {
                    "_id": "$code",
                    "data": {"$push": f"${array_name}"}
                }
            }
        ]
    data_agm = offline_collection.aggregate(pipeline)
    for doc in data_agm:
        data[doc['_id']] = doc['data']

    
    return render_template("offline_submited_data.html",success_message=success_message,data=data,role=role,allImages=info,type='offline_submited_Str',notify=notify)

@app.route('/offline_STR_download_page',methods=['POST','GET'])
@secure_route(required_role='IT Officer')
def offline_STR_download_page():
    
        data = []
        all_collections = [offline_collection]
        array_names = ["data"]
        for collection, array_name in product(all_collections, array_names):
            pipeline = [
                {
                    "$unwind": f"${array_name}"
                },
                {
                    "$match": {
                        f"{array_name}.finalReport":"Approved",
                        f"{array_name}.finalReport_Submited_on":{"$exists":True}
                    }
                },
                {
                    "$group": {
                "_id": "code",
                "data":{"$push":{
                    "AccountNumber": f"${array_name}.AccountNumber",
                    "Date": f"${array_name}.finalReport_Submited_on",
                    "TicketId": f"${array_name}.ticket_id",
                }},

            }
                }
            ]
            data_from_collection = collection.aggregate(pipeline)
            for doc in data_from_collection:
                data = (doc['data'])

        user = users_collection.find_one({'role': 'IT Officer'})

        ituser = {'image': ""}
        if user:
            ituser = users_collection.find_one({'emailid': user.get('emailid')})

            if ituser and 'image' in ituser:
                ituser['image'] = base64.b64encode(ituser['image']).decode('utf-8')

        return render_template('offline_STR_Downloads.html',data=data,role='IT Officer',ituser=ituser,type='FINnetReports')

@app.route('/update_offline_str_dgm',  methods=['GET', 'POST'])
@secure_route(required_role=['DGM/PO'])
def update_offline_str_dgm():
     current_datetime = datetime.now()
     current_date = current_datetime.date()
     midnight_datetime = datetime.combine(current_date, datetime.min.time())
     if request.method == 'POST':
        print("helooo this is str page")
        comments = request.form.get('comments')
        ticket_id = request.form.get('ticket_id')
        approval_status = request.form.get('approvel_status')
        print("comments",comments)
        print("ticket_id",ticket_id)
        result = offline_collection.update_one(
            {'data.ticket_id': ticket_id},
            {'$set': {'data.$.comment.DGM_comments': comments,'data.$.finalReport': approval_status,'data.$.finalReport_Submited_on': midnight_datetime}}
            
        )
        # offline_collection.update_one({'_id': ObjectId(ticket_id)}, {'$set': {'DGM_comments': comments,'Final_Approval': approval_status}})

        session['success_message'] = 'DGM Comments Updated successfully.'

        return redirect(url_for("offline_dgm_Str"))

# ==================================== 10% of Closed data Auto Distribution Functions======================================================

def closedDataAuto():
    closedTickets = []
    current_datetime = datetime.now()
    current_date = current_datetime.date()
    midnight_datetime = datetime.combine(current_date, datetime.min.time())
    

    closed_tickets_cm = []
    data = {}
    collections = [CLOSE_CASE_collection]
    for collection in collections:
                for array_name in ["output_data1", "output_data2", "output_data3"]:
                    for doc in collection.find({f"{array_name}.updated_on":midnight_datetime}):
                        if array_name in doc:
                            for obj in doc[array_name]:
                                if obj.get("updated_on") is not None and obj.get("updated_on") == midnight_datetime:
                                    closed_tickets_cm.append(obj['ticket_id'])
                                   
   
    num_elements_to_select = max(1, int(0.1 * len(closed_tickets_cm)))

    randomly_selected_tickets = random.sample(closed_tickets_cm, num_elements_to_select) 

    Cm_distribution =[cm["emailid"] for cm in users_collection.find({'role':"CM/SM","status":"Approved","leaveStatus":"Working"})]

    if Cm_distribution :
            for cms in randomly_selected_tickets:
              if len(randomly_selected_tickets) !=  0:
                randomCm = random.choice(Cm_distribution)
                randomTickets = random.choice(randomly_selected_tickets)
                randomly_selected_tickets.remove(randomTickets)
                risedField = users_collection.find_one({'emailid':randomCm,'rised_closed_tickets':{"$exists":True}})
                all_collections = [CLOSE_CASE_collection]
                array_names = ["output_data1", "output_data2", "output_data3"]
               
                for array_name in array_names:
                    closed_daa = CLOSE_CASE_collection.find_one({f"{array_name}.updated_on":{"$ne":None},
                                                               f"{array_name}.reason":{"$exists":False},
                                                                f"{array_name}.sentBack":{"$exists":False},
                                                               f"{array_name}.ticket_id":randomTickets})
                print("closed_daa : ",closed_daa)    
                if risedField and closed_daa:
                    users_collection.update_one(
                        {'emailid':randomCm},
                        {
                            "$set":{"rised_closed_tickets":[randomTickets]}
                        }
                    )
                elif closed_daa:
                    users_collection.update_one(
                        {'emailid':randomCm},
                        {
                            "$push":{"rised_closed_tickets":randomTickets}
                        }
                    )
    print("10% CLosed Alerts are distributed to CM/SM's")
    

@app.route('/closed_Data_To_CM',methods=['GET','POST']) 
@secure_route(required_role='CM/SM')
def closed_Data_To_CM():
    success_message = session.pop('success_message', None)
    # Check user login
    if 'email_id' not in session:
        return redirect(url_for('post_login'))
    cm_email = session['email_id']
    notify = clearnotification(cm_email,'closedVerify')

    if 'ACC_Num' in session and 'ticket_id' in session and 'CUST_ID' in session:
                        session.pop('ACC_Num')
                        session.pop('ticket_id')
                        session.pop('CUST_ID')
    session['closed_Data_To_CM'] = "closed_Data_To_CM"
    cm = users_collection.find_one({"emailid": cm_email})
    if cm is None:
        return "User data not found. Please log in again."
    if 'image' in cm:
        # Encode the image data as a base64 string
        cm['image'] = base64.b64encode(cm['image']).decode('utf-8')
    
    ticket_numbers = cm.get("rised_closed_tickets", [])
    data = {}
    all_collections = [CLOSE_CASE_collection]
    array_names = ["output_data1", "output_data2", "output_data3"]
    for collection, array_name in product(all_collections, array_names):
        pipeline = [
            {
                "$unwind": f"${array_name}"
            },
            {
                "$match": {
                    f"{array_name}.updated_on":{"$ne":None},
                    f"{array_name}.reason":{"$exists":False},
                    f"{array_name}.sentBack":{"$exists":False},
                    f"{array_name}.ticket_id":{"$in":ticket_numbers}
                }
            },
            {
                "$group": {
                    "_id": "$code",
                    "data": {"$push": f"${array_name}"}
                }
            }
        ]
        data_from_collection = collection.aggregate(pipeline)
        for doc in data_from_collection:
            if doc['_id'] not in list(data.keys()):
                data[doc['_id']] = []
                data[doc['_id']].extend(doc['data'])
            else:
                data[doc['_id']].extend(doc['data'])
    return render_template('rised_closed_cm.html',data=data,success_message=success_message,cm=cm,role='CM/SM',type='closed_Data_To_CM',notify=notify)





# ====================== rised  10% closed data send back to MLRO form CM/SM to create a form with comment=============================

@app.route('/sendBackAlert',methods=['POST'])
@secure_route(required_role=['MLRO','AGM','CM/SM','DGM/PO'])
def sendBackAlert():
    ticketId = request.form.get('tickId')
    comment = request.form.get('reason')
    allocateTo = request.form.get('allocateTo')




    all_collections = [CLOSE_CASE_collection]
    array_names = ["output_data1", "output_data2", "output_data3"]
    for collection, array_name in product(all_collections, array_names):
        collection.update_one( {f"{array_name}.ticket_id": ticketId},{"$set":{f"{array_name}.$.reason":comment,f"{array_name}.$.sentBack":True}})
    
    findUser = users_collection.find_one({'emailid':allocateTo,'status':'Approved','Sent_Back_Alerts':{'$exists':True}})
    if findUser:
       users_collection.update_one({'emailid':allocateTo,'status':'Approved'},{"$push":{'Sent_Back_Alerts':ticketId}})
    else:
       users_collection.update_one({'emailid':allocateTo,'status':'Approved'},{"$set":{'Sent_Back_Alerts':[ticketId]}})
    
    users_collection.update_one({'emailid':allocateTo,'status':'Approved',"commented_tickets":ticketId},{"$pull":{'commented_tickets':ticketId}})


    mailid = session['email_id']
    users_collection.update_one({'emailid': mailid, 'rised_closed_tickets': ticketId},
                {
                    '$pull': {'rised_closed_tickets': ticketId}
                    }) 

    
    return redirect(url_for("closed_Data_To_CM"))



@app.route('/rejectAlert',methods=['POST'])
@secure_route(required_role=['MLRO','CM/SM'])
def rejectAlert():
    ticketId = request.form.get('tickId')
    comment = request.form.get('reason')
    all_collections = [CLOSE_CASE_collection]
    array_names = ["output_data1", "output_data2", "output_data3"]
    for collection, array_name in product(all_collections, array_names):
        collection.update_one( {f"{array_name}.ticket_id": ticketId},{"$set":{f"{array_name}.$.reason":comment}})
    mailid = session['email_id']
    user = users_collection.find_one({'emailid':mailid})
    users_collection.update_one({'emailid': mailid, 'rised_closed_tickets': ticketId},
                {
                    '$pull': {'rised_closed_tickets': ticketId}})
    if  "closed_tickets" in user:
        users_collection.update_one({'emailid':mailid},{"closed_tickets":{"$push":ticketId}})
    else:
        users_collection.update_one({'emailid':mailid},{"$set":{"closed_tickets":[ticketId]}})
    return redirect(url_for("closed_Data_To_CM"))



@app.route('/closed_alerts_cm',methods=['POST','GET'])
@secure_route(required_role='CM/SM')
def closed_alerts_cm():
    success_message = session.pop('success_message', None)
    # Check user login
    if 'email_id' not in session:
        return redirect(url_for('post_login'))
    mailid = session['email_id']
    notify = notification(mailid)

    user = users_collection.find_one({'emailid':mailid})
    if 'image' in user:
                # Encode the image data as a base64 string
                user['image'] = base64.b64encode(user['image']).decode('utf-8')
    ticket_numbers = user.get("closed_tickets", [])
    data = {}
    all_collections = [CLOSE_CASE_collection]
    array_names = ["output_data1", "output_data2", "output_data3"]
    for collection, array_name in product(all_collections, array_names):
        pipeline = [
            {
                "$unwind": f"${array_name}"
            },
            {
                "$match": {
                    f"{array_name}.updated_on":{"$ne":None},
                    f"{array_name}.reason":{"$exists":True},
                    f"{array_name}.sentBack":{"$exists":False},
                    f"{array_name}.ticket_id":{"$in":ticket_numbers}
                }
            },
            {
                "$group": {
                    "_id": "$code",
                    "data": {"$push": f"${array_name}"}
                }
            }
        ]
        data_from_collection = collection.aggregate(pipeline)
        
        for doc in data_from_collection:
            if doc['_id'] not in list(data.keys()):
                data[doc['_id']] = []
                data[doc['_id']].extend(doc['data'])
            else:
                data[doc['_id']].extend(doc['data'])
    return render_template('CM_SM_Closed.html',data=data,success_message=success_message,cmuser=user,role='CM/SM',type='closed_alerts_cm',notify=notify)


@app.route('/return_Mlro_Alerts',methods=['POST','GET'])
@secure_route(required_role='MLRO')
def return_Mlro_Alerts():
    success_message = session.pop('success_message', None)
    # Check user login
    if 'email_id' not in session:
        return redirect(url_for('post_login'))
    mlro_email = session['email_id']
    notify = clearnotification(mlro_email,"sentBackClosed")

    mlro = users_collection.find_one({"emailid": mlro_email})
    if mlro is None:
        return "User data not found. Please log in again."
    if 'image' in mlro:
                # Encode the image data as a base64 string
                mlro['image'] = base64.b64encode(mlro['image']).decode('utf-8')
    
    ticket_numbers = mlro.get("Sent_Back_Alerts", [])
    print("ticket_numbers",ticket_numbers)
    data = {}
    all_collections = [CLOSE_CASE_collection]
    array_names = ["output_data1", "output_data2", "output_data3"]
    for collection, array_name in product(all_collections, array_names):
        pipeline = [
            {
                "$unwind": f"${array_name}"
            },
            {
                "$match": {
                    f"{array_name}.allocate_to":mlro_email,
                    f"{array_name}.ticket_id":{"$in":ticket_numbers}
                }
            },
            {
                "$group": {
                    "_id": "$code",
                    "data": {"$push": f"${array_name}"}
                }
            }
        ]
        data_from_collection = collection.aggregate(pipeline)
        for doc in data_from_collection:
            if doc['_id'] not in list(data.keys()):
                data[doc['_id']] = []
                data[doc['_id']].extend(doc['data'])
            else:
                data[doc['_id']].extend(doc['data'])
    # for k,v in data.items():
    #     print(k)
    #     print(len(v))
    return render_template('returned_Alerts_MLRO.html', data=data,msgg=session.get('msgg'), success_message=success_message,mlrouser=mlro,role='MLRO',type='return_Mlro_Alerts',notify=notify)


@app.route('/returnCaseFormEdit',methods=['POST','GET'])
@secure_route(required_role=['MLRO','CM/SM'])
def returnCaseFormEdit():
    # mlro_email = session['email_id']
    msgg = session.pop('msgg', None) 
    email = session['email_id']
    user = users_collection.find_one({"emailid":email})
    allocatedCM = user["assigned_to"]
    notify = notification(email)
    mlro = users_collection.find_one({"emailid": email})
    if mlro is None:
        return "User data not found. Please log in again."
    if 'image' in mlro:
                # Encode the image data as a base64 string
                mlro['image'] = base64.b64encode(mlro['image']).decode('utf-8')
    data = {}
    # TY_collection, TM_collection, RM_collection,
    all_collections = [CLOSE_CASE_collection]
    array_names = ["output_data1", "output_data2", "output_data3"]

    if request.method == 'POST':
        ticket_id_from_form = request.form['ticket_id']
        CustomerId = request.form['custId']
        # formDAta = mlroCaseForm(ticket_id_from_form)
        
        
        
        for collection, array_name in product(all_collections, array_names):
            pipeline = [
                {
                    "$unwind": f"${array_name}"
                },
                {
                    "$match": {
                        f"{array_name}.ticket_id":ticket_id_from_form,
                        f"{array_name}.sentBack":{"$exists":True}
                    }
                },
                {
                    "$group": {
                        "_id": "$code",
                        "data": {"$push": f"${array_name}"}
                    }
                }
            ]
            data_from_collection = collection.aggregate(pipeline)
            for doc in data_from_collection:
                if doc['_id'] not in list(data.keys()):
                    data[doc['_id']] = []
                    data[doc['_id']].extend(doc['data'])
                else:
                    data[doc['_id']].extend(doc['data'])
        print(data)
       
        return render_template('closed_Form_Page.html',ticket_id=ticket_id_from_form,CustomerId=CustomerId,role=user["role"],allocated=allocatedCM,data=data,type='return_Mlro_Alerts',allImages=mlro,notify=notify, msgg=msgg)
    ticket_id_from_session = session.get('ticket_id')
    CustomerId = session.get('custid')
    print('ticket_id:', ticket_id_from_session)
    print('custid:', CustomerId)
    for collection, array_name in product(all_collections, array_names):
        pipeline = [
            {
                "$unwind": f"${array_name}"
            },
            {
                "$match": {
                    f"{array_name}.ticket_id":ticket_id_from_session,
                    f"{array_name}.sentBack":{"$exists":True}
                }
            },
            {
                "$group": {
                    "_id": "$code",
                    "data": {"$push": f"${array_name}"}
                }
            }
        ]
        data_from_collection = collection.aggregate(pipeline)
        for doc in data_from_collection:
            if doc['_id'] not in list(data.keys()):
                data[doc['_id']] = []
                data[doc['_id']].extend(doc['data'])
            else:
                data[doc['_id']].extend(doc['data'])
    print(data)
    
    return render_template('closed_Form_Page.html',ticket_id=ticket_id_from_session,CustomerId=CustomerId,role=user["role"],allocated=allocatedCM,data=data,type='return_Mlro_Alerts',allImages=mlro,notify=notify, msgg=msgg)






# CHANGES
def for_reports(collections_list):
    code_alert_title = {}
    for col in collections_list:
        data_from_col = col.find({},{"code":1,"Alert_title":1,"_id":0})
        for doc in data_from_col:
            code_alert_title[doc['code']]=doc['Alert_title']
    return code_alert_title

@app.route('/reports')
@secure_route(required_role='DGM/PO')
def reports():
    collections_list =[TM_collection,TY_collection,RM_collection]
    col_data = for_reports(collections_list)
    user = users_collection.find_one({'role': 'DGM/PO'})

    notify = notification(user.get('emailid'))

    ituser = {'image': None}
    if user:
        ituser = users_collection.find_one({'emailid': user.get('emailid')})
        if ituser and 'image' in ituser:
            ituser['image'] = base64.b64encode(ituser['image']).decode('utf-8')

    return render_template('reports.html',notify=notify,total_reports_data = col_data,type='dashbord',dgmuser=ituser,role='DGM/PO')


# ==============profile section===============

@app.route('/profile', methods=['GET', 'POST'])
@secure_route(required_role='MLRO')
def profile():
     email = session['email_id']
     notify = notification(email)

     user = users_collection.find_one({'emailid':email})
     if 'image' in user:
        # Encode the image data as a base64 string
        user['image'] = base64.b64encode(user['image']).decode('utf-8')
     return render_template('profileMLRO.html',mlrouser=user,role='MLRO',type='profile',notify=notify)


@app.route('/profileIT', methods=['GET', 'POST'])
@secure_route(required_role='IT Officer')
def profileIT():
     email = session['email_id']
     notify = notification(email)

     user = users_collection.find_one({'emailid':email})
     if 'image' in user:
        user['image'] = base64.b64encode(user['image']).decode('utf-8')
     return render_template('profileIT.html',ituser=user,role='IT Officer',type='profileIT',notify=notify)

@app.route('/profileAGM', methods=['GET', 'POST'])
@secure_route(required_role='AGM')
def profileAGM():
     email = session['email_id']
     notify = notification(email)

     user = users_collection.find_one({'emailid':email})
     if 'image' in user:
        user['image'] = base64.b64encode(user['image']).decode('utf-8')
     return render_template('profileAGM.html',agmuser=user,role='AGM',type='profileAGM',notify=notify)

@app.route('/profileDGM', methods=['GET', 'POST'])
@secure_route(required_role='DGM/PO')
def profileDGM():
     email = session['email_id']
     notify = notification(email)

     user = users_collection.find_one({'emailid':email})
     if 'image' in user:
        user['image'] = base64.b64encode(user['image']).decode('utf-8')
     return render_template('profileDGM.html',dgmuser=user,role='DGM/PO',type='profileDGM',notify=notify)

@app.route('/profile_CM_SM', methods=['GET', 'POST'])
@secure_route(required_role='CM/SM')
def profile_CM_SM():
     email = session['email_id']
     notify = notification(email)

     user = users_collection.find_one({'emailid':email})
     if 'image' in user:
        user['image'] = base64.b64encode(user['image']).decode('utf-8')
     return render_template('profile_CM_SM.html',cmuser=user,role='CM/SM',type='profile_CM_SM',notify=notify)


@app.route('/profileBranchMaker', methods=['GET', 'POST'])
@secure_route(required_role='BranchMakers')
def profileBranchMaker():
     email = session['email_id']
     notify = notification(email)

     user = users_collection.find_one({'emailid':email})
     if 'image' in user:
        user['image'] = base64.b64encode(user['image']).decode('utf-8')
     return render_template('profileBranchMaker.html',branchmakeruser=user,role='BranchMakers',type='profileBranchMaker',notify=notify)


@app.route('/profileROS', methods=['GET', 'POST'])
@secure_route(required_role='ROS')
def profileROS():
     email = session['email_id']
     notify = notification(email)

     user = users_collection.find_one({'emailid':email})
     if 'image' in user:
        user['image'] = base64.b64encode(user['image']).decode('utf-8')
     return render_template('profileROS.html',rosuser=user,role='ROS',type='profileROS',notify=notify)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
MAX_BINARY_SIZE = 50
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def compress_image(image_data):
    img = Image.open(BytesIO(image_data))
    img.thumbnail((300, 300))  # Adjust the size as needed
    try:
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        jpeg_data = buffered.getvalue()
        return jpeg_data
    except:
        # Save as PNG
        buffered_png = BytesIO()
        img.save(buffered_png, format="PNG")
        png_data = buffered_png.getvalue()
    
        return png_data

@app.route('/profileSDN', methods=['GET', 'POST'])
@secure_route(required_role='SDN/USER')
def profileSDN():
     email = session['email_id']
     notify = notification(email)
     user = users_collection.find_one({'emailid':email})
     if 'image' in user:
        user['image'] = base64.b64encode(user['image']).decode('utf-8')
     return render_template('profileSDN.html',sdnuser=user,role='SDN/USER',type='profileSDN',notify=notify)


@app.route('/edit_profile', methods=['POST'])
@secure_route(required_role=['MLRO','IT Officer','AGM','BranchMakers','CM/SM','ROS','DGM/PO','SDN/USER'])
def edit_profile():
    email = session['email_id']
    user = users_collection.find_one({'emailid': email})
    if 'image' not in user:
        users_collection.update_one({'emailid': email}, {'$set': {'image': None}})
    if 'profilePicture' in request.files:
        profile_picture = request.files['profilePicture']
        if profile_picture and allowed_file(profile_picture.filename):
            compressed_image = compress_image(profile_picture.read())
            users_collection.update_one({'emailid': email}, {'$set': {'image': compressed_image}})
    # Determine the redirect URL based on the user's role
    role = user.get('role', '')
    if role == 'IT Officer':
        return redirect(url_for('profileIT'))
    elif role == 'AGM':
        return redirect(url_for('profileAGM'))
    elif role == 'DGM/PO':
        return redirect(url_for('profileDGM'))
    elif role == 'CM/SM':
        return redirect(url_for('profile_CM_SM'))
    elif role == 'BranchMakers':
        return redirect(url_for('profileBranchMaker'))
    elif role == 'ROS':
        return redirect(url_for('profileROS'))
    elif role == 'SDN/USER':
        return redirect(url_for('profileSDN'))
    else:
        # Default to redirecting to 'profile' route
        return redirect(url_for('profile'))



@app.route('/sdn_data', methods=['GET', 'POST'])
@secure_route(required_role='IT Officer')
def sdn_data():
    data = list(sdn_collection.find())
    # Render HTML template with data
    exact_matches = []
    partial_matches = []
    for local_doc in local_col.find({}):
        name_input = local_doc.get('Name3')
        dob_input = local_doc.get('DOB')
        place_input = local_doc.get('POB')
        # Exact match query
        exact_match_query = {
            'Name3': name_input,
            'DOB': dob_input,
            'POB': place_input
        }
        exact_match_count = cloud_collection.count_documents(exact_match_query)
        if exact_match_count > 0:
            exact_matches.append(cloud_collection.find_one(exact_match_query))
            continue
        name_pattern = re.compile(f".*{re.escape(name_input[:4])}.*", re.IGNORECASE)
        partial_match_query = {
            'Name3': {'$regex': name_pattern},
            'DOB': dob_input,
            'POB': place_input
        }
        matching_cloud_docs = cloud_collection.find(partial_match_query,{"_id":0,"Name3":1,"DOB":1,"POB":1,"FirstName":1,"LastName":1,"PassportID":1,"NationalID":1,"OtherID":1,"Ent_ID":1,"EntryType":1,"EntryCategory":1,"Positions":1})
        for cloud_doc in matching_cloud_docs:
            partial_matches.append(cloud_doc)
    matching_data = {"Exact Match":exact_matches,"Partial Match":partial_matches}

    user = users_collection.find_one({'role': 'IT Officer'})

    ituser = {'image': ""}
    if user:
            ituser = users_collection.find_one({'emailid': user.get('emailid')})

            if ituser and 'image' in ituser:
                ituser['image'] = base64.b64encode(ituser['image']).decode('utf-8')

    return render_template('SDN_data.html',data=data,matching_data=matching_data,ituser=ituser,role='IT Officer',type='sdn_data')

###########  SDN DATA DOWNLOAD AS PER DAY ##################################################################################################

@app.route('/sdndownload', methods=['GET'])
@secure_route(required_role='IT Officer')
def sdndownload():
    mlro_email = session['email_id']
    mlro = users_collection.find_one({"emailid": mlro_email})
    ituser = {}

    if 'image' in mlro:
        # Encode the image data as a base64 string
        ituser['image'] = base64.b64encode(mlro['image']).decode('utf-8')

    data = {}  # Initialize data as a dictionary
    all_collections = [RM_collection, TM_collection, TY_collection]
    array_names = ["output_data1", "output_data2", "output_data3"]

    for collection, array_name in product(all_collections, array_names):
        pipeline = [
            {"$unwind": f"${array_name}"},
            {"$group": {
                "_id": {
                    "date": {"$dateToString": {"format": "%Y-%m-%d", "date": f"${array_name}.alert_created_on"}}
                },
                "count": {"$sum": 1}
            }},
            {"$sort": {"_id.date": 1}}
        ]
        dates_from_collection = collection.aggregate(pipeline)

        for doc in dates_from_collection:
            date_str = doc['_id']['date']
            data[date_str] = []
    print("SDDD",data)

    return render_template('sdndownload.html', ituser=ituser, data=data, role='IT Officer', type='sdndownload')



@app.route('/downloadsdndata', methods=['POST'])
def downloadsdndata():
    alert_created_date = request.form['alert_created_date']
    target_date = datetime.strptime(alert_created_date, '%Y-%m-%d')

    data = set()  # Initialize data as a set
    all_collections = [RM_collection, TM_collection, TY_collection]
    array_names = ["output_data1", "output_data2", "output_data3"]

    for collection, array_name in product(all_collections, array_names):
        pipeline = [
            {"$unwind": f"${array_name}"},
            {"$match": {
                f"{array_name}.alert_created_on": target_date,
                f"{array_name}.Customer Name": {"$exists": True}
            }},
            {
                "$group": {
                    "_id": None,
                    "data": {"$addToSet": f"${array_name}.Customer Name"},
                }
            }
        ]
        data_from_collection = list(collection.aggregate(pipeline))
        for doc in data_from_collection:
            data.update(doc.get('data', []))  # Use data.update() to add elements to the set

    if data:
        fileData = {'Customer Name': list(data)}
        df = pd.DataFrame(fileData)
        temp_dir = tempfile.mkdtemp()
        temp_filename = os.path.join(temp_dir, "customername.csv")
        df.to_csv(temp_filename, index=False)
        return send_file(temp_filename, as_attachment=True)
    else:
        return "No customer names found."


# ============== Downloading all STR Starts ===============
@app.route('/download_all_report', methods=['GET'])
@secure_route(required_role=['IT Officer', 'DGM/PO'])
def download_all_report():
    # Define filenames and categories
    categories = {
        "CWTR": {
            "Account Details": "Account_Detail.csv",
            "Account Personal Relation": "Account_Person_Relation.csv",
            "KC 1": "TC_2_Report_data.csv",
            "KC 2": "TS_2_Report_data.csv",
            "CB 1": "TS_3_Report_data.csv"
        },
        "CTR": {
            "Account Details": "Account_Detail.csv",
            "Account Personal Relation": "Account_Person_Relation.csv",
            "KC 1": "TS_1_Report_data.csv",
            "KC 2": "TS_2_Report_data.csv",
            "TC 1": "TC_1_Report_data.csv",
            "TC 2": "TC_2_Report_data.csv",
        },
        "NTR": {
            "Account Details": "Account_Detail.csv",
            "Account Personal Relation": "Account_Person_Relation.csv",
            "GT 1": "TC_1_Report_data.csv",
            "KC 2": "TC_2_Report_data.csv",
            "TC 1": "TC_1_Report_data.csv",
            "TC 2": "TC_2_Report_data.csv",
            "TS 1": "TS_1_Report_data.csv",
            "TS 2": "TS_2_Report_data.csv",
            "TS 3": "TS_3_Report_data.csv",
        }
    }

    # Create a temporary directory to store CSV files
    temp_dir = tempfile.mkdtemp()
    zip_filename = os.path.join(temp_dir, 'All_Reports.zip')

    try:
        # Create a temporary directory to organize files according to structure
        structured_temp_dir = os.path.join(temp_dir, 'structured_data')
        os.makedirs(structured_temp_dir)

        # Create temporary CSV files and add them to the structured directory
        for category, files in categories.items():
            category_dir = os.path.join(structured_temp_dir, category)
            os.makedirs(category_dir)
            for filename in files.values():
                data = Finnet_collection.find_one({'name': filename.replace('.csv', '')})
                if data is not None:
                    csv_data = data.get('data', [])
                    if csv_data:
                        temp_filename = os.path.join(category_dir, filename)
                        with open(temp_filename, 'w', newline='') as csvfile:
                            fieldnames = csv_data[0].keys() if csv_data else []
                            csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                            csv_writer.writeheader()
                            csv_writer.writerows(csv_data)

        # Create the zip file and add files according to structure
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for category, files in categories.items():
                category_dir = os.path.join(structured_temp_dir, category)
                for filename in files.values():
                    temp_filename = os.path.join(category_dir, filename)
                    if os.path.exists(temp_filename):
                        zipf.write(temp_filename, arcname=f"{category}/{filename}")

            # Add offline data to the zip file
            data = []
            all_collections = [offline_collection]
            array_names = ["data"]
            for collection, array_name in product(all_collections, array_names):
                pipeline = [
                    {"$unwind": f"${array_name}"},
                    {"$match": {
                        f"{array_name}.finalReport": "Approved",
                        f"{array_name}.finalReport_Submited_on": {"$exists": True}
                    }},
                    {"$group": {
                        "_id": "code",
                        "data": {"$push": {
                            "AccountNumber": f"${array_name}.AccountNumber",
                            "Date": f"${array_name}.finalReport_Submited_on",
                            "TicketId": f"${array_name}.ticket_id",
                        }},
                    }}
                ]
                data_from_collection = collection.aggregate(pipeline)
                for doc in data_from_collection:
                    data = (doc['data'])

            for ticket_info in data:
                TicketId = ticket_info['TicketId']
                all_collections = [offline_collection]
                array_names = ["data"]
                for collection, array_name in product(all_collections, array_names):
                    query = {f"{array_name}.ticket_id": TicketId, f"{array_name}.finalReport": "Approved"}
                    cursor = collection.find(query)
                    for document in cursor:
                        matching_object = document.get(array_name, [])
                        for obj in matching_object:
                            if obj["ticket_id"] == TicketId:
                                temp_csv_filename = os.path.join(temp_dir, f"{TicketId}_offline_data.csv")
                                temp_pdf_filename = os.path.join(temp_dir, f"{TicketId}_offline_data.pdf")
                                flattened_data_list = [flatten_data(obj)]
                                df = pd.DataFrame(flattened_data_list)
                                df.to_csv(temp_csv_filename, index=False)
                                list_of_dicts = df.to_dict(orient='records')
                                generate_pdf_from_csv(temp_csv_filename, temp_pdf_filename, list_of_dicts)
                                # Add PDF files to the zip file
                                if os.path.exists(temp_pdf_filename):
                                    zipf.write(temp_pdf_filename, arcname=f"STR_OFFLINE_DATA/{TicketId}_offline_data.pdf")

            # Add online data to the zip file
            data = []
            all_collections = [CASE_collection]
            array_names = ["output_data1", "output_data2", "output_data3"]
            for collection, array_name in product(all_collections, array_names):
                pipeline = [
                    {
                        "$unwind": f"${array_name}"
                    },
                    {
                        "$match": {
                            f"{array_name}.finalReport":"Approved",
                            f"{array_name}.finalReport_Submited_on":{"$exists":True}
                        }
                    },
                    {
                        "$group": {
                            "_id": "code",
                            "data":{"$push":{
                                "AccountNumber": f"${array_name}.Account Number",
                                "Date": f"${array_name}.finalReport_Submited_on",
                                "TicketId": f"${array_name}.ticket_id",
                            }},
                        }
                    }
                ]
                data_from_collection = collection.aggregate(pipeline)
                for doc in data_from_collection:
                    data = (doc['data'])

            for ticket_info in data:
                TicketId = ticket_info['TicketId']
                all_collections = [CASE_collection]
                array_names = ["output_data1", "output_data2", "output_data3"]
                for collection, array_name in product(all_collections, array_names):
                    query = {f"{array_name}.ticket_id": TicketId, f"{array_name}.finalReport": "Approved"}
                    cursor = collection.find(query)
                    for document in cursor:
                        matching_object = document.get(array_name, [])
                        for obj in matching_object:
                            if obj["ticket_id"] == TicketId:
                                temp_pdf_filename = os.path.join(temp_dir, f"{TicketId}_online_data.pdf")
                                flattened_data_list = [flatten_data(obj)]
                                df = pd.DataFrame(flattened_data_list)
                                df.to_csv(temp_csv_filename, index=False)
                                list_of_dicts = df.to_dict(orient='records')
                                generate_pdf_from_csv(temp_csv_filename, temp_pdf_filename, list_of_dicts)
                                # Add PDF files to the zip file
                                if os.path.exists(temp_pdf_filename):
                                    zipf.write(temp_pdf_filename, arcname=f"STR_ONLINE_DATA/{TicketId}_online_data.pdf")

        # Read the zip file and send its content as a response
        with open(zip_filename, 'rb') as zip_file:
            zip_data = zip_file.read()
        response = Response(zip_data, mimetype='application/zip')
        response.headers.set('Content-Disposition', 'attachment', filename='All_Reports.zip')
        return response
    
    finally:
        # Clean up: remove temporary directory and its contents
        shutil.rmtree(temp_dir)
# ============== Downloading all STR Starts ===============
    
# ===================== table data download starts==============
def flatten_dict(d):
    flattened = {}
    for key, value in d.items():
        if isinstance(value, dict):
            flattened.update(flatten_dict(value))
        else:
            flattened[key] = value
    return flattened

@app.route('/activeCases',methods=['POST','GET'])
def activeCases():
    data = request.get_json()
    ticket_numbers = data.get('ticket_numbers', [])
    print(ticket_numbers)
    resData = [flatten_dict(doc) for value in ticket_numbers.values() for doc in value]
    res = pd.DataFrame(resData)
    temp_dir = tempfile.mkdtemp()
    temp_filename = os.path.join(temp_dir, "AlltableData.csv")
    res.to_csv(temp_filename, index=False)
    return send_file(temp_filename, as_attachment=True)

# ===================== table data download Ends==============
#############   IT SDN PAGE ########################################################################################################################


@app.route('/sdndata', methods=['GET'])
@secure_route(required_role='IT Officer')
def sdndata():
    sdn_data = list(SDN_customers_collection.find({}, {'_id': 0}))
    sdn_names = [data['Name'] for data in sdn_data]
    print('sdn_names : ', sdn_names)
    
    # collections = ['Absconding_Criminals' ,'Adverse_Media' ,'Associated_Entity' ,'BSE_Defaulters_Expelled' ,'BSE_Delist_Companies' ,'BSE_Suspended_Companies' ,'Blacklisted_Doctors' ,'Blacklisted_NGOs' ,'CBI' ,'CIBIL' ,'CVC' ,'EOCN_UAE' ,'EU_Sanction_List' ,'Enforcement' ,'FATF'  ,'FCRA_Cancelled' ,'FIU_Defaulter_List' ,'IRDA' ,'Interpol' ,'MCA_Defaulter_Company' ,'MCA_Defaulter_Director' ,'MCA_Disqualified_Directors' ,'MCA_Dormant_Directors' ,'MCA_MLM_Company' ,'MCA_Proclaimed_Offenders' ,'MCX_Defaulters' ,'MHA_UAPA' ,'NBFC' ,'NCDEX_Cessation_Members' ,'NCDEX_Defaulter_Members' ,'NCDEX_Expelled_Members' ,'NIA_Arrested_Person' ,'NIA_Most_Wanted' ,'OFAC' ,'OFAC_SDN_Criminal_Individuals_List' ,'OFSI_UK_Sanction_list' ,'PEP','Registrations','SFIO_Conviction','SFIO_Proclaimed','SFIO_Prosecution','SOE','Sanction_List','UN_Sanction_List','World_Bank']
    collections = ['demo']

    result_dict = {}

    for doc in collections:
        collection = kamaldb[doc]
        pipeline = [
            {'$match': {'_source.name': {'$in': sdn_names}}},
            {'$group': {'_id': '$_source.name', 'items': {'$push': '$$ROOT'}}}
        ]

        res = list(collection.aggregate(pipeline))
        for entry in res:
            name = entry['_id']
            if name in result_dict:
                result_dict[name]['items'].extend(entry['items'])
            else:
                result_dict[name] = entry

    # Convert the dictionary to a list
    result = list(result_dict.values())

    return render_template('sdndata.html', matched_data=result, role='IT Officer', type='sdndata')

######## IT SDN  DATA PREVIEW PAGE ##################################################################################################################

@app.route('/sdndataPreview', methods=['POST', 'GET'])
@secure_route(required_role='IT Officer')
def sdndataPreview():
    
    sdn_data = list(SDN_customers_collection.find({}, {'_id': 0}))
    sdn_names = [data['Name'] for data in sdn_data]
    
    # collections = ['Absconding_Criminals', 'Adverse_Media', 'Associated_Entity', 'BSE_Defaulters_Expelled', 'BSE_Delist_Companies', 'BSE_Suspended_Companies', 'Blacklisted_Doctors', 'Blacklisted_NGOs', 'CBI', 'CIBIL', 'CVC', 'EOCN_UAE', 'EU_Sanction_List', 'Enforcement', 'FATF', 'FCRA_Cancelled', 'FIU_Defaulter_List', 'IRDA', 'Interpol', 'MCA_Defaulter_Company', 'MCA_Defaulter_Director', 'MCA_Disqualified_Directors', 'MCA_Dormant_Directors', 'MCA_MLM_Company', 'MCA_Proclaimed_Offenders', 'MCX_Defaulters', 'MHA_UAPA', 'NBFC', 'NCDEX_Cessation_Members', 'NCDEX_Defaulter_Members', 'NCDEX_Expelled_Members', 'NIA_Arrested_Person', 'NIA_Most_Wanted', 'OFAC', 'OFAC_SDN_Criminal_Individuals_List', 'OFSI_UK_Sanction_list', 'PEP', 'Registrations', 'SFIO_Conviction', 'SFIO_Proclaimed', 'SFIO_Prosecution', 'SOE', 'Sanction_List', 'UN_Sanction_List', 'World_Bank']
    # collections = ['Absconding_Criminals', 'Adverse_Media', 'Associated_Entity', 'BSE_Defaulters_Expelled', 'BSE_Delist_Companies', 'BSE_Suspended_Companies', 'Blacklisted_Doctors', 'Blacklisted_NGOs', 'CBI', 'CIBIL', 'CVC', 'EOCN_UAE', 'EU_Sanction_List', 'Enforcement', 'FATF', 'FCRA_Cancelled', 'FIU_Defaulter_List', 'IRDA', 'Interpol', 'MCA_Defaulter_Company', 'MCA_Defaulter_Director', 'MCA_Disqualified_Directors', 'MCA_Dormant_Directors', 'MCA_MLM_Company', 'MCA_Proclaimed_Offenders', 'MCX_Defaulters', 'MHA_UAPA', 'NBFC', 'NCDEX_Cessation_Members', 'NCDEX_Defaulter_Members', 'NCDEX_Expelled_Members', 'NIA_Arrested_Person', 'NIA_Most_Wanted', 'OFAC', 'OFAC_SDN_Criminal_Individuals_List', 'OFSI_UK_Sanction_list', 'PEP', 'Registrations', 'SFIO_Conviction', 'SFIO_Proclaimed', 'SFIO_Prosecution', 'SOE', 'Sanction_List', 'UN_Sanction_List', 'World_Bank']
    collections = ['demo']
    result_dict = {}

    for doc in collections:
        collection = kamaldb[doc]
        pipeline = [
            {'$match': {'_source.name': {'$in': sdn_names}}},
            {'$group': {'_id': '$_source.name', 'items': {'$push': '$$ROOT'}}}
        ]

        res = list(collection.aggregate(pipeline))
        for entry in res:
            name = entry['_id']
            if name in result_dict:
                result_dict[name]['items'].extend(entry['items'])
            else:
                result_dict[name] = entry

    # Convert the dictionary to a list
    result = list(result_dict.values())

    selected_name = request.form.get('selected_name')
    selected_matched_data = None
    
    # Find all data associated with the selected name
    for data in result:
        if data['_id'] == selected_name:
            selected_matched_data = data['items']
            break
            
    return render_template('sdndataPreview.html', matched_data=selected_matched_data, role='IT Officer', type='sdndata')

###########  IT SDN  VIW ALL PAGE #################################################################################################################

@app.route('/sdndataView', methods=['POST', 'GET'])
@secure_route(required_role='IT Officer')
def sdndataView():
    sdn_data = list(SDN_customers_collection.find({}, {'_id': 0}))
    sdn_names = [data['Name'] for data in sdn_data]
    
    # collections = ['Absconding_Criminals' ,'Adverse_Media' ,'Associated_Entity' ,'BSE_Defaulters_Expelled' ,'BSE_Delist_Companies' ,'BSE_Suspended_Companies' ,'Blacklisted_Doctors' ,'Blacklisted_NGOs' ,'CBI' ,'CIBIL' ,'CVC' ,'EOCN_UAE' ,'EU_Sanction_List' ,'Enforcement' ,'FATF'  ,'FCRA_Cancelled' ,'FIU_Defaulter_List' ,'IRDA' ,'Interpol' ,'MCA_Defaulter_Company' ,'MCA_Defaulter_Director' ,'MCA_Disqualified_Directors' ,'MCA_Dormant_Directors' ,'MCA_MLM_Company' ,'MCA_Proclaimed_Offenders' ,'MCX_Defaulters' ,'MHA_UAPA' ,'NBFC' ,'NCDEX_Cessation_Members' ,'NCDEX_Defaulter_Members' ,'NCDEX_Expelled_Members' ,'NIA_Arrested_Person' ,'NIA_Most_Wanted' ,'OFAC' ,'OFAC_SDN_Criminal_Individuals_List' ,'OFSI_UK_Sanction_list' ,'PEP','Registrations','SFIO_Conviction','SFIO_Proclaimed','SFIO_Prosecution','SOE','Sanction_List','UN_Sanction_List','World_Bank']
    collections = ['demo']
    result_dict = {}

    for doc in collections:
        collection = kamaldb[doc]
        pipeline = [
            {'$match': {'_source.name': {'$in': sdn_names}}},
            {'$group': {'_id': '$_source.name', 'items': {'$push': '$$ROOT'}}}
        ]

        res = list(collection.aggregate(pipeline))
        for entry in res:
            name = entry['_id']
            if name in result_dict:
                result_dict[name]['items'].extend(entry['items'])
            else:
                result_dict[name] = entry

    # Convert the dictionary to a list
    result = list(result_dict.values())

    selected_name = request.form.get('selected_id')
    selected_matched_data = None

    # Iterate over each data in result
    for data in result:
        for item in data['items']:
            if item['_id'] == selected_name:
                if selected_matched_data is None:
                    selected_matched_data = []
                    selected_matched_data.append(item)
                    break

        if selected_matched_data:
            break


    return render_template('sdndataView.html', matched_data=selected_matched_data, role='IT Officer', type='sdndata')

############## IT SDN CUSTOMER FORM #############################################################################################

@app.route('/sdncustomerform', methods=['GET', 'POST'])
@secure_route(required_role='IT Officer')
def sdncustomerform():
    if request.method == 'POST':
        try:
            # Validate input data
            name = request.form.get('name')
            pan = request.form.get('pan')
            aadhar = request.form.get('aadhar')
            dob = request.form.get('dob')
            
            # Add file upload date
            upload_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Insert validated data into the database
            SDN_customers_collection.insert_one({
                'Name': name,
                'pan': pan,
                'aadhar': aadhar,
                'dob': dob,
                'upload_date': upload_date  # Add file upload date
            })

            session['success'] = 'Form submitted successfully!'
            return render_template('sdndata.html', role='IT Officer', type='sdndata')

        except Exception as e:
            session['error'] = f'Error submitting form: {e}'
            return render_template('sdndata.html', error=session.get('error', None), role='IT Officer', type='sdndata')

    return render_template('sdndata.html', role='IT Officer', type='sdndata')
            
#############  IT SDN UPLOAD FILE ################################################################################################################


@app.route('/sdnuploadfile', methods=['GET', 'POST'])
@secure_route(required_role='IT Officer')
def sdnuploadfile():    
    if request.method == 'POST':
        uploaded_file = request.files.get('file')

        if not uploaded_file:
            session['error'] = "No file part"
        elif uploaded_file.filename == '':
            session['error'] = "No selected file"
        elif uploaded_file.filename.endswith(('.xlsx', '.csv')):
            try:
                if uploaded_file.filename.endswith('.xlsx'):
                    df = pd.read_excel(uploaded_file)
                else:  # Assume CSV for any other format
                    df = pd.read_csv(uploaded_file)

                # Add File_Upload_Date field with current date
                df['File_Upload_Date'] = datetime.now()

                records = df.to_dict(orient='records')
                SDN_customers_collection.insert_many(records)

                session['success'] = "File uploaded successfully"

            except Exception as e:
                session['error'] = f"Error processing file: {e}"

        else:
            session['error'] = "Unsupported file format. Please upload a .xlsx or .csv file."

    return render_template('sdndata.html', role='IT Officer', type='sdndata', success='Data Upload successfully!')


############   NEW SDN USER  #######################################################################################################################


@app.route('/SDN_user', methods=['GET'])
@secure_route(required_role='SDN/USER')
def SDN_user():
    mlro_email = session['email_id']
    mlro = users_collection.find_one({"emailid": mlro_email})
    ituser = {}
    notify=notification(mlro_email)

    if mlro and 'image' in mlro:
        # Encode the image data as a base64 string
        ituser['image'] = base64.b64encode(mlro['image']).decode('utf-8')


    return render_template('SDN_User.html', sdnuser=ituser, role='SDN/USER', type='SDN_user',notify=notify)

########## SDN USER UPLOAD JSON FILE #################################################################################################################

@app.route('/sdnuserfileupload', methods=['POST'])
@secure_route(required_role=['SDN/USER'])
def sdnuserfileupload():
    # Retrieve user email and notification
    mlro_email = session.get('email_id')
    mlro = db.users_collection.find_one({"emailid": mlro_email})
    notify = notification(mlro_email)
    ituser = {'image': base64.b64encode(mlro['image']).decode('utf-8')} if mlro and 'image' in mlro else {}

    # List of valid collection names
    valid_collections = [
        'Absconding_Criminals', 'Adverse_Media', 'Associated_Entity', 'BSE_Defaulters_Expelled',
        'BSE_Delist_Companies', 'BSE_Suspended_Companies', 'Blacklisted_Doctors', 'Blacklisted_NGOs',
        'CBI', 'CIBIL', 'CVC', 'EOCN_UAE', 'EU_Sanction_List', 'Enforcement', 'FATF', 'FCRA_Cancelled',
        'FIU_Defaulter_List', 'IRDA', 'Interpol', 'MCA_Defaulter_Company', 'MCA_Defaulter_Director',
        'MCA_Disqualified_Directors', 'MCA_Dormant_Directors', 'MCA_MLM_Company', 'MCA_Proclaimed_Offenders',
        'MCX_Defaulters', 'MHA_UAPA', 'NBFC', 'NCDEX_Cessation_Members', 'NCDEX_Defaulter_Members',
        'NCDEX_Expelled_Members', 'NIA_Arrested_Person', 'NIA_Most_Wanted', 'OFAC', 'OFAC_SDN_Criminal_Individuals_List',
        'OFSI_UK_Sanction_list', 'PEP', 'Registrations', 'SFIO_Conviction', 'SFIO_Proclaimed', 'SFIO_Prosecution',
        'SOE', 'Sanction_List', 'UN_Sanction_List', 'World_Bank'
    ]

    if request.method == 'POST':
        uploaded_file = request.files.get('file')

        if uploaded_file:
            try:
                json_data = uploaded_file.read().decode('utf-8')
                entities = json.loads(json_data)

                for entity in entities:
                    category = entity.get('_source', {}).get('category')
                    if category:
                        # Convert category to collection name format
                        collection_name = category.replace(' ', '_')
                        if collection_name in valid_collections:
                            # Get the collection and insert the entity
                            collection = kamaldb[collection_name]
                            collection.insert_one(entity)

                session['success'] = "File uploaded successfully"
            except Exception as e:
                session['error'] = f"Error processing file: {e}"
        else:
            session['error'] = "Unsupported file format. Please upload a JSON file."

    return render_template('SDN_User.html', role='SDN/USER', type='SDN_user', notify=notify)

@app.route('/tele_mon', methods=['GET', 'POST'])
@secure_route(required_role=['DGM/PO'])
def tele_mon():
    mlro_email = session['email_id']
    notify = notification(mlro_email)
    mlro = users_collection.find_one({"emailid": mlro_email})
    if mlro is None:
                return "User data not found. Please log in again."
    if 'image' in mlro:
                # Encode the image data as a base64 string
                mlro['image'] = base64.b64encode(mlro['image']).decode('utf-8')
    role = users_collection.find_one({'emailid':mlro_email})['role']
   
    collections = [TELE_MON]
    result_data = []
    for collection in collections:
        for document in collection.find():
            for array_name in ["output_data1", "output_data2", "output_data3"]:
                if array_name in document:
                    for obj in document[array_name]:
                        # Check if 'ip_address' field is present in obj
                        if 'IP ADDRESS' in obj:
                            result_data.append(obj)
    return render_template('tele_mon.html',notify=notify, result_data=result_data,type="dashbord",role=role,allImages=mlro)
def convert_datetime_to_js_date(data):
    # Convert datetime objects to ISO 8601 format
    if 'First Seen' in data and isinstance(data['First Seen'], datetime):
        data['First Seen'] = data['First Seen'].isoformat()
    if 'Last Seen' in data and isinstance(data['Last Seen'], datetime):
        data['Last Seen'] = data['Last Seen'].isoformat()
    return data
@app.route('/telemon_graph')
@secure_route(required_role=['DGM/PO'])
def telemon_graph():
    total_data = {}
    # database = Mongodb['Bank_Details']
    # sdn_col = database['Customer_Details']
    # telemon_col = database['Tele_MON']
    # Retrieve SDN_data directly from MongoDB
    SDN_data = local_col.find_one({"Name3": "Lee, Han-dong"}, {"_id": 0, "DirectID": 0,"EntrySubCategory":0,"Related_ID":0,"EntryType":0})
    total_data['SDN_data'] = SDN_data
    # Retrieve telemon_data directly from MongoDB
    telemon_data = TELE_MON_1.find_one({
        "Search Entity (mobile no)": 62811117164,
        "Name": "Lee, Han-dong",
        "Account No": 6051271060
    }, {"_id": 0,"Name":0})
    total_data['telemon_data'] = convert_datetime_to_js_date(telemon_data)
    # Query the MongoDB collection directly without using aggregation
    pipeline =txn_collection.aggregate( [
            {
                "$unwind":"$TXNDATA"
            },
            {
                "$match":{
                    "TXNDATA.Account Number":"6051271060",
                    "TXNDATA.Mobile Number":62811117164,
                    "TXNDATA.Customer Name":"Lee, Han-dong"
                }
            },
            {
                "$group": {
                    "_id": "$TXNDATA.Account Number",
                    "data": {"$push": "$TXNDATA"}
                }
            }
        ])
    agg_result = list(pipeline)
    data_from_col_df = pd.DataFrame()
    for doc in agg_result:
        data_from_col_df = pd.concat([data_from_col_df, pd.DataFrame(doc['data'])])
    if not data_from_col_df.empty:
        main_df = data_from_col_df[['Account Number','Customer Profile','Nature of account','Address','Pincode','Type of account']]
        main_df=main_df.drop_duplicates()
        nested_dict = {str(main_df['Account Number'].iloc[0]): main_df.drop('Account Number', axis=1).to_dict(orient='records')[0]}
        total_data['main_df']=nested_dict
    return render_template('graph2.html', total_data=total_data)
@app.route('/fiu_lea', methods=['GET', 'POST'])
@secure_route(required_role=['IT Officer'])
def fiu_lea():
    mlro_email = session['email_id']
    mlro = users_collection.find_one({"emailid": mlro_email})
    ituser = {}
    
    if 'image' in mlro:
                # Encode the image data as a base64 string
                ituser['image'] = base64.b64encode(mlro['image']).decode('utf-8')
    
    return render_template('fiu_lea.html',ituser=ituser,role='IT Officer',type='fiu_lea')
  
@app.route('/fiu_data', methods=['GET', 'POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def fiu_data():
    mlro_email = session['email_id']
    notify = notification(mlro_email)

    mlro = users_collection.find_one({"emailid": mlro_email})
    if mlro is None:
                return "User data not found. Please log in again."
    if 'image' in mlro:
                # Encode the image data as a base64 string
                mlro['image'] = base64.b64encode(mlro['image']).decode('utf-8')
    role = users_collection.find_one({'emailid':mlro_email})['role']
   
    try:
        user_role = session['user_role']
    except KeyError:
        session["Pls_login"] = "Session expired, Login again"
        return redirect(url_for('sign_in'))
    user_role = session.get('user_role')
    print("user_role",user_role)
    collections = [FIU]
    result_data = []
    
    for collection in collections:
        for document in collection.find():
            for array_name in ["output_data1", "output_data2", "output_data3"]:
                if array_name in document:
                    for obj in document[array_name]:
                        if "lea_fiu_status" in obj and obj["lea_fiu_status"] == "approved":
                            continue
                        result_data.append(obj)

    heading= "FIU"

   

    return render_template('fiu_lea_data.html', notify=notify ,result_data=result_data,heading=heading,user_role=user_role,type="fiu_data",role=role,allImages=mlro)

@app.route('/lea_data', methods=['GET', 'POST'])
@secure_route(required_role=['IT Officer','DGM/PO'])
def lea_data():
    mlro_email = session['email_id']
    notify = notification(mlro_email)

    mlro = users_collection.find_one({"emailid": mlro_email})
    if mlro is None:
                return "User data not found. Please log in again."
    if 'image' in mlro:
                # Encode the image data as a base64 string
                mlro['image'] = base64.b64encode(mlro['image']).decode('utf-8')
    role = users_collection.find_one({'emailid':mlro_email})['role']
   
    try:
        session['user_role']
    except:
        session["Pls_login"]="Session expired, Login again"
        return redirect(url_for('sign_in'))
    user_role = session.get('user_role')
    print("user_role",user_role)
    collections = [LEA]
    result_data = []
    
    for collection in collections:
        for document in collection.find():
            for array_name in ["output_data1", "output_data2", "output_data3"]:
                if array_name in document:
                    for obj in document[array_name]:
                        if "lea_status" in obj and obj["lea_status"] == "Approved":
                            continue
                        result_data.append(obj)
    heading= "LEA"

    return render_template('fiu_lea_data.html',notify=notify, result_data=result_data,heading=heading,user_role=user_role,type="lea_data",role=role,allImages=mlro)

@app.route('/lea_update', methods=['GET', 'POST'])
@secure_route(required_role=['DGM/PO'])
def lea_update():
    if request.method == "POST":
        print("hiiiiiiiiiiii")
        # action = request.form.get('action')
        # print("action", action)
        ticket_id = request.form.get('ticket_id')
        print("ticket_id", ticket_id)
        lea_status = request.form.get('status')
        # comments_added_date = datetime.now()

        # Update in the first collection (TM_collection)
        for document in LEA.find():
            for array_name in ["output_data1", "output_data2", "output_data3"]:
                if array_name in document:
                    for obj in document[array_name]:
                        if "ticket_id" in obj and obj["ticket_id"] == ticket_id:
                            LEA.update_one(
                                {"_id": document["_id"], f"{array_name}.ticket_id": ticket_id},
                                {"$set": 
                                    {f"{array_name}.$[elem].lea_status": lea_status}
                                },
                                array_filters=[{"elem.ticket_id": ticket_id}]
                            )
        for document in LEA.find():
            for array_name in ["output_data1", "output_data2", "output_data3"]:
                if array_name in document:
                    for obj in document[array_name]:
                        if "ticket_id" in obj and obj["ticket_id"] == ticket_id:
                            FIU.update_one(
                                {"_id": document["_id"], f"{array_name}.ticket_id": ticket_id},
                                {"$set": 
                                    {f"{array_name}.$[elem].lea_status": lea_status}
                                },
                                array_filters=[{"elem.ticket_id": ticket_id}]
                            )
        source_page = request.form.get('source_page')
        print("source_page",source_page)
        if source_page == 'lea_data':
            return redirect(url_for('lea_data'))
        else:
            return redirect(url_for('fiu_data'))


##### //    it officer TEN LAKHS DATA  ///########
@app.route('/tenlakcollection',methods=['POST','GET'])
@secure_route(required_role='IT Officer')
def tenlakcollection():
    mlro_email = session['email_id']
    mlro = users_collection.find_one({"emailid": mlro_email})
    ituser = {}
    
    if 'image' in mlro:
                # Encode the image data as a base64 string
                ituser['image'] = base64.b64encode(mlro['image']).decode('utf-8')

    data = TENLAKS.find({},{'_id':0})
    result = []
    for doc in data:
        date = str(doc['uploaded Date']).split(' ')[0]
        doc['date'] = date
        result.append(doc)
    return render_template('TenLaksData.html',data=result,ituser=ituser,role='IT Officer',type='tenlakcollection')
@app.route('/tenlakcollectionPreview',methods=['POST','GET'])
@secure_route(required_role='IT Officer')
def tenlakcollectionPreview():
    mlro_email = session['email_id']
    mlro = users_collection.find_one({"emailid": mlro_email})
    ituser = {}
    
    if 'image' in mlro:
                # Encode the image data as a base64 string
                ituser['image'] = base64.b64encode(mlro['image']).decode('utf-8')
    date = request.form.get('dateofupload')
    originalDate = datetime.strptime(date.split(' ')[0],'%Y-%m-%d')
    data = TENLAKS.find({'uploaded Date':originalDate},{'_id':0})
    result = []
    for doc in data:
        result = doc['output_data1']
    return render_template('TenLaksDataPreview.html',data=result,ituser=ituser,role='IT Officer',type='tenlakcollection')
@app.route('/downloadTenLaks',methods=['POST','GET'])
def downloadTenLaks():
    date = request.form.get('dateofupload')
    originalDate = datetime.strptime(date.split(' ')[0],'%Y-%m-%d')
    data = TENLAKS.find_one({'uploaded Date':originalDate})
    mainData = data['output_data1']
    fileData = []
    count = 0;
    for doc in mainData:
        count += 1
        obj = {
            'S.no.':count,
            'Date of Transaction':doc['Transaction Date'] if doc['Transaction Date'] else 'NIL',
            'District of the bank branch':doc['District'] if doc['District'] else 'NIL',
            'Bank Code':'NIL',
            'Bank Name':doc['Bank Name'] if doc['Bank Name'] else 'NIL',
            'Branch ID':'NIL',
            'Branch Name':'NIL',
            'BSR Code':'NIL',
            'IFSC Code':'NIL',
            'Unique Ref No.':'NIL',
            'PAN of customer':doc['PAN'] if doc['PAN'] else 'NIL',
            'Aadhar of customer':doc['Identification/Aadhar Number'] if doc['Identification/Aadhar Number'] else 'NIL',
            'Name of customer':doc['Customer Name'] if doc['Customer Name'] else 'NIL',
            'Address of customer':doc['Address'] if doc['Address'] else 'NIL',
            'Mobile Number of customer':doc['Mobile Number'] if doc['Mobile Number'] else 'NIL',
            'Transaction Type':doc['Transaction Type'] if doc['Transaction Type'] else 'NIL',
            'Transaction Category':doc['Transaction Category'] if doc['Transaction Category'] else 'NIL',
            'Account Number':doc['Account Number'] if doc['Account Number'] else 'NIL',
            'Amount involved':doc['Transaction Amount'] if doc['Transaction Amount'] else 'NIL',
            'PAN of bank account holder':doc['PAN'] if doc['PAN'] else 'NIL',
            'Remarks':'NIL',
            'Is this the usual type of transaction that SEC undertakes ?':'Yes'
        }
        fileData.append(obj)
    df = pd.DataFrame(fileData)
    temp_dir = tempfile.mkdtemp()
    temp_filename = os.path.join(temp_dir, "Cashmap_data.csv")
    df.to_csv(temp_filename, index=False)
    return send_file(temp_filename, as_attachment=True)

# @app.route('/NTR')
# def NTR():
#     reports_list_heding="NTR"
#     reports_list_data = ["Account Details", "Account Personal Relation", "GT 1", "KC 2", "TC 1", "TC 2", "TS 1", "TS 2", "TS 3"]
#     return render_template('ntr.html',reports_list_data=reports_list_data,reports_list_heding=reports_list_heding)

# @app.route('/CRT')
# def CRT():
#     reports_list_heding="CTR"
#     reports_list_data = ["Account Details", "Account Personal Relation", "KC 1", "KC 2", "TC 1", "TC 2"]
#     return render_template('ntr.html',reports_list_data=reports_list_data,reports_list_heding=reports_list_heding)

# @app.route('/CWTR')
# def CWTR():
#     reports_list_heding="CWTR"
#     reports_list_data = ["Account Details", "Account Personal Relation", "KC 1", "KC 2", "CB 1"]
#     return render_template('ntr.html',reports_list_data=reports_list_data,reports_list_heding=reports_list_heding)



    
schedule.every().day.at("10:50").do(closedDataAuto) 

def run_closed_alerts_loop(): 
    while True:
        schedule.run_pending()
        time.sleep(1)



if "__main__" == __name__:
    # while_thread = threading.Thread(target=run_while_loop)
    # while_thread.start()
    closed_while_thread = threading.Thread(target=run_closed_alerts_loop)
    closed_while_thread.start()
    app.run(port=5050,host="0.0.0.0",debug=False)
