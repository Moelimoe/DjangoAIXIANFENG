# Generated by Django 2.1.4 on 2020-03-18 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('axf', '0005_goods_goodstypes_order_trolley_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='marketprice',
            field=models.FloatField(max_length=10),
        ),
        migrations.AlterField(
            model_name='goods',
            name='price',
            field=models.FloatField(max_length=10),
        ),
    ]