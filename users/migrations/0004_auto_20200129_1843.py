# Generated by Django 3.0.2 on 2020-01-29 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200129_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Indirizzo email'),
        ),
    ]