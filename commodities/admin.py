from django.contrib import admin;
from .models import CommodityType, Commodity, Hotel, Restaurant;

admin.site.register(CommodityType);
admin.site.register(Commodity);
admin.site.register(Hotel);
admin.site.register(Restaurant);


