
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse

#convert to json type 
from django.core import serializers
import json

#see listed events
from django.db.models import F


#register
from django.contrib.auth import login
from django.contrib import messages
from .forms import NewUserForm

#set permisso=ion for registered users
from django.contrib.auth.models import Group, Permission



#login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate

#logout
from django.contrib.auth import logout

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import ListEvents , Event , Ticket
# Create your views here.
@csrf_exempt
def create_user(request):
    if request.method == 'POST':

        #print(request.POST.get('name'))
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        ''' phone = request.POST['phone']
        if len(phone)<10 or len(phone)>10:
            raise ValidationError("Phone number length is not right")
        query = request.POST['query']
        '''
        #print(name ,  email ,  password  )
        
        u = User.objects.filter(username = name ).first() 
        if u is None :
            user = User.objects.create_user(username=name,
                                 email=email,
                                 password=password , is_staff=True)
        else:
            return HttpResponse(' user already there ')

    return HttpResponse('created a user')

def index(request):
    if  request.user.is_authenticated :
       
        
        if request.method == "POST":
            event_name = request.POST.get('Event_name')
            desc = request.POST.get('desc')
            max_seats = request.POST.get('max_seats')
            
            try: 
                event_ob = Event(event_name=event_name, desc=desc,max_seats =max_seats )
                event_ob.save()
                messages.success(request,"Your details are saved")
            except:    
                messages.error(request,"Event not created some issue .")
            
        
        
        all_events = ListEvents.objects.all().values('event__id','event__event_name','event__desc','seats_avaialble','booking_start','booking_end','price_per_seat', 'event__status','event__max_seats').annotate(id=F('event__id') ,name=F('event__event_name'), desc = F('event__desc') , status = F('event__status') ,max_seats = F('event__max_seats'))
        messages.success(request,"Your index page events list")
        #print(all_events)
        if request.user.is_superuser and request.user.is_authenticated :
            all_events2 = Event.objects.all().values('id','event_name','desc', 'status','max_seats').annotate(name=F('event_name') )
            #print(all_events2)
            res = list(all_events) 
            #print(res)
            res.extend(list(all_events2))
            resu = []
            s = set()
            for ev in res:
                if ev['id'] not in s:
                    resu.append(ev)
                    s.add(ev['id'])    
            return render(request,'index.html',{'all_events':resu  })
            
        return render(request,'index.html',{'all_events':list(all_events)})
    else:
        return redirect("eventrr:home")

def delete(request,id):
    #html doesn't allow DEPETE method only POst and get is allowed 
    if True:
        Event.objects.filter(id=id).delete()
        messages.success(request, "Delete successful." )
        return redirect("/")
    else:
        return HttpResponse("Unable to delete ")

def update(request,id):
    #html doesn't allow DEPETE method only POst and get is allowed 
    if request.method == 'POST':
        name = request.POST.get('name')
        max_seats = request.POST.get('max_seats')
        desc = request.POST.get('desc')
        # if desc is None:
        #     desc = ''

        event  = Event.objects.get(id=id) 
        event.name = name
        event.desc = desc
        event.max_seats = max_seats
       
        event.save()
        messages.success(request, "Update successful." )
        return redirect("/")
    event  = Event.objects.get(id=id) 
    #print(book_ob,book_ob.name , book_ob.price)
    return render(request,'update.html',{'event':event})

from datetime import datetime, timedelta

