# Generated by Django 3.2.20 on 2023-08-13 22:04

from django.db import migrations, models
import django_cryptography.fields


class Migration(migrations.Migration):

    dependencies = [
        ('labelbase', '0003_auto_20230812_2144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='label',
            name='spendable',
            field=django_cryptography.fields.encrypt(models.BooleanField(
                default=None, help_text="One of true or false, denoting if an output should be spendable by the wallet. The spendable property only where type is 'output'.", null=True)),
        ),
    ]
