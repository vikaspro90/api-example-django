import requests
import json
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail

DOCTORS_URI = "https://drchrono.com/api/doctors"
PATIENTS_URI = "https://drchrono.com/api/patients"
USERS_URI = "https://drchrono.com/api/users"

def getDocId(token, uid):
	response = requests.get(USERS_URI, params={"access_token": token})
	users = json.loads(response.content)["results"]
	for user in users:
		print user["id"], uid
		if(str(user["id"])==uid):
			return user["doctor"]
	# this will never happen
	return ""

def getCurrUserDocName(token, uid):
	# Gets the currently logged in doctor
	docId = getDocId(token, uid)
	response = requests.get(DOCTORS_URI, params={"access_token": token})
	doctors = json.loads(response.content)["results"]
	for doc in doctors:
		print doc["id"], docId
		if(doc["id"]==docId):
			return doc["first_name"], doc["last_name"]
	# this will never happen
	return ""

def getAllPatients(token):
	response = requests.get(PATIENTS_URI, params={"access_token": token})
	# A list of all the patients
	return json.loads(response.content)["results"]

def getPatientsWithDOBToday(token, today):
	patients = getAllPatients(token)
	return [{"id": patient["id"],
			 "first_name": patient["first_name"],
			 "last_name": patient["last_name"],
			 "email": patient["email"],
			 "phone": patient["cell_phone"]}
			for patient in patients if patient["date_of_birth"]!=None and patient["date_of_birth"][5:]==today[5:10]
	       ]

def sendBirthdayEmail(toList, message, subject="!!Happy Birthday!!"):
	send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, toList, fail_silently=False)