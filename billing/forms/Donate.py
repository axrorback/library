from django import forms

class DonateForm(forms.Form):
    amount = forms.IntegerField(min_value=1000, max_value=50_000_000)
