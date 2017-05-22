from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
import helper

# Create your views here.
# Main page for authenticated users
@login_required(login_url="/")
def main(request):
	name = request.user.get_username()
	social = request.user.social_auth.get(provider="drchrono")
	token = social.extra_data['access_token']
	# bornToday = [p["first_name"]+" "+p["last_name"] for p in helper.getPatientsWithDOBToday(token)]
	heading = "Here are all your patients born on this day."
	bornToday = helper.getPatientsWithDOBToday(token)
	if len(bornToday)==0:
		heading = "None of your patients was born on this day."
	return render_to_response("main.html", {"username": name, "patients": bornToday, "heading": heading})

def logout(request):
	auth_logout(request=request)
	return redirect("/")