from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import ContactForm

# Create your views here.


@login_required
def contact_page(request):
    contact_form = ContactForm()
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            messages.success(
                request, 'Thank you for contacting us. We will reach out to you soon.')
    return render(request, 'contact.html', {
        'contact_form': contact_form,
    })
