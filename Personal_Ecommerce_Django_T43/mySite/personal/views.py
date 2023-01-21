from django.shortcuts import render

# Handles the /personal and /personal/about-me request
def about_me(request):

    return render(request, "personal/about-me.html")

# Handles the /personal/skills-certifications request
def skills(request):

    return render(request, "personal/skills-certifications.html")

# Handles the /personal/education request
def education(request):

    return render(request, "personal/education.html")

# Handles the /personal/work-experience request
def work(request):

    return render(request, "personal/work-experience.html")

# Handles the /personal/projects request
def projects(request):

    return render(request, "personal/projects.html")

# Handles the /personal/contact-me request
def contact(request):

    return render(request, "personal/contact-me.html")