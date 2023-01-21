from django.shortcuts import render

# Handles the /ecommerce request
def index(request):

    return render(request, "ecommerce/index.html")
