import time

from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
import os
from dotenv import find_dotenv, load_dotenv
from google_sheet import Icont_sheet
from letters import panda_letter

ICONT_REF = ''
BOOKING = ''
TRUCK_NUMBER =''
CONT = ''
SEAL = ''

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)


app = Flask(__name__)

app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['MAIL_SERVER'] = 'mail.i-cont.eu'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
#app.config['MAIL_DEBAG'] = True
app.config['MAIL_USERNAME'] = 'tomi@i-cont.eu'
app.config['MAIL_PASSWORD'] = os.getenv('PASS')

app.config['MAIL_DEFAULT_SENDER'] = ('Tomi I-CONT','tomi@i-cont.eu')
app.config['MAIL_SMAX_EMAILS'] = 2
#app.config['MAIL_SUPRESS_SEND'] = False
app.config['MAIL_ASCII_ATTACHMENTS'] = False

mail = Mail(app)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/error')
def not_good():
    return render_template("not_good.html"), {"Refresh": "8; url='https://panda-lejelentes.onrender.com'"}

@app.route('/email_sent')
def success():
    return render_template("lejelentes.html",icont_ref=ICONT_REF, booking=BOOKING, cont=CONT, seal=SEAL,
                truck_number=TRUCK_NUMBER)

@app.route("/email_sent", methods=["POST"])
def receive_data():
    global ICONT_REF
    global BOOKING
    global CONT
    global SEAL
    global TRUCK_NUMBER


    BOOKING = (request.form['booking'])
    ICONT_REF = (request.form['icont_ref'])
    CONT = ((request.form['cont']).upper().replace(' ', ''))
    SEAL = ((request.form['seal']))
    TRUCK_NUMBER = (request.form['rendszam']).upper().replace(' ', '/')
    # button = ((request.form['button']))
    # print(f"BUTTOOOMNNN.: {button}")
    print(f"Icont ref.: {ICONT_REF}")
    print(f"Booking: {BOOKING}")
    print(f"Konténer: {CONT}")
    print(f"Zár: {SEAL}")
    print(f"Rendszám: {TRUCK_NUMBER}\n")


    if googlesheet_kitoltes(ICONT_REF, BOOKING, CONT, SEAL, TRUCK_NUMBER) == False:
        return redirect(url_for('not_good'))
    else:
        # msg = Message(subject=f"booking: {booking} / {CONT}",
        #               recipients=os.getenv('RECIPIENTS'),
        #               cc=os.getenv('CC')
        #               )

        recipients_str = os.getenv('RECIPIENTS')
        print(recipients_str)
        recipients_list = recipients_str.split(',')
        print(recipients_list)
        cc_list = os.getenv('CC').split(',')

        msg = Message(subject=f"booking: {BOOKING} / {CONT}",
                      recipients=recipients_list,
                      cc=cc_list
                      )

        #cdsg = Message(f"booking: {booking} / {cont}", recipients=['kele.tomka@gmail.com'])

        #msg.body = "Kerlek jelentsetek le Bilken az alabbi kontenert:"
        #<h5 style=”font-family: ’Calibri’; font-size:11; color:black;”>
        msg.html = panda_letter(CONT,SEAL)

        mail.send(msg)

        return redirect(url_for('success'))

def googlesheet_kitoltes(icont_ref, booking, cont,seal, truck_number):
    icont_ref = ICONT_REF
    booking = BOOKING
    cont = CONT
    truck_number = TRUCK_NUMBER

    googletabla = Icont_sheet()
    googlesheet = "https://docs.google.com/spreadsheets/d/1mQN5woJVHJrqf49D4TlEwQGtDx8PsnqKiLa6B_3Fd4g/edit#gid=0"
    worksheet = "Munkalap1"

    if googletabla.opensheet(googlesheet, worksheet) == False:
        exit()

    #googletabla.opensheet(sheetname="KISZALLITASOK", worksheet="Munkalap1")

    first_row = googletabla.get_container_rows("ICONT Ref.")[0]
    print(first_row)

    try:
        row = googletabla.get_container_rows(icont_ref)[0]
    except:
        return False
    print(row)
    row_dict = googletabla.bild_dictionary(first_row, row)
    print(row_dict)
    row_number = int(googletabla.get_container_row_numbers(icont_ref)[0])
    print(f"sorszám: {row_number}")
    print(row_number)
    print(row_dict["CONTAINER NO.."])


    if row_dict["CONTAINER NO.."] == booking and row_dict["ICONT Ref."] == icont_ref:
        print("MINDEN RENDBEN!!!!!")
        googletabla.updating_cell(row_number, 6, cont)
        googletabla.updating_cell(row_number, 15, truck_number)
        googletabla.updating_cell(row_number, 24, seal)
        return True
    else:
        print("NEM JÓÓÓÓÓÓÓÓÓÓÓÓÓÓÓ")
        return False


    #email(booking, container, seal)

if __name__ == "__main__":
    app.run(port=5005)
