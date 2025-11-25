from django.shortcuts import render
from form_example.forms.forms import MakeOrderForm

# Create your views def here.
def placeOrder(request):
    form = MakeOrderForm(request.POST)
    message= ""
    if form.is_valid():
        message = "sucessfully sent"
    else:
        message = "please check the box"
    context = {"form": form, "message": message}
    return render(request, "form_example/order.html", context )
