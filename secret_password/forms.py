# secret/forms.py
from django import forms

class SecretForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea, label="Isi Rahasia, silahkan masukkan teks")