#book ticket
def book_ticket(request,id):
    if request.user.is_authenticated :
        

        

        try: 
            le = ListEvents.objects.filter(event__id=id).first()
            #print(le,le.booking_start)


            now = le.booking_start + timedelta(minutes=1)
            
            start_time = le.booking_start 
            end_time = le.booking_end  
            #print(now)
            
            seats_avaialble = int( le.seats_avaialble)    
            if seats_avaialble > 0  and ( start_time <= now <= end_time) :
                
                if Ticket.objects.filter(user = request.user , ListEvents  = le  ).first() :
                    messages.error(request,"ticket was already there ")
                else:
                    seats_avaialble -=1
                    le.seats_avaialble = seats_avaialble
                    le.save()
                    price_per_seat = le.price_per_seat
                    ticket_ob = Ticket( ListEvents = le  , user = request.user , seats_booked=1 , total_price = price_per_seat  )
                    ticket_ob.save()
                    messages.success(request,"ticket created and saved")
            
            else:
                messages.error(request,"ticket not created some issue like seats already full or time NOW is OUT of BOOKING WINDOW.")   
        except:    
            messages.error(request,"ticket not created some other issue.")
        return redirect("eventrr:index")

    else:
        return redirect("eventrr:home")

#UN-book ticket
def unbook_ticket(request,id):
    if  request.user.is_authenticated :
            
        try: 
            te = Ticket.objects.get(ticket_id=id)
            le = ListEvents.objects.get(id = te.ListEvents.id)
           
            le.seats_avaialble +=1
            le.save()
            te.delete() 
            messages.success(request,"ticket deletd and Events updated ")
        
        except:    
            messages.error(request,"ticket not deletd some other issue.")
        return redirect("eventrr:index")

    else:
        return redirect("eventrr:home")

#('ticket_id', 'user', 'ListEvents', 'seats_booked', 'total_price', )

def registeredEvents(request):
    te = Ticket.objects.filter( user = request.user  ).values('ticket_id', 'user', 'ListEvents__event__event_name', 'seats_booked', 'total_price').annotate(event_name = F('ListEvents__event__event_name'))
    print(te)
    
    return render(request , "get_ticket.html",{'all_tickets' : te} )


def home(request):
    #messages.success(request, "RSTful. in home" )
    return render(request , template_name="base.html")


def register_request(request):
    #print(Permission.objects.all())
    #print(permission.codename)
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            try:
                permission = Permission.objects.get(codename='view_listevents')
                user.user_permissions.add(permission)

                mygroup = Group.objects.get( name = "rin")
                #mygroup.user_set.add(user)
                request.user.groups.add(mygroup)
                messages.success(request, "Registration successful.  and basic permissions set for the user" )
            except:
                messages.success(request, "Unable to set permissions  for the user" )

            
            return redirect("eventrr:index")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request=request, template_name="register.html", context={"register_form":form})




def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST) # fill the form by sending request
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("eventrr:index")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm() # to create an empty form and send ths as a context
	return render(request=request, template_name="login.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("eventrr:index")


def listevents(request):
    #print(Event.objects.all())
    #print(ListEvents.objects.all())
  
    #print(request.user.is_authenticated,request.user.username,request.user.is_staff , request.user.is_superuser) 
    if  request.user.is_authenticated and (request.user.is_staff or  request.user.is_superuser ) :
        
        SomeModel_json = serializers.serialize("json", Event.objects.all())
        
        listeventsJSON = serializers.serialize("json", ListEvents.objects.all())
        
        cf = json.loads(listeventsJSON)
        #print(cf,len(cf))
        for i in cf:
            #print( i)
            #pass
            ev_id = i["fields"]["event"] 
            event = serializers.serialize("json",Event.objects.filter(id = ev_id) ) 
            #print(event)
            i["fields"]["event"] =   json.loads(event)
        #results=ListEvents.objects.all().values('event__event_name','event__desc', 'event__status','event__max_seats').annotate(name=F('event__event_name'), desc = F('event__desc') , status = F('event__status') ,max_seats = F('event__max_seats'))
        #results=ListEvents.objects.all().values(id3 ='id',name = 'event__event_name',desc = 'event__desc',status = 'event__status', max_seats = 'event__max_seats')
        #print(list(results ))

        return HttpResponse(str(cf),content_type ="application/json")
        #return HttpResponse(str(list(results)),content_type ="application/json")
    else:
        return HttpResponse("No user logged in , log in first")    
    