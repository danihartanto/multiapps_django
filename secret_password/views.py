# secret/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import OneTimeSecret
from .forms import SecretForm

from django.urls import reverse
from django.shortcuts import redirect

def create_secret(request):
    form = SecretForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        secret = OneTimeSecret.objects.create(
            message=form.cleaned_data['message']
        )
        return redirect('secret_created', secret_id=secret.secret_id)
    
    return render(request, 'secret_password/index.html', {'form': form})

def secret_created(request, secret_id):
    link = request.build_absolute_uri(reverse('view_secret', args=[secret_id]))
    return render(request, 'secret_password/created.html', {'link': link})

def expired_view(request):
    return render(request, 'secret_password/expired.html')

def view_secret(request, secret_id):
    secret = get_object_or_404(OneTimeSecret, secret_id=secret_id)
    if secret.viewed:
        return render(request, 'secret_password/already_viewed.html')
    message = secret.message
    secret.viewed = True
    secret.save()
    return render(request, 'secret_password/view.html', {'message': message})
