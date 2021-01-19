# Generated by Django 3.1.5 on 2021-01-18 05:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordereditem',
            name='product',
        ),
        migrations.AddField(
            model_name='ordereditem',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='books.book'),
            preserve_default=False,
        ),
    ]
