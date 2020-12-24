from django import forms
from django.utils.translation import gettext_lazy as _
from vitudo.forms import BaseForm

class TransferForm(BaseForm):
	end = forms.DateField(input_formats=['%Y-%m-%d'], widget = forms.DateInput(attrs={'class':'form-control', 'placeholder': _('End Date'), 'type':'date'}), required=True, label=_('End Date'))
	comment = forms.CharField(widget = forms.Textarea(attrs={'class':'form-control', 'placeholder':_('Comment')}), required=False, label=_('Comment'))
