# Generated by Django 4.1.3 on 2022-12-08 00:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_entreprise_influenceurs_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entreprise',
            name='influenceurs',
        ),
        migrations.RemoveField(
            model_name='influenceur',
            name='enterprises',
        ),
        migrations.CreateModel(
            name='SimpleSolicitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_sollicitation', models.CharField(max_length=50)),
                ('date_solicitation', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=False)),
                ('entreprise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.entreprise')),
                ('influenceur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.influenceur')),
            ],
        ),
        migrations.AddField(
            model_name='influenceur',
            name='sollicitations',
            field=models.ManyToManyField(related_name='sollicitations', through='core.SimpleSolicitation', to='core.entreprise'),
        ),
    ]
