from django.shortcuts import redirect, render, get_object_or_404
from pages.models import Template
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import stripe
from order.models import Order, OrderItem
from users.models import TemplatesOwned
from vouchers.models import Voucher
from vouchers.forms import VoucherApplyForm
from decimal import Decimal

from django.contrib.auth.decorators import login_required


@login_required(login_url='/accounts/login/')
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


@login_required(login_url='/accounts/login/')
def add_cart(request, template_id):
    email = str(request.user.email)
    template = Template.objects.get(id=template_id)
    purchased = False
    try:
        check = TemplatesOwned.objects.get(
            user=request.user, template=template.id)
        purchased = True
    except TemplatesOwned.DoesNotExist:
        purchased = False

    if purchased == False:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))

        try:
            cart_item = CartItem.objects.get(template=template, cart=cart)
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                template=template, quantity=1, cart=cart)

        cart_item.quantity = 1
        cart_item.save()

    return redirect('cart:cart_detail')


@login_required(login_url='/accounts/login/')
def cart_detail(request, total=0, counter=0, cart_items=None):
    email = str(request.user.email)
    discount = 0
    voucher_id = 0
    new_total = 0
    voucher = None

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            purchased = False
            try:
                check = TemplatesOwned.objects.get(
                    user=request.user, template=cart_item.template.id)
                purchased = True
            except TemplatesOwned.DoesNotExist:
                purchased = False

            if purchased == False:
                total += (cart_item.template.price * cart_item.quantity)
                counter += cart_item.quantity
            else:
                print("Purchased")
                full_remove(request=request, template_id=cart_item.template.id)
    except ObjectDoesNotExist:
        pass
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_total = int(total*100)
    description = 'Online Shop - New Order'
    data_key = settings.STRIPE_PUBLISHABLE_KEY
    voucher_apply_form = VoucherApplyForm()
    try:
        voucher_id = request.session.get('voucher_id')
        voucher = Voucher.objects.get(id=voucher_id)
        if Voucher != None:
            discount = (total*(voucher.discount/Decimal('100')))
            new_total = (total - discount)
            stripe_total = int(new_total * 100)
    except:
        ObjectDoesNotExist
        pass
    if request.method == 'POST':
        print(request.POST)
        try:
            token = request.POST['stripeToken']
            billingName = request.POST['stripeBillingName']
            billingAddress1 = request.POST['stripeBillingAddressLine1']
            billingcity = request.POST['stripeBillingAddressCity']
            billingCountry = request.POST['stripeBillingAddressCountryCode']
            customer = stripe.Customer.create(email=email, source=token)
            stripe.Charge.create(amount=stripe_total,
                                 currency="eur",
                                 description=description,
                                 customer=customer.id)

            '''Creating the order'''
            try:
                order_details = Order.objects.create(
                    token=token,
                    total=total,
                    emailAddress=email,
                    billingName=billingName,
                    billingAddress1=billingAddress1,
                    billingCity=billingcity,
                    billingCountry=billingCountry,
                )
                order_details.save()
                if voucher != None:
                    order_details.total = new_total
                    order_details.voucher = voucher
                    order_details.discount = discount
                    order_details.save()

                for order_item in cart_items:
                    print(request.user.id)
                    try:
                        check = TemplatesOwned.objects.get(
                            user=request.user,
                            template=order_item.template.id)
                        if check:
                            return
                    except:
                        oi = TemplatesOwned.objects.create(
                            user=request.user,
                            template=order_item.template.id,
                        )
                        oi.save()
                        templates = Template.objects.get(
                            id=order_item.template.id)
                        templates.save()
                        print('2 The order has been created')

                for order_item in cart_items:
                    oi = OrderItem.objects.create(
                        template=order_item.template.name,
                        quantity=order_item.quantity,
                        price=order_item.template.price,
                        order=order_details
                    )
                    if voucher != None:
                        discount = (oi.price*(voucher.discount/Decimal('100')))
                        oi.price = (oi.price - discount)
                    else:
                        oi.price = oi.price*oi.quantity
                    oi.save()
                    templates = Template.objects.get(id=order_item.template.id)
                    templates.save()
                    order_item.delete()
                    print('The order has been created')
                return redirect('order:thanks', order_details.id)

            except ObjectDoesNotExist:
                pass

        except stripe.error.CardError as e:
            return e

    return render(request, 'cart.html', {'cart_items': cart_items,
                                         'total': total, 'counter': counter, 'data_key': data_key, 'stripe_total': stripe_total, 'description': description, 'voucher_apply_form': voucher_apply_form, 'new_total': new_total, 'voucher': voucher, 'discount': discount})


@login_required(login_url='/accounts/login/')
def cart_remove(request, template_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    template = get_object_or_404(Template, id=template_id)
    cart_item = CartItem.objects.get(template=template, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart_detail')


@login_required(login_url='/accounts/login/')
def full_remove(request, template_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    template = get_object_or_404(Template, id=template_id)
    cart_item = CartItem.objects.get(template=template, cart=cart)
    cart_item.delete()
    return redirect('cart:cart_detail')
