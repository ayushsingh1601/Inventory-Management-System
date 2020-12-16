from django.contrib import admin
from django.conf.urls import url
from django.urls import path,include
from . import views
from .views import *

urlpatterns = [
   path('',views.index,name="index"),
   path('inventorytable',views.inventorytable,name="inventorytable"),
   path('suppliertable',views.suppliertable,name="suppliertable"),  
   path('ordertable',views.ordertable,name="ordertable"),  
   path('purchasetable',views.purchasetable,name="purchasetable"),   
   path('to_ordertable',views.to_ordertable,name="to_ordertable"),   
   path('search',views.search,name="search"),  
   path('search1',views.search1,name="search1"),  
   path('search2',views.search2,name="search2"),   

   path('add_orders',views.add_orders,name="add_orders"),
   path('add_suppliers',views.add_suppliers,name="add_suppliers"),
   path('add_purchases',views.add_purchases,name="add_purchases"),
   path('add_inventory',views.add_inventory,name="add_inventory"),
   path('add_to_order',views.add_to_order,name="add_to_order"),

   url(r'^edit_inventory/(?P<pk>\d+)$' , edit_inventory, name="edit_inventory"),
   url(r'^edit_orders/(?P<pk>\d+)$' ,edit_orders,name="edit_orders"),
   url(r'^edit_purchases/(?P<pk>\d+)$' ,edit_purchases,name="edit_purchases"),
   url(r'^edit_suppliers/(?P<pk>\d+)$' ,edit_suppliers,name="edit_suppliers"),
   url(r'^edit_to_order/(?P<pk>\d+)$' ,edit_to_order,name="edit_to_order"),


   url(r'^delete_inventory/(?P<pk>\d+)$' , delete_inventory, name="delete_inventory"),
   url(r'^delete_orders/(?P<pk>\d+)$' ,delete_orders,name="delete_orders"),
   url(r'^delete_purchases/(?P<pk>\d+)$' ,delete_purchases,name="delete_purchases"),
   url(r'^delete_suppliers/(?P<pk>\d+)$' ,delete_suppliers,name="delete_suppliers"),
   url(r'^delete_to_order/(?P<pk>\d+)$' ,delete_to_order,name="delete_to_order"),
]
