# Generated by Django 2.2.2 on 2019-07-16 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_auto_20190716_0807'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('coupon_id', models.AutoField(primary_key=True, serialize=False)),
                ('coupon_txt', models.CharField(max_length=50)),
                ('pub_date', models.DateField()),
            ],
        ),
    ]
