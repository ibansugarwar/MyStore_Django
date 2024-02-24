
from django.shortcuts import render

def CompanyView(request):
    return render(request, 'pages/company.html')