# Generated by Django 3.0.5 on 2020-05-23 07:25

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0008_questions_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataSets',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=512)),
                ('json_data', models.TextField(max_length=65536, null=True)),
            ],
        ),
    ]