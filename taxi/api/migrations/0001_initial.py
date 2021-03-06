# Generated by Django 4.0.1 on 2022-01-14 01:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField(max_length=40, null=True)),
                ('gender', models.CharField(max_length=1, null=True)),
                ('phone_number', models.IntegerField(null=True)),
                ('address', models.CharField(max_length=200, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='client', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField(max_length=40, null=True)),
                ('gender', models.CharField(max_length=1, null=True)),
                ('phone_number', models.IntegerField(null=True)),
                ('address', models.CharField(max_length=200, null=True)),
                ('commission', models.FloatField(null=True)),
                ('scheduled_rides', models.IntegerField(null=True)),
                ('unscheduled_rides', models.IntegerField(null=True)),
                ('documentation', models.FileField(null=True, upload_to='files')),
                ('license_issue_date', models.DateField(null=True)),
                ('license_expiry_date', models.DateField(null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('locationName', models.CharField(max_length=200, null=True)),
                ('latitude', models.FloatField(null=True)),
                ('longitude', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carMake', models.CharField(max_length=40, null=True)),
                ('carModel', models.CharField(max_length=200, null=True)),
                ('carCapacity', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(null=True)),
                ('time', models.TimeField(null=True)),
                ('numPassengers', models.IntegerField(null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('status', models.CharField(choices=[('CD', 'CREATED'), ('CD', 'CANCELLED'), ('AD', 'ACCEPTED'), ('FSH', 'FINISH')], max_length=200, null=True)),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.client')),
                ('driver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.driver')),
                ('end_location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='end_location', to='api.location')),
                ('start_location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='start_location', to='api.location')),
                ('vehicle', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.vehicle')),
            ],
            options={
                'ordering': ['date_created'],
            },
        ),
        migrations.AddField(
            model_name='driver',
            name='vehicle',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.vehicle'),
        ),
    ]
