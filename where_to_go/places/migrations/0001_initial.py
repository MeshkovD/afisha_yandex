# Generated by Django 3.1.4 on 2020-12-26 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description_short', models.TextField(max_length=500)),
                ('description_long', models.TextField(max_length=1000)),
                ('lng', models.DecimalField(decimal_places=16, max_digits=20)),
                ('lat', models.DecimalField(decimal_places=16, max_digits=20)),
            ],
        ),
    ]