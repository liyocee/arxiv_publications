# Generated by Django 3.1.7 on 2021-04-04 21:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFavourite',
            fields=[
                ('id', models.IntegerField(editable=False, primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user_favourite',
                'verbose_name_plural': 'user_favourites',
                'ordering': ['-timestamp'],
                'abstract': False,
            },
        ),
    ]