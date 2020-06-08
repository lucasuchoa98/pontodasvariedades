from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
        #Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
	path('product/<slug>/', views.ItemDetailView.as_view(), name='product'),
	path('search/', views.SearchResultsView.as_view(), name='search_results'),
]

#path('contato/', views.ContatoView.as_view(), name='contato'),