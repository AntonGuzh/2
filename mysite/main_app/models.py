from django.db import models
from django.contrib.auth.models import User

from django.core.validators import MinLengthValidator


class CVModel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)

    full_name = models.CharField(max_length=128, verbose_name='Фамилия и имя')
    photo = models.ImageField(blank=True, null=True, verbose_name='Фото')
    desired_position = models.CharField(max_length=128, verbose_name='Желаемая должность')
    phone_number = models.CharField(max_length=10, validators=[MinLengthValidator(10)],
                                    blank=True, null=True, verbose_name='Телефонный номер +7')
    email = models.EmailField(blank=True, null=True, verbose_name='Email')

    skills = models.TextField(blank=True, null=True, verbose_name='Ваши навыки')
    education = models.TextField(blank=True, null=True, verbose_name='Ваше образование')
    experience = models.TextField(blank=True, null=True, verbose_name='Ваш опыт')
