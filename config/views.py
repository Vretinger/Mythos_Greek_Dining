from django.shortcuts import render

def home(request):
    return render(request, 'home.html')


def menu(request):
    # Your logic here
    return render(request, 'menu.html')



def contact(request):
    # Your logic for the contact page here
    return render(request, 'contact.html')