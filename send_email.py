from email.mime.text import MIMEText
import smtplib

def send_email(email,height,avg_height,count):
    from_email="testbhumika28@gmail.com"
    from_password="qsthanrmgleorzwa"
    to_email=email

    subject="Height Data"
    message="Hey There! Your height is <strong>%s</strong>cm. \n Average height of everyone who took the survey is <strong>%s</strong> and that is calculated out of <strong>%s</strong> people." % (height,avg_height,count)

    msg=MIMEText(message,'html')
    msg['Subject']=subject
    msg['To']=to_email
    msg['From']=from_email

    gmail=smtplib.SMTP('smtp.gmail.com',587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email,from_password)
    gmail.send_message(msg)
