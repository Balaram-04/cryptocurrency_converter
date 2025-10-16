
from django import forms

class ConvertForm(forms.Form):
    from_currency = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder':'bitcoin'}))
    to_currency = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder':'usd'}))
    amount = forms.FloatField(min_value=0.0, initial=1.0)
