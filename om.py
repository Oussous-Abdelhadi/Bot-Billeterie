import requests
from bs4 import BeautifulSoup
import smtplib #lib pour la partie email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


SMTP_SERVER =  "smtp.office365.com" #Serveur email
SMTP_PORT = 587 #Port du serveur
GMAIL_USERNAME  = "" #Votre adresse  email
GMAIL_PASSWORD = "" #Votre  mot de passe
receiverAddress = "" #Adresse mail destinataire

emailSubject = "Rapport du bot OM \u26BD" #Objet du email 
emailBase = "Les matchs disponibles :\n\n" #Début du corps du email
emailContent = "" #Contenu du mail
emailSignature = "\n Cordialement,\n Le bot" #Signature du mail
sendEmail = False #Variable de contrôle permettant de savoir s'il faut envoyer l'email

url = "https://billetterie.om.fr/fr"
reponse = requests.get(url)
page = reponse.content



# transforme (parse) le HTML en objet BeautifulSoup
soup = BeautifulSoup(page, "html.parser")

# # récupération de tous les titres
match = soup.find_all("div", class_="participant second")

equipe = []
for titre in match:
	equipe.append(titre.text.strip())

resultantList = []
 
for element in equipe:
    if element not in resultantList:
        resultantList.append(element)


nb = 2
array = []
if len(resultantList) == nb :
    sendEmail = True
    for matchs in resultantList:
        contenu = "OM vs "+ matchs + '\n'
        array.append(contenu)
emailContent = '\n'.join(array)


#Envoi de l'email
if(sendEmail == True):
    #Le corps du mail est composé de la phrase de base, des noms des jeux à acheter et de la signature
    emailBody = emailBase + emailContent + emailSignature

    #Creation de  l'email
    message = MIMEMultipart()
    message['From'] = GMAIL_USERNAME
    message['To'] = receiverAddress
    message['Subject'] = emailSubject
    message['Content'] = emailContent
    message.attach(MIMEText(emailBody, 'plain'))

    #Connexion  au serveur Gmail
    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    session.ehlo()
    session.starttls()
    session.ehlo()
 
    #Authentification
    session.login(GMAIL_USERNAME, GMAIL_PASSWORD)

    #Envoi de l'email
    session.sendmail(GMAIL_USERNAME, receiverAddress, message.as_string())
    session.quit
    
    #Le mail vient d'être envoyé, on remet la variable de controle à False
    sendEmail = False
    