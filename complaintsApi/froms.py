from django import forms
from . import models as mdl

class ComplaintCreationForm(forms.ModelForm):
    class Meta:
        model = mdl.Complaint
        fields = ['title','description']
        widgets = {
            'title':forms.TextInput(attrs={
                'class':'form-control','required':True,'placeholder':'Enter Complaint Title...',
                'autofocus':True,
            }),
            'description':forms.Textarea(attrs={
                'class':'form-control','placeholder':'Enter the description of your complaint ...',
                'required':True,'rows':3,
            })
        }