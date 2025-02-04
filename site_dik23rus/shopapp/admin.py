from decimal import Decimal
from io import TextIOWrapper
from csv import DictReader
from django.contrib import admin, messages
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import path

from django.contrib.auth.models import User
from .models import Product, Order, ProductImage
from .forms import CSVImportform


class OrderInline(admin.TabularInline):
    model = Product.orders.through

class ProductInline(admin.StackedInline):
    model = ProductImage


@admin.action(description='Archived selected products')
def make_archived(adminmodel: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)


@admin.action(description='Unarchived selected products')
def make_unarchived(adminmodel: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    change_list_template = "shopapp/product_change_list.html"
    actions = [make_archived, make_unarchived]
    fieldsets = (
        ('General', {
            'fields': ('name', 'description')
        }),
        ('Financial', {
            'fields': ('price', 'discount', 'created_by'),
            'classes': ('collapse', 'wide',),
        }),
        ('Images', {
            'fields': ('preview',),
        }),
        ('Extra Options', {
            'fields': ('archived',),
            'classes': ('collapse',),
        })
    )
    inlines = [
        OrderInline,
        ProductInline,
    ]
    list_display = "pk", "name", "description_short", "price", "discount", "archived",
    list_display_links = "pk", "name"
    ordering = "pk", "name"
    search_fields = "name", "price"

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == "GET":
            form = CSVImportform()
            context = {
                "form": form,
            }
            return render(request, "admin/csv_form.html", context)
        form = CSVImportform(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                "form": form,
            }
            return render(request, "admin/csv_form.html", context, status=400)
        
        csv_file = TextIOWrapper(
            form.files["csv_file"].file,
            encoding=request.encoding,
        )
        reader = DictReader(csv_file)

        try:
            for row in reader:
                try:
                    price_str=row["price"].strip()
                    price = Decimal(price_str)
                except (ValueError, KeyError) as e:
                    self.message_user(request, f"Ошибка в строке {row}: неверный формат цены", level=messages.ERROR)
                    continue

                product=Product(
                    name=row["name"],
                    description=row["description"],
                    price=price,
                    discount=int(row["discount"]),
                    created_by=request.user
                )
                product.save()
            
            self.message_user(request, "Товары успешно ипортированы", level=messages.SUCCESS)
        except Exception as e:
            self.message_user(request, f"Ошибка при импорте: {str(e)}", level=messages.ERROR)

        return redirect("..")
    
    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path(
                "import-products-csv",
                self.import_csv,
                name="admin_product_csv",
            ),
        ]
        return new_urls + urls



class ProductInline(admin.TabularInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    change_list_template = "shopapp/order_change_list.html"
    inlines = [
        ProductInline,
    ]
    list_display = "delivery_adress", "promocode", "created_at", "user_verbose"

    def get_queryset(self, request):
        return Order.objects.select_related("user").prefetch_related("products")

    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username
    
    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == "GET":
            form = CSVImportform()
            context = {
                "form": form,
            }
            return render(request, "admin/csv_form.html", context)
        form = CSVImportform(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                "form": form,
            }
            return render(request, "admin/csv_form.html", context, status=400)
        csv_file = TextIOWrapper(
            form.files['csv_file'].file,
            encoding=request.encoding,
        )
        reader = DictReader(csv_file)
        try:
            for row in reader:
                print(row["delivery_adress"])
                print(row["user"])
                # Получаем пользователя по имени
                user = User.objects.get(username=row["user"])

                # Создаем заказ
                order = Order(
                    delivery_adress=row["delivery_adress"],
                    promocode=row["promocode"],
                    user=user,
                )
                order.save() # Сохраняем заказ для получения его ID

                # Добавляем товары к заказу
                product_names = row["products"].split(",") # Если товары перечислены через запятую,
                                                           # они будут разделены по этому знаку
                for product_name in product_names:
                    product = Product.objects.get(name=product_name.strip())
                    order.products.add(product)
            
            self.message_user(request, "Заказы успешно импортированы", level=messages.SUCCESS)

        except Exception as e:
            self.message_user(request, f"Ошибка при импорте: {str(e)}", level=messages.ERROR)

        return redirect("..")

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path(
                "import-orders-csv",
                self.import_csv,
                name="admin_orders_csv",
            ),
        ]
        return new_urls + urls