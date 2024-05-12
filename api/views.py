from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from api.serializers import VendorSerializer, PurchaseOrderSerializer,HistoricalPerformance,HistoricalPerformanceSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Vendor
from .serializers import VendorSerializer,PurchaseOrderUpdateSerializer


class VendorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class RetrieveVendorAPIView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class UpdateVendorAPIView(generics.UpdateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class DeleteVendorAPIView(generics.DestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class CreatePurchaseOrderAPIView(generics.CreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer


@api_view(['GET','POST'])
def purchase_order(request):
    if request.method=='GET':
        queryset=PurchaseOrder.objects.all()
        serializers=PurchaseOrderSerializer(queryset,many=True)
        return Response(serializers.data)
    elif request.method=='POST':
        data=request.data
        seri=PurchaseOrderSerializer(data=data)
        if seri.is_valid():
            seri.save()
            return Response(seri.data)
        return Response(seri._errors)
 
@api_view(['GET', 'PUT', 'DELETE','PATCH'])
def purchase_order_detail(request, po_id):
    try:
        purchase_order = PurchaseOrder.objects.get(pk=po_id)
    except PurchaseOrder.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PurchaseOrderSerializer(purchase_order)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PurchaseOrderSerializer(purchase_order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PATCH':
        serializer = PurchaseOrderSerializer(purchase_order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    elif request.method == 'DELETE':
        purchase_order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
def vendor_performance(request, vendor_id):
    try:
        vendor = Vendor.objects.get(pk=vendor_id)
        vendor_serializer = VendorSerializer(vendor)
        
        historical_performance = HistoricalPerformance.objects.filter(vendor=vendor)
        historical_performance_serializer = HistoricalPerformanceSerializer(historical_performance, many=True)
        
        return Response({
            'current_performance': vendor_serializer.data,
            'historical_performance': historical_performance_serializer.data
        })
    except Vendor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)



def vendor_performance_metrics(request, vendor_id):
    try:
        vendor = Vendor.objects.get(pk=vendor_id)
    except Vendor.DoesNotExist:
        return Response({'error': 'Vendor not found'}, status=404)
    
    # Calculate performance metrics
    performance_metrics = {
        'on_time_delivery_rate': vendor.on_time_delivery_rate,
        'quality_rating_avg': vendor.quality_rating_avg,
        'average_response_time': vendor.average_response_time,
        'fulfillment_rate': vendor.fulfillment_rate,
    }
    
    return Response(performance_metrics)

class PurchaseOrderUpdateAPIView(generics.UpdateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderUpdateSerializer