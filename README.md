## Requirements 
- [x] Django , Heroku , Python , HTML CSS
- [X] DB = SQLITE
- [X] A book is unique based on the google id(volume id obtained using the google API) used in the table BOOKS .
- [X] On adding same book again increase the Quantity 
	 


# Event Browse

Users can 
- View events
- Book ticket for an event
- View Ticket
- View all registered events

Admin can 
- Create event 
- List events  
- Update events
- View Summary of an event


## Running locally

To install:

* clone this repo
* in your terminal, run:
  
``` 
> brew install python3 #if you don't already have python3
> python3 -m pip install -r requirements.txt
```

To run locally:

``` 
> python3 manage.py runserver
```


## Features Added 
- [x] Home page ; shows list of events to book . 
	For ADMIN shows all events also .
	For User only listed events.
	GET : http://127.0.0.1:8000/
```
	path('admin/', admin.site.urls),
    path('home/',views.home,name='home'),
    path('',views.index,name='index'), # shows all the events for a user (to book tickets) , and update , delete option only for superuser
    path('update/<int:id>',views.update,name='update'), # UPDATE an event
    path('delete/<int:id>',views.delete,name='delete'), # delete an event
    
    path('registeredEvents/',views.registeredEvents,name='registeredEvents') , # Registered Tickets 
    path('bookticket/<int:id>',views.book_ticket,name='bookticket'), # book  a ticket
    path('unbookticket/<int:id>',views.unbook_ticket,name='unbookticket'), # book  a ticket

    path('createuser/',views.create_user,name='createuser'),#for internal use
    path('listevents/',views.listevents,name='listevents'),# for internal use
    
    path("register/", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout"),
```
		


## Features I'd like to add

- [ ] Search by event name
- [ ] Search by event desc
- [ ] Search events based on booking window open
- [ ] Filter / sort functionality



