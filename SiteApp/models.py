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


class Invoice(models.Model):
    invoice_number = models.CharField(max_length=20)
    invoice_date = models.DateField()
    invoice_code = models.CharField(max_length=20)
    order_number = models.CharField(max_length=20)
    shipped_date = models.DateField()
    received_date = models.DateField()
    del_number = models.CharField(max_length=50)
    shipper = models.CharField(max_length=100)
    consignee = models.CharField(max_length=100)
    frieght_description = models.CharField(max_length=100)
    frieght_weight = models.CharField(max_length=20)
    frieght_quantity = models.CharField(max_length=20)
    comments = models.TextField()
    frieght_rate = models.IntegerField()
    miles_travelled = models.IntegerField()
    fsc_per_mile = models.FloatField()
    fsc_percent = models.FloatField()
    fsc_amount = models.IntegerField()
    sub_total = models.IntegerField()
    total = models.IntegerField()

    def __str__(self):
        return self.invoice_number

    def get_absolute_url(self):
        return reverse("view_invoice", args=[self.invoice_number])


class Schedule(models.Model):
    name = models.CharField(max_length=50)
    csv_file = models.FileField(upload_to='uploads/schedules/', null="True")

    def get_absolute_url(self):
        return reverse('view_schedule', args=[self.id])


class ScheduleData(models.Model):
    schedule = models.ForeignKey(
        Schedule, on_delete=models.CASCADE, related_name="schedule_data")
    fuel_price = models.FloatField()
    tl_surcharge_percent = models.FloatField()
    ltl_surcharge_percent = models.FloatField()


class FuelSurcharge(models.Model):
    input_diesel_price = models.FloatField()
    #schedule = models.ForeignKey(Schedule)


class FuelData(models.Model):
    surcharge_percentage = models.FloatField(
        blank=False, default=0.00, null=False)
    surcharge_per_mile = models.FloatField(
        blank=False, null=False, default=0.00)
    miles = models.FloatField(blank=False, null=False, default=0.00)
    rate_per_mile = models.FloatField(blank=False, null=False, default=0.00)
    surcharge_amount = models.FloatField(blank=False, null=False, default=0.00)
    linehaul_amount = models.FloatField(blank=False, null=False, default=0.00)
    total_amount = models.FloatField(blank=False, null=False, default=0.00)
