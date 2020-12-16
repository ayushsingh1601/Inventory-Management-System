from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User,auth
from .models import *
from .forms import *
from django.contrib import messages
import datetime
# Create your views here.
def index(request):
    return render(request,'index.html')
def inventorytable(request):
    king=request.user.username
    query_results = inventory.objects.filter(login_id=king)
    #query_results = inventory.objects.all()
    context = {
        'query_results' : query_results,
        'header' : 'Inventory Table'
    }
    return render(request,'inventorytable.html',context)
def suppliertable(request):
    king=request.user.username
    query_results2 = suppliers.objects.filter(login_id=king)
    context = {
        'query_results2' : query_results2,
        'header' : 'Suppliers'
    }
    return render(request,'suppliers.html',context)
def ordertable(request):
    king=request.user.username
    query_results3 = orders.objects.filter(login_id=king)
    context = {
        'query_results3' : query_results3,
        'header' : 'Orders Table'
    }
    return render(request,'orders.html',context)
def purchasetable(request):
    king=request.user.username
    query_results4 = purchases.objects.filter(login_id=king)
    context = {
        'query_results4' : query_results4,
        'header' :'Purchases Table'
    }
    return render(request,'purchases.html',context)
def to_ordertable(request):
    king=request.user.username
    query_results5 = to_order.objects.filter(login_id=king)
    context = {
        'query_results5' : query_results5,
        'header' : 'To_Order Table'
    }
    return render(request,'to_order.html',context)

def add_suppliers(request):
    if request.method == "POST":
        form = suppliersForm(request.POST)
        if form.is_valid():
            fs=form.save(commit=False)
            fs.login_id= request.user.username
            fs.save()
            return redirect('suppliertable')
    else:
        form = suppliersForm()
        return render(request,'add.html', {'form':form})
def add_inventory(request):
    if request.method == "POST":
        form = inventoryForm(request.POST)
        if form.is_valid():
            sid=request.POST['supplier_id']
            p=request.POST['price']
            si=request.POST['starting_inventory']
            mr=request.POST['minimum_required']
            user=request.user.username
            if suppliers.objects.filter(id=sid,login_id=user).exists():
                if int(p)>=0 and int(si)>=0 and int(mr)>=0:  
                    fs=form.save(commit=False)
                    fs.login_id= request.user.username
                    fs.save()
                    return redirect('inventorytable')
                else:
                    messages.info(request,'Do not enter negative values')
                    return redirect('add_inventory')
            else:
                messages.info(request,'No such supplier')
                return redirect('add_inventory')

    else:
        form = inventoryForm()
        return render(request,'add.html', {'form':form})
def add_orders(request):
    dt=datetime.datetime.now()+ datetime.timedelta(hours=5.5)
    dt1=str(dt)[0:19]
    if request.method == "POST":
        form = ordersForm(request.POST)
        if form.is_valid():
            sid=request.POST['product_id']
            ns=request.POST['number_shipped']
            user=request.user.username
            if inventory.objects.filter(id=sid,login_id=user).exists():
                if int(ns)>=0:
                    if int(ns)<=get_object_or_404(inventory,id=sid).current_inventory:
                        fs=form.save(commit=False)
                        fs.login_id= request.user.username
                        fs.order_date=dt1
                        fs.save()
                        mr=get_object_or_404(inventory,id=sid).minimum_required
                        if get_object_or_404(inventory,id=sid).current_inventory<get_object_or_404(inventory,id=sid).minimum_required:
                            too(fs.login_id,sid,mr)
                        return redirect('ordertable')
                    else:
                        messages.info(request,'Shipping more than currently present')
                        return redirect('add_orders')
                else:
                    messages.info(request,'Do not enter negative values')
                    return redirect('add_orders')
            else:
                messages.info(request,'No such product')
                return redirect('add_orders')
    else:
        form = ordersForm()
        return render(request,'add.html', {'form':form})
def add_purchases(request):
    dt=(datetime.datetime.now()+ datetime.timedelta(hours=5.5))
    dt1=str(dt)[0:19]
    if request.method == "POST":
        form = purchasesForm(request.POST)
        if form.is_valid():
            pid=request.POST['product_id']
            pidi=get_object_or_404(inventory,id=pid).model_number
            nr=request.POST['number_received']
            user=request.user.username
            if to_order.objects.filter(model_number=pidi,login_id=user).exists():
                if int(nr)>=0:  
                        fs=form.save(commit=False)
                        fs.login_id= request.user.username
                        fs.date=dt1
                        fs.save()
                        check(fs.login_id,pidi,int(nr))
                        return redirect('purchasetable')
                else:
                        messages.info(request,'Do not enter negative values')
                        return redirect('add_purchases')
            else:
                messages.info(request,'Product does not exist in To-order table')
                return redirect('add_purchases')
    else:
        form = purchasesForm()
        return render(request,'add.html', {'form':form})
def check(l_id,pidi,nr):
    item=get_object_or_404(to_order,model_number=pidi).number
    si=get_object_or_404(to_order,model_number=pidi).supplier_id
    if nr>=int(item):
        to_order.objects.filter(model_number=pidi).delete()
    else:
        to_order.objects.filter(model_number=pidi).delete()
        form=to_order(login_id=l_id,supplier_id=si,model_number=pidi,number=int(item)-nr)
        form.save()


