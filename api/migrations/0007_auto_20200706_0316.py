# Generated by Django 3.0.7 on 2020-07-06 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_politician_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='location',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='preference',
            name='abortion',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='preference',
            name='corporations',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='preference',
            name='criminal_justice',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='preference',
            name='economy_taxes',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='preference',
            name='education',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='preference',
            name='environment',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='preference',
            name='gun_control',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='preference',
            name='health_care',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='preference',
            name='immigration',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='preference',
            name='lbgtq_rights',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='preference',
            name='minority_support',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='preference',
            name='national_security',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='preference',
            name='womens_rights',
            field=models.SmallIntegerField(default=0),
        ),
    ]
