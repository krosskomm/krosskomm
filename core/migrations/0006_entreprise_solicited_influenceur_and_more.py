# Generated by Django 4.1.3 on 2022-12-07 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_pays_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='entreprise',
            name='solicited_influenceur',
            field=models.ManyToManyField(related_name='influenceursolicite', to='core.influenceur'),
        ),
        migrations.AddField(
            model_name='influenceur',
            name='solicited_enterprise',
            field=models.ManyToManyField(related_name='entreprisesollicite', to='core.entreprise'),
        ),
    ]