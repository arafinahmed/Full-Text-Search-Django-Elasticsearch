# Generated by Django 4.1.7 on 2023-11-16 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_update_search_vector'),
    ]

    operations = [
        migrations.CreateModel(
            name='WineSearchWord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=255, unique=True)),
            ],
        ),
    ]
