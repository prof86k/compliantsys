# Generated by Django 4.0.4 on 2022-08-22 21:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_dean_faculty_alter_hod_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='user_department', to='accounts.department'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='faculty',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='user_faculty', to='accounts.faculty'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='programme',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='user_programme', to='accounts.programme'),
        ),
    ]
