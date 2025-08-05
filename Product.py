class Product:
    count_id = 0

    def __init__(self, product, description, price, image_url):
        Product.count_id += 1
        self.__product_id = Product.count_id
        self.__product = product
        self.__description = description
        self.__price = price
        self.__image_url = image_url

    # Accessors (Getters)
    def get_product_id(self):
        return self.__product_id

    def get_product(self):
        return self.__product

    def get_description(self):
        return self.__description

    def get_price(self):
        return self.__price

    def get_image_url(self):
        return self.__image_url

    # Mutators (Setters)
    def set_product(self, product):
        self.__product = product

    def set_description(self, description):
        self.__description = description

    def set_price(self, price):
        self.__price = price

    def set_image_url(self, image_url):
        self.__image_url = image_url
