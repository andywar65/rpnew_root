# Generated by Django 2.2.7 on 2019-12-02 17:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pagine', '0015_auto_20191202_1815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pagine.ImageEntry'),
        ),
    ]
