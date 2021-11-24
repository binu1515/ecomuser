from django.db import models
from django.utils.html import mark_safe
import uuid

# Create your models here.
class user(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=20)
    password = models.CharField(max_length=20)

class Categrory(models.Model):
    cname=models.CharField(max_length=100)

    def __str__(self):
        return self.cname

    @staticmethod
    def get_all_categories():
        return Categrory.objects.all()
        
    class Meta:
        db_table='category'
    

class product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.ForeignKey(Categrory,on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=0)
    weight = models.IntegerField()
    disc = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images', null=True, blank=True)

    def __str__(self):
        return self.product_name

    @staticmethod
    def get_all_product():
        return product.objects.all()

    @staticmethod
    def get_all_products_id(id):
        if id:
            return product.objects.filter(Categrory=id)
        else:
            return product.objects.all()

    @property
    def total_price(self):
        return self.quantity * self.price




class Cart(models.Model):
    customer = models.ForeignKey(user, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE, null=True)
    product_qty = models.IntegerField(null=True, blank=False)
    

    @property
    def get_cart_total(self):
        cartitems = self.cartitems_set.all()
        total = sum([item.get_total for item in cartitems])
        return total
    
    @property
    def get_itemtotal(self):
        cartitems = self.cartitems_set.all()
        total = sum([item.quantity for item in cartitems])
        return total

    def __str__(self):
        return str(self.id)

class Cartitems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product =  models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)


    @property
    def get_total(self):
        total = self.quantity * self.product.price
        if total == 0.00:
            self.delete()
        return total

    

    def __str__(self):
        return self.product.name




class Order(models.Model):
    #order_id = models.AutoField
    customer_email = models.EmailField()
    date_ordered = models.DateTimeField(auto_now=True)
    products = models.ManyToManyField(product, blank=True)
    total = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    quantity = models.IntegerField(default=0)

    def total(self):
        return self.quantity * self.products.price

    def __str__(self):
        return self.order_id





class Check(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField()
    address = models.CharField(max_length=150)
    postal_code = models.CharField(max_length=30)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created', )

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
	order = models.ForeignKey(Check, related_name='items', on_delete=models.CASCADE)
	product = models.ForeignKey(product, related_name='order_items', on_delete=models.CASCADE)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	quantity = models.PositiveIntegerField(default=1)

	def __str__(self):
		return '{}'.format(self.id)

	def get_cost(self):
		return self.price * self.quantity


class Transaction (models.Model):
    items = models.ForeignKey(product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()

#Transaction.objects.annotate(total_price=F('items') * F('qty'))
