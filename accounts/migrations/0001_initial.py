# Generated by Django 4.0.4 on 2022-08-19 20:47

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_administrator', models.BooleanField(default=False)),
                ('is_student', models.BooleanField(default=False)),
                ('is_hod', models.BooleanField(default=False)),
                ('is_dean', models.BooleanField(default=False)),
                ('is_registry', models.BooleanField(default=False)),
                ('is_it_support', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, null=True, verbose_name='Title:')),
            ],
            options={
                'verbose_name': 'Department',
                'verbose_name_plural': 'Departments',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Programme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, null=True, verbose_name='Title:')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='department_programmes', to='accounts.department')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='programme_users', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Programme',
                'verbose_name_plural': 'Programmes',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(null=True, upload_to='images/profile_pics/%Y/%M/%d', verbose_name='Profile Picture:')),
                ('full_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Full Name:')),
                ('gender', models.CharField(blank=True, max_length=255, null=True, verbose_name='Gender:')),
                ('phone', models.CharField(blank=True, max_length=255, null=True, verbose_name='Phone:')),
                ('department', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='user_department', to=settings.AUTH_USER_MODEL)),
                ('faculty', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='user_faculty', to=settings.AUTH_USER_MODEL)),
                ('programme', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='user_programme', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'UserProfile',
                'verbose_name_plural': 'UserProfiles',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('programme', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='programme_students', to='accounts.programme')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_users', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Registry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registry_users', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Registry',
                'verbose_name_plural': 'Registrys',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Itsupport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='it_support_users', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'IT Support',
                'verbose_name_plural': 'IT Supports',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Hod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='department_hod', to='accounts.department')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hod_users', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'HOD',
                'verbose_name_plural': 'HODS',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, null=True, verbose_name='Title:')),
                ('code', models.CharField(max_length=255, null=True, verbose_name='Code:')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='faculty_users', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Faculty',
                'verbose_name_plural': 'Faculties',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='department',
            name='faculty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='faculty_departments', to='accounts.faculty'),
        ),
        migrations.AddField(
            model_name='department',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='department_users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Dean',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='faculty_deans', to='accounts.faculty')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dean_users', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'DEAN',
                'verbose_name_plural': 'DEANS',
                'managed': True,
            },
        ),
    ]
