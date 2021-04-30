from django import forms

class AddressForm(forms.Form):
    county = forms.CharField()
    location = forms.CharField()
    phone_number = forms.CharField()
    save_info = forms.BooleanField(required=False)                
    use_default = forms.BooleanField(required=False)