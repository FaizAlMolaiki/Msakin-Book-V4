from django.contrib import admin
from .models import Property, PropertyImage, PropertyRequest, PropertyLike, PropertyComment, CommentLike, UserFollow, Chat, Message, Governorate, District

@admin.register(Governorate)
class GovernorateAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'governorate')
    list_filter = ('governorate',)
    search_fields = ('name', 'governorate__name')

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'property_type', 'listing_type', 'price', 'currency', 'governorate', 'district', 'is_available')
    list_filter = ('property_type', 'listing_type', 'is_available', 'governorate', 'district')
    search_fields = ('title', 'description', 'location')
    raw_id_fields = ('owner',)

admin.site.register(PropertyImage)
admin.site.register(PropertyRequest)
admin.site.register(PropertyLike)
admin.site.register(PropertyComment)
admin.site.register(CommentLike)
admin.site.register(UserFollow)
admin.site.register(Chat)
admin.site.register(Message)
