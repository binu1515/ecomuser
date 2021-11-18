# Generated by Django 3.2.7 on 2021-11-03 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('klog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_email', models.EmailField(max_length=254)),
                ('date_ordered', models.DateTimeField(auto_now=True)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=100)),
                ('quantity', models.IntegerField(default=0)),
                ('products', models.ManyToManyField(blank=True, to='klog.product')),
            ],
        ),
    ]
