from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=100)
   

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__ (self):
        return self.title

class Brand(models.Model):
    title = models.CharField(max_length=100)
    best_seller = models.BooleanField(default=False)

    def __str__ (self):
        return self.title


class Item(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    new_price = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(upload_to='static/images')
    old_price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    slug = models.SlugField()
    description = models.TextField(max_length=2000)
    featured = models.BooleanField(default=False)

    def __str__ (self):
        return self.title

    def get_item_discount(self):
        discount = self.old_price - self.new_price 
        save = discount * 100
        discount_percentage = save // self.old_price 
        return discount_percentage

    def get_add_to_cart_url(self):
        return reverse('add_to_cart', kwargs={'slug':self.slug})

    def get_remove_from_cart_url(self):
        return reverse('remove_from_cart', kwargs={'slug':self.slug})

    def get_remove_single_item_from_cart_url(self):
        return reverse('remove_single_item_from_cart', kwargs={'slug':self.slug})         
   


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def __str__ (self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.new_price        

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    address = models.ForeignKey('Address', on_delete=models.SET_NULL, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
       
    def get_items(self):
        # return "\n".join([i.item for i in self.items.all()])
        return ",".join([str(i) for i in self.items.all()])

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        return total        



class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    county = models.CharField(max_length=500)
    location = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=500)
    save_info = models.BooleanField(default=False)
    default = models.BooleanField(default=False)
    use_default = models.BooleanField(default=False)
    # payment_option = models.CharField(max_length=500)

    class Meta:
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return self.user.username