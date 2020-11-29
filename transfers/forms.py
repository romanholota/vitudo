from django import forms
from vitudo.forms import BaseForm

class TransferForm(BaseForm):
	end = forms.DateField(input_formats=['%Y-%m-%d'], widget = forms.DateInput(attrs={'class':'form-control', 'placeholder':'Dátum vrátenia', 'type':'date'}), required=True, label='End date')
	comment = forms.CharField(widget = forms.Textarea(attrs={'class':'form-control', 'placeholder':'Poznámka'}), required=False, label='Comment')
