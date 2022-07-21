# Generated by Django 4.0.6 on 2022-07-18 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeftPanel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('component', models.CharField(max_length=50)),
                ('icon', models.CharField(default=None, max_length=50)),
                ('text', models.CharField(max_length=50)),
                ('route', models.CharField(max_length=50)),
                ('allow', models.SmallIntegerField()),
                ('props', models.JSONField(default=None)),
            ],
        ),
    ]
