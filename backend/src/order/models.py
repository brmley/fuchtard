from urllib.parse import urljoin

from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models import Sum, F

from food.models import FoodItem
from .helpers import shifthash, send_templated_email, telegram_notify_channel


class CartManager(models.Manager):
    def create_from_dict(self, cart_data):
        cart = self.create()
        cart_items = []
        for food_item_id, quantity in cart_data.items():
            try:
                food_item = FoodItem.objects.get(id=int(food_item_id))
            except FoodItem.DoesNotExist:
                continue
            cart_items.append(CartItem(cart=cart,
                                       product=food_item,
                                       quantity=quantity,
                                       history_price=food_item.price, ))
        CartItem.objects.bulk_create(cart_items)
        return cart


class Cart(models.Model):
    objects = CartManager()

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return '{}₸:\n{}'.format(self.total_price, self.cart_items)

    @property
    def cart_items(self):
        return '\n'.join(map(lambda x: x.repr_with_price, self.cartitem_set.all()))

    @property
    def total_price(self):
        total = self.cartitem_set.aggregate(cart_total_price=Sum(F('history_price') * F('quantity'))) \
            .get('cart_total_price', 0)
        return total


class CartItem(models.Model):
    class Meta:
        verbose_name = 'Содержимое корзины'
        verbose_name_plural = 'Содержимое корзины'

    cart = models.ForeignKey(Cart)
    product = models.ForeignKey(FoodItem)
    quantity = models.IntegerField()
    history_price = models.IntegerField(null=True)

    def __str__(self):
        return '{cart_item.quantity} × {cart_item.product.title}'.format(cart_item=self)

    @property
    def repr_with_price(self):
        return '{cart_item} = {cart_item.total_item_price}₸'.format(cart_item=self)

    @property
    def price(self):
        return self.product.price

    @property
    def total_item_price(self):
        return self.price * self.quantity


class OrderManager(models.Manager):
    def get_by_hash(self, hashed_id):
        return self.get(id=shifthash(hashed_id))


class Order(models.Model):
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
    objects = OrderManager()
    email = models.CharField(verbose_name='Email', max_length=60, null=True, blank=True)
    name = models.CharField(verbose_name='Имя', max_length=60, null=True, blank=True)
    phone = models.CharField(verbose_name='Телефон', max_length=20)
    street = models.CharField(verbose_name='Улица', max_length=60, null=True, blank=True)
    building = models.CharField(verbose_name='Дом', max_length=20, null=True, blank=True)
    apartment = models.CharField(verbose_name='Квартира', max_length=60, null=True, blank=True)
    floor = models.CharField(verbose_name='Этаж', max_length=20, null=True, blank=True)
    cart = models.OneToOneField(Cart)
    deliver_at = models.DateTimeField(verbose_name='Доставка ко времени', null=True, blank=True)
    comment = models.TextField(verbose_name='Комментарий', blank=True)
    gift_food_item = models.ForeignKey(FoodItem, verbose_name='Подарок', null=True, blank=True)
    order_created_timestamp = models.DateTimeField('Заказ создан', auto_now_add=True)

    def __str__(self):
        return '[{order.hashed_id}] {order.name}, {order.phone}'.format(order=self)

    def get_absolute_url(self):
        return reverse('admin:order_orderdetails_change', args=[self.id])

    @property
    def edit_url(self):
        return reverse('admin:order_order_change', args=[self.id])

    @property
    def hashed_id(self):
        return shifthash(self.id)

    def notify_restaurant(self):
        order_hashed_id = self.hashed_id
        order_absolute_url = urljoin('http://{}'.format(settings.SITE_DOMAIN), self.get_absolute_url())
        email_params = {
            'template': 'order/email_new_order',
            'template_params': {
                'order_url': order_absolute_url,
                'order': self,
            },
            'subject': 'Новый заказ №{}'.format(order_hashed_id),
            'from_email': settings.FUCHTARD_NOREPLY_EMAIL,
            'recipient_list': [settings.FUCHTARD_ORDERS_EMAIL]
        }
        send_templated_email(email_params)
        telegram_notify_channel('Новый заказ №{}\n{}'.format(order_hashed_id, order_absolute_url))


class OrderDetails(Order):
    class Meta:
        proxy = True
        verbose_name = 'Детали заказа'
        verbose_name_plural = 'Детали заказов'


class Gift(models.Model):
    class Meta:
        verbose_name = 'Подарок'
        verbose_name_plural = 'Подарки'
        ordering = ('requirement', )
    food_item = models.ForeignKey(FoodItem, verbose_name='Блюдо')
    requirement = models.PositiveIntegerField('Требование')

    def __str__(self):
        return self.food_item.title
