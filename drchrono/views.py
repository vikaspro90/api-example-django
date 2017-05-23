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
	name = request.user.get_username()
	return render_to_response("main.html", {"username": name})

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