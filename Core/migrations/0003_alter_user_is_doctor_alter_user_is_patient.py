# Generated by Django 5.1.4 on 2024-12-25 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0002_user_is_doctor_user_is_patient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_doctor',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_patient',
            field=models.BooleanField(null=True),
        ),
    ]
