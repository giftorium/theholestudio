from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Event, ContactMessage
from .forms import ContactForm


def home(request):
    event = Event.objects.first()
    return render(request, 'core/home.html', {'event': event})


def feedback(request):
    event = Event.objects.prefetch_related('photos', 'videos', 'artists').first()
    return render(request, 'core/feedback.html', {'event': event})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message'],
            )
            messages.success(request, 'Your message has been sent.')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'core/contact.html', {'form': form})
