
# 1. اختر صورة بايثون أساسية (استبدل 3.9 بالنسخة التي تستخدمها إذا لزم الأمر)
FROM python:3.9-slim

# 2. تعيين متغيرات البيئة
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. إنشاء وتحديد مجلد العمل
WORKDIR /app

# 4. تثبيت التبعيات
# نسخ ملف المتطلبات أولاً للاستفادة من التخزين المؤقت لـ Docker
COPY requirements.txt /app/
# تأكد من أن requirements.txt يحتوي على gunicorn
RUN pip install --no-cache-dir -r requirements.txt

# 5. نسخ كود المشروع بالكامل
COPY . /app/

# 6. تحديد المنفذ الذي ستستمع إليه الحاوية
EXPOSE 8000

# 7. الأمر الافتراضي لتشغيل التطبيق باستخدام Gunicorn
# !!! استبدل 'your_project_name' بالاسم الفعلي لمجلد مشروعك الذي يحتوي على wsgi.py !!!
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "msakin.asgi:application"]
# مثال لـ CMD في Dockerfile أو command في docker-compose.yml
# CMD ["uvicorn", "msakin.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "msakin.asgi:application"]

# --- بديل للتطوير فقط (إذا كنت تفضل خادم تطوير جانجو مؤقتًا) ---
# يمكنك التعليق على سطر CMD أعلاه وإلغاء تعليق السطرين التاليين
# EXPOSE 8000
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]