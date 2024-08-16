# Generated by Django 4.1.5 on 2023-02-14 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='shipping_status',
            field=models.CharField(choices=[('Waiting Payment', 'در انتظار پرداخت'), ('Paid', 'پرداخت شده'), ('Posted', 'ارسال شده'), ('Delivered', 'تحویل داده شده'), ('Returned', 'مرجوعی'), ('Canceled', 'لغو شده'), ('Waiting For Checking', 'منتظر تایید شدن چک')], default='Waiting Payment', max_length=20, verbose_name='وضعیت'),
        ),
    ]
