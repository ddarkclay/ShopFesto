# Generated by Django 2.2.2 on 2019-07-10 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('item_json', models.CharField(max_length=5000)),
                ('amount', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('zip_code', models.CharField(max_length=100)),
                ('phone', models.CharField(default='', max_length=20)),
            ],
        ),
    ]
