from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404
from .models import Category, Template
from subscription.models import Sub

from users.models import TemplatesOwned
from pages.models import Type, Style
from django.core.paginator import Paginator, EmptyPage, InvalidPage


# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home.html'


def temp_list(request, category_id=None):
    category = None
    templates = Template.objects.filter()
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        templates = Template.objects.filter(category=category)

    paginator = Paginator(templates, 5)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        templates = paginator.page(page)
    except (EmptyPage, InvalidPage):
        templates = paginator.page(paginator.num_pages)

    return render(request, 'shop/template_list.html', {'category': category, 'temps': templates})


def temp_detail(request, category_id, template_id):
    purchased = False
    pro = False
    subbed = False

    template = get_object_or_404(
        Template, category_id=category_id, id=template_id)
    if request.user.is_authenticated:

        types = Type.objects.filter(
            template=template)
        type = " "
        if types:
            for i in types:
                type += "(" + i.name + ") "

        styles = Style.objects.filter(
            template=template)
        style = " "
        if styles:
            for i in styles:
                style += "(" + i.name + ") "

        try:
            check = TemplatesOwned.objects.get(
                user=request.user, template=template_id)
            purchased = True
        except TemplatesOwned.DoesNotExist:
            purchased = False

        try:
            check = Sub.objects.get(
                user=request.user)
            if check.active == True:
                subbed = True
        except Sub.DoesNotExist:
            subbed = False

    if template.pro == True:
        pro = True

    return render(request, 'shop/template.html', {'template': template, "purchased": purchased, "pro": pro, "subbed": subbed, "type":type, "style":style  })
