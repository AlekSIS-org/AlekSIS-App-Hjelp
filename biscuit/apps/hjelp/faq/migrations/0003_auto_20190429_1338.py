# Generated by Django 2.1.5 on 2019-04-29 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0002_auto_20190429_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faqquestion',
            name='question_text',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=models.TextField(),
        ),
    ]
