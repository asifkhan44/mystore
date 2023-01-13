from django.shortcuts import render
from django.views.generic import View
from owner.forms import LoginForm, RegisterForm, ProductForm
from django.contrib.auth.models import User

# Create your views here.
class HomeView(View):
    def get(self,request,*args,**kw):
        return render(request,'home.html')

class SignUpView(View):
    def get(self,request,*args,**kw):
        form=RegisterForm()
        return render(request,'register.html',{'form':form})
    def post(self,request,*args,**kw):
        form=RegisterForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            return render(request,'login.html')
        else:
            return render(request,'register.html',{'form':form})


class SignInView(View):
    def get(self, request,*args, **kw):
        form=LoginForm()
        return render(request, 'login.html',{'form':form})

    def post(self,request):
        print(request.POST.get('username'))
        print(request.POST.get('password'))
        return render(request,'home.html')

class ProductAddView(View):
    def get(self,request,*args,**kw):
        form=ProductForm()
        return render(request,'create-product.html',{'form':form})

    def post(self,request,*args,**kw):
        form=ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,'create-product.html')
        else:
            return render(request,'create-product.html',{'form':form})