from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import QuoteRequest, DriverResume, Employee, Customer
from .forms import DriverResumeForm, QuoteRequestForm, EmployeeForm, CustomerForm
from django.contrib.auth import logout

import urllib3
import re


def index(request):
    return render(request, 'SiteApp/index.html')


def ViewServices(request):
    return render(request, 'SiteApp/services.html')


def ViewAbout(request):
    return render(request, 'SiteApp/about.html')


def viewContact(request):
    if request.method == "POST":
        form = QuoteRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            return HttpResponse('Invalid Form')
    else:
        form = QuoteRequestForm()
        return render(request, 'SiteApp/contact_us.html', {'form': form})


def UserLogout(request):
    logout(request)
    return redirect('/')


def UserDashBoard(request):
    return render(request, 'SiteApp/dashboard.html')


def ViewQuoteRequests(request):
    quote_requests = QuoteRequest.objects.all()
    return render(request, 'SiteApp/list_quote_requests.html', {'quote_requests': quote_requests})


def ViewDriverResumes(request):
    resumes = DriverResume.objects.all()
    return render(request, 'SiteApp/list_driver_resumes.html', {'resumes': resumes})


def DriveWithUs(request):
    if request.method == "POST":
        form = DriverResumeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            return HttpResponse('Invalid Form')
    else:
        form = DriverResumeForm()
        return render(request, 'SiteApp/drive_with_us.html', {'form': form})


def RequestQuote(request):
    if request.method == "POST":
        form = QuoteRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            return HttpResponse('Invalid Form')
    else:
        form = QuoteRequestForm()
        return render(request, 'SiteApp/quote_request.html', {'form': form})


def ViewQuote(request, id):
    quote = QuoteRequest.objects.get(id=id)
    return render(request, 'SiteApp/view_quote.html', {'quote': quote})


def ViewResume(request, id):
    resume = DriverResume.objects.get(id=id)
    return render(request, 'SiteApp/view_resume.html', {'resume': resume})


def FuelSurcharge(request):
    http = urllib3.PoolManager()
    r = http.request(
        'GET', 'https://www.eia.gov/petroleum/gasdiesel/includes/gas_diesel_rss.xml')
    content = r.data.decode('utf-8')

    result = content.find('On-Highway Diesel Fuel Retail Price')

    floats = re.findall(r'[+-]?\d+\.?\d*\.\d+', content[result:])

    regions = ['U.S.', 'East Coast', 'New England', 'Central Atlantic', 'Lower Atlantic', 'Midwest',
               'Gulf Coast', 'Rocky Mountain', 'West Coast', 'West Coast less California', 'California']
    price_dict = {}
    for i, region in enumerate(regions):
        price_dict[region] = floats[i]

    return render(request, 'Siteapp/fuel_surcharge.html', {'price_dict': price_dict})


def ListEmployees(request):
    employees = Employee.objects.all()
    return render(request, 'SiteApp/list_employees.html', {'employees': employees})


def AddEmployee(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        else:
            return HttpResponse('Invalid Form')
    else:
        form = EmployeeForm()
        return render(request, 'SiteApp/add_employee.html', {'form': form})


def EditEmployee(request, id):
    pass


def DeleteEmployee(request, id):
    pass


def ListCustomers(request):
    customers = Customer.objects.all()
    return render(request, 'SiteApp/list_customers.html', {'customers': customers})


def AddCustomer(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        else:
            return HttpResponse('Invalid Form')
    else:
        form = CustomerForm()
        return render(request, 'SiteApp/add_customer.html', {'form': form})


def EditCustomer(request, id):
    pass


def DeleteCustomer(request, id):
    pass
