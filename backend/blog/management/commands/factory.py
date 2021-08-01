
from django.core.management.base import BaseCommand, CommandError

from faker import Faker

# from blog.factories.Factory import Factory
from blog.factories.PostFactory import PostFactory


#python manage.py factory poll -amount=5

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument(
            'factories',
            nargs='+',
            type=str,
            help='Factories to be called',
        )

        parser.add_argument(
            '-a', '--amount',
            type=int,
            dest='amount',
            default=1,
            help='Amount of elements to be created',
        )

    def handle(self, *args, **options):
        factory_classes = self.get_factory_classes()

        faker = Faker()
        amount = options['amount']
        factories = options['factories']

        for factory in factories:
            if not factory in factory_classes:
                raise CommandError(f'Factory "{factory}" does not exist')

        for factory in factories:
            for i in range(amount):
                factory_classes[factory]()
        # factories_to_be_called = list()
        # for factory in factories:
        #     obj = factory_classes[factory](amount=amount, faker=faker)
        #     factories_to_be_called.append(obj)

        # Factory.create(factories_to_be_called)
        self.stdout.write(self.style.SUCCESS('Successfully created all elements'))

    def get_factory_classes(self):
        factory_classes = {}
        factory_classes['poll'] = PostFactory

        return factory_classes

