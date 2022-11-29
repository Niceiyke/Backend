# Generated by Django 4.1.3 on 2022-11-27 18:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('social', '0006_alter_comment_options_alter_post_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReplyComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social.comment')),
                ('dislikes', models.ManyToManyField(blank=True, related_name='reply_dislikes', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(blank=True, related_name='reply_likes', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='social.comment')),
                ('tags', models.ManyToManyField(blank=True, to='social.tag')),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
    ]
