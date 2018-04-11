from django import forms


class CreateDeviceForm(forms.Form):
    name = forms.CharField()
