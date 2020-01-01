# Generated by Django 2.2.7 on 2020-01-01 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagine', '0043_auto_20191231_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='notice',
            field=models.CharField(blank=True, choices=[('NOSP', 'Non inviare'), ('SPAM', 'Da inviare'), ('DONE', 'Già inviata')], help_text="Non invia in automatico, per farlo seleziona l'Evento\n            dalla Lista degli Eventi, imposta l'azione 'Invia notifica' e fai\n            clic su 'Vai'.\n            ", max_length=4, null=True, verbose_name='Notifica via email'),
        ),
    ]
