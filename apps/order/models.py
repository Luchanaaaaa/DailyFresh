from django.db import models
from db.base_model import BaseModel

# Create your models here.

class OrderInfo(BaseModel):

    PAY_METHOD_CHOICES = (
        (1, 'Paypal'),
        (2, 'Wechat Payment'),
        (3, 'Alipay'),
        (4, 'Credit Card')
    )

    ORDER_STATUS_CHOICES = (
        (1, 'Wait for payment'),
        (2, 'Pending'),
        (3, 'Shipping'),
        (4, 'Waiting for evaluation'),
        (5, 'Completed')
    )

    order_id = models.CharField(max_length=128, primary_key=True, verbose_name='OrderId')
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='User')
    addr = models.ForeignKey('user.Address', on_delete=models.CASCADE, verbose_name='Address')
    pay_method = models.SmallIntegerField(choices=PAY_METHOD_CHOICES, default=3, verbose_name='Payment methon')
    total_count = models.IntegerField(default=1, verbose_name='商品数量')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品总价')
    transit_price = models.DecimalField(max_digits=10, decimal_places=2,verbose_name='订单运费')
    order_status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES, default=1, verbose_name='订单状态')
    trade_no = models.CharField(max_length=128, verbose_name='支付编号')

    class Meta:
        db_table = 'df_order_info'
        verbose_name = 'order'
        verbose_name_plural = verbose_name


class OrderGoods(BaseModel):
    'The Order Goods'

    order = models.ForeignKey('OrderInfo', on_delete=models.CASCADE, verbose_name='order')
    sku = models.ForeignKey('goods.GoodsSKU', on_delete=models.CASCADE, verbose_name='Goods SKU')
    count = models.IntegerField(default=1, verbose_name='The amount of Goods')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Goods Price')
    comment = models.CharField(max_length=256, verbose_name='Comment')

    class Meta:
        db_table = 'df_order_goods'
        verbose_name = 'OderGoods'
        verbose_name_plural = verbose_name