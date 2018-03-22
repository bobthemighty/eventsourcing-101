import pprint
import click
from .baskets import Basket

@click.group()
def basket():
    pass

@basket.command()
@click.argument('product')
@click.option('--quantity', default=1)
def create(product, quantity):
    basket = Basket(items={
        product: quantity
    })
    basket.save()
    print(f"Created basket with id '{basket.id}'")

@basket.command()
@click.argument('basket_id')
@click.argument('product')
@click.option('--quantity', default=1)
def add(basket_id, product, quantity):
    basket = Basket.get(basket_id)
    basket.add_item(product, quantity)
    basket.save()

@basket.command()
@click.argument('basket_id')
def get(basket_id):
    basket = Basket.get(basket_id)
    print(basket)

@basket.command()
@click.argument('basket_id')
@click.argument('product')
@click.option('--quantity')
def remove(basket_id, product, quantity):
    basket = Basket.get(basket_id)
    basket.remove(product)
    basket.save()

def main():
    basket()

