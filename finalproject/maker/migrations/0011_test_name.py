# Generated by Django 2.1.7 on 2019-04-08 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maker', '0010_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='name',
            field=models.CharField(default=None, max_length=256),
        ),
    ]
