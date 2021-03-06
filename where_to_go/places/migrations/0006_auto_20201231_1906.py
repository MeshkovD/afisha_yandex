# Generated by Django 3.1.4 on 2020-12-31 12:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0005_photo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='place',
            options={'ordering': ['title'], 'verbose_name': 'Место', 'verbose_name_plural': 'Места'},
        ),
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(upload_to='images/', verbose_name='Иллюстрация к месту'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='order',
            field=models.IntegerField(db_index=True, default=0, verbose_name='Порядок показа'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='place',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='places.place', verbose_name='Место'),
        ),
        migrations.AlterField(
            model_name='place',
            name='lat',
            field=models.DecimalField(decimal_places=13, max_digits=17),
        ),
        migrations.AlterField(
            model_name='place',
            name='lng',
            field=models.DecimalField(decimal_places=13, max_digits=17),
        ),
    ]
