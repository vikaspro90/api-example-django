import requests
import json
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail

def getAllPatients(token):
	PATIENTS_URI = "https://drchrono.com/api/patients"
	response = requests.get(PATIENTS_URI, params={"access_token": token})
	# A list of all the patients
	return json.loads(response.content)["results"]

def getPatientsWithDOBToday(token):
	patients = getAllPatients(token)
	today = str(timezone.now())
	return [{"id": patient["id"],
			 "first_name": patient["first_name"],
			 "last_name": patient["last_name"],
			 "email": patient["email"],
			 "phone": patient["cell_phone"]}
			for patient in patients if patient["date_of_birth"]!=None and patient["date_of_birth"][5:]==today[5:10]
	       ]

def sendBirthdayEmail(toList, message, subject="Yay.. Happy Birthday!!"):
	send_mail(subject, message, settings.EMAIL_HOST_USER, toList, fail_silently=False)
