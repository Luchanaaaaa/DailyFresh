from django.db import models
from db.base_model import BaseModel
from ckeditor.fields import RichTextField

# Create your models here.

class GoodsType(BaseModel):
    "GoodsType"
    name = models.CharField(max_length=20, verbose_name='TypeName')
    logo = models.CharField(max_length=20, verbose_name='logo')
    image = models.ImageField(upload_to='type', verbose_name='ImageType')

    class Meta:
        db_table = 'df_goods_type'
        verbose_name = 'Type of Goods'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class GoodsSKU(BaseModel):
    ''
    status_choices = (
        (0,'OffStock'),
        (1,'InStock'),
    )

    #SKU通常包含了商品的型号、规格、颜色等信息，可以帮助商家在库存中跟踪商品 Stock Keeping Unit
    type = models.ForeignKey('GoodsType',on_delete=models.CASCADE, verbose_name='GoodType')
    goods = models.ForeignKey('Goods', on_delete=models.CASCADE,verbose_name='goodsSPU')
    name = models.CharField(max_length=20, verbose_name='Name of Goods')
    desc = models.CharField(max_length=300, verbose_name='Description of Goods')
    price = models.DecimalField(max_digits=5,decimal_places=2, verbose_name='Goods Price')
    unite = models.CharField(max_length=20, verbose_name='Unite of Goods')
    image = models.ImageField(upload_to='goods', verbose_name= 'image of goods')
    stock = models.IntegerField(default=1, verbose_name='The Stock of Goods')
    sales = models.IntegerField(default=0, verbose_name='Goods Sales')
    status = models.SmallIntegerField(default=1, choices=status_choices, verbose_name="The Status of Good")

    class Meta:
        db_table = 'df_goods_sku'
        verbose_name = 'goods'
        verbose_name_plural = verbose_name

class Goods(BaseModel):
    '商品SPU模型类'
    name = models.CharField(max_length=20, verbose_name='SPUnameOfGoods')
    #富文本
    detail = RichTextField(blank=True, verbose_name='detail')

    class Meta:
        db_table = 'df_goods'
        verbose_name = 'GoodsSPU'
        verbose_name_plural = verbose_name

class GoodsImage(BaseModel):

    sku = models.ForeignKey('GoodsSKU', on_delete=models.CASCADE, verbose_name='Goods')
    image = models.ImageField(upload_to='goods', verbose_name='ImagePath')

    class Meta:
        db_table = 'df_goods_image'
        verbose_name = 'The image of goods'
        verbose_name_plural = verbose_name

class IndexGoodsBanner(BaseModel):
    'Rotation Display of prodeuct at Home Page'
    sku = models.ForeignKey('GoodsSKU', on_delete=models.CASCADE, verbose_name='Goods')
    image = models.ImageField(upload_to='banner', verbose_name='Image')
    index = models.SmallIntegerField(default=0, verbose_name='the display order')

    class Meta:
        db_table = 'df_index_banner'
        verbose_name = 'Carousel Goods'
        verbose_name_plural = verbose_name

class IndexTypeGoodsBanner(BaseModel):
    'Promotions'
    DISPLAY_TYPE_CHOICES = (
        (0,"Title"),
        (1,"Image"),
    )
    type = models.ForeignKey('GoodsType', on_delete=models.CASCADE, verbose_name='Type of Goods')
    sku = models.ForeignKey('GoodsSKU', on_delete=models.CASCADE, verbose_name='GoodsSKU')
    display_type = models.SmallIntegerField(default=1, choices=DISPLAY_TYPE_CHOICES, verbose_name='Displayed Type')
    index = models.SmallIntegerField(default=0, verbose_name='Displayed order')

    class Meta:
        db_table = 'df_index_type_goods'
        verbose_name = 'Home Category Display Products'
        verbose_name_plural = verbose_name


class IndexPromotionBanner(BaseModel):

    name = models.CharField(max_length= 20,  verbose_name='Name of Activity')
    url = models.URLField(verbose_name='Link of activity')
    image = models.ImageField(upload_to='banner',verbose_name='The activity image')
    index = models.SmallIntegerField(default= 0, verbose_name='Oder of display')

    class Meta:
        db_table = 'df_index_promotion'
        verbose_name = "Homepage Promotions"
        verbose_name_plural = verbose_name



