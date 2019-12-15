# Generated by Django 2.2.7 on 2019-12-14 10:58

import ckeditor_uploader.fields
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagine', '0026_auto_20191214_1052'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='chronicle',
            field=ckeditor_uploader.fields.RichTextUploadingField(default="Inserisci qui la cronaca dell'evento", verbose_name='Cronaca'),
        ),
        migrations.AddField(
            model_name='event',
            name='notice',
            field=models.CharField(blank=True, choices=[('SPAM', 'Da inviare'), ('DONE', 'Già inviata')], max_length=4, null=True, verbose_name='Notifica via email'),
        ),
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 14, 11, 58, 24, 351243), verbose_name='Quando'),
        ),
        migrations.AlterField(
            model_name='eventupgrade',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 14, 11, 58, 24, 351321), verbose_name='Data'),
        ),
    ]