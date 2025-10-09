from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .forms import ContactForm

def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            
            # Send email notification
            send_mail(
                subject=f"New contact message from {contact.name}",
                message=contact.message,
                from_email=contact.email,
                recipient_list=['riyabasnet0924@gmail.com'],  # Replace with your email or use env var
                fail_silently=True,
            )
            
            messages.success(request, "Thanks! Your message has been sent.")
            return redirect('contact')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ContactForm()
    return render(request, 'core/contact.html', {'form': form})
