from django import forms
from django.utils.translation import gettext_lazy as _

class SearchForm(forms.Form):
	search = forms.CharField(widget = forms.TextInput(attrs={'class':'form-control mr-sm-2'}), required=False, label='')

class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')  
        super(BaseForm, self).__init__(*args, **kwargs)

class BaseModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(BaseModelForm, self).__init__(*args, **kwargs)

class NumberForm(BaseForm):
	amount = forms.IntegerField(label='Amount', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': _('Amount')}))
