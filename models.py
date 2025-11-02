# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Cart(models.Model):
    cart_id = models.CharField(max_length=250)
    date_added = models.DateField()

    class Meta:
        managed = False
        db_table = 'Cart'


class Cartitem(models.Model):
    quantity = models.PositiveIntegerField()
    active = models.BooleanField()
    cart = models.ForeignKey(Cart, models.DO_NOTHING)
    template = models.ForeignKey('PagesTemplate', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'CartItem'


class Order(models.Model):
    token = models.CharField(max_length=250)
    total = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    emailaddress = models.CharField(db_column='emailAddress', max_length=250)  # Field name made lowercase.
    created = models.DateTimeField()
    billingname = models.CharField(db_column='billingName', max_length=250)  # Field name made lowercase.
    billingaddress1 = models.CharField(db_column='billingAddress1', max_length=250)  # Field name made lowercase.
    billingcity = models.CharField(db_column='billingCity', max_length=250)  # Field name made lowercase.
    billingpostcode = models.CharField(db_column='billingPostcode', max_length=10)  # Field name made lowercase.
    billingcountry = models.CharField(db_column='billingCountry', max_length=200)  # Field name made lowercase.
    shippingname = models.CharField(db_column='shippingName', max_length=250)  # Field name made lowercase.
    shippingaddress1 = models.CharField(db_column='shippingAddress1', max_length=250)  # Field name made lowercase.
    shippingcity = models.CharField(db_column='shippingCity', max_length=250)  # Field name made lowercase.
    shippingpostcode = models.CharField(db_column='shippingPostcode', max_length=10)  # Field name made lowercase.
    shippingcountry = models.CharField(db_column='shippingCountry', max_length=200)  # Field name made lowercase.
    discount = models.IntegerField()
    voucher = models.ForeignKey('VouchersVoucher', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Order'


class Orderitem(models.Model):
    template = models.CharField(max_length=250)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    order = models.ForeignKey(Order, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'OrderItem'


class Sub(models.Model):
    startdate = models.DateTimeField(db_column='startDate', blank=True, null=True)  # Field name made lowercase.
    active = models.BooleanField()
    user = models.OneToOneField('UsersCustomuser', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Sub'


class Templatesowned(models.Model):
    template = models.CharField(max_length=250)
    user = models.OneToOneField('UsersCustomuser', models.DO_NOTHING, blank=True, null=True)
    price = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'TemplatesOwned'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('UsersCustomuser', models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class PagesCategory(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'pages_category'


class PagesStyle(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'pages_style'


class PagesTemplate(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    name = models.CharField(unique=True, max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    created = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)
    pro = models.BooleanField()
    category = models.ForeignKey(PagesCategory, models.DO_NOTHING)
    image = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'pages_template'


class PagesTemplateStyle(models.Model):
    template = models.ForeignKey(PagesTemplate, models.DO_NOTHING)
    style = models.ForeignKey(PagesStyle, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'pages_template_style'
        unique_together = (('template', 'style'),)


class PagesTemplateType(models.Model):
    template = models.ForeignKey(PagesTemplate, models.DO_NOTHING)
    type = models.ForeignKey('PagesType', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'pages_template_type'
        unique_together = (('template', 'type'),)


class PagesType(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'pages_type'


class UsersCustomuser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    age = models.PositiveBigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users_customuser'


class UsersCustomuserGroups(models.Model):
    customuser = models.ForeignKey(UsersCustomuser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'users_customuser_groups'
        unique_together = (('customuser', 'group'),)


class UsersCustomuserUserPermissions(models.Model):
    customuser = models.ForeignKey(UsersCustomuser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'users_customuser_user_permissions'
        unique_together = (('customuser', 'permission'),)


class UsersProfile(models.Model):
    date_of_birth = models.DateField(blank=True, null=True)
    user = models.OneToOneField(UsersCustomuser, models.DO_NOTHING, blank=True, null=True)
    bio = models.CharField(max_length=2555, blank=True, null=True)
    occupation = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users_profile'


class VouchersVoucher(models.Model):
    code = models.CharField(unique=True, max_length=50)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField()
    active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'vouchers_voucher'
