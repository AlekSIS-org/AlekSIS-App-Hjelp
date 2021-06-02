# Generated by Django 3.2.3 on 2021-05-28 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hjelp', '0003_faqsection_position_and_show'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='faqsection',
            options={'ordering': ['position'], 'verbose_name': 'FAQ section', 'verbose_name_plural': 'FAQ sections'},
        ),
        migrations.AlterModelOptions(
            name='hjelpglobalpermissions',
            options={'managed': False, 'permissions': (('view_faq', 'Can view FAQ'), ('ask_faq', 'Can ask FAQ question'), ('report_issue', 'Can report issues'), ('send_feedback', 'Can send feedback'))},
        ),
        migrations.AlterField(
            model_name='faqsection',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='faqsection',
            name='position',
            field=models.PositiveIntegerField(blank=True, default=1, verbose_name='Order'),
        ),
        migrations.AlterField(
            model_name='issuecategory',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='issuecategory',
            name='placeholder',
            field=models.CharField(blank=True, max_length=255, verbose_name='Placeholder'),
        ),
        migrations.AddConstraint(
            model_name='faqsection',
            constraint=models.UniqueConstraint(fields=('site_id', 'name'), name='unique_section_name_per_site'),
        ),
        migrations.AddConstraint(
            model_name='issuecategory',
            constraint=models.UniqueConstraint(fields=('site_id', 'name'), name='unique_category_name_per_site'),
        ),
    ]
