from django.shortcuts import render
from django.db.models import Q
from rest_framework import generics
from rest_framework.response import Response
from product.models import Department , Basic_Info , PriceCost
from product.serializers import DepartmentSerializer , BasicInfoSerializer , PriceCostSerializer


class ListAPIView(generics.GenericAPIView):
    queryset = Basic_Info.objects.select_related('department_id').all()
    def get(self,request):
        items = self.get_queryset()

        search_query = request.query_params.get('search', None)

        if search_query:
            items = items.filter(Q(product_name__icontains=search_query) | Q(sku__icontains=search_query) | Q(department_id__name__icontains=search_query))

        sort_by = request.query_params.get('sort_by', None)
        sort_order = request.query_params.get('sort_order', None)

        if sort_by:
            if sort_order == 'descending':
                sort_by = '-' + sort_by
            items = items.order_by(sort_by)

        basic_info_serializer = BasicInfoSerializer(items, many=True).data
        department_serializer = DepartmentSerializer([item.department_id for item in items], many=True).data
        price_cost_serializer = []
        for item in items:
            price_cost_serializer.extend(PriceCostSerializer(item.pricecost_set.all(), many=True).data)
        
        context = [
            {
                "basic_info": basic_info,
                "department": department,
                "price_cost": price_cost,
            }
        for basic_info, department, price_cost in zip(basic_info_serializer, department_serializer, price_cost_serializer)
]


        return Response(context)