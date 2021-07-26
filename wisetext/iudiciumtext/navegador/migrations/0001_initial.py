# Generated by Django 2.1.8 on 2019-06-05 05:54

from django.db import migrations, models
import djongo.models.fields
import navegador.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acordao', djongo.models.fields.EmbeddedModelField(model_container=navegador.models.Acordao, null=True)),
                ('headline', models.CharField(max_length=255)),
            ],
        ),
    ]