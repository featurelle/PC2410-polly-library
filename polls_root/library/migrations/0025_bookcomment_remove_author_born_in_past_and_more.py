# Generated by Django 4.1.5 on 2023-01-28 13:22

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0024_remove_author_born_in_past_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=64)),
                ('text', models.TextField()),
                ('datetime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
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
            constraint=models.CheckConstraint(check=models.Q(('birth__gt', datetime.datetime(2023, 1, 28, 13, 22, 30, 922478, tzinfo=datetime.timezone.utc)), _negated=True), name='born_in_past', violation_error_message="Author can't be born in future"),
        ),
        migrations.AddConstraint(
            model_name='author',
            constraint=models.CheckConstraint(check=models.Q(('death__gt', datetime.datetime(2023, 1, 28, 13, 22, 30, 922503, tzinfo=datetime.timezone.utc)), _negated=True), name='died_in_past', violation_error_message="You can't set author's death in future"),
        ),
        migrations.AddField(
            model_name='bookcomment',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='library.book'),
        ),
    ]
