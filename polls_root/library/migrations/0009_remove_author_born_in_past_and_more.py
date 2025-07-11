# Generated by Django 4.1.5 on 2023-01-26 19:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0008_remove_author_born_in_past_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='author',
            name='born_in_past',
        ),
        migrations.RemoveConstraint(
            model_name='author',
            name='died_in_past',
        ),
        migrations.AddConstraint(
            model_name='author',
            constraint=models.CheckConstraint(check=models.Q(('birth__gt', datetime.datetime(2023, 1, 26, 19, 10, 42, 674647, tzinfo=datetime.timezone.utc)), _negated=True), name='born_in_past', violation_error_message="Author can't be born in future"),
        ),
        migrations.AddConstraint(
            model_name='author',
            constraint=models.CheckConstraint(check=models.Q(('death__gt', datetime.datetime(2023, 1, 26, 19, 10, 42, 674674, tzinfo=datetime.timezone.utc)), _negated=True), name='died_in_past', violation_error_message="Author't death can't be in future"),
        ),
    ]
