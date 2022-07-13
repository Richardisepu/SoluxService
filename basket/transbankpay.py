import random
from django.http import HttpResponse, JsonResponse

from django.shortcuts import render
from transbank.error.transbank_error import TransbankError
from transbank.webpay.webpay_plus.transaction import Transaction
from django.views.decorators.csrf import csrf_exempt
import datetime as dt
from transbank.common.options import WebpayOptions
from django.contrib.auth.decorators import login_required

from orders.models import Order, OrderItem

from .basket import Basket

@login_required
def webpay_plus_create(request):
    basket = Basket(request)
    print("Webpay Plus Transaction.create")
    buy_order = str(random.randrange(1000000, 99999999))
    session_id = str(random.randrange(1000000, 99999999))
    total = basket.get_total_price()
    amount = total
    
    return_url = request.build_absolute_uri(location='commit-pay/')

    print('buy_order: {0}'.format(buy_order))
    print('session_id: {0}'.format(session_id))
    print('amount: {0}'.format(amount))
    print('return_url: {0}'.format(return_url))
    print('request.headers: {0}'.format(request.headers))
    response = (Transaction()).create(buy_order, session_id, amount,return_url)

    print('response: {0}'.format(response))

    return render(request,'plus/send-pay.html', {'response': response})
    # return render(request, 'plus/send-pay.html', {'response': response, 'amount': amount})     

@csrf_exempt 
def commitpay(request):
    basket = Basket(request)
    token = request.GET.get('token_ws')
    
    print("commit for token_ws: {}".format(token))

    response = (Transaction()).commit(token=token)
    print("response: {}".format(response))
    order_key = response.buy_order

    if response.status == 'AUTHORIZED' and response.response_code == 0:
            payment_confirmation(order_key)
            state = ''
            if response.status == 'AUTHORIZED':
                state = 'Aceptado'
            pay_type = ''
            if response.payment_type_code == 'VD':
                pay_type = 'Tarjeta de Débito'
            amount = int(response.amount)
            amount2 = f'{amount:,.0f}'.replace(',', '.')
            transaction_date = dt.datetime.strptime(response.transaction_date, '%Y-%m-%dT%H:%M:%S.%fZ')
            transaction_date = '{:%d-%m-%Y %H:%M:%S}'.format(transaction_date)
            transaction_detail = {  'card_number': response.card_detail,
                                    'transaction_date': transaction_date,
                                    'state': state,
                                    'pay_type': pay_type,
                                    'amount': amount2,
                                    'authorization_code': response.authorization_code,
                                    'buy_order': response.buy_order, }
            
            user_id = request.user.id
            print(user_id)
            print(order_key)

            # Check if order exists
            if Order.objects.filter(order_key=order_key).exists():
                pass
            else:                
                order = Order.objects.create(user_id=user_id, total_paid=amount, order_key=order_key)
                order_id = order.pk
                Order.objects.filter(order_key=order_key).update(billing_status=True)
                print(order_id)

                for item in basket:
                    OrderItem.objects.create(order_id=order_id, product=item['product'], price=amount, quantity=item['qty'])

            return render(request, 'plus/commit-pay.html', {'transaction_detail': transaction_detail})
    else:
    #TRANSACCIÓN RECHAZADA            
        return HttpResponse('ERROR EN LA TRANSACCIÓN, SE RECHAZA LA TRANSACCIÓN.')

def payment_confirmation(data):
    
    return Order.objects.filter(order_key=data).update(billing_status=True)

def user_orders(request):
    user_id = request.user.id
    print("USERID: {}".format(user_id))
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    print("ORDER: {}".format(orders))
    return orders