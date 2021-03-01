from django.urls import path
from . import views


urlpatterns = [
   path("",views.home,name="home"),
   path("contact",views.contact,name="contact"),
   path("about",views.about,name="about"),
   path("login",views.hlogin,name="login"),
   path("logout",views.hlogout,name="logout"),
   path("register",views.register,name="register"),
   path("service",views.service,name="service"),
   path("appointement",views.appointement,name="appointement"),
   path("search",views.searchappointement,name="search"),
   path("billgeneration",views.billgeneration,name="billgeneration"),
   path("viewbill/<int:bid>/",views.viewbill,name="viewbill"),
   path("bills",views.bill,name="bill"),
   path("contactview",views.viewcontact,name="contactview"),
   path("serviceabout",views.serviceabout,name="serviceabout"),
]