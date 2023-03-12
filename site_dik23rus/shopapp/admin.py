from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from .models import Product, Order


class OrderInline(admin.TabularInline):
    model = Product.orders.through


@admin.action(description='Archived selected products')
def make_archived(adminmodel: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)


@admin.action(description='Unarchived selected products')
def make_unarchived(adminmodel: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    actions = [make_archived, make_unarchived]
    fieldsets = (
        ('General', {
            'fields': ('name', 'description')
        }),
        ('Financial', {
            'fields': ('price', 'discount', 'created_by'),
            'classes': ('collapse', 'wide',),
        }),
        ('Extra Options', {
            'fields': ('archived',),
            'classes': ('collapse',),
        })
    )
    inlines = [
        OrderInline,
    ]
    list_display = "pk", "name", "description_short", "price", "discount", "archived",
    list_display_links = "pk", "name"
    ordering = "pk", "name"
    search_fields = "name", "price"




class ProductInline(admin.TabularInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ProductInline,
    ]
    list_display = "delivery_adress", "promocode", "created_at", "user_verbose"

    def get_queryset(self, request):
        return Order.objects.select_related("user").prefetch_related("products")

    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username