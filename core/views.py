# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from django.conf import settings
from .forms import ContactForm
from .models import Testimonial, BlogPost
from projects.models import Project
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

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

            subject = f"New contact message from {contact.name}"
            body = (
                f"You have a new contact message:\n\n"
                f"Name: {contact.name}\n"
                f"Email: {contact.email}\n\n"
                f"Message:\n{contact.message}"
            )

            try:
                send_mail(
                    subject,
                    body,
                    settings.DEFAULT_FROM_EMAIL,  # from .env
                    [settings.EMAIL_HOST_USER],   # send to your inbox
                    fail_silently=False,
                )
                messages.success(request, "✅ Thanks! Your message has been sent successfully.")
            except BadHeaderError:
                messages.error(request, "⚠️ Invalid header detected.")
            except Exception as e:
                messages.error(request, f"⚠️ Error sending email: {e}")

            return redirect('contact')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ContactForm()

    return render(request, 'core/contact.html', {'form': form})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()

            subject = f"New contact message from {contact.name}"

            # Context for templates
            context = {
                'name': contact.name,
                'email': contact.email,
                'message': contact.message,
            }

            # Render both text and HTML
            text_body = render_to_string('emails/contact_notification.html', context)
            html_body = render_to_string('emails/contact_notification.html', context)

            try:
                # Send to site owner
                msg = EmailMultiAlternatives(
                    subject,
                    text_body,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.EMAIL_HOST_USER],
                )
                msg.attach_alternative(html_body, "text/html")
                msg.send()

                # Send confirmation to sender
                confirm_subject = "Thanks for contacting me!"
                confirm_text = render_to_string('emails/contact_confirmation.html', context)
                confirm_html = render_to_string('emails/contact_confirmation.html', context)

                confirmation = EmailMultiAlternatives(
                    confirm_subject,
                    confirm_text,
                    settings.DEFAULT_FROM_EMAIL,
                    [contact.email],
                )
                confirmation.attach_alternative(confirm_html, "text/html")
                confirmation.send()

                messages.success(request, "✅ Message sent! Check your email for confirmation.")
            except Exception as e:
                messages.error(request, f"⚠️ Email failed: {e}")

            return redirect('contact')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ContactForm()

    return render(request, 'core/contact.html', {'form': form})