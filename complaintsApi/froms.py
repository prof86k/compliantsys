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
        model = mdl.Complaint
        fields = ('forward_to_dean', 'forward_to_registry',
                  'forward_to_it', 'user_repond_text')
        labels = [
            {'forward_to_dean': "To Dean:"}, {
                'forward_to_registry': 'To Registry:'},
            {'forward_to_it': 'To IT Support:'}, {
                'user_reponse_text': 'Response Text:'}
        ]
        widgets = {
            'forward_to_dean': forms.Select(attrs={
                'class': 'form-control'
            }),
            'forward_to_registry': forms.Select(attrs={
                'class': 'form-control'
            }),
            'forward_to_it': forms.Select(attrs={
                'class': 'form-control'
            }),
            'user_repond_text': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 2
            })
        }