def too(l_id,product_id,number):
    si=get_object_or_404(inventory,id=product_id).supplier_id
    mn=get_object_or_404(inventory,id=product_id).model_number
    form=to_order(login_id=l_id,supplier_id=si,model_number=mn,number=number)
    form.save()

def add_to_order(request):
    if request.method == "POST":
        form = to_orderForm(request.POST)
        if form.is_valid():
            sid=request.POST['supplier_id']
            pid=request.POST['model_number']
            n=request.POST['number']
            if suppliers.objects.filter(id=sid).exists():
                if inventory.objects.filter(model_number=pid).exists():
                    if int(n)>=0:  
                        fs=form.save(commit=False)
                        fs.login_id= request.user.username
                        fs.save()
                        return redirect('to_ordertable')
                    else:
                        messages.info(request,'Do not enter negative values')
                        return redirect('add_to_order')
                else:
                    messages.info(request,'model number does not exists')
                    return redirect('add_to_order')
            else:
                messages.info(request,'No such supplier')
                return redirect('add_to_order')
    else:
        form = to_orderForm()
        return render(request,'add.html', {'form':form})


def edit_inventory(request,pk):
    item =  get_object_or_404(inventory,pk = pk)
    if request.method == "POST":
        form = inventoryForm(request.POST,instance=item)
        if form.is_valid():
            sid=request.POST['supplier_id']
            p=request.POST['price']
            si=request.POST['starting_inventory']
            mr=request.POST['minimum_required']
            if suppliers.objects.filter(id=sid).exists():
                if int(p)>=0 and int(si)>=0 and int(mr)>=0:  
                    fs=form.save(commit=False)
                    fs.login_id= request.user.username
                    fs.save()
                    return redirect('inventorytable')
                else:
                    messages.info(request,'Do not enter negative values')
                    return redirect('add_inventory')

            else:
                messages.info(request,'No such supplier')
                return redirect('add_inventory')
    else:
        form = inventoryForm(instance=item)
        return render(request,'edit_item.html', {'form':form})
def edit_orders(request,pk):
    item = get_object_or_404(orders,pk = pk)
    if request.method == "POST":
        form = ordersForm(request.POST,instance=item)
        if form.is_valid():
            fs=form.save(commit=False)
            fs.login_id= request.user.username
            fs.save()
            return redirect('ordertable')           
    else:
        form = ordersForm(instance=item)
        return render(request,'edit_item.html', {'form':form})
                    
def edit_suppliers(request,pk):
    item =  get_object_or_404(suppliers,pk = pk)
    if request.method == "POST":
        form = suppliersForm(request.POST,instance=item)
        if form.is_valid():
            form.save()
            return redirect('suppliertable')
    else:
        form = suppliersForm(instance=item)
        return render(request,'edit_item.html', {'form':form})

def edit_purchases(request,pk):
    item =  get_object_or_404(purchases,pk = pk)
    if request.method == "POST":
        form = purchasesForm(request.POST,instance=item)
        if form.is_valid():
            form.save()
            return redirect('purchasetable')
    else:
        form = purchasesForm(instance=item)
        return render(request,'edit_item.html', {'form':form})
def edit_to_order(request,pk):
    item =  get_object_or_404(to_order,pk = pk)
    if request.method == "POST":
        form = to_orderForm(request.POST,instance=item)
        if form.is_valid():
            form.save()
            return redirect('to_ordertable')
    else:
        form = to_orderForm(instance=item)
        return render(request,'edit_item.html', {'form':form})
        
def delete_inventory(request,pk):
    inventory.objects.filter(id=pk).delete()
    return redirect('inventorytable')
def delete_orders(request,pk):
    pid=get_object_or_404(orders,id=pk).product_id
    oc=get_object_or_404(inventory,id=pid).current_inventory
    mr=get_object_or_404(inventory,id=pid).minimum_required
    orders.objects.filter(id=pk).delete()
    nc=get_object_or_404(inventory,id=pid).current_inventory
    if oc<mr and nc>=mr:
        mn=get_object_or_404(inventory,id=pid).model_number
        to_order.objects.filter(model_number=mn).delete()
    return redirect('ordertable')
def delete_purchases(request,pk):
    purchases.objects.filter(id=pk).delete()
    return redirect('purchasetable')
def delete_suppliers(request,pk):
    suppliers.objects.filter(id=pk).delete()
    return redirect('suppliertable')
def delete_to_order(request,pk):
    to_order.objects.filter(id=pk).delete()
    return redirect('to_ordertable')
def search(request):
    king=request.user.username
    if request.method=='POST':
        c=request.POST['var']
        query_results=inventory.objects.filter(model_number=c,login_id=king)
        return render(request,'inventorytable.html',{'query_results':query_results})
    else:
        return redirect('inventorytable')
def search1(request):
    king=request.user.username
    if request.method=='POST':
        c=request.POST['var']
        query_results=inventory.objects.filter(model_name=c,login_id=king)
        return render(request,'inventorytable.html',{'query_results':query_results})
    else:
        return redirect('inventorytable')
def search2(request):
    king=request.user.username
    if request.method=='POST':
        c=request.POST['var']
        query_results=inventory.objects.filter(brand=c,login_id=king)
        return render(request,'inventorytable.html',{'query_results':query_results})
    else:
        return redirect('inventorytable')   