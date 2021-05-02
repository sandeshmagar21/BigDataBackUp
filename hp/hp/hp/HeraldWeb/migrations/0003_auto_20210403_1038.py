# Generated by Django 3.1.4 on 2021-04-03 04:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HeraldWeb', '0002_auto_20210327_2339'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.TextField()),
                ('message', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='feedbackstudent',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 3, 10, 38, 53, 486934)),
        ),
        migrations.AlterField(
            model_name='feedbackstudent',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 3, 10, 38, 53, 486934)),
        ),
        migrations.AlterField(
            model_name='feedbackteacher',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 3, 10, 38, 53, 486934)),
        ),
        migrations.AlterField(
            model_name='feedbackteacher',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 3, 10, 38, 53, 486934)),
        ),
        migrations.AlterField(
            model_name='notificationstudent',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 3, 10, 38, 53, 486934)),
        ),
        migrations.AlterField(
            model_name='notificationstudent',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 3, 10, 38, 53, 486934)),
        ),
        migrations.AlterField(
            model_name='notificationteacher',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 3, 10, 38, 53, 486934)),
        ),
        migrations.AlterField(
            model_name='notificationteacher',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 3, 10, 38, 53, 486934)),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 3, 10, 38, 53, 485935)),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 3, 10, 38, 53, 485935)),
        ),
    ]
