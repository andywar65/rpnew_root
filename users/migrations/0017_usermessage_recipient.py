# Generated by Django 2.2.7 on 2019-12-13 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_member_thumb'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermessage',
            name='recipient',
            field=models.EmailField(default='rifondazionepodistica96@gmail.com', max_length=254),
        ),
    ]
