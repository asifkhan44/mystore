from django.shortcuts import render, redirect
from django.views.generic import CreateView, FormView, TemplateView, ListView, DetailView
from django.urls import reverse_lazy
from customer.forms import RegistrationForm, LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from api.models import Products, Carts, Orders
from django.db.models import Sum
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
# Create your views here.

def signin_required(fn):
        def wrapper(request, *args, **kw):
                if not request.user.is_authenticated:
                        messages.error(request,'Please login to continue')
                        return redirect('signin')
                else:
                        return fn(request,*args, **kw)
        return wrapper

decs=[signin_required,never_cache]

class SignUpView(CreateView):
        template_name='signup.html'
        form_class=RegistrationForm
        success_url=reverse_lazy('signin')

        def form_valid(self, form):
                messages.success(self.request,'Account created')
                return super().form_valid(form)

        def form_invalid(self, form):
                messages.error(self.request,'Account creation failed')
                return super().form_invalid(form)


class SignInView(FormView):
        template_name='cust-signin.html'
        form_class=LoginForm

        def post(self,request,*args,**kw):
                form=LoginForm(request.POST)
                if form.is_valid():
                        uname=form.cleaned_data.get('username')
                        pwd=form.cleaned_data.get('password')
                        usr=authenticate(request,username=uname,password=pwd)
                        if usr:
                                login(request,usr)
                                return redirect('user-home')

                        else:
                                messages.error(request,'Invalid credentials')
                                return render(request,'cust-signin.html',{'form':form})


@method_decorator(decs, name='dispatch')
class HomeView(ListView):
        template_name='customer-index.html'
        model=Products
        context_object_name='products'

@method_decorator(decs, name='dispatch')
class ProductDetailView(DetailView):
        template_name='customer-productdetail.html'
        context_object_name='product'
        pk_url_kwarg='id'
        model=Products

decs
def addto_cart(request,*args,**kw):
        id=kw.get('id')
        product=Products.objects.get(id=id)
        user=request.user
        Carts.objects.create(user=user,product=product)
        messages.success(request,'Item added to cart')
        return redirect('user-home')

@method_decorator(decs, name='dispatch')       
class CartListView(ListView):
        model=Carts
        template_name='cart-list.html'
        context_object_name='carts'

        def get(self,request,*args,**kw):
                qs=Carts.objects.filter(user=request.user, status='in-cart')
                total=Carts.objects.filter(user=request.user, status='in-cart').aggregate(tot=Sum('product__price'))
                return render(request,'cart-list.html',{'carts':qs,'total':total})
        
        # def get_queryset(self):
        #         return Carts.objects.filter(user=self.request.user)

@method_decorator(decs, name='dispatch')
class OrderView(TemplateView):
        template_name='checkout.html'

        def get(self, request,*args,**kw):
                pid=kw.get('pid')
                qs=Products.objects.get(id=pid)
                return render(request,'checkout.html',{'product':qs,'cid':kw.get('cid'),'pid':pid})


        def post(self, request, *args, **kw):
                cid=kw.get('cid')
                pid=kw.get('pid')
                cart=Carts.objects.get(id=cid)
                product=Products.objects.get(id=pid)
                user=request.user
                mobile=request.POST.get('mobile')
                address=request.POST.get('address')
                Orders.objects.create(product=product, user=user, address=address, phone=mobile)
                cart.status='order-placed'
                cart.save()
                messages.success(request, 'Order has been placed')
                return redirect('user-home')

@method_decorator(decs, name='dispatch')
class MyOrdersView(ListView):
        model=Carts
        template_name='orders-list.html'
        context_object_name='orders'

        def get_queryset(self):
                return Orders.objects.filter(user=self.request.user)


decs
def cancelorder_view(request,*args,**kw):
        id=kw.get('id')
        Orders.objects.filter(id=id).update(status='cancelled')
        messages.success(request,'Order has been cancelled')
        return redirect('user-home')

decs
def logout_view(request, *args, **kw):
        logout(request)
        messages.success(request,"You've been successfully logged out")
        return redirect('signin')