from flask import Flask, render_template, request, json, flash
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


app = Flask(__name__)
app.secret_key = 'super secret key'

@app.route('/')
def index_en():
    return render_template('index_en.html', overall=overall_2022(), fm=overall(), peak=peak(), age=age_vict(), abuse=age_abuser())

@app.route('/', methods=['POST'])
def index_en_post():
    name = request.form['name']
    email = request.form['email']
    report_message = request.form['message']
    sender_address = 'SENDER_EMAIL'
    sender_pass = 'APP_SECRET'
    receiver_address = 'RECIEVER_EMAIL'
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Domestic Violence Report'
    message.attach(MIMEText(f"Name: {name}\nEmail: {email}\nMessage: {report_message}", 'plain'))
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    return render_template('index_en.html', overall=overall_2022(), fm=overall(), peak=peak(), age=age_vict(), abuse=age_abuser())


@app.route('/ka',)
def index_ka():
    return render_template('index_ka.html', overall=overall_2022(), fm=overall(), peak=peak(), age=age_vict(), abuse=age_abuser())

@app.route('/ka', methods=['POST'])
def index_ka_post():
    name = request.form['name']
    email = request.form['email']
    report_message = request.form['message']
    sender_address = 'SENDER_EMAIL'
    sender_pass = 'APP_PASSWORD'
    receiver_address = 'RECIEVER_EMAIL'
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Domestic Violence Report'
    message.attach(MIMEText(f"Name: {name}\nEmail: {email}\nMessage: {report_message}", 'plain'))
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    return render_template('index_ka.html', overall=overall_2022(), fm=overall(), peak=peak(), age=age_vict(), abuse=age_abuser())


def overall_2022():
    with open(f'json/2022_Jan.json') as f:
        data = json.loads(f.read())
        January = data['saqarTvelo']['Victims']['Male']['All'] + data['saqarTvelo']['Victims']['Female']['All']
    with open(f'json/2022_Feb.json') as f:
        data = json.loads(f.read())
        February = data['saqarTvelo']['Victims']['Male']['All'] + data['saqarTvelo']['Victims']['Female']['All']
    with open(f'json/2022_March.json') as f:
        data = json.loads(f.read())
        March = data['saqarTvelo']['Victims']['Male']['All'] + data['saqarTvelo']['Victims']['Female']['All']
    with open(f'json/2022_April.json') as f:
        data = json.loads(f.read())
        April = data['saqarTvelo']['Victims']['Male']['All'] + data['saqarTvelo']['Victims']['Female']['All']
    with open(f'json/2022_May.json') as f:
        data = json.loads(f.read())
        May = data['saqarTvelo']['Victims']['Male']['All'] + data['saqarTvelo']['Victims']['Female']['All']
    with open(f'json/2022_June.json') as f:
        data = json.loads(f.read())
        June = data['saqarTvelo']['Victims']['Male']['All'] + data['saqarTvelo']['Victims']['Female']['All']
    with open(f'json/2022_Jule.json') as f:
        data = json.loads(f.read())
        July = data['saqarTvelo']['Victims']['Male']['All'] + data['saqarTvelo']['Victims']['Female']['All']
    with open(f'json/2022_Aug.json') as f:
        data = json.loads(f.read())
        August = data['saqarTvelo']['Victims']['Male']['All'] + data['saqarTvelo']['Victims']['Female']['All']
    with open(f'json/2022_Sep.json') as f:
        data = json.loads(f.read())
        September = data['saqarTvelo']['Victims']['Male']['All'] + data['saqarTvelo']['Victims']['Female']['All']

    return January,February,March,April,May,June,July,August,September

