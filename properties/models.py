from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Governorate(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Governorate Name'))
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Governorate')
        verbose_name_plural = _('Governorates')

class District(models.Model):
    governorate = models.ForeignKey(Governorate, on_delete=models.CASCADE, related_name='districts')
    name = models.CharField(max_length=100, verbose_name=_('District Name'))
    
    def __str__(self):
        return f"{self.name} - {self.governorate.name}"
    
    class Meta:
        verbose_name = _('District')
        verbose_name_plural = _('Districts')

class Property(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('apartment', _('شقة')),
        ('house', _('منزل')),
        ('villa', _('فلة')),
        ('land', _('أرض')),
        ('commercial', _('دكان')),
    ]


    LISTING_TYPE_CHOICES = [
        ('sale', _('للبيع')),
        ('rent', _('للإجار')),
    ]

    CURRENCY_CHOICES = [
        ('YER', _('ريال يمني ')),
        ('USD', _('دولار')),
        ('SAR', _(' ريال سعودي')),
    ]
    area_meas=[
        ('meter',_('متر مربع')),
        ('labinh',_( 'لبنه')),
        ('q',_( 'قصبة')),


    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=200)
    description = models.TextField()
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES)
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='YER')
    halls_count = models.PositiveIntegerField(verbose_name=_('Number of Halls'), default=0)
    councils_count = models.PositiveIntegerField(verbose_name=_('Number of Councils'), default=0)
    rooms_count = models.PositiveIntegerField(verbose_name=_('Number of Rooms'), default=0)
    area = models.DecimalField(max_digits=10, decimal_places=2)
    area_measurment= models.CharField(max_length = 20,choices=area_meas)
    
    # Location fields
    governorate = models.ForeignKey(Governorate, on_delete=models.SET_NULL, null=True, related_name='properties')
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, related_name='properties')
    neighborhood = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('Neighborhood/Street'))
    map_location = models.CharField(max_length=500, blank=True, null=True, verbose_name=_('Map Location'))
    
    # Room details
    bedrooms = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('Number of Bedrooms'))
    living_rooms = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('Number of Living Rooms'))
    bathrooms = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('Number of Bathrooms'))
    kitchens = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('Number of Kitchens'))
    majlis = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('Number of Majlis'))
    
    # Specific property details
    floor_number = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('Floor Number'))  # For apartments
    number_of_floors = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('Number of Floors'))  # For houses
    
    
    location = models.CharField(max_length=200)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)
    views_count = models.PositiveIntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name='liked_properties', blank=True)

    class Meta:
        verbose_name_plural = 'Properties'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/')
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_primary', '-created_at']

class PropertyRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='property_requests')
    property_type = models.CharField(max_length=20, choices=Property.PROPERTY_TYPE_CHOICES)
    listing_type = models.CharField(max_length=10, choices=Property.LISTING_TYPE_CHOICES)
    preferred_location = models.CharField(max_length=200)
    max_price = models.DecimalField(max_digits=12, decimal_places=2)
    min_area = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s request for {self.property_type}"

class PropertyLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='property_likes')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'property')

class PropertyComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='property_comments')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    liked_by = models.ManyToManyField(User, related_name='liked_comments', through='CommentLike')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.user.username} on {self.property.title}'

class CommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_likes')
    comment = models.ForeignKey(PropertyComment, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'comment')

class UserFollow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

class Chat(models.Model):
    participants = models.ManyToManyField(User, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='property_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Message from {self.sender} in {self.chat}"
