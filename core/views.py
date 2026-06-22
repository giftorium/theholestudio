from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Production, ContactMessage, Founder
from .forms import ContactForm


def home(request):
    featured = Production.objects.filter(status='upcoming').first() or Production.objects.first()
    upcoming = Production.objects.filter(status='upcoming')[:3]
    return render(request, 'core/home.html', {'featured': featured, 'upcoming': upcoming})


def productions(request):
    upcoming = Production.objects.filter(status='upcoming')
    archive = Production.objects.filter(status='past')
    return render(request, 'core/productions.html', {'upcoming': upcoming, 'archive': archive})


def production_detail(request, slug):
    production = get_object_or_404(Production, slug=slug)
    return render(request, 'core/production_detail.html', {'production': production})


def about(request):
    founders = Founder.objects.all()
    return render(request, 'core/about.html', {'founders': founders})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message'],
            )
            messages.success(request, 'Your message has been sent.')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'core/contact.html', {'form': form})