def overall():
    with open(f'json/2022_Jan.json') as f:
        data = json.loads(f.read())
        M_22 = data['saqarTvelo']['Victims']['Male']['All']
        F_22 = data['saqarTvelo']['Victims']['Female']['All']

    with open(f'json/2022_Feb.json') as f:
        data = json.loads(f.read())
        M_22 += data['saqarTvelo']['Victims']['Male']['All']
        F_22 += data['saqarTvelo']['Victims']['Female']['All']

    with open(f'json/2022_March.json') as f:
        data = json.loads(f.read())
        M_22 += data['saqarTvelo']['Victims']['Male']['All']
        F_22 += data['saqarTvelo']['Victims']['Female']['All']

    with open(f'json/2022_April.json') as f:
        data = json.loads(f.read())
        M_22 += data['saqarTvelo']['Victims']['Male']['All']
        F_22 += data['saqarTvelo']['Victims']['Female']['All']

    with open(f'json/2022_May.json') as f:
        data = json.loads(f.read())
        M_22 += data['saqarTvelo']['Victims']['Male']['All']
        F_22 += data['saqarTvelo']['Victims']['Female']['All']

    with open(f'json/2022_June.json') as f:
        data = json.loads(f.read())
        M_22 += data['saqarTvelo']['Victims']['Male']['All']
        F_22 += data['saqarTvelo']['Victims']['Female']['All']

    with open(f'json/2022_Jule.json') as f:
        data = json.loads(f.read())
        M_22 += data['saqarTvelo']['Victims']['Male']['All']
        F_22 += data['saqarTvelo']['Victims']['Female']['All']

    with open(f'json/2022_Aug.json') as f:
        data = json.loads(f.read())
        M_22 += data['saqarTvelo']['Victims']['Male']['All']
        F_22 += data['saqarTvelo']['Victims']['Female']['All']

    with open(f'json/2022_Sep.json') as f:
        data = json.loads(f.read())
        M_22 += data['saqarTvelo']['Victims']['Male']['All']
        F_22 += data['saqarTvelo']['Victims']['Female']['All']

    with open(f'json/2021.json') as f:
        M_21 = 0
        F_21 = 0
        data = json.loads(f.read())
        for i in data:
            M_21 += data[i]['Victims']['Male']['All']
            F_21 += data[i]['Victims']['Female']['All']
       
    with open(f'json/2020.json') as f:
        data = json.loads(f.read())
        M_20 = data['saqarTvelo']['Victims']['Male']['All']
        F_20 = data['saqarTvelo']['Victims']['Female']['All']

    with open(f'json/2019.json') as f:
        data = json.loads(f.read())
        M_19 = data['saqarTvelo']['Victims']['Male']['All']
        F_19 = data['saqarTvelo']['Victims']['Female']['All']
    
    with open(f'json/2018.json') as f:
        data = json.loads(f.read())
        M_18 = data['saqarTvelo']['Victims']['Male']['All']
        F_18 = data['saqarTvelo']['Victims']['Female']['All']

    return [M_22, F_22], [M_21, F_21], [M_20, F_20], [M_19, F_19], [M_18, F_18]

def peak():
    with open(f'json/2020.json') as f:
        data = json.loads(f.read())
        tbilisi_m = data['Tbilisi']['Victims']['Male']['All']
        ajara_m = data['aWara']['Victims']['Male']['All']
        imereti_m = data['imereTi']['Victims']['Male']['All']
        svaneti_m = data['svaneTi']['Victims']['Male']['All']
        qartli_m = data['qvemo qarTli']['Victims']['Male']['All']
        tbilisi_f = data['Tbilisi']['Victims']['Female']['All']
        ajara_f = data['aWara']['Victims']['Female']['All']
        imereti_f = data['imereTi']['Victims']['Female']['All']
        svaneti_f = data['svaneTi']['Victims']['Female']['All']
        qartli_f = data['qvemo qarTli']['Victims']['Female']['All']
        
    return [tbilisi_m, tbilisi_f], [ajara_m, ajara_f], [imereti_m, imereti_f], [svaneti_m, svaneti_f], [qartli_m, qartli_f]

def age_vict():
    with open(f'json/2022_Sep.json') as f:
        data = json.loads(f.read())
        unknown = data['saqarTvelo']['Victims']['Male']['Unknown'] + data['saqarTvelo']['Victims']['Female']['Unknown']
        child = data['saqarTvelo']['Victims']['Male']['<13'] + data['saqarTvelo']['Victims']['Female']['<13'] 
        teenage = data['saqarTvelo']['Victims']['Male']['14-17'] + data['saqarTvelo']['Victims']['Female']['14-17'] 
        midle = data['saqarTvelo']['Victims']['Male']['18-24'] + data['saqarTvelo']['Victims']['Female']['18-24'] 
        overage = data['saqarTvelo']['Victims']['Male']['25-44'] + data['saqarTvelo']['Victims']['Female']['25-44'] 
        old = data['saqarTvelo']['Victims']['Male']['45-60'] + data['saqarTvelo']['Victims']['Female']['45-60']
        older = data['saqarTvelo']['Victims']['Male']['61>'] + data['saqarTvelo']['Victims']['Female']['61>']
    
    return unknown, child, teenage, midle, overage, old, older

def age_abuser():
    with open(f'json/2022_Sep.json') as f:
        data = json.loads(f.read())
        unknown = data['saqarTvelo']['Abusers']['Male']['Unknown'] + data['saqarTvelo']['Abusers']['Female']['Unknown']
        child = data['saqarTvelo']['Abusers']['Male']['<13'] + data['saqarTvelo']['Abusers']['Female']['<13'] 
        teenage = data['saqarTvelo']['Abusers']['Male']['14-17'] + data['saqarTvelo']['Abusers']['Female']['14-17'] 
        midle = data['saqarTvelo']['Abusers']['Male']['18-24'] + data['saqarTvelo']['Abusers']['Female']['18-24'] 
        overage = data['saqarTvelo']['Abusers']['Male']['25-44'] + data['saqarTvelo']['Abusers']['Female']['25-44'] 
        old = data['saqarTvelo']['Abusers']['Male']['45-60'] + data['saqarTvelo']['Abusers']['Female']['45-60']
        older = data['saqarTvelo']['Abusers']['Male']['61>'] + data['saqarTvelo']['Abusers']['Female']['61>']
    
    return unknown, child, teenage, midle, overage, old, older
