import os
from PIL import Image
from django.conf import settings
from django.core.mail import send_mail, get_connection
from django.db import models
from django.contrib.auth.models import AbstractUser
from pagine.models import CourseSchedule
from .choices import *

def user_directory_path(instance, filename):
    return 'user_uploads/{0}/{1}'.format(instance.user.username, filename)

class User(AbstractUser):

    def __str__(self):
        full_name = '%s %s' % (self.last_name, self.first_name)
        return full_name.strip()

    def get_full_name(self):
        full_name = '%s %s' % (self.last_name, self.first_name)
        return full_name.strip()

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        if self.is_active:
            try:
                memb = Member.objects.get(user_id = self.id)
                return
            except:
                memb = Member.objects.create(user = self, )
                memb.save()
                return
        else:
            children = Member.objects.filter(parent = self.id)
            if children:
                children.update(parent = None)

class Member(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE,
        primary_key=True, editable=False)
    sector = models.CharField(max_length = 4, choices = SECTOR,
        default = '0-NO', verbose_name = 'Corre con noi?')
    parent = models.ForeignKey(User, on_delete = models.SET_NULL,
        blank = True, null = True, related_name = 'member_parent',
        verbose_name = 'Genitore')
    avatar = models.ImageField(blank = True, null=True,
        upload_to = user_directory_path,)
    thumb = models.CharField(editable=False, blank=True, null=True,
        max_length = 200,)
    gender = models.CharField(max_length = 1, choices = GENDER,
        blank = True, null=True, verbose_name = 'Sesso', )
    date_of_birth = models.DateField( blank=True, null=True,
        verbose_name = 'Data di nascita',)
    place_of_birth = models.CharField(max_length = 50,
        blank = True, null = True, verbose_name = 'Luogo di nascita',)
    nationality = models.CharField(max_length = 50,
        blank = True, null = True, verbose_name = 'Nazionalità',)
    fiscal_code = models.CharField(max_length = 16,
        blank = True, null = True, verbose_name = 'Codice fiscale',)
    address = models.CharField(max_length = 100,
        blank = True, null = True, verbose_name = 'Indirizzo',
        help_text = 'Via/Piazza, civico, CAP, Città',)
    phone = models.CharField(max_length = 50,
        blank = True, null = True, verbose_name = 'Telefono/i',)
    email_2 = models.EmailField(blank = True, null = True,
        verbose_name = 'Seconda email',)
    course2 = models.ManyToManyField(CourseSchedule,
        blank = True, verbose_name = 'Orari scelti', )
    course_alt = models.CharField(max_length = 100,
        blank = True, null = True, verbose_name = 'Altro orario',)
    course_membership = models.CharField(max_length = 4, choices = COURSE,
        blank = True, null = True, verbose_name = 'Federazione / Ente sportivo',
        help_text = 'Solo se si segue un corso')
    no_course_membership = models.CharField(max_length = 4, choices = NO_COURSE,
        blank = True, null = True, verbose_name = 'Federazione / Ente sportivo',
        help_text = 'Solo se non si segue un corso')
    sign_up = models.FileField(
        upload_to = user_directory_path,
        blank = True, null = True, verbose_name = 'Richiesta di tesseramento',
        )
    privacy = models.FileField(
        upload_to = user_directory_path,
        blank = True, null = True, verbose_name = 'Privacy',
        )
    med_cert = models.FileField(
        upload_to = user_directory_path,
        blank = True, null = True, verbose_name = 'Certificato medico',
        )
    membership = models.CharField(max_length = 50,
        blank = True, null = True, verbose_name = 'Tessera',)
    mc_expiry = models.DateField( blank=True, null=True,
        verbose_name = 'Scadenza CM/CMA',)
    mc_state = models.CharField(max_length = 4, choices = MC_STATE,
        verbose_name = 'Stato del CM/CMA',
        default = '0-NF',)
    total_amount = models.FloatField( default = 0.00,
        verbose_name = 'Importo totale')
    settled = models.CharField(max_length = 4, choices = SETTLED,
        blank=True, null=True,
        verbose_name = 'In regola?',)

    def get_full_name(self):
        return self.user.get_full_name()
    get_full_name.short_description = 'Nome'

    def get_thumb(self):
        if self.thumb:
            thumb = format_html('<img src="{}" alt="" class="rounded-circle" />',
                self.thumb)
        else:
            thumb = format_html('<img src="/static/images/thumb_rp.png" alt="" class="rounded-circle" />')
        return thumb
    get_thumb.short_description = ''

    def __str__(self):
        full_name = '%s %s' % (self.user.last_name, self.user.first_name)
        return full_name.strip()

    def save(self, *args, **kwargs):
        super(Member, self).save(*args, **kwargs)
        if self.avatar:
            url_extension = os.path.splitext(self.avatar.url)
            thumb_name = url_extension[0] + "_thumb" + url_extension[1]
            if not self.thumb == thumb_name:
                try:
                    root_extension = os.path.splitext(self.avatar.path)
                    img = Image.open(root_extension[0] + root_extension[1])
                    xsize, ysize = img.size
                    if xsize > ysize:
                        cropped = img.crop(((xsize-ysize)/2,0,
                            xsize-(xsize-ysize)/2,ysize))
                    elif xsize < ysize:
                        cropped = img.crop((0,(ysize-xsize)/2,
                            xsize,ysize-(ysize-xsize)/2))
                    else:
                        cropped = img.copy()
                    size = (32, 32)
                    cropped.thumbnail(size)
                    cropped.save(root_extension[0] + "_thumb" + root_extension[1])
                    self.thumb = thumb_name
                    super(Member, self).save(*args, **kwargs)
                except:
                    pass

    class Meta:
        verbose_name = 'Iscritto'
        verbose_name_plural = 'Iscritti'

