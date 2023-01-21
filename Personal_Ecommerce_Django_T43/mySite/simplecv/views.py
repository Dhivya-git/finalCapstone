from django.shortcuts import render

# Handles the /simplecv request
def index(request):

    return render(request, "simplecv/index.html")
