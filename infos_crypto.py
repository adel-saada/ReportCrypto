#!/usr/bin/env python

from pycoingecko import CoinGeckoAPI
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from collections import OrderedDict
from dotenv import load_dotenv
import os

load_dotenv()


# Variables log 
GMAIL_PASSWORD = os.environ.get('GMAIL_PASSWORD')
GMAIL_ADRESS = os.environ.get('GMAIL_ADRESS')
PORT=587

# List of email(s) that will receive the report
# By Default, the sender
# example : TO_LIST_MAILS = [frederic@yahoo.fr,john@my-mail.com] 
TO_LIST_MAILS = [GMAIL_ADRESS]


import csv

# dict possessions crypto (numbers pieces and invest cost)

POSSESSIONS={}

with open('possession.csv','r') as file:
    reader = csv.reader(file, delimiter= '|')
    for row in reader:
        POSSESSIONS[row[0]] = [float(row[1]),int(row[2])]

# Goal : Connection to API and return prices of crypto with EUR currency (dict)
def dict_crypto():
    cg = CoinGeckoAPI()
    list_crypto = [key for key in POSSESSIONS.keys()]
    return cg.get_price(ids=list_crypto, vs_currencies='eur')


# Ordered dictionnary (more plaisant with each email report)
cryptos = OrderedDict(sorted(dict_crypto().items(),key=lambda t: t[0]))

contents = ""
total_benefices = float(0)

# Calculation of amounts, benefits... and puts in HTML code
for key,values in cryptos.items():
    name = key
    value = float(values["eur"])
    for k,v in POSSESSIONS.items():
        if name in k:
            pieces = v[0]
            cout = v[1]
            montant_total = value*pieces
            benefices = montant_total-cout
            total_benefices += round(benefices,2)
            
            contents += "<tr>"
            contents += "<td> {} </td>".format(name)
            contents += "<td> {} </td>".format(round(pieces,2))
            contents += "<td> {} </td>".format(round(cout,2))
            contents += "<td> {} </td>".format(round(value,4))
            contents += "<td> {} </td>".format(round(montant_total,2))
            contents += "<td> {} </td>".format(round(benefices,2))
            contents += "</tr>"


html_str="""
<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Crypto</title>
  <style type="text/css">
      table {{
        background: white;
        border-radius:3px;
        border-collapse: collapse;
        height: auto;
        max-width: 900px;
        padding:5px;
        width: 100%;
        animation: float 5s infinite;
      }}
      th {{
        color:#D5DDE5;;
        background:#1b1e24;
        border-bottom: 4px solid #9ea7af;
        font-size:14px;
        font-weight: 300;
        padding:10px;
        text-align:center;
        vertical-align:middle;
      }}
      tr {{
        border-top: 1px solid #C1C3D1;
        border-bottom: 1px solid #C1C3D1;
        border-left: 1px solid #C1C3D1;
        color:#666B85;
        font-size:16px;
        font-weight:normal;
      }}
      tr:hover td {{
        background:#4E5066;
        color:#FFFFFF;
        border-top: 1px solid #22262e;
      }}
      td {{
        background:#FFFFFF;
        padding:10px;
        text-align:left;
        vertical-align:middle;
        font-weight:300;
        font-size:13px;
        border-right: 1px solid #C1C3D1;
      }}
    </style>
</head>
<body>
  <table>
     <thead>
        <tr> <th colspan="6"> Table des cryptos </th> </tr>
     </thead>
     <tbody>
        <tr>
           <td>Crypto</td>
           <td>coins</td>
           <td>Invest</td>
           <td>unité €</td>
           <td>Total</td>
           <td>Benefices</td>
        </tr>

        {}

        <tr>
           <td colspan="5">Total Benefices :</td>
           <td>{}</td>
        </tr>
     </tbody>
  </table>
</body>
</html>
""".format(contents,total_benefices)



def mail(html_str):
    message = MIMEMultipart("alternative")
    message["Subject"] = "[CRYPTO] - Report Journalier"
    message["From"] = "myserver"
    message["To"] = GMAIL_ADRESS

    # Convert both parts to MIMEText objects and add them to the MIMEMultipart message
    message.attach(MIMEText(html_str,'html') )

    # Send email
    with smtplib.SMTP('smtp.gmail.com',587) as server:
        server.starttls()
        server.login(GMAIL_ADRESS,GMAIL_PASSWORD)
        server.sendmail(GMAIL_ADRESS,TO_LIST_MAILS,message.as_string() )



if __name__ == '__main__':
   mail(html_str) 
