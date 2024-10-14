from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for contacting us! We will get back to you shortly.')
            return redirect('message_view')  # Redirect to the updated message view
    else:
        form = ContactForm()

    return render(request, 'contact/contact.html', {'form': form})


def message_view(request):
    return render(request, 'contact/message_sent.html')  # Make sure to create this template
