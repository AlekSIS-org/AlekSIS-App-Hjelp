# Generated by Django 3.1.4 on 2020-12-21 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hjelp', '0002_auto_20201221_1815'),
    ]

    operations = [
        migrations.AddField(
            model_name='faqsection',
            name='position',
            field=models.PositiveIntegerField(default=1, verbose_name='Order'),
        ),
    ]
