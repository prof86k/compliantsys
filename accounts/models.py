from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    """
    @ all the users are registered 
    @ all users login and verify
    @ all users get assigned to their roles
    """
    is_administrator = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_hod = models.BooleanField(default=False)
    is_dean = models.BooleanField(default=False)
    is_registry = models.BooleanField(default=False)
    is_it_support = models.BooleanField(default=False)


class Faculty(models.Model):
    """
    @ the host deans
    """
    title = models.CharField(verbose_name='Title:',
                             max_length=255, blank=False, null=True)
    code = models.CharField(verbose_name='Code:',
                            max_length=255, blank=False, null=True)
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='faculty_users', null=True)

    class Meta:
        managed = True
        verbose_name = 'Faculty'
        verbose_name_plural = 'Faculties'

    def __str__(self):
        return self.title


class Department(models.Model):
    """
    @ the host of Hods
    """
    title = models.CharField(verbose_name='Title:',
                             max_length=255, blank=False, null=True)
    faculty = models.ForeignKey(
        Faculty, on_delete=models.CASCADE, related_name='faculty_departments')
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='department_users', null=True)

    class Meta:
        managed = True
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def __str__(self):
        return self.title


class Programme(models.Model):
    """
    @ the host of students
    """
    title = models.CharField(verbose_name='Title:',
                             max_length=255, blank=False, null=True)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name='department_programmes')
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='programme_users', null=True)

    class Meta:
        managed = True
        verbose_name = 'Programme'
        verbose_name_plural = 'Programmes'

    def __str__(self):
        return self.title


class Student(models.Model):
    """
    @ The Student can send complaints to only their HOD
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='student_users')
    programme = models.OneToOneField(
        Programme, null=True, on_delete=models.CASCADE, related_name='programme_students')

    class Meta:
        managed = True
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self) -> str:
        return f'{self.user.username}'


class Hod(models.Model):
    """ 
    @ The Hod first receive the Students complaints and resolve
    @ The Hod can also forward the complaints to the appropriate administrator
        IT support or Registry or Dean
    @ The Hod can also add programmes to their department
    @ The Hod can send new complaints or broadcast messages
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='hod_users')
    department = models.OneToOneField(
        Department, on_delete=models.PROTECT, related_name='department_hod', null=True)

    class Meta:
        managed = True
        verbose_name = 'HOD'
        verbose_name_plural = 'HODS'

    def __str__(self):
        return f'{self.user.username}'


class Dean(models.Model):
    """
    @ The Dean will only see the Complaints Forwarded to them by their hods
    @ The Dean can resolve the Complaints or Forward to Either IT Support or Registry
    @ The Dean can create departments
    @ The Dean can send complaints or broadcast message
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='dean_users')
    faculty = models.ForeignKey(
        Faculty, on_delete=models.PROTECT, related_name='faculty_deans', null=True)

    class Meta:
        managed = True
        verbose_name = 'DEAN'
        verbose_name_plural = 'DEANS'

    def __str__(self):
        return f'{self.user.username}'


class Registry(models.Model):
    """
    @ The Registry can receive complaints Forwarded to him by either hods or Deans
    @ The Registry can forward complaints to IT Support
    @ The Registry can can create faculties
    @ The Registry can send new complaints or Broadcast messages
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='registry_users')

    class Meta:
        managed = True
        verbose_name = 'Registry'
        verbose_name_plural = 'Registrys'

    def __str__(self):
        return f'{self.user.username}'


class Itsupport(models.Model):
    """
    @ The IT support is the super administrator
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='it_support_users')

    class Meta:
        managed = True
        verbose_name = 'IT Support'
        verbose_name_plural = 'IT Supports'

    def __str__(self):
        return f'{self.user.username}'


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='user_profile')
    faculty = models.ForeignKey(
        Faculty, on_delete=models.PROTECT, null=True, blank=True, related_name='user_faculty')
    department = models.ForeignKey(
        Department, on_delete=models.PROTECT, null=True, blank=True, related_name='user_department')
    programme = models.ForeignKey(
        Programme, on_delete=models.PROTECT, null=True, blank=True, related_name='user_programme')
    profile_picture = models.ImageField(verbose_name='Profile Picture:',
                                        upload_to='images/profile_pics/%Y/%M/%d', null=True)
    full_name = models.CharField(verbose_name='Full Name:', max_length=255,
                                 blank=True, null=True)
    gender = models.CharField(verbose_name='Gender:',
                              max_length=255, blank=True, null=True)
    phone = models.CharField(verbose_name="Phone:",
                             max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        verbose_name = 'UserProfile'
        verbose_name_plural = 'UserProfiles'

    def __str__(self):
        return f'{self.user.username}'
