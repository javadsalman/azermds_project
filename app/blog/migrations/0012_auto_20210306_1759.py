# Generated by Django 3.0.11 on 2021-03-06 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_auto_20210201_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='title_english',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='İngiliscə Başlıq'),
        ),
    ]
