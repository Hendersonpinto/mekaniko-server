# Generated by Django 3.2 on 2021-04-18 12:14

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0002_postgis_extension_db'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('city', models.CharField(blank=True, max_length=120, null=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('open_time', models.TimeField(blank=True, null=True, verbose_name='Open time')),
                ('close_time', models.TimeField(blank=True, null=True, verbose_name='Close time')),
                ('wifi', models.BooleanField(blank=True, null=True)),
                ('physical_store', models.BooleanField(blank=True, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=20, null=True, verbose_name='Postal Code')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shops', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
