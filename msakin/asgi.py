# import os
# from channels.routing import get_default_application
# # from channels.auth import AuthMiddlewareStack
# # from channels.security.websocket import AllowedHostsOriginValidator
# # from chat.consumers import ChatConsumer
# # from django.urls import re_path

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'msakin.settings')


# application = get_default_application()
# المحتوى الصحيح لـ /app/msakin/asgi.py
import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

# 1. تحديد متغير بيئة ملف الإعدادات
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'msakin.settings') # <-- تأكد من اسم الإعدادات الصحيح

# 2. تهيئة Django بشكل صريح - !!مهم جداً!!
django.setup()

# 3. استيراد ملفات التوجيه بعد التهيئة
import notifications.routing # <-- تأكد من المسار الصحيح

# 4. تعريف الـ application
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(
        notifications.routing.websocket_urlpatterns # <-- تأكد من اسم المتغير الصحيح
    ),
})

# import os
# import django
# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.core.asgi import get_asgi_application

# # 1. تعيين متغير بيئة الإعدادات أولاً
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'msakin.settings') # <--- تأكد من أن 'msakin.settings' هو المسار الصحيح لملف الإعدادات

# # 2. استدعاء django.setup() لتهيئة Django وتحميل التطبيقات
# #    هذه الخطوة مهمة جدًا قبل استيراد أي شيء يعتمد على نماذج Django
# #    أو إعدادات Channels التي قد تستورد نماذج بشكل غير مباشر.
# django.setup()

# # 3. الآن يمكنك استيراد كود التوجيه الخاص بـ Channels بأمان
# #    لأن django.setup() قد تم استدعاؤه بالفعل.
# import notifications.routing # أو أي ملف routing آخر تستخدمه

# # 4. إعداد تطبيق ASGI
# application = ProtocolTypeRouter({
#     # معالج HTTP الأساسي لـ Django (يجب أن يأتي أولاً في كثير من الحالات)
#     "http": get_asgi_application(),

#     # معالج WebSocket (أو بروتوكولات أخرى)
#     "websocket": URLRouter(
#         # قائمة بأنماط URL الخاصة بـ WebSocket
#         notifications.routing.websocket_urlpatterns
#         # يمكنك إضافة قوائم أخرى من تطبيقات مختلفة هنا
#         # other_app.routing.websocket_urlpatterns,
#     ),
#     # يمكنك إضافة معالجات بروتوكولات أخرى هنا
# })

# # ملاحظة: إذا كنت لا تستخدم Channels وتحتاج فقط إلى ASGI الأساسي لـ Django:
# # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'msakin.settings')
# # application = get_asgi_application()
# # في هذه الحالة، الخطأ غالبًا ما يحدث بسبب استيراد نماذج في مكان آخر يتم تحميله مبكرًا.