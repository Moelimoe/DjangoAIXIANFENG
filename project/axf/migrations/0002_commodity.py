# Generated by Django 2.1.4 on 2020-03-18 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('axf', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commodity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=150)),
                ('name', models.CharField(max_length=20)),
                ('track_id', models.CharField(max_length=20)),
                ('isDelete', models.BooleanField(null=True)),
            ],
        ),
    ]
