"""
Definition of views.
"""

from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest
from django.http.response import HttpResponseRedirect
from datetime import datetime
from app.forms import EventForm
from app.models import Event, Confirmation
from django.contrib import messages
from django.db.models import Count
from django.contrib.sessions.models import Session

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    _create_session(request)
    events = Event.objects.all().annotate(num_conf=Count('confirmation')).order_by('-added_at')
    user_confirmations = list(map(lambda c: c.event_id, Confirmation.objects.filter(session_key=request.session.session_key)))
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
            'events':events,
            'confirmations':user_confirmations,
        }
    )

def events(request, tag):
    """Renders the events page."""
    assert isinstance(request, HttpRequest)
    events = Event.objects.filter(tags__name__in=[tag]).annotate(num_conf=Count('confirmation')).order_by('-added_at')
    user_confirmations = list(map(lambda c: c.event_id, Confirmation.objects.filter(session_key=request.session.session_key)))
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
            'events':events,
            'confirmations':user_confirmations,
        }
    )

def confirm(request, event_id):
    """Renders the events page."""
    assert isinstance(request, HttpRequest)
    c = Confirmation(session_key=Session.objects.get(session_key=request.session.session_key), event_id=event_id)
    c.save()
    messages.success(request, 'Event has been confirmed.')
    return HttpResponseRedirect('/')

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def add_event(request):
    """Renders the page to add event"""
    assert isinstance(request, HttpRequest)
    _create_session(request)
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.cleaned_data['session_key'] = Session.objects.get(session_key=request.session.session_key)
            form.save()
            messages.success(request, 'Event has been added.')
            return HttpResponseRedirect('/')
        elif any(coordinate in form.errors for coordinate in ['latitude', 'longitude']):
            messages.error(request, 'The Geolocation service is required.')
    return render(
        request,
        'app/add_event.html',
        {
            'form': form
        }
    )

def view_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    tags = event.tags.all()

    return render(
        request,
        'app/view_event.html',
        {
            'r': event,
            'tags': tags,
        }
    )

def _create_session(request):
    if not request.session.session_key:
        request.session.create()
