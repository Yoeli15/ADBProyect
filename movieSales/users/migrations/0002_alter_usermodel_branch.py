# Generated by Django 4.2.2 on 2023-06-17 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='branch',
            field=models.CharField(blank=True, choices=[('INSURGENTES', 'insurgentes'), ('CUATRO CAMINOS', 'cuatro caminos'), ('LOMAS ESTRELLA', 'lomas estrella'), ('SANTA FE', 'santa fe'), ('UNIVERSIDAD', 'universidad')], null=True),
        ),
    ]