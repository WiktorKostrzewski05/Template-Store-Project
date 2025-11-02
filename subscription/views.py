from django.shortcuts import redirect, render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView
from django.conf import settings
import stripe
from .models import Sub
from datetime import date

class SubscribedView(TemplateView):
    template_name = 'subscribed.html'

def FlowPro(request, total=0, counter=0):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_total = int(total*100)
    description = 'Flow Pro - Subscription'
    data_key = settings.STRIPE_PUBLISHABLE_KEY

    subbed = False
    if request.user.is_authenticated:
        email = str(request.user.email)
        try:
            check = Sub.objects.get(
                user=request.user)
            if check.active == True:
                subbed = True
        except Sub.DoesNotExist:
            subbed = False

    if request.method == 'POST':
        print(request.POST)
        try:
            token = request.POST['stripeToken']
            email = str(request.user.email)
            customer = stripe.Customer.create(email=email, source=token)

            stripe.Subscription.create(
                customer=customer,
                items=[{"price": "price_1OIZ7rBgeCr0bwx6y2rwtKh4"}],
            )

            '''Creating the order'''
            try:
                sub_details = Sub.objects.get(
                    user=request.user,
                )
                print(sub_details)
                sub_details.startDate=str(date.today())
                sub_details.active=True
                print(sub_details.active)
                sub_details.save()
                return redirect('subscribed')

            except ObjectDoesNotExist:
                pass

        except stripe.error.CardError as e:
            return e

    return render(request, 'flowpro.html', {'total': total, 'counter': counter, 'data_key': data_key, 'stripe_total': stripe_total, 'description': description, 'subbed': subbed})
