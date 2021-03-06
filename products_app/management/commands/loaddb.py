from django.core.management.base import BaseCommand
from products_app.models import Product, Category

from .load_db.downloader import Downloader
from .load_db.sort import Sort


class Command(BaseCommand):
    help = """Populate product and category tables.
           You have to specify a number of products.
           "python manage.py load_db 3000" for example."""

    def add_arguments(self, parser):
        parser.add_argument('products', type=int)

    def handle(self, *args, **options):

        page = 1

        while Product.objects.all().count() < options['products']:
            if Product.objects.all().count() == 0:
                self.stdout.write('Loading database...')
            self.stdout.write('Calling OpenFoodFacts API')

            download = Downloader(page)
            data = download.json

            data_sorted_out = Sort(data)
            self.stdout.write('Downloaded and sorted out 1000 products')

            how_much_left_to_register = options[
                                            'products'] - Product.objects.all().count()

            if how_much_left_to_register < len(data_sorted_out.products):
                data_sorted_out.products = data_sorted_out.products[
                                           :how_much_left_to_register]

            Product.objects.bulk_create([
                Product(**product['informations'])
                for product in data_sorted_out.products
            ], ignore_conflicts=True)

            Category.objects.bulk_create([
                Category(name=category)
                for product in data_sorted_out.products
                for category in product['categories']
            ], ignore_conflicts=True)

            registered_products = Product.objects.all()
            registered_categories = Category.objects.all()

            ProductCategoryRelationShip = Product.categories.through

            for index, product in enumerate(data_sorted_out.products):
                ProductCategoryRelationShip.objects.bulk_create([
                    ProductCategoryRelationShip(
                        product=registered_products.get(
                            barre_code=product["informations"]["barre_code"]),
                        category=registered_categories.get(name=category), )
                    for category in product['categories']
                ], ignore_conflicts=True)

            page += 1

        self.stdout.write(
            f'Successfully saved {Product.objects.all().count()} products in database.')
