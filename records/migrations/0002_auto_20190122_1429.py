# Generated by Django 2.1.5 on 2019-01-22 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='callrecord',
            name='type',
            field=models.CharField(choices=[('start', 'Call Start Record'), ('end', 'Call End Record')], max_length=5),
        ),
    ]
