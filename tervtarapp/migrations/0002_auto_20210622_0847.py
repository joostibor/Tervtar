# Generated by Django 2.2.12 on 2021-06-22 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tervtarapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dolgozo',
            name='id',
        ),
        migrations.RemoveField(
            model_name='dolgozo',
            name='torzsszam',
        ),
        migrations.AddField(
            model_name='dolgozo',
            name='felhnev',
            field=models.CharField(default='asd', max_length=25, primary_key=True, serialize=False),
        ),
    ]