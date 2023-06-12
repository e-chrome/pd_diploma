from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from requests import get
from yaml import Loader
from yaml import load as load_yaml

from orders.celery import celery_app

from .models import Category, ConfirmEmailToken, Parameter, Product, ProductInfo, ProductParameter, Shop, User


@celery_app.task()
def password_reset_token_created_task(sender, instance, reset_password_token, **kwargs):
    """
    Отправляем письмо с токеном для сброса пароля
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param kwargs:
    :return:
    """
    # send an e-mail to the user

    msg = EmailMultiAlternatives(
        # title:
        f'Password Reset Token for {reset_password_token.user}',
        # message:
        reset_password_token.key,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [reset_password_token.user.email],
    )
    msg.send()


@celery_app.task()
def new_user_registered_task(user_id, **kwargs):
    """
    отправляем письмо с подтверждением почты
    """
    # send an e-mail to the user
    token, _ = ConfirmEmailToken.objects.get_or_create(user_id=user_id)

    msg = EmailMultiAlternatives(
        # title:
        f'Password Reset Token for {token.user.email}',
        # message:
        token.key,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [token.user.email],
    )
    msg.send()


@celery_app.task()
def new_order_task(user_id, **kwargs):
    """
    отправяем письмо при изменении статуса заказа
    """
    # send an e-mail to the user
    user = User.objects.get(id=user_id)

    msg = EmailMultiAlternatives(
        # title:
        'Обновление статуса заказа',
        # message:
        'Заказ сформирован',
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [user.email],
    )
    msg.send()


@celery_app.task()
def do_import_task(partner_id, url):
    """
    Импорт прайса от поставщика
    """
    # if url:
    # validate_url = URLValidator()
    # try:
    #     validate_url(url)
    # except ValidationError as e:
    #     return {'Status': False, 'Error': str(e)}
    # else:
    stream = get(url).content

    data = load_yaml(stream, Loader=Loader)
    print(data)
    # file = open_file(data)
    # print(file)
    shop, _ = Shop.objects.get_or_create(name=data['shop'], user_id=partner_id)

    for category in data['categories']:
        category_object, _ = Category.objects.get_or_create(id=category['id'], name=category['name'])
        category_object.shops.add(shop.id)
        category_object.save()

    ProductInfo.objects.filter(shop_id=shop.id).delete()
    for item in data['goods']:
        product, _ = Product.objects.get_or_create(name=item['name'], category_id=item['category'])

        product_info = ProductInfo.objects.create(
            product_id=product.id,
            external_id=item['id'],
            model=item['model'],
            price=item['price'],
            price_rrc=item['price_rrc'],
            quantity=item['quantity'],
            shop_id=shop.id,
        )
        for name, value in item['parameters'].items():
            parameter_object, _ = Parameter.objects.get_or_create(name=name)
            ProductParameter.objects.create(
                product_info_id=product_info.id, parameter_id=parameter_object.id, value=value
            )
