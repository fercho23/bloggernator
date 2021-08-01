
import random

from django.contrib.auth import get_user_model
from django.db.models import Q

import factory

from blog.models.Post import Post
from blog.models.Community import Community
from blog.models.Language import Language

User = get_user_model()

USER_ID_LIST_EXCLUDE = [
    1,
]


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.Faker('sentence', nb_words=random.randint(5, 15))
    slug = factory.LazyAttribute(lambda o: o.title)
    body = factory.Faker('paragraph', nb_sentences=random.randint(10, 25))
    abstract = factory.LazyAttribute(lambda o: o.body[0:250])

    # author = factory.Iterator(User.objects.exclude(id__in=USER_ID_LIST_EXCLUDE).all())
    # author = factory.LazyAttribute(lambda o: User.objects.exclude(id__in=USER_ID_LIST_EXCLUDE).order_by('?').first())
    # author = factory.LazyAttribute(lambda o: User.objects.exclude(owner_set__isnull=True).exclude(id__in=USER_ID_LIST_EXCLUDE).order_by('?').first())
    # author = factory.LazyAttribute(lambda o: User.objects.filter(Q(members__isnull=False) | Q(owner__isnull=False)).exclude(id__in=USER_ID_LIST_EXCLUDE).order_by('?').first())
    # author = factory.LazyAttribute(lambda o: User.objects.exclude(id__in=USER_ID_LIST_EXCLUDE).select_related('owner_set').prefetch_related('members_set').order_by('?').first())
    author = factory.LazyAttribute(lambda o:
        User.objects
            .filter(Q(members__isnull=False) | Q(community__isnull=False))
            .exclude(id__in=USER_ID_LIST_EXCLUDE)
            .order_by('?')
            .first()
        )

    # community = factory.Iterator(Community.objects.all()[randint(0, count - 1)])
    community = factory.LazyAttribute(lambda o:
        Community.objects
            .filter(Q(owner=o.author) | Q(members=o.author))
            .order_by('?')
            .first()
        )

    # language = factory.Iterator(Language.objects.all())
    language = factory.LazyAttribute(lambda o:
        Language.objects
            .order_by('?')
            .first()
        )

    is_public = 1

