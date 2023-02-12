from django.db import models
from django.utils import timezone
from account.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from extensions.utils import jalali_converter


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250, verbose_name="عنوان مقاله")
    slug = models.SlugField(max_length=250, unique_for_date='publish', verbose_name="اسلاگ مقاله")
    image = models.ImageField(upload_to='images/post_image', verbose_name="عکس مقاله")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name="نویسنده مقاله")
    body = models.TextField(verbose_name="متن مقاله")
    publish = models.DateTimeField(default=timezone.now, verbose_name="تاریخ انتشار مقاله")
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد مقاله")
    updated = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی مقاله")
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT, verbose_name="وضعیت مقاله")

    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.
    tags = TaggableManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]
        verbose_name = "مقاله"
        verbose_name_plural = "مقاله ها"

    def __str__(self):
        return self.title

    def jpublish(self):
        return jalali_converter(self.publish)


    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name="نظر روی مقاله ی")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_comments', verbose_name="نظر توسط کاربر")
    title = models.CharField(max_length=100, verbose_name="عنوان نظر")
    email = models.EmailField(verbose_name="ایمیل کاربر")
    body = models.TextField(verbose_name="محتوای نظر")
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد نظر")
    active = models.BooleanField(default=False, verbose_name="فعال بودن")

    def jcreated(self):
        return jalali_converter(self.created)


    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"

    def __str__(self):
        return f'{self.user.get_full_name()} ---> {self.post}'