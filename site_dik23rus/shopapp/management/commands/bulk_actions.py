from django.contrib.auth.models import User
from django.core.management import BaseCommand

from shopapp.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Start demo bulk actions")

        result = Product.objects.filter(
            name__contains="Smartphone"
        ).update(discount=10)

        print(result)
        # info = [
        #     ('Smartphone1', 199, 1),
        #     ('Smartphone2', 299, 1),
        #     ('Smartphone3', 399, 1),
        # ]
        # products =[
        #     Product(name=name, price=price, created_by_id=created_by)
        #     for name, price, created_by in info
        # ]
        #
        # result = Product.objects.bulk_create(products)
        #
        # for obj in result:
        #     print(obj)

        self.stdout.write(f"Done")