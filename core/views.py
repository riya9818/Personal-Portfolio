from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .forms import ContactForm
from django.shortcuts import render, get_object_or_404
from .models import Testimonial, BlogPost
from projects.models import Project

def home(request):
    projects = Project.objects.all()[:3]  # latest 3 projects
    testimonials = Testimonial.objects.all()[:3]
    return render(request, 'core/home.html', {'projects': projects, 'testimonials': testimonials})



def about(request):
    return render(request, 'core/about.html')


def testimonials_view(request):
    testimonials = Testimonial.objects.all()
    return render(request, 'core/testimonials.html', {'testimonials': testimonials})

def blog_list(request):
    posts = BlogPost.objects.all()
    return render(request, 'core/blog_list.html', {'posts': posts})

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    return render(request, 'core/blog_detail.html', {'post': post})

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
