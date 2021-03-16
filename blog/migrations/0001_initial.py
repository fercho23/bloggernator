# Generated by Django 3.1.7 on 2021-03-16 18:38

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('uuid', models.CharField(blank=True, db_index=True, default=uuid.uuid4, editable=False, max_length=254, unique=True, verbose_name='uuid')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('username', models.CharField(max_length=254, unique=True, verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='users', verbose_name='photo')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
        migrations.CreateModel(
            name='Community',
            fields=[
                ('group_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.group')),
                ('uuid', models.CharField(blank=True, db_index=True, default=uuid.uuid4, editable=False, max_length=254, unique=True, verbose_name='uuid')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='slug')),
                ('detail', models.CharField(blank=True, max_length=180, verbose_name='detail')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
            ],
            options={
                'verbose_name': 'community',
                'verbose_name_plural': 'communities',
                'ordering': ('-created_at',),
                'permissions': [('community_owner', 'Community owner'), ('community_member', 'Community member')],
            },
            bases=('auth.group',),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(blank=True, db_index=True, default=uuid.uuid4, editable=False, max_length=254, unique=True, verbose_name='uuid')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='name')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'language',
                'verbose_name_plural': 'languages',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(blank=True, db_index=True, default=uuid.uuid4, editable=False, max_length=254, unique=True, verbose_name='uuid')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='name')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'tag',
                'verbose_name_plural': 'tags',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(blank=True, db_index=True, default=uuid.uuid4, editable=False, max_length=254, unique=True, verbose_name='uuid')),
                ('title', models.CharField(max_length=150, verbose_name='title')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='slug')),
                ('body', models.TextField(verbose_name='body')),
                ('abstract', models.CharField(max_length=250, verbose_name='abstract')),
                ('is_public', models.BooleanField(default=True, verbose_name='public')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.community', verbose_name='community')),
                ('contributors', models.ManyToManyField(blank=True, related_name='contributors', to=settings.AUTH_USER_MODEL, verbose_name='contributors')),
                ('language', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='blog.language', verbose_name='language')),
                ('tags', models.ManyToManyField(blank=True, related_name='tags', to='blog.Tag', verbose_name='tags')),
            ],
            options={
                'verbose_name': 'post',
                'verbose_name_plural': 'posts',
                'ordering': ('-created_at',),
                'permissions': [('post_owner', 'Post owner'), ('post_contributor', 'Post contributor')],
            },
        ),
    ]
