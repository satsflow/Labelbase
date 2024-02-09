# Generated by Django 3.2.20 on 2023-12-02 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0006_profile_use_fiatfinances'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='my_currency',
            field=models.CharField(choices=[('USD', 'US Dollar'), ('EUR', 'Euro'), ('GBP', 'British Pound'), ('CAD', 'Canadian Dollar'), (
                'CHF', 'Swiss Franc'), ('AUD', 'Australian Dollar'), ('JPY', 'Japanese Yen')], default='USD', max_length=3),
        ),
    ]
