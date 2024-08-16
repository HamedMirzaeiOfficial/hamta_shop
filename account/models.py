from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from .managers import MyUserManager
from django.db import models



class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, null=True, blank=True, unique=True, verbose_name='نام کاربری')
    first_name = models.CharField(max_length=150, blank=True, null=True, verbose_name='نام')
    last_name = models.CharField(max_length=150, blank=True, null=True, verbose_name='نام خانوادگی')
    email = models.EmailField(max_length=255, verbose_name='ایمیل', blank=True, null=True)
    ssn = models.BigIntegerField(unique=True, verbose_name='کد ملی', blank=True, null=True)
    phone_number = models.CharField(max_length=11, verbose_name='شماره تلفن', blank=True, null=True, unique=True)
    wallet_amount = models.BigIntegerField(default=0, verbose_name='موجودی کیف پول')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = MyUserManager()

    USERNAME_FIELD = 'phone_number'
    # just for createsuperuser
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def __str__(self):
        return self.get_full_name()

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def get_full_name(self):
        text = str()
        if self.first_name:
            text += self.first_name
        if self.last_name:
            text += " " + self.last_name

        return text



class OtpCode(models.Model):
    phone_number = models.CharField(max_length=11)
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.phone_number} - {self.code} - {self.created}"

