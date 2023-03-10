# Generated by Django 4.1.3 on 2022-11-26 12:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Announce',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=200)),
                ('description', models.TextField(null=True)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('version', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Solicitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_solicitation', models.DateTimeField(auto_now_add=True)),
                ('announce', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='announce.announce')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProfilAnnonce',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pays', models.ManyToManyField(to='core.pays')),
                ('reputation', models.ManyToManyField(to='core.reputation')),
                ('reseaux', models.ManyToManyField(to='core.reseaux')),
                ('type_influenceur', models.ManyToManyField(to='core.typeinfluenceur')),
            ],
        ),
        migrations.AddField(
            model_name='announce',
            name='Solicitations',
            field=models.ManyToManyField(related_name='solicitations', through='announce.Solicitation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='announce',
            name='auteur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.entreprise'),
        ),
        migrations.AddField(
            model_name='announce',
            name='profil_recherche',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='announce.profilannonce'),
        ),
    ]
