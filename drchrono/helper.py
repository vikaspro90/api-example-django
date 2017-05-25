import requests
import json
from django.conf import settings
from django.core.mail import send_mail

DOCTORS_URI = "https://drchrono.com/api/doctors"
PATIENTS_URI = "https://drchrono.com/api/patients"
USERS_URI = "https://drchrono.com/api/users"
# Access token will be set when the main page is loaded(when views.main is called)
ACCESS_TOKEN = ""

def getAuthHeaders():
	"""
	Return a header with access token.
	:return:
	"""
	return {"Authorization": "Bearer "+ACCESS_TOKEN, }

def getDocId(uid):
	"""
	Return the doctor field of a user object.
	:param uid:
	:return:
	"""
	headers=getAuthHeaders()
	response = requests.get(USERS_URI, headers=headers)
	users = json.loads(response.content)["results"]
	for user in users:
		if(str(user["id"])==uid):
			return user["doctor"]
	# this will never happen
	return ""

def getCurrUserDocName(uid):
	"""
	Return the name of currently logged in doctor.
	:param uid:
	:return:
	"""
	headers=getAuthHeaders()
	docId = getDocId(uid)
	response = requests.get(DOCTORS_URI, headers=headers)
	doctors = json.loads(response.content)["results"]
	for doc in doctors:
		if(doc["id"]==docId):
			return doc["first_name"], doc["last_name"]
	# this will never happen
	return ""

def getAllPatients():
	"""
	Return a list of all the patients associated with the current doctor.
	:return:
	"""
	headers = getAuthHeaders()
	patients = []
	toFetch = PATIENTS_URI
	while toFetch:
		data = json.loads(requests.get(PATIENTS_URI, headers=headers).content)
		patients.extend(data["results"])
		toFetch = data["next"]
	return patients

def getPatientsWithDOBToday(today):
	"""
	Return a list of patients that were born on this day.
	:param today:
	:return:
	"""
	patients = getAllPatients()
	return [{"id": patient["id"],
			 "first_name": patient["first_name"],
			 "last_name": patient["last_name"],
			 "email": patient["email"],
			 "phone": patient["cell_phone"],
			 "date_of_birth": patient["date_of_birth"]}
			for patient in patients if patient["date_of_birth"]!=None and patient["date_of_birth"][5:]==today[5:10]
	       ]

def getPatientDetails(fname, lname, dob):
	"""
	Return a patient object associated withe details received as arguments.
	:param fname:
	:param lname:
	:param dob:
	:return:
	"""
	params = {"first_name": fname, "last_name": lname, "date_of_birth": dob}
	headers = getAuthHeaders()
	patients = json.loads(requests.get(PATIENTS_URI,params=params, headers=headers).content)["results"]
	return None if len(patients)==0 else patients[0]

def sendBirthdayEmail(toList, message, subject="!!Happy Birthday!!"):
	"""
	Send email to the given email addresses with the message as body.
	:param toList:
	:param message:
	:param subject:
	:return:
	"""
	send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, toList, fail_silently=False)