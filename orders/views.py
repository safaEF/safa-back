import csv

from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView,ListAPIView,GenericAPIView
from testproject.pagination import CustomPagination
from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer
from users.authentication import JWTAuthentication

class OrderGenericAPIView(GenericAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
class GetAllOrder(OrderGenericAPIView,ListAPIView):
   pagination_class = CustomPagination
class GetanOrder(OrderGenericAPIView,RetrieveAPIView):
    lookup_field = "id"	
    lookup_url_kwarg ="pk"

class ExportAPIView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="order.csv"'
        

        orders = Order.objects.all()
        writer = csv.writer(response)

        writer.writerow(['ID', 'Name', 'Email', 'Product Title', 'Price', 'Quantity','\n' ])


        for order in orders:
            print("order",order)
            
            writer.writerow([order.id, order.name, order.email, '\n'])
            orderItems = OrderItem.objects.all().filter(order_id=order.id)

            print(orderItems)

            for item in orderItems:
                print("items",item)
                writer.writerow(["    ", item.product_title, item.price, item.quantity,'\n'])
        
        return response


class ChartAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, _):
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT DATE_FORMAT(o.created_at, '%Y-%m-%d') as date, sum(i.quantity * i.price) as sum
            FROM orders_order as o
            JOIN orders_orderitem as i ON o.id = i.order_id
            GROUP BY date
            """)


            row = cursor.fetchall()

        data = [{
            'date': result[0],
            'sum': result[1]
        } for result in row]

        return Response({
            'data': data
        })