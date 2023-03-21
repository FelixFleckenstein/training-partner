# Generated by Django 4.0.6 on 2023-03-21 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workoutplan', '0002_exercisebase_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='TemplateDetail',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('exerciseBaseNr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workoutplan.exercisebase')),
                ('templateNr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercises', to='workoutplan.template')),
            ],
        ),
    ]
