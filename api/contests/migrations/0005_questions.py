# Generated by Django 3.0.5 on 2020-04-13 13:13

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0004_auto_20200413_0859'),
    ]

    operations = [
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=2048)),
                ('comment', models.CharField(max_length=512, null=True)),
                ('status', models.CharField(default='pending', max_length=50)),
                ('point', models.IntegerField(null=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('task', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contests.Tasks')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contests.Teams')),
            ],
            options={
                'db_table': 'questions',
                'ordering': ['-date_created', 'id'],
            },
        ),
    ]