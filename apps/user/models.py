from django.db import models
from django.contrib.auth.models import AbstractUser
from db.base_model import BaseModel
# Create your models here.


class User(AbstractUser, BaseModel):
    '''用户模型类'''

    class Meta:
        db_table = 'df_user'
        verbose_name = 'User'
        verbose_name_plural = verbose_name


class Address(BaseModel):
    '''地址模型类'''
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='Account Belong')
    receiver = models.CharField(max_length=20, verbose_name='Receiver')
    addr = models.CharField(max_length=256, verbose_name='Receiver Address')
    zip_code = models.CharField(max_length=6, null=True, verbose_name='Zipcode')
    phone = models.CharField(max_length=11, verbose_name='TEL')
    is_default = models.BooleanField(default=False, verbose_name='Is Default')

    class Meta:
        db_table = 'df_address'
        verbose_name = 'Address'
        verbose_name_plural = verbose_name
