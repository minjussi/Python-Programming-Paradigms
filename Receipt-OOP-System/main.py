from datetime import datetime
# Store Class
class Store:
    def __init__(self, id, name, address, tel):
        self.__id = id
        self.__name = name
        self.__address = address
        self.__tel = tel
    @property
    def id(self):
        return self.__id
    @id.setter
    def id(self, value):
        self.__id = value
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, value):
        self.__name = value
    @property
    def address(self):
        return self.__address
    @address.setter
    def address(self, value):
        self.__address = value
    @property
    def tel(self):
        return self.__tel
    @tel.setter
    def tel(self, value):
        self.__tel = value
    def __str__(self):
        return f"Welcome to {self.__name}"

# Staff Class
class Staff:
    def __init__(self, id, ssn, name, address, job, salary):
        self.__id = id
        self.__ssn = ssn
        self.__name = name
        self.__address = address
        self.__job = job
        self.__salary = salary
    @property
    def id(self):
        return self.__id
    @id.setter
    def id(self, value):
        self.__id = value
    @property
    def ssn(self):
        return self.__ssn
    @ssn.setter
    def ssn(self, value):
        self.__ssn = value
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, value):
        self.__name = value
    @property
    def address(self):
        return self.__address
    @address.setter
    def address(self, value):
        self.__address = value
    @property
    def job(self):
        return self.__job
    @job.setter
    def job(self, value):
        self.__job = value
    @property
    def salary(self):
        return self.__salary
    @salary.setter
    def salary(self, value):
        self.__salary = value
    def __str__(self):
        return f"Staff{self.__id}: {self.__name} ({self.__job})"
    
# Customer Class
class Customer:
    def __init__(self, ssn, name, address, point, tel, membership=[]):
        self.__ssn = ssn
        self.__name = name
        self.__address = address
        self.__point = point
        self.__tel = tel
        self.__membership = membership
    @property
    def ssn(self):
        return self.__ssn
    @ssn.setter
    def ssn(self, value):
        self.__ssn = value
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, value):
        self.__name = value
    @property
    def address(self):
        return self.__address
    @address.setter
    def address(self, value):
        self.__address = value
    @property
    def point(self):
        return self.__point
    @point.setter
    def point(self, value):
        self.__point = value
    @property
    def tel(self):
        return self.__tel
    @tel.setter
    def tel(self, value):
        self.__tel = value
    @property
    def membership(self):
        return self.__membership
    @membership.setter
    def membership(self, value):
        self.__membership = value
    def __str__(self):
        return f"Customer: {self.__ssn} {self.__name} (Points: {self.__point})"

# Product Class  
class Product:
    def __init__(self, code, name, description, price, point):
        self.__code = code
        self.__name = name
        self.__description = description
        self.__price = price
        self.__point = point
    @property
    def code(self):
        return self.__code
    @code.setter
    def code(self, value):
        self.__code = value   
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, value):
        self.__name = value
    @property
    def description(self):
        return self.__description
    @description.setter
    def description(self, value):
        self.__description = value
    @property
    def price(self):
        return self.__price
    @price.setter
    def price(self, value):
        self.__price = value
    @property
    def point(self):
        return self.__point
    @point.setter
    def point(self, value):
        self.__point = value
    def __str__(self):
        return f"{self.__name} | {self.__code} | {self.__price}"

# Order Class
class Order:
    def __init__(self, store, customer, staff):
        self.__store = store
        self.__customer = customer
        self.__staff = staff
        self.__products = []
        self.__quantities = []
    def addProduct(self, product, quantity):
        self.__products.append(product)
        self.__quantities.append(quantity)
    def printReceipt(self):
        now = datetime.now()
        print("==RECEIPT==")
        print(f"{now.month}/{now.day}/{now.year}")
        print(f"{now.hour}:{now.minute}:{now.second}")
        print(f"ST #{self.__store.id}")
        print(f"Staff: {self.__staff.name} | Customer {self.__customer.ssn}: {self.__customer.name}")
        total_price = 0
        total_quantities = 0
        total_points = 0
        print(f"{'Product Name':<15} {'Product Code':<15} {'Price':>10} {'Q':>5}")
        print("-" * 50)
        for i in range(len(self.__products)):
            product = self.__products[i]
            quantity = self.__quantities[i]
            print(f"{product.name:<15} {product.code:<15} {product.price:>10} {quantity:>5}")
            total_price += product.price * quantity
            total_quantities += quantity
            total_points += product.point * quantity
        self.__customer.point = total_points
        print("=" * 50)
        print(f"Total Price: {total_price}")
        print(f"Items Sold: {total_quantities}")
        print(f"Total Points: {total_points}")

def main():
    new_store = Store("0123456789", "HomeStore", "Seoul", "010-1234-5678")
    print(new_store)

    staff1 = Staff("1", "2022567890", "Kim YoungJae", "Seoul", "Manager", 5000)
    staff2 = Staff("2", "2023312782", "Kang MinJu", "Busan", "Worker", 3000)
    print(staff1)
    print(staff2)

    customer1 = Customer("1000", "Emily", "Seoul", 0, "010-1234-5678", ["VIP"])
    customer2 = Customer("1005", "Sophia", "Japan", 100, "010-5555-7777")
    print(customer1)
    print(customer2)

    order = Order(new_store, customer1, staff1)

    while True:
        print("Purchasing (If you want to stop, press 'q'+'enter')")
        code = input("Product code: ")
        if code == 'q':
            break
        name = input("Product Name: ")
        description = input("Description: ")
        price = float(input("Price: "))
        point = int(input("Point: "))
        quantity = int(input("Quantity: "))

        good = Product(code, name, description, price, point)
        order.addProduct(good, quantity)

    order.printReceipt()

main()