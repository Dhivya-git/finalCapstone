from django.shortcuts import render

# Handles the request for root url
def index(request):

    return render(request, "index.html")