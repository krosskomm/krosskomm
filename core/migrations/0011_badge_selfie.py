# Generated by Django 4.1.3 on 2022-12-10 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_remove_entreprise_influenceurs_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='badge',
            name='selfie',
            field=models.ImageField(blank=True, null=True, upload_to='selfie'),
        ),
    ]
