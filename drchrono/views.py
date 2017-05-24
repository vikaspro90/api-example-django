from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponse
from models import SessionWithDate, Session
import json, requests
import helper

# Create your views here.

# Main page for authenticated users
@login_required(login_url="/")
def main(request):
	username = request.user.get_username()
	social = request.user.social_auth.get(provider="drchrono")
	token = social.extra_data['access_token']
	uid = social.uid
	# print social.uid
	docName = helper.getCurrUserDocName(token, uid)
	request.user.first_name = docName[0]
	request.user.last_name = docName[1]
	data = social.uid
	# return render_to_response("main.html", {"name": docName})
	return render_to_response("main.html", {"docName": " ".join(docName), "data": data})

@login_required(login_url="/")
def updateClientDate(request):
	print "In update client Date."
	# Associating the client date with the current session
	SessionWithDate.objects.create(sess=Session.objects.filter(session_key=request.session.session_key)[0], date=json.loads(request.body)["clientDate"])
	return HttpResponse(200)

@login_required(login_url="/")
def updatePatientList(request):
	print "In updatePatientList."
	clientDate = SessionWithDate.objects.filter(sess=request.session.session_key)[0].date
	social = request.user.social_auth.get(provider="drchrono")
	token = social.extra_data['access_token']
	patients = helper.getPatientsWithDOBToday(token, clientDate)
	return HttpResponse(json.dumps({"patients": patients}), 200)

@login_required(login_url="/")
def sendEmail(request):
	print "In send email"
	toList = json.loads(request.body)["toList"]
	message = json.loads(request.body)["message"]
	helper.sendBirthdayEmail(toList, message)
	return HttpResponse(200)

def logout(request):
	auth_logout(request=request)
	return redirect("/")