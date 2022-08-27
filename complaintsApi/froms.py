from django import forms
from . import models as mdl


class ComplaintCreationForm(forms.ModelForm):
    class Meta:
        model = mdl.Complaint
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 'required': True, 'placeholder': 'Enter Complaint Title...',
                'autofocus': True,
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 'placeholder': 'Enter the description of your complaint ...',
                'required': True, 'rows': 3,
            })
        }


class ForwardComplainForm(forms.ModelForm):
    '''
    @ select the user to forwar to
    @ add any text for the next description
    '''

    class Meta:
        TITLE = (('', '...'), ('dean', 'DEAN'), ('registry',
                 'REGISTRY'), ('itSupport', 'IT SUPPORT'))
        model = mdl.Complaint
        fields = ('forward_to', 'user_repond_text')
        widgets = {
            'forward_to': forms.Select(attrs={
                'class': 'form-control', 'required': True,
            }, choices=TITLE),
            'user_repond_text': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 2, 'required': False,
            }),
        }
