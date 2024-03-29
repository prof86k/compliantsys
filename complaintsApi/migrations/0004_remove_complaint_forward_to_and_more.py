# Generated by Django 4.0.4 on 2022-08-23 15:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_userprofile_department_and_more'),
        ('complaintsApi', '0003_rename_forword_to_complaint_forward_to'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='complaint',
            name='forward_to',
        ),
        migrations.AddField(
            model_name='complaint',
            name='forward_to_dean',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='forward_to_dean', to='accounts.dean'),
        ),
        migrations.AddField(
            model_name='complaint',
            name='forward_to_it',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='forward_to_it', to='accounts.itsupport'),
        ),
        migrations.AddField(
            model_name='complaint',
            name='forward_to_registry',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='forward_to_registry', to='accounts.registry'),
        ),
    ]
