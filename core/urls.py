from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.home, name='home'),
    path('about/', core_views.about, name='about'),
    path('contact/', core_views.contact, name='contact'),
    path('testimonials/', core_views.testimonials_view, name='testimonials'),
    path('blog/', core_views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', core_views.blog_detail, name='blog_detail'),
    path('projects/', include('projects.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
