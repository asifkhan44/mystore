from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers import ProductsSerializer,ProductModelSerializer,UserSerializer,CartSerializer,ReviewsSerializer
from api.models import Products,Carts,Reviews
from rest_framework import viewsets
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework import authentication,permissions


# Create your views here.
class ProductView(APIView):
    def get(self,request,*args,**kwargs):
        qs=Products.objects.all()
        serializer=ProductsSerializer(qs,many=True)

        return Response(data=serializer.data)

    def post(self,request,*args,**kwargs):
        serializer=ProductsSerializer(data=request.data)
        if serializer.is_valid():
            Products.objects.create(**serializer.validated_data)
            return Response(serializer.data)
        else:
            return Response(data=serializer.errors)



class ProductDetailView(APIView):

    def get(self,request,*args,**kwargs):
        id=kwargs.get('id')
        qs=Products.objects.get(id=id)
        serializer=ProductsSerializer(qs,many=False)
        return Response(data=serializer.data)

    def put(self,request,*args,**kwargs):
        id=kwargs.get('id')
        Products.objects.filter(id=id).update(**request.data)
        qs=Products.objects.get(id=id)
        serializer=ProductsSerializer(qs,many=False)
        return Response(data=serializer.data)

    def delete(self,request,*args,**kwargs):
        id=kwargs.get('id')
        Products.objects.filter(id=id).delete()
        return Response(data='Product Deleted..!!')


class ProductViewSetView(viewsets.ModelViewSet):
    serializer_class = ProductModelSerializer
    queryset = Products.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    # def list(self,request,*args,**kwargs):
    #     qs=Products.objects.all()
    #     serializer=ProductModelSerializer(qs,many=True)
    #     return Response(data=serializer.data)
    #
    # def create(self,request,*args,**kwargs):
    #     serializer=ProductModelSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(serializer.errors)
    #
    # def retrieve(self,request,*args,**kwargs):
    #     id=kwargs.get('pk')
    #     qs=Products.objects.get(id=id)
    #     serializer=ProductModelSerializer(qs,many=False)
    #     return Response(data=serializer.data)
    #
    # def destroy(self,request,*args,**kwargs):
    #     id=kwargs.get('pk')
    #     Products.objects.filter(id=id).delete()
    #     return Response(data="Product Deleted''!!")
    #
    # def update(self,request,*args,**kwargs):
    #     id=kwargs.get('pk')
    #     obj=Products.objects.get(id=id)
    #     serializer=ProductModelSerializer(data=request.data, instance=obj)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)


#implementation of custom methods in views
#custom method for categories only view

    @action(methods=['GET'],detail=False)
    def categories(self,request,*args,**kwargs):
        cat=Products.objects.values_list('category',flat=True).distinct()
        return Response(data=cat)

    @action(methods=['POST'],detail=True)
    def add_to_cart(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        item=Products.objects.get(id=id)
        user=request.user
        user.carts_set.create(product=item)
        return Response(data="Item Added")

    @action(methods=['POST'],detail=True)
    def add_review(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        item=Products.objects.get(id=id)
        user=request.user
        serializer=ReviewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=item, user=user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    @action(methods=['GET'], detail=True)
    def reviews(self,request,*args,**kwargs):
        product=self.get_object()
        qs=product.reviews_set.all()
        serializer=ReviewsSerializer(qs,many=True)
        return Response(data=serializer.data)





class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # def create(self,request,*args,**kwargs):
    #     serializer=UserSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)

class CartView(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    queryset = Carts.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        return self.request.user.carts_set.all()

    # def list(self, request, *args, **kwargs):
    #     qs=request.user.carts_set.all()
    #     serializer=CartSerializer(qs,many=True)
    #     return Response(data=serializer.data)


    # def list(self, request, *args, **kwargs):


