# Generated by Django 4.0.4 on 2022-04-23 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='level',
            field=models.IntegerField(blank=True, null=True, verbose_name='Уровень вложенности'),
        ),
    ]