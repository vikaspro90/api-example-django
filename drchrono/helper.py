import requests
import datetime
import json

def getAllPatients(token):
	PATIENTS_URI = "https://drchrono.com/api/patients"
	response = requests.get(PATIENTS_URI, params={"access_token": token})
	#names = [p["first_name"].encode("utf-8")+" "+p["last_name"].encode("utf-8") for p in json.loads(response.content)["results"]]
	# A list of all the patients
	return json.loads(response.content)["results"]

def getPatientsWithDOBToday(token):
	patients = getAllPatients(token)
	today = datetime.datetime.now().isoformat()[:10]
	for patient in patients:
		print patient["date_of_birth"]
	return [{"id": patient["id"],
			 "first_name": patient["first_name"],
			 "last_name": patient["last_name"],
			 "email": patient["email"],
			 "phone": patient["cell_phone"]}
			for patient in patients if patient["date_of_birth"]!=None and patient["date_of_birth"][5:]==today[5:]
			]