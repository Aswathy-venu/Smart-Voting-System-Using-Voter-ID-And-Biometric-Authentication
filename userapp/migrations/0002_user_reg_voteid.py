# Generated by Django 3.2.11 on 2023-04-10 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_reg',
            name='voteid',
            field=models.CharField(default='0', max_length=500),
        ),
    ]
