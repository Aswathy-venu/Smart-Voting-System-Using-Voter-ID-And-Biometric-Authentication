# Generated by Django 4.1.1 on 2023-04-13 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0004_user_reg_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_reg',
            name='flag',
            field=models.BooleanField(default=False),
        ),
    ]
