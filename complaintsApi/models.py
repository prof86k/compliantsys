from django.db import models
from datetime import datetime
from accounts import models as acmdl

# Create your models here.

class Complaint(models.Model):
    complainer = models.ForeignKey(acmdl.User,on_delete=models.PROTECT,related_name='user_complaints')
    title = models.CharField(verbose_name='Title:',max_length=255,null=True,blank=False)
    description = models.TextField(verbose_name='Description:',null=True,blank=False)
    hod_forward = models.BooleanField(verbose_name='Forward:',default=False)
    hod_solve = models.BooleanField(verbose_name='Solve:',default=False)
    dean_forward = models.BooleanField(verbose_name='Forward:',default=False)
    dean_solve = models.BooleanField(verbose_name='solve:',default=False)
    registry_forward = models.BooleanField(verbose_name='Forward:',default=False)
    registry_solve = models.BooleanField(verbose_name='Solve:',default=False)
    support_repond = models.BooleanField(verbose_name='Respond:',default=False)
    user_repond_text = models.TextField(verbose_name='Respond Text:',null=True,blank=True)
    resolved_complaint = models.BooleanField(verbose_name='resolved:',default=False)
    forword_to = models.ForeignKey(acmdl.User,on_delete=models.PROTECT,related_name='forward_to_users',null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.title}'

    @classmethod
    def current_model_count(cls):
        '''return the number of complaints made today by all users'''
        return len([complaint.date_updated.date==datetime.today() for complaint in cls.objects.filter(resolved_complaint=False).all()])

    @classmethod
    def current_complaints(cls):
        '''return all the current complaints'''
        return [complaint.date_update.date==datetime.today() for complaint in cls.objects.filter(resolved_complaint=False).all()]

    @classmethod
    def user_current_model_count(cls,user):
        '''return the number of complaints made by a particular user'''
        return len([complaint.date_updated.date==datetime.today() for complaint in cls.objects.filter(complainer=user).all()])