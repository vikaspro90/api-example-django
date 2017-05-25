from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponse
from models import SessionWithDate, Session
import json
import helper

# Create your views here.

@login_required(login_url="/")
def main(request):
	"""
	Render the main page for authenticated users.
	:param request:
	:return:
	"""
	social = request.user.social_auth.get(provider="drchrono")
	# All api calls will be handled in the helper module
	helper.ACCESS_TOKEN = social.extra_data['access_token']
	uid = social.uid
	# if the current user name is already not in the user model,
	# fetch it from the doctors api, else fetch it from database and send as response.
	if len(request.user.first_name)==0 or len(request.user.last_name)==0:
		docName = helper.getCurrUserDocName(uid)
		request.user.first_name = docName[0]
		request.user.last_name = docName[1]
		request.user.save()
	else:
		docName = [request.user.first_name, request.user.last_name]
	return render_to_response("main.html", {"docName": " ".join(docName)})

@login_required(login_url="/")
def handShake(request):
	"""
	Save the client date in SessionWithDate model and return
	the current doctor name.
	:param request:
	:return:
	"""
	# Associating the client date with the current session
	currSession = SessionWithDate.objects.filter(sess_id=request.session.session_key)
	# if current session is not in the db, create a new one, else update it
	# needed to make sure consistency if same session is used when the date changes
	if len(currSession)==0:
		SessionWithDate.objects.create(sess=Session.objects.filter(session_key=request.session.session_key)[0], date=json.loads(request.body)["clientDate"])
	else:
		SessionWithDate.objects.filter(sess_id=request.session.session_key).update(date=json.loads(request.body)["clientDate"])
	docName = request.user.first_name+" "+request.user.last_name;
	return HttpResponse(json.dumps({"docName": docName}), 200)

@login_required(login_url="/")
def updatePatientList(request):
	"""
	Return a list of patients that were born on this day.
	:param request:
	:return:
	"""
	clientDate = SessionWithDate.objects.filter(sess_id=request.session.session_key)[0].date
	patients = helper.getPatientsWithDOBToday(clientDate)
	return HttpResponse(json.dumps({"patients": patients}), 200)

@login_required(login_url="/")
def getPatientDetails(request):
	"""
	Return all the details of a patient.
	:param request:
	:return:
	"""
	params = (request.GET.get("fname"), request.GET.get("lname"), request.GET.get("dob"))
	patient = helper.getPatientDetails(*params)
	return HttpResponse(json.dumps({"patient":patient}), 200)

@login_required(login_url="/")
def sendEmail(request):
	"""
	Send email to the list of email IDs given.
	Same endpoint for single or multiple emails.
	Decide based on the mode parameter.
	Append patient names to the message if mode is multiple.
	:param request:
	:return:
	"""
	toList = json.loads(request.body)["toList"]
	message = json.loads(request.body)["message"]
	mode = json.loads(request.body)["mode"]
	if mode=="multiple":
		names = json.loads(request.body)["names"]
		for i in range(len(toList)):
			newMessage = "Hello {}\n\n".format(names[i])+message
			helper.sendBirthdayEmail([toList[i]], newMessage)
	else:
		helper.sendBirthdayEmail(toList, message)
	return HttpResponse(200)

def logout(request):
	"""
	Log the user out.
	:param request:
	:return:
	"""
	auth_logout(request=request)
	return redirect("/")