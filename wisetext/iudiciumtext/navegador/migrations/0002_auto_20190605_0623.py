# Generated by Django 2.1.8 on 2019-06-05 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navegador', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Acordao',
            fields=[
                ('id_processo', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('URL', models.URLField(max_length=500)),
                ('URL_inteiro_teor', models.URLField(max_length=500)),
                ('URL_dj_dj3', models.URLField(blank=True, max_length=500)),
                ('HTML_texto_basico', models.TextField()),
                ('texto_basico', models.TextField(blank=True)),
                ('pdf_inteiro_teor', models.URLField(blank=True, max_length=100)),
                ('txt_inteiro_teor', models.URLField(blank=True, max_length=100)),
                ('texto_inteiro_teor', models.TextField(blank=True)),
                ('classe', models.CharField(blank=True, max_length=100)),
                ('codigoClasse', models.CharField(blank=True, max_length=30)),
                ('origem', models.CharField(blank=True, max_length=10)),
                ('recurso', models.CharField(blank=True, max_length=10)),
                ('tipoJulgamento', models.CharField(blank=True, max_length=10)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('alterado_em', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Entry',
        ),
    ]