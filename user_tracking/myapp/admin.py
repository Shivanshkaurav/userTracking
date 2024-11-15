from django.contrib import admin
from .models import TodoTracking, Product, Order, CustomerProfile

class TrackableAdmin(admin.ModelAdmin):
    """
    Custom admin to pass the logged-in user to the model instance
    before saving.
    """
    def save_model(self, request, obj, form, change):
        # Set the user on the object being saved
        if not hasattr(obj, 'user') or not obj.user:
            obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'description', 'price', 'stock')
    search_fields = ('name', 'user__username')
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'quantity', 'status', 'order_date')
    search_fields = ('customer__username', 'product__name')

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'phone_number')
    search_fields = ('user__username', 'address')

@admin.register(TodoTracking)
class TodoTrackingAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'model_name', 'timestamp', 'details')
    list_filter = ('action', 'timestamp')
    search_fields = ('user__username', 'details')

    def get_readonly_fields(self, request, obj=None):
        """
        Make all fields read-only in the admin panel.
        """
        return [field.name for field in self.model._meta.fields]

    def has_add_permission(self, request):
        """
        Disable the add functionality.
        """
        return False

    def has_change_permission(self, request, obj=None):
        """
        Disable the edit functionality.
        """
        return False

    def has_delete_permission(self, request, obj=None):
        """
        Disable the delete functionality.
        """
        return True