#!/usr/bin/env python
# coding: utf-8

from pycoingecko import CoinGeckoAPI
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from collections import OrderedDict
from dotenv import load_dotenv
import os
import argparse
import csv
import sys
load_dotenv()

#################################################################################################################
#                                           GLOBAL VARIABLES                                                    #
#################################################################################################################

GMAIL_PASSWORD = os.environ.get('GMAIL_PASSWORD')
GMAIL_ADRESS = os.environ.get('GMAIL_ADRESS')
PORT=587
LIST_MAIL_TO = [GMAIL_ADRESS]
SUBJECT =  "[CRYPTO] - Report Journalier"
FROM = "myserver"

#################################################################################################################
#                                               FUNCTIONS                                                       #
#################################################################################################################

def parseArguments():
    parser = argparse.ArgumentParser(prog='ReportCrypto',
                                     usage='%(prog)s [options] file',
                                     description='Reports your crypto profits by email')
    parser.version = '1.1'
    parser.add_argument('--file',
                        type=argparse.FileType('r'), 
                        help='Input file csv wich contains your possessions in crypto',
                        required=True)
    args = parser.parse_args()
    return args

def check_and_fill_argfile(argfile, possessions):
    with argfile as file:
        csv_reader = csv.reader(file, delimiter = '|')
        for line, row in enumerate(csv_reader,1):
            if len(row) == 3 :
                try:
                    name_crypto = str(row[0])
                    total_pieces = float(row[1])
                    total_cost = int(row[2])
                    possessions[name_crypto] = [total_pieces,total_cost]
                except ValueError:
                    print(f"* /!\ Type Format Error in line {line} of file {argfile.name} => {row}") 
                    print("* The good format is Crypto [string] Total Pieces [float] Total Cost [int]")
                    print("* Example : bitcoin|3.2|104000")
                    sys.exit()
            else:
                print(f"* /!\ Number column Error in line {line} of file {argfile.name} => {row} ")
                print("* The good format is 3 data by line separated by '|'")
                print("* Example : bitcoin|3.2|104000")
                sys.exit()
    return possessions

# Goal : Connect to API and and return prices of somes crypo (dictionnary)
def dict_crypto():
    cg = CoinGeckoAPI()
    list_crypto = [key for key in possessions.keys()]
    return cg.get_price(ids=list_crypto, vs_currencies='eur')

# Goal : Do calculation with cryptos and possessions dico and return results in html code
# Input :
#   cryptos [dictionnary] 
#   possessions [dictionnary]

def calculation_and_fill(cryptos,possessions):
    contents = ""
    total_benefits = float(0)

    for name_crypto,value in cryptos.items():
        value = float(value["eur"])
        for k,v in possessions.items():
            if name_crypto in k:
                pieces = v[0]
                cost = v[1]
                total_amount = value*pieces
                benefits = total_amount-cost
                total_benefits += round(benefits,2)
                
                contents += "<tr>"
                contents += "<td> {} </td>".format(name_crypto)
                contents += "<td> {} </td>".format(round(pieces,2))
                contents += "<td> {} </td>".format(round(cost,2))
                contents += "<td> {} </td>".format(round(value,4))
                contents += "<td> {} </td>".format(round(total_amount,2))
                contents += "<td> {} </td>".format(round(benefits,2))
                contents += "</tr>"
    return contents,total_benefits
                
# Goal : Send an email with the contents html (report)
def mail(html_str):
    message = MIMEMultipart("alternative")
    message["Subject"] = SUBJECT
    message["From"] = FROM
    message["To"] = GMAIL_ADRESS

    message.attach(MIMEText(html_str,'html') )

    with smtplib.SMTP('smtp.gmail.com',587) as server:
        server.starttls()
        server.login(GMAIL_ADRESS,GMAIL_PASSWORD)
        server.sendmail(GMAIL_ADRESS,LIST_MAIL_TO,message.as_string() )


#################################################################################################################
#                                                  MAIN                                                         #
#################################################################################################################

if __name__ == '__main__':
    args = parseArguments()
    
    # Check if the format of csv file is correct
    possessions = check_and_fill_argfile(args.file, {})

    # Do an order of the dictionnary 
    cryptos = OrderedDict(sorted(dict_crypto().items(),key=lambda t: t[0]))
    
    contents,total_benefits = calculation_and_fill(cryptos,possessions)

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
    </html>""".format(contents,total_benefits)

    mail(html_str) 
