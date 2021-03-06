# Generated by Django 2.0.5 on 2020-08-13 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_movement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movement',
            name='image',
            field=models.ImageField(default='group-blank.png', upload_to='event_pics'),
        ),
        migrations.AlterField(
            model_name='movement',
            name='mission',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
