# Generated by Django 4.1.1 on 2023-04-12 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0002_user_reg_voteid'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_reg',
            name='voterid',
            field=models.CharField(default='0', max_length=500),
        ),
    ]