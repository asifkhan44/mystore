from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator

# Create your models here.
class Products(models.Model):                           #ORM for creating table using django itself
    name=models.CharField(unique=True,max_length=200)
    description=models.CharField(max_length=200)
    price=models.PositiveIntegerField()
    category=models.CharField(max_length=200)
    image=models.ImageField(null=True,upload_to='images')

    @property
    def avg_rating(self):
        ratings=self.reviews_set.all().values_list('rating',flat=True)
        if ratings:
            return sum(ratings)/len(ratings)
        else:
            return 0

    @property
    def no_rating(self):
        ratings=self.reviews_set.all().values_list('rating',flat=True)
        return len(ratings)

    def __str__(self):
        return self.name                #to display name once the product is subjected to view


#ORM query for creating a resource
#modelname.objects.create(field1=value1, field2=value2,.....................)
#Products.objects.create(name='Apple Iphone 13', description='Apple', price=75000, category='mobile')


#ORM query for fetcing all the datas and assign to a variable
#qs=modelname.objects.all()

class Carts(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    options=(
        ('order-placed','order-placed'),
        ('in-cart','in-cart'),
        ('cancelled','cancelled')
    )
    status=models.CharField(max_length=100, choices=options, default='in-cart')

class Reviews(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    comment=models.CharField(max_length=200)
    rating=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])

    def __str__(self):
        return self.comment


class Orders(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    options=(
        ('order-placed','order-placed'),
        ('dispatched','dispatched'),
        ('in-transit','in-transit'),
        ('cancelled','cancelled'),
        ('delivered','delivered')
    )
    status=models.CharField(max_length=100, choices=options, default='order-placed')
    date=models.DateTimeField(auto_now_add=True)
    address=models.CharField(max_length=250)
    phone=models.CharField(max_length=20)