class MemberPayment(models.Model):
    member = models.ForeignKey(Member, on_delete = models.CASCADE,
        blank = True, null = True, related_name='member_payments')
    date = models.DateField( blank=True, null=True, verbose_name = 'Data')
    amount = models.FloatField( default = 0.00, verbose_name = 'Importo')

    def __str__(self):
        return 'Pagamento - %s' % (self.id)

    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamenti'

class Applicant(models.Model):
    first_name = models.CharField(max_length = 50,
        verbose_name = 'Nome',)
    last_name = models.CharField(max_length = 50,
        verbose_name = 'Cognome',)
    email = models.EmailField(verbose_name = 'Indirizzo email',)
    sector = models.CharField(max_length = 4, choices = SECTOR,
        default = '0-NO', verbose_name = 'Vuoi correre con noi?')
    children_str = models.TextField(max_length = 200,
        verbose_name = 'Figli', blank = True, null = True,
        help_text='Nome e cognome dei figli che si intende iscrivere, separati da una virgola.')

    def get_full_name(self):
        full_name = '%s %s' % (self.last_name, self.first_name)
        return full_name.strip()
    get_full_name.short_description = 'Nome'

    def __str__(self):
        full_name = '%s %s' % (self.last_name, self.first_name)
        return full_name.strip()

    class Meta:
        verbose_name = 'Richiedente'
        verbose_name_plural = 'Richiedenti'

class ApplicantChild(models.Model):
    parent = models.ForeignKey(Applicant, on_delete = models.CASCADE,
        related_name='applicant_children', editable=False)
    first_name = models.CharField(max_length = 50,
        verbose_name = 'Nome',)
    last_name = models.CharField(max_length = 50,
        verbose_name = 'Cognome',)
    class Meta:
        verbose_name = 'Figlio'
        verbose_name_plural = 'Figli'

class UserMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name='user_message', blank=True, null=True,
        verbose_name = 'Utente', )
    nickname = models.CharField(max_length = 50,
        verbose_name = 'Nome', blank=True, null=True,)
    email = models.EmailField(blank=True, null=True,
        verbose_name = 'Inviato da',)
    recipient = models.EmailField(blank=True, null=True, verbose_name = 'Destinatario')
    subject = models.CharField(max_length = 200,
        verbose_name = 'Soggetto', )
    body = models.TextField(verbose_name = 'Messaggio', )

    def get_full_name(self):
        if self.user:
            return self.user.get_full_name()
        else:
            return self.nickname
    get_full_name.short_description = 'Nome'

    def get_email(self):
        if self.user:
            return self.user.email
        else:
            return self.email
    get_email.short_description = 'Indirizzo email'

    def save(self, *args, **kwargs):
        if not self.recipient:
            self.recipient = 'rifondazionepodistica96@gmail.com'
        super(UserMessage, self).save(*args, **kwargs)
        con = get_connection(settings.EMAIL_BACKEND)
        send_mail(
            self.subject + ' da ' + self.get_email(),
            self.body,
            'no-reply@rifondazionepodistica.it',
            [self.recipient, ] ,
            connection = con,
        )

    def __str__(self):
        return 'Messaggio - %s' % (self.id)

    class Meta:
        verbose_name = 'Messaggio'
        verbose_name_plural = 'Messaggi'
