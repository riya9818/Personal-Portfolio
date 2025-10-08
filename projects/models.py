from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    technologies = models.CharField(max_length=300, help_text="Comma-separated list")
    demo_link = models.URLField(blank=True, null=True)
    source_link = models.URLField(blank=True, null=True)
    featured_image = models.ImageField(upload_to='projects/', blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='projects/')
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.project.title} Image"
