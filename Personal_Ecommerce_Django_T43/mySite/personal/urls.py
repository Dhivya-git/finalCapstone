from django.urls import path
from . import views

# Handles all the requests under personal app
urlpatterns = [
    path('', views.about_me),
    path('about-me', views.about_me),
    path('skills-certifications', views.skills),
    path('education', views.education),
    path('work-experience', views.work),
    path('projects', views.projects),
    path('contact-me', views.contact),
]
