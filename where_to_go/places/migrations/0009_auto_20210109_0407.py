# Generated by Django 3.1.5 on 2021-01-08 21:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0008_auto_20210109_0352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='place',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='photo', to='places.place', verbose_name='Место'),
        ),
    ]
