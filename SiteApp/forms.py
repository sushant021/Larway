from django.forms import ModelForm
from . models import QuoteRequest, DriverResume, Employee, Customer, FuelSurcharge


class QuoteRequestForm(ModelForm):
    class Meta:
        model = QuoteRequest
        fields = '__all__'


class DriverResumeForm(ModelForm):
    class Meta:
        model = DriverResume
        fields = '__all__'


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'


class FuelSurchargeForm(ModelForm):
    class Meta:
        model = FuelSurcharge
        fields = '__all__'
