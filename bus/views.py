from django.shortcuts import render , HttpResponse,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.conf import settings
from .models import Contact ,Appointement ,Billgeneration,Contact
from django.core import mail
from django.template.loader import render_to_string , get_template
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.core.paginator import Paginator
from xhtml2pdf import pisa
from io import BytesIO
from datetime import datetime
import time
# Create your views here.

import json

with open('./info.json', 'r') as myfile:
    data=myfile.read()

obj = json.loads(data)





def hlogin(request):

    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginuserpassword']

        user = authenticate(username=loginusername,password=loginpassword)

        if user is not None:
            login(request,user)
            messages.success(request," Sucessfully Logged In")
            return redirect('/')
        else:
            messages.error(request,"Invalid Credentials, Please try again")
            # return redirect('/')
    return render(request,'login.html')







def hlogout(request):
    # if request.method == 'POST':
    logout(request)
    
    return redirect("home")







def register(request):

    if request.method =='POST':
        username = request.POST.get('userid')
        fname = request.POST.get('username')
        lname = request.POST.get('userlastname')
        email = request.POST.get('useremail')
        password = request.POST.get('userpassword')
        cpassword = request.POST.get('usercpassword')

        if not username:
            messages.error(request," Username Required")
        elif len(username) < 4:
            messages.error(request," Username must be under characters")
        elif User.objects.filter(username=username).exists():
            messages.error(request," Already User exist. Try Another username")
        elif not fname:
            messages.error(request," First Name Required !!")
        elif len(fname) < 3 or len(fname) > 10:
            messages.error(request,' First Name must be 4 char long or more')
        elif not lname:
            messages.error(request,' Last Name Required..')
        elif len(lname) < 4 or len(lname) > 10:
            messages.error(request,' Last Name must be 4 char long or more')
        elif len(email) < 5 or len(email) < 16:
            messages.error(request,'Email must be 5 char long')
        elif User.objects.filter(email=email).exists():
            messages.error(request," Email Already exist. Try Another Email")
        elif not password:
            messages.error(request," Password Required")
        elif not cpassword:
            messages.error(request," Confirm Password Required")
        elif len(password) < 6 or len(password) > 20:
            messages.error(request,' Password must be 6 char long')
        elif password != cpassword:
            messages.error(request," Password do not match")
            
        else:
            
            myuser = User.objects.create_user(username,email,password)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()
            messages.success(request," Account has been sucessfully created")
            return redirect('login')

   


    return render(request,'signup.html')







def home(request):
    return render(request,'loaded/index.html')







def service(request):
    user = request.user
    if request.method =='POST' or user.is_authenticated :
        name = request.POST.get('cname')
        address = request.POST.get('caddress')
        pin_code = request.POST.get('cpin')
        phone = request.POST.get('cphone')
        email = request.POST.get('cemail')
        busno = request.POST.get('cbusno')
        issue = request.POST.get('cbusproblem')

        if not name:
            messages.error(request," Name Required")
        elif len(name) < 4:
            messages.error(request," Name must be under characters")
        elif not address:
            messages.error(request," address Required")
        elif len(address) < 15:
            messages.error(request," address must be under characters")
        elif not pin_code:
            messages.error(request," pin_code Required")
        elif len(pin_code) < 6:
            messages.error(request," pin_code must be under characters")
        elif not phone:
            messages.error(request," phone Required")
        elif len(phone) < 9:
            messages.error(request," phone must be under characters")
        elif not email:
            messages.error(request," email Required")
        elif len(email) < 9:
            messages.error(request," email must be under characters")
        elif not busno:
            messages.error(request," busno Required")
        elif len(busno) < 7:
            messages.error(request," busno must be under characters")
        elif not issue:
            messages.error(request," issue Required")
        elif len(issue) < 20:
            messages.error(request," issue must be under characters")

        else:
            appointement = Appointement(name=name,email=email,phone=phone,busno=busno,issue=issue,address=address,pin_code=pin_code,user=user)
            appointement.save()
            id = appointement.apt_id
            t = time.localtime(time.time() + 48*3600)
            day = t.tm_mday
            month = t.tm_mon
            year = t.tm_year
            messages.success(request," We will contact you within Hour ")

            subject, from_email, to = "Appointement from Daddy's Garage", obj['from_mail'], email

            html_content = render_to_string('mail_template.html', {'id':id,'user':user,'name':name,'day':day,'mon':month,'yr':year}) # render with dynamic value
            text_content = strip_tags(html_content) # Strip the html tag. So people can see the pure text at least.

            # create the email, and attach the HTML version as well.
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

    return render(request,'loaded/service.html')







