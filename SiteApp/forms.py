from django.forms import ModelForm
from . models import QuoteRequest, DriverResume, Employee, Customer, FuelSurcharge, FuelData, Invoice, Schedule, ScheduleData, Department


class QuoteRequestForm(ModelForm):
    class Meta:
        model = QuoteRequest
        fields = '__all__'


class DriverResumeForm(ModelForm):
    class Meta:
        model = DriverResume
        fields = '__all__'


class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = '__all__'


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'


class InvoiceForm(ModelForm):
    class Meta:
        model = Invoice
        fields = '__all__'


class FuelSurchargeForm(ModelForm):
    class Meta:
        model = FuelSurcharge
        fields = ('input_diesel_price', )


class FuelDataForm(ModelForm):
    class Meta:
        model = FuelData
        fields = '__all__'


class ScheduleForm(ModelForm):
    class Meta:
        model = Schedule
        fields = '__all__'


class ScheduleDataForm(ModelForm):
    class Meta:
        model = ScheduleData
        fields = '__all__'
