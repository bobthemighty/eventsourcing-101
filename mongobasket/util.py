
def print_basket(basket):

    item_list = "\n".join(
        (f"\t* {product}: {qty}" for product, qty in basket._values.items())
    )
    event_list = "\n".join((f"\t* {e}" for e in basket.events))

    return (
        f"Basket {basket.id}:\n\n"
        f"{len(basket.events)} Events:\n\n"
        f"{event_list}\n\n"
        "Items:\n"
        f"{item_list}\n"
    )