def contact(request):

    if request.method == "POST" :
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('feedback', '')
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(desc)<5:
            messages.error(request,"please fill the form correctly")
        else:
            contact = Contact(name=name, email=email, phone=phone, desc=desc)
            contact.save()
            messages.success(request,"Message  sent Sucessfully")

            subject, from_email, to = f'Contact Message from {name}', obj['from_mail'], obj['from_mail']

            html_content = render_to_string('contactsend.html', {'phone':phone,'email':email,'name':name , 'desc':desc}) # render with dynamic value
            text_content = strip_tags(html_content) # Strip the html tag. So people can see the pure text at least.

            # create the email, and attach the HTML version as well.
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        


    return render(request,'loaded/Contact.html')


def about(request):
    return render(request,'loaded/about.html')



def appointement(request):
    user = request.user
    if user.is_staff :
        detials = Appointement.objects.all().order_by('mdate')
        paginator = Paginator(detials,10)
        page_number = request.GET.get('page')
        page_obj =paginator.get_page(page_number)
        context = {'detail': page_obj }
        return render(request,'appointement.html',context)
    else :
        return HttpResponse(404)


def searchappointement(request):
    query = request.GET['query']
    if len(query)>80:
        detail = Appointement.objects.none()
    else:
        detail = Appointement.objects.filter(Q(apt_id__icontains=query) | Q(user__icontains=query)
        | Q(name__icontains=query) | Q(email__icontains=query)
        )
        
        
    # if detail.count() == 0:
    params = {'detail':detail,'query':query}
    return render(request,'searchappointement.html',params)





def render_to_pdf(template_file,data={}):
    temp = get_template(template_file)
    html = temp.render(data)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type='application/pdf')
    return None

def viewbill(request,bid):
    user = request.user
    if user.is_staff :
       
        billgen = Billgeneration.objects.get(bil_id=bid)
        context = {'bil':billgen}
        pdf = render_to_pdf('viewbill.html',context)
        return HttpResponse(pdf,content_type='application/pdf')

    if user.is_authenticated :
       
        billgen = Billgeneration.objects.filter(user=user).get(bil_id=bid)
        context = {'bil':billgen}
        pdf = render_to_pdf('viewbill.html',context)
        return HttpResponse(pdf,content_type='application/pdf')
    elif user.is_anonymous :
        return HttpResponse(404)
    else :
        return HttpResponse(404)
            



