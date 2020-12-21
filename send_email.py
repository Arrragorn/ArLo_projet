import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime


def mailto(attachedFileBytes):
      
    dateTimeObj = datetime.now()
    dateStr = dateTimeObj.date().strftime("%b %d %Y ")
    timeStr = dateTimeObj.time().strftime("%H:%M:%S.%f")
    subject = "Mouvement détecté dans le logiciel de surveillance video"
    body = "Mouvement detecté le : " + dateStr + " à " + timeStr
    sender_email = "surveillance.video.2020@gmail.com"
    #receiver_email = "the_noctivagus@hotmail.com"
    password = "6GEI311%logiciel"
    
    #Ouvrir le fichier d'adresse de distribution des alertes et remplir un array
    fileEmailList = open("ListeDistributionAlertes.txt", "r")
    array_reciever_email = fileEmailList.readlines()
    
    #Pour chaque adresse dans le fichier, envoyer une alerte
    for receiver_email in array_reciever_email:
        
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Bcc"] = receiver_email  # Recommended for mass emails
        
        # Add body to email
        message.attach(MIMEText(body, "plain"))
        
        
        # Open attachent file in binary mode
        
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachedFileBytes)
        
        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part)
        
        filename = 'alerte.jpg'
        
        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )
        
        # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()
        
        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)
        
    return 1

#tests pour ce module
if (__name__ == "__main__"):
    
    file = open("gandalf2.jpg",'rb')
    
    mailto(file.read())
