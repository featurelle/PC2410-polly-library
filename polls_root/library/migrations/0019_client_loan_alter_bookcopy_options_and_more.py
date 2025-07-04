# Generated by Django 4.1.5 on 2023-01-27 17:41

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0018_remove_author_born_in_past_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('book_copy', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='library.bookcopy')),
                ('due_back', models.DateField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='bookcopy',
            options={},
        ),
        migrations.RemoveConstraint(
            model_name='author',
            name='born_in_past',
        ),
        migrations.RemoveConstraint(
            model_name='author',
            name='died_in_past',
        ),
        migrations.RemoveConstraint(
            model_name='bookcopy',
            name='due_date_if_loan',
        ),
        migrations.RemoveField(
            model_name='bookcopy',
            name='client',
        ),
        migrations.RemoveField(
            model_name='bookcopy',
            name='due_back',
        ),
        migrations.AddConstraint(
            model_name='author',
            constraint=models.CheckConstraint(check=models.Q(('birth__gt', datetime.datetime(2023, 1, 27, 17, 41, 0, 483398, tzinfo=datetime.timezone.utc)), _negated=True), name='born_in_past', violation_error_message="Author can't be born in future"),
        ),
        migrations.AddConstraint(
            model_name='author',
            constraint=models.CheckConstraint(check=models.Q(('death__gt', datetime.datetime(2023, 1, 27, 17, 41, 0, 483425, tzinfo=datetime.timezone.utc)), _negated=True), name='died_in_past', violation_error_message="You can't set author's death in future"),
        ),
        migrations.AddField(
            model_name='loan',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loans', to='library.client'),
        ),
    ]
