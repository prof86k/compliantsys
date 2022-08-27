from django.db import models
from datetime import datetime
from accounts import models as acmdl

# Create your models here.


class Complaint(models.Model):
    complainer = models.ForeignKey(
        acmdl.User, on_delete=models.PROTECT, related_name='user_complaints')
    title = models.CharField(verbose_name='Title:',
                             max_length=255, null=True, blank=False)
    description = models.TextField(
        verbose_name='Description:', null=True, blank=False)
    forward = models.BooleanField(verbose_name='Forward:', default=False)
    solve = models.BooleanField(verbose_name='Solve:', default=False)
    user_repond_text = models.TextField(
        verbose_name='Respond Text:', null=True, blank=True)
    forward_to = models.CharField(
        verbose_name="Forward To:", max_length=255, null=True, blank=True)
    forward_to_user = models.ForeignKey(
        acmdl.User, on_delete=models.PROTECT, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.title}'

    @classmethod
    def current_model_count(cls):
        '''return the number of complaints made today by all users'''
        return len([
            complaint
            for complaint in cls.objects.filter(solve=False).all()
            if complaint.date_updated.date() == datetime.today().date()
        ])

    @classmethod
    def current_complaints(cls):
        '''return all the current complaints'''
        return [
            complaint for complaint in cls.objects.filter(solve=False).all()
            if complaint.date_updated.date() == datetime.today().date()
        ]

    @classmethod
    def user_current_model_count(cls, user):
        '''return the number of complaints made by a particular user'''
        return len([
            complaint
            for complaint in cls.objects.filter(complainer=user).all()
            if complaint.date_updated.date() == datetime.today().date()
        ])
