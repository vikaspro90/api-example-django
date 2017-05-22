import requests
import json
from django.utils import timezone
import smtplib

def getAllPatients(token):
	PATIENTS_URI = "https://drchrono.com/api/patients"
	response = requests.get(PATIENTS_URI, params={"access_token": token})
	#names = [p["first_name"].encode("utf-8")+" "+p["last_name"].encode("utf-8") for p in json.loads(response.content)["results"]]
	# A list of all the patients
	return json.loads(response.content)["results"]

def getPatientsWithDOBToday(token):
	patients = getAllPatients(token)
	today = str(timezone.now())
	print "***"+today
	for patient in patients:
		print patient["date_of_birth"]
	return [{"id": patient["id"],
			 "first_name": patient["first_name"],
			 "last_name": patient["last_name"],
			 "email": patient["email"],
			 "phone": patient["cell_phone"]}
			for patient in patients if patient["date_of_birth"]!=None and patient["date_of_birth"][5:]==today[5:10]
	       ]

# def sendBirthdayEmail(toEmailAddr, body, subject="Yay.. Happy Birthday!!"):
# import django
# from django.conf import settings
# from django.core.mail import send_mail
# send_mail("Subject here", "This is the message", settings.EMAIL_HOST_USER, ["vikas1590@gmail.com"], fail_silently=False)
