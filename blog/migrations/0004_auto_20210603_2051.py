# Generated by Django 2.1 on 2021-06-03 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_commentary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
