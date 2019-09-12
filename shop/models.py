from django.db import models

# Create your models here.

class Productheader(models.Model):
	header_id = models.AutoField(primary_key=True)
	header_name = models.CharField(max_length=100)
	category = models.CharField(max_length=50, default="")
	subcategory = models.CharField(max_length=50, default="")
	desc = models.CharField(max_length=1000)
	rating = models.FloatField(default=3.0)
	pub_date = models.DateField()
	image = models.ImageField(upload_to="shop/images", default="")

	def __str__(self):
		return self.header_name

class Product(models.Model):
	product_id = models.AutoField(primary_key=True)
	product_name = models.CharField(max_length=100)
	category = models.CharField(max_length=50, default="")
	subcategory = models.CharField(max_length=50, default="")
	old_price = models.BigIntegerField(default=0)
	new_price = models.BigIntegerField(default=0)
	desc = models.CharField(max_length=1000)
	rating = models.FloatField(default=3.0)
	pub_date = models.DateField()
	image = models.ImageField(upload_to="shop/images", default="")

	def __str__(self):
		return self.product_name

class Contact(models.Model):
	msg_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	email = models.CharField(max_length=50, default="")
	phone = models.CharField(max_length=50, default="")
	message = models.CharField(max_length=500)

	def __str__(self):
		return self.name

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    item_json = models.CharField(max_length=5000)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, default="")

    def __str__(self):
        return self.name

class OrderUpdate(models.Model):
	update_id = models.AutoField(primary_key=True)
	order_id = models.IntegerField(default="")
	email = models.CharField(max_length=100, default="")
	update_desc = models.CharField(max_length=5000)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f" Order Id : {self.order_id}"

class Category(models.Model):
	category_id = models.AutoField(primary_key=True)
	category_1 = models.CharField(max_length=100)
	subcategory_1 = models.CharField(max_length=100)
	category_2 = models.CharField(max_length=100)
	subcategory_2 = models.CharField(max_length=100)
	pub_date_1 = models.DateField()
	pub_date_2 = models.DateField()
	image_1 = models.ImageField(upload_to="shop/images", default="")
	image_2 = models.ImageField(upload_to="shop/images", default="")

	def __str__(self):
		return self.category_1+ " and " +self.category_2
		
class Coupon(models.Model):
	coupon_id = models.AutoField(primary_key=True)
	coupon_txt = models.CharField(max_length=50)
	discount = models.IntegerField(default=0)
	pub_date = models.DateField()

	def __str__(self):
		return self.coupon_txt
 