from django import forms
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm
from . import models as mdl

class CreateUserAdminForm(UserCreationForm):
    
    class Meta(UserCreationForm.Meta):
        model = mdl.User
        fields = ['username','password1','password2']
        widgets = {
            'username':forms.TextInput(attrs={
                'class':'form-control','placeholder':'Enter your username...','autofocus':True,
                'blank':False,
            }),
            'password1':forms.PasswordInput(attrs={
                'class':'form-control','placeholder':'Enter your password...','blank':False,
            }),
            'password2':forms.PasswordInput(attrs={
                'class':'form-control','placeholder':'Confirm password....','blank':False,
            })
        }

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.username = self.cleaned_data.get('username')
        user.password1 = self.cleaned_data.get('password1')
        user.password2 = self.cleaned_data.get('password2')
        user.is_administrator = True
        user.save()

        administrator = mdl.Itsupport.objects.create(user=user)
        return user

class CreateNewUserForm(forms.ModelForm):
    # programme = forms.CharField('Programme',max_length=255,)
    dean = forms.BooleanField(label='Dean:',required=False,widget=forms.CheckboxInput(attrs={
        'class':'form-check-input'
    }))
    student = forms.BooleanField(label='Student:',required=False,widget=forms.CheckboxInput(attrs={
    'class':'form-check-input'
    }))
    hod = forms.BooleanField(label='HOD:',required=False,widget=forms.CheckboxInput(attrs={
        'class':'form-check-input'
    }))
    registry = forms.BooleanField(label='Registry:',required=False,widget=forms.CheckboxInput(attrs={
        'class':'form-check-input'
    }))
    it_support = forms.BooleanField(label='IT Support:',required=False,widget=forms.CheckboxInput(attrs={
        'class':'form-check-input'
    }))
    username = forms.CharField(label="Username:",widget=forms.TextInput(attrs={
    'class':'form-control','autofocus':True,'placeholder':'Enter the student ID/ Staff ID....'
    }))

    class Meta:
        model = mdl.User
        fields = ['email','profile_picture','phone']
        widgets = {
            'email':forms.EmailInput(attrs={
                'class':'form-control','placeholder':'Enter email','blank':False,
            }),
            'profile_picture':forms.ClearableFileInput(attrs={
                'class':'form-control','required':False,
            }),
            'phone':forms.TextInput(attrs={
                'class':'form-control','placeholder':'Enter Phone Number...','type':'tel'
            })
        }

class FacultyForm(forms.ModelForm):
    class Meta:
        model = mdl.Faculty
        fields = ['title','code']
        widgets = {
            'title':forms.TextInput(attrs={
                'class':'form-control','required':True,
                'placeholder':'Enter faculty title ...','autofocus':True,
            }),
            'code':forms.TextInput(attrs={
                'class':'form-control','required':True,'placeholder':'Enter faculty code...'
            })
        }

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = mdl.Department
        fields = ['title','faculty']
        widgets = {
            'title':forms.TextInput(attrs={
                'class':'form-control','required':True,'placeholder':'Enter department title...',
                'autofocus':True,
            }),
            'faculty':forms.Select(attrs={
                'class':'form-control','required':True
            })
        }

class ProgrammeForm(forms.ModelForm):
    class Meta:
        model = mdl.Programme
        fields = ['title','department']
        widgets = {
            'title':forms.TextInput(attrs={
                'class':'form-control','required':True,'placeholder':'Enter programme Name...',
                'autofocus':True,
            }),
            'department':forms.Select(attrs={
                'class':'form-control','required':True
            })
        }

class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username/Student Id/Staff ID:',required=True,widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'Username/Student Id/Staff ID:'
    }))
    password = forms.CharField(label='Password:',required=True,widget=forms.PasswordInput(attrs={
        'class':'form-control','placeholder':'Password...'
    }))

class UserProfileForm(forms.ModelForm):
    programme = forms.ChoiceField(label="Programme:",required=False,widget=forms.Select(attrs={
        'class':'form-control'
    }),choices=[(programme,programme.title) for index,programme in enumerate(mdl.Programme.objects.all())])
    
    department = forms.ChoiceField(label='Department:',required=False,widget=forms.Select(attrs={
        'class':'form-control'
    }),choices=[(department,department.title) for index,department in enumerate(mdl.Department.objects.all())])
    
    faculty = forms.ChoiceField(label='Faculty:',required=False,widget=forms.Select(attrs={
        'class':'form-control',
    }),choices=[(faculty,faculty) for index, faculty in enumerate(mdl.Faculty.objects.all())])
    
    class Meta:
        model = mdl.User
        fields = [
            'full_name','email','gender','profile_picture','phone',
            'is_dean','is_student','is_hod','is_registry','is_it_support'
        ]
        GENDER = (('',  '...'),('male','Male'),('female','Female'))
        widgets = {
            'full_name':forms.TextInput(attrs={
            'class':'form-control','placeholder':'Enter fullname ...',
            'required':False,'autofocus':True,
            }),
            'email':forms.EmailInput(attrs={
                'class':'form-control','required':True,
                'placeholder':'Enter email...','autofocus':True,
            }),
            'gender':forms.Select(attrs={
                'class':'form-control', 'required':True,
            },choices=GENDER),
            'profile_picture':forms.ClearableFileInput(attrs={
                'class':'form-control','required':False
            }),
            'phone':forms.TextInput(attrs={
                'class':'form-control','placeholder':'Enter Phone Number...','type':'tel'            
                
            }),
            'is_dean':forms.CheckboxInput(attrs={
            'class':'form-check-input'
            }),
            'is_student':forms.CheckboxInput(attrs={
            'class':'form-check-input'
            }),
            'is_hod':forms.CheckboxInput(attrs={
                'class':'form-check-input'
            }),
            'is_registry':forms.CheckboxInput(attrs={
                'class':'form-check-input'
            }),
            'is_it_support':forms.CheckboxInput(attrs={
                'class':'form-check-input'
            }),
        }