def billgeneration(request):
    user = request.user
    if user.is_staff :
        if request.method =='POST':
            aptid = request.POST.get('baptid')
            email = request.POST.get('bemail')
            phone = request.POST.get('bphone')
            futurework = request.POST.get('futurework')
            userid = request.POST.get('userid')
            amount = request.POST.get('billamount')
            name = request.POST.get('bname')
            busno = request.POST.get('busno')
            wamount1 = request.POST.get('wamount1')
            workdone1 = request.POST.get('workdone1')
            wamount2 = request.POST.get('wamount2')
            workdone2 = request.POST.get('workdone2')
            wamount3 = request.POST.get('wamount3')
            workdone3 = request.POST.get('workdone3')
            wamount4 = request.POST.get('wamount4')
            workdone4 = request.POST.get('workdone4')
            wamount5 = request.POST.get('wamount5')
            workdone5 = request.POST.get('workdone5')
            wamount6 = request.POST.get('wamount6')
            workdone6 = request.POST.get('workdone6')
            wamount7 = request.POST.get('wamount7')
            workdone7 = request.POST.get('workdone7')
            wamount9 = request.POST.get('wamount9')
            workdone9 = request.POST.get('workdone9')
            wamount8 = request.POST.get('wamount8')
            workdone8 = request.POST.get('workdone8')
            wamount10 = request.POST.get('wamount10')
            workdone10 = request.POST.get('workdone10')
            wamount11 = request.POST.get('wamount11')
            workdone11 = request.POST.get('workdone11')
            wamount12 = request.POST.get('wamount12')
            workdone12 = request.POST.get('workdone12')
            wamount13 = request.POST.get('wamount13')
            workdone13 = request.POST.get('workdone13')
            wamount14 = request.POST.get('wamount14')
            workdone14 = request.POST.get('workdone14')
            wamount15 = request.POST.get('wamount15')
            workdone15 = request.POST.get('workdone15')

            if not aptid :
                messages(request," Appointement is Required ")
            elif not aptid.isnumeric() :
                messages.warning(request," Appointement id should be number ")
        
           
            elif len(futurework)<2 or len(email)<3 or len(phone)<10:
                messages.warning(request," Please fill the Form correctly ")
            elif len(workdone1)<4  or len(wamount1) <2 :
                 messages.warning(request," First 1 workdone column must be filled  ")
            elif not User.objects.filter(username=user).exists():
                messages.error(request," Already does not exist. Try Another username")
            else:
                
                a = int(wamount1) + int(wamount2) + int(wamount3)+ int(wamount4) + int(wamount5) + int(wamount6) + int(wamount7) +int( wamount8) + int(wamount9) + int(wamount10) + int(wamount11) + int(wamount12) + int(wamount13) + int(wamount14) + int(wamount15)

            

                billgeneration = Billgeneration(email=email,phone=phone,futurework=futurework,amount=a,user=userid,byuser=user,name=name,apt_id=aptid,busno=busno,workdone1=workdone1,wamount1=wamount1,workdone2=workdone2,wamount2=wamount2,workdone3=workdone3,wamount3=wamount3,workdone4=workdone4,wamount4=wamount4,workdone5=workdone5,wamount5=wamount5,workdone6=workdone6,wamount6=wamount6,workdone7=workdone7,wamount7=wamount7,workdone8=workdone8,wamount8=wamount8,workdone9=workdone9,wamount9=wamount9,workdone10=workdone10,wamount10=wamount10,workdone11=workdone11,wamount11=wamount11,workdone12=workdone12,wamount12=wamount12,workdone13=workdone13,wamount13=wamount13,workdone14=workdone14,wamount14=wamount14,workdone15=workdone15,wamount15=wamount15).save()




                

                subject, from_email, to = "Daddy's Garage Invoice " , obj['from_mail'], email

                html_content = render_to_string('billsend.html', {'email':email,'phone':phone,'futurework':futurework,'amount':a,'user':userid,'byuser':user,'name':name,'apt_id':aptid,'busno':busno,'workdone1':workdone1,'wamount1':wamount1,'workdone2':workdone2,'wamount2':wamount2,'workdone3':workdone3,'wamount3':wamount3,'workdone4':workdone4,'wamount4':wamount4,'workdone5':workdone5,'wamount5':wamount5,'workdone6':workdone6,'wamount6':wamount6,'workdone7':workdone7,'wamount7':wamount7,'workdone8':workdone8,'wamount8':wamount8,'workdone9':workdone9,'wamount9':wamount9,'workdone10':workdone10,'wamount10':wamount10,'workdone11':workdone11,'wamount11':wamount11,'workdone12':workdone12,'wamount12':wamount12,'workdone13':workdone13,'wamount13':wamount13,'workdone14':workdone14,'wamount14':wamount14,'workdone15':workdone15,'wamount15':wamount15,'date':datetime.now()}) # render with dynamic value
                text_content = strip_tags(html_content) # Strip the html tag. So people can see the pure text at least.

                # create the email, and attach the HTML version as well.
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()




               
                messages.success(request," Bill Generated Please Check BillBox ")
            
        
        
        return render(request,'billgeneration.html',{'range':range(1,16)})
    else :
        return HttpResponse(404)




                
            
        
           
        



def bill(request):
    user = request.user
    if  user.is_staff :
        bill = Billgeneration.objects.all().order_by('apt_id')
    elif user.is_anonymous :
        return HttpResponse(404)
    else :
       
        bill = Billgeneration.objects.all().filter(user=user).order_by('apt_id')
    
    # paginator = Paginator(bill,25)
    # page_number = request.GET.get('page')
    # page_obj =paginator.get_page(page_number)
    context = {'bill':bill,'id':id}
    return render(request,'bills.html',context)

def viewcontact(request):
    user = request.user
    if user.is_staff:
        con = Contact.objects.all()
        paginator = Paginator(con,10)
        page_number = request.GET.get('page')
        page_obj =paginator.get_page(page_number)
        return render(request,'contactview.html',{'con':page_obj})
    else :
        return HttpResponse(404)




def serviceabout(request):
    return render(request,'serviceabout.html')
