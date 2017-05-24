from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponse
from models import SessionWithDate, Session
import json
import helper

# Create your views here.

# Main page for authenticated users
@login_required(login_url="/")
def main(request):
	# username = request.user.get_username()
	social = request.user.social_auth.get(provider="drchrono")
	helper.ACCESS_TOKEN = social.extra_data['access_token']
	uid = social.uid
	if len(request.user.first_name)==0 or len(request.user.last_name)==0:
		docName = helper.getCurrUserDocName(uid)
		request.user.first_name = docName[0]
		request.user.last_name = docName[1]
		request.user.save()
	else:
		docName = [request.user.first_name, request.user.last_name]
	data = helper.getPatientDetails("Vikas", "Nahi Hai", "1990-05-24")
	# return render_to_response("main.html", {"name": docName})
	return render_to_response("main.html", {"docName": " ".join(docName), "data": data})

@login_required(login_url="/")
def handShake(request):
	print "In handShake."
	# Associating the client date with the current session
	currSession = Session.objects.filter(session_key=request.session.session_key)
	if len(currSession)==0:
		SessionWithDate.objects.create(sess=Session.objects.filter(session_key=request.session.session_key)[0], date=json.loads(request.body)["clientDate"])
	else:
		SessionWithDate.objects.filter(sess_id=request.session.session_key).update(date=json.loads(request.body)["clientDate"])
	docName = request.user.first_name+" "+request.user.last_name;
	return HttpResponse(json.dumps({"docName": docName}), 200)

@login_required(login_url="/")
def updatePatientList(request):
	print "In updatePatientList."
	clientDate = SessionWithDate.objects.filter(sess=request.session.session_key)[0].date
	patients = helper.getPatientsWithDOBToday(clientDate)
	return HttpResponse(json.dumps({"patients": patients}), 200)

@login_required(login_url="/")
def getPatientDetails(request):
	print "Getting patient details"
	params = (request.GET.get("fname"), request.GET.get("lname"), request.GET.get("dob"))
	patient = helper.getPatientDetails(*params)
	return HttpResponse(json.dumps({"patient":patient}), 200)

@login_required(login_url="/")
def sendEmail(request):
	print "In send email"
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
	auth_logout(request=request)
	return redirect("/")