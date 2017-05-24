from django.conf.urls import include, url
from django.views.generic import TemplateView

import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^main/', views.main, name='main'),
    url(r'^handShake/', views.handShake, name='handShake'),
    url(r'^updatePatientList/', views.updatePatientList, name='updatePatientList'),
    url(r'^getPatientDetails/', views.getPatientDetails, name='getPatientDetails'),
    url(r'^sendEmail/', views.sendEmail, name='sendEmail'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
]