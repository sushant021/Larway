from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Department(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Employee(models.Model):
    employee_id = models.IntegerField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    cell_number = models.BigIntegerField()
    address = models.CharField(max_length=200)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="employees")
    designation = models.CharField(max_length=50)
    salary = models.IntegerField()
    date_of_join = models.DateField()

    def __str__(self):
        return self.first_name

    def get_absolute_url(self):
        pass
        # return reverse('views.viewEmployee',args=[self.employee_id])


class Customer(models.Model):
    customer_id = models.IntegerField()
    company_name = models.CharField(max_length=200)
    key_person_name = models.CharField(max_length=200)
    key_person_contact = models.BigIntegerField()
    address = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.company_name

    def get_absolute_url(self):
        pass
        # return reverse('views.viewEmployee',args=[self.employee_id])


class QuoteRequest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.BigIntegerField()
    organization = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('view_quote', args=[self.id])


class DriverResume(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    contact = models.BigIntegerField()
    email = models.EmailField()
    experience = models.TextField()
    cover_letter = models.TextField()
    references = models.TextField()

    def __str__(self):
        return self.first_name

    def get_absolute_url(self):
        return reverse('view_resume', args=[self.id])


class FuelSurcharge(models.Model):
    input_diesel_price = models.FloatField()
