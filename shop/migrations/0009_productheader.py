# Generated by Django 2.2.2 on 2019-07-14 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_order_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='Productheader',
            fields=[
                ('header_id', models.AutoField(primary_key=True, serialize=False)),
                ('header_name', models.CharField(max_length=100)),
                ('category', models.CharField(default='', max_length=50)),
                ('subcategory', models.CharField(default='', max_length=50)),
                ('desc', models.CharField(max_length=1000)),
                ('pub_date', models.DateField()),
                ('image', models.ImageField(default='', upload_to='shop/images')),
            ],
        ),
    ]
