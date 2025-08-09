class Transaction:
    # Class-level variable for auto-incrementing IDs
    count_id = 0

    def __init__(self, product_id, product_name, quantity, price, customer_name, payment_type, date):
        self.__transaction_id = Transaction.count_id
        self.__product_id = product_id
        self._product_name = product_name
        self.__quantity = quantity
        self.__price = price
        self.__customer_name = customer_name
        self.__payment_type = payment_type
        self.__date = date

    # Accessor Methods
    def get_transaction_id(self):
        return self.__transaction_id

    def get_product_id(self):
        return self.__product_id

    def get_product_name(self):
        return self._product_name

    def get_quantity(self):
        return self.__quantity

    def get_price(self):
        return self.__price

    def get_customer_name(self):
        return self.__customer_name

    def get_payment_type(self):
        return self.__payment_type

    def get_date(self):
        return self.__date

    # Mutator Methods
    def set_product_id(self, product_id):
        self.__product_id = product_id

    def set_product_name(self, product_name):
        self._product_name = product_name

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def set_price(self, price):
        if price >= 0:
            self.__price = price
        else:
            raise ValueError("Price cannot be negative.")

    def set_customer_name(self, customer_name):
        self.__customer_name = customer_name

    def set_payment_type(self, payment_type):
        self.__payment_type = payment_type

    def set_date(self, date):
        self.__date = date

    # Utility
    def get_total_amount(self):
        """Returns the total cost for the transaction."""
        return self.__quantity * self.__price

    def increment_transaction_id(self):
        Transaction.count_id += 1