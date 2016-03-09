from django.db import models
from django.core.urlresolvers import reverse
from parler.models import TranslatableModel, TranslatedFields
from sorl.thumbnail import ImageField
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from django.core.exceptions import ValidationError


# Create your models here.


class KeyWord(TranslatableModel):
    class Meta:
        verbose_name = _('Keyword')
        verbose_name_plural = _('Keywords')

    translations = TranslatedFields(
        keywords=models.CharField(max_length=200, verbose_name=_('Keywords'), help_text='keywords split by ,',
                                  blank=True, null=True),
        description=models.CharField(max_length=400, verbose_name=_('Google\'s description'),
                                     help_text=_('What goes inside the description metadata'), blank=True, null=True),
        facebook_msg=models.CharField(max_length=300, verbose_name=_('Facebook message'),
                                      help_text=_('What goes inside og:title metadata'), blank=True, null=True),
        twitter_msg=models.CharField(max_length=300, verbose_name=_('Twitter message'),
                                     help_text=_('What goes inside twitter:title metadata'), blank=True, null=True),
    )
    facebook_img = ImageField(verbose_name=_('Facebook Image'), upload_to='/facebook', blank=True, null=True)

    is_index = models.BooleanField(default=False, verbose_name=_('Is index?'),
                                   help_text=_('Check if the keyword belongs to the homepage'))

    twitter_img = ImageField(verbose_name=_('Twitter Image'), upload_to='/twitter', blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.is_index:
            index_keyowrds = KeyWord.objects.filter(is_index=True)
            for key in index_keyowrds:
                key.is_index = False
                key.save()
            self.is_index = True
        super(KeyWord, self).save(args, kwargs)

    def __str__(self):
        return self.keywords


class Travels(models.Model):
    class Meta:
        verbose_name = _('Travel')
        verbose_name_plural = _('Travels')
        ordering = ['date']

    date = models.DateTimeField(verbose_name=_('Date'), help_text=_('Travel\'s Date'))
    grade = models.IntegerField(verbose_name=_('Grade'), help_text=_('Evaluation for the travel'),
                                blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(5)])
    origin_code = models.CharField(verbose_name=_('Origin'), max_length=10,
                                   help_text=_('The origin of the travel, city code is saved'))
    destination_code = models.CharField(verbose_name=_('Destination'), max_length=10,
                                        help_text=_('The destination of the travel, city code is saved'))

    users = models.ManyToManyField('User', related_name='travels', verbose_name=_('Users'),
                                   help_text=_('Users in the travel'))

    def __str__(self):
        return str(self.date) + ' ' + str(self.origin_code) + '-' + str(self.destination_code)


class User(models.Model):
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    photo = models.ImageField(upload_to='users/%Y/%m/%d',
                              blank=True)

    def __str__(self):
        return self.user.username


measures = (
    ('m', 'M'),
    ('dm', 'Dm'),
    ('cm', 'Cm'),
    ('mm', 'Mm')
)


class Categories(TranslatableModel):
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    translations = TranslatedFields(
        name=models.CharField(verbose_name=_('Name'), max_length=200, help_text=_('Name of the category'))
    )

    travels = models.ManyToManyField('Travels', related_name='categories', verbose_name=_('Travels'))

    def __str__(self):
        return self.name or ''


class ContainedIn(models.Model):
    class Meta:
        verbose_name = _('ContainedIn')
        verbose_name_plural = _('ContainedIn')

    min = models.IntegerField(verbose_name=_('Min'), validators=[MinValueValidator(1)], blank=True, null=True)
    max = models.IntegerField(verbose_name=_('Max'), validators=[MinValueValidator(1)], blank=True, null=True)
    measure = models.CharField(verbose_name=_('Measure'), max_length=3, choices=measures)

    def __str__(self):
        return str(self.min) + 'x' + str(self.max) + str(self.measure)
