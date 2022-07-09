from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    is_administrator = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_hod = models.BooleanField(default=False)
    is_dean = models.BooleanField(default=False)
    is_registry = models.BooleanField(default=False)
    is_it_support = models.BooleanField(default=False)
    profile_picture = models.ImageField(verbose_name='Profile Picture:',upload_to='images/profile_pics/%Y/%M/%d',null=True)
    full_name = models.CharField(verbose_name='Full Name:',max_length=255, blank=True,null=True)
    gender = models.CharField(verbose_name='Gender:',max_length=255, blank=True,null=True)
    phone = models.CharField(verbose_name="Phone:",max_length=255, blank=True,null=True)

class Faculty(models.Model):
    title = models.CharField(verbose_name='Title:',max_length=255, blank=False,null=True)
    code = models.CharField(verbose_name='Code:',max_length=255, blank=False,null=True)
    user = models.ForeignKey(User,on_delete=models.PROTECT,related_name='faculty_users',null=True)
    class Meta:
        managed = True
        verbose_name = 'Faculty'
        verbose_name_plural = 'Faculties'

    def __str__(self):
        return self.title

class Department(models.Model):
    title = models.CharField(verbose_name='Title:',max_length=255, blank=False,null=True)
    faculty = models.ForeignKey(Faculty,on_delete=models.CASCADE,related_name='faculty_departments')
    user = models.ForeignKey(User,on_delete=models.PROTECT,related_name='department_users',null=True)

    class Meta:
        managed = True
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def __str__(self):
        return self.title

class Programme(models.Model):
    title = models.CharField(verbose_name='Title:',max_length=255, blank=False,null=True)
    department = models.ForeignKey(Department,on_delete=models.CASCADE,related_name='department_programmes')
    user = models.ForeignKey(User,on_delete=models.PROTECT,related_name='programme_users',null=True)

    class Meta:
        managed = True
        verbose_name = 'Programme'
        verbose_name_plural = 'Programmes'

    def __str__(self):
        return self.title
        
class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='student_users')
    programme = models.CharField(verbose_name='Programme:',max_length=255,null=True,blank=False)

    class Meta:
        managed = True
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self) -> str:
        return f'{self.user.username}'


class Hod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='hod_users')
    department = models.ForeignKey(Department,on_delete=models.PROTECT,related_name='department_hods')
    
    class Meta:
        managed = True
        verbose_name = 'HOD'
        verbose_name_plural = 'HODs'

    def __str__(self):
        return f'{self.user.username}'

class Dean(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='dean_users')
    faculty = models.ForeignKey(Faculty,on_delete=models.PROTECT,related_name='faculty_deans')
    
    class Meta:
        managed = True
        verbose_name = 'DEAN'
        verbose_name_plural = 'DEANs'

    def __str__(self):
        return f'{self.user.username}'


class Register(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='registry_users')

    class Meta:
        managed = True
        verbose_name = 'Registry'
        verbose_name_plural = 'Registrys'

    def __str__(self):
        return f'{self.user.username}'

class Itsupport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='it_support_users')

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'IT Support'
        verbose_name_plural = 'IT Supports'

    def __str__(self):
        return f'{self.user.username}'
