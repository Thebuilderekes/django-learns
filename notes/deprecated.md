Here are the **major deprecations and breaking changes** across recent Django versions that affect day-to-day development:

## **Django 5.1+ (Critical Changes)**

### **STATICFILES_STORAGE & DEFAULT_FILE_STORAGE Removed**

The DEFAULT_FILE_STORAGE and STATICFILES_STORAGE settings are removed

**Old way (doesn't work in 5.1+):**
```python
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
```

**New way (must use in 5.1+):**
```python
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
    },
}
```

### **Model.save() Positional Arguments Deprecated**

Passing positional arguments to Model.save() and Model.asave() is deprecated in favor of keyword-only arguments

**Old:**
```python
book.save(False, True)  # Deprecated
```

**New:**
```python
book.save(force_insert=False, force_update=True)
```

### **CheckConstraint check → condition**

The check keyword argument of CheckConstraint is deprecated in favor of condition

**Old:**
```python
models.CheckConstraint(check=models.Q(price__gte=0), name='positive_price')
```

**New:**
```python
models.CheckConstraint(condition=models.Q(price__gte=0), name='positive_price')
```

### **Meta.index_together Removed**

The model's Meta.index_together option is removed

**Old:**
```python
class Meta:
    index_together = [['field1', 'field2']]
```

**New:**
```python
class Meta:
    indexes = [
        models.Index(fields=['field1', 'field2']),
    ]
```

### **Password Hashers Removed**

The django.contrib.auth.hashers.SHA1PasswordHasher, django.contrib.auth.hashers.UnsaltedSHA1PasswordHasher, and django.contrib.auth.hashers.UnsaltedMD5PasswordHasher are removed

These were insecure and should have been replaced long ago.

### **length_is Template Filter Removed**

The length_is template filter is removed

**Old:**
```html
{% if items|length_is:"3" %}
```

**New:**
```html
{% if items|length == 3 %}
```

## **Django 5.0 Changes**

### **Database Version Requirements**
- PostgreSQL 12+ (13+ in Django 5.1)
- MariaDB 10.5+
- SQLite 3.31.0+

### **Python Support**
- Django 5.0: Python 3.10+
- Django 5.1: Python 3.10, 3.11, 3.12, 3.13

## **Django 4.2 → 5.x Breaking Changes**

### **USE_TZ Behavior**
Now defaults to `True` - all datetimes should be timezone-aware

### **JSONField Encoded Strings**

Support for passing encoded JSON string literals to JSONField and associated lookups and expressions is removed

**Old:**
```python
Document.objects.create(data='"string"')  # JSON-encoded
```

**New:**
```python
Document.objects.create(data='string')  # Direct value
```

## **Common Patterns That Changed**

### **1. File Storage Configuration**
**Before Django 4.2:** Individual settings  
**Django 5.0+:** Must use `STORAGES` dict

### **2. Unique Constraints**
**Before:** `unique_together` in Meta  
**Now:** Use `UniqueConstraint` in `Meta.constraints`

### **3. Index Definition**
**Before:** `index_together` in Meta  
**Now:** Use `Index` in `Meta.indexes`

### **4. URL Converters**
Overriding converters with `register_converter()` is deprecated

### **5. Admin Changes**
- HTML structure changed for accessibility (uses semantic HTML5 tags)
- `collapse.js` removed
- Fieldsets now use `<details>` and `<summary>` tags

## **Quick Migration Checklist for Django 5.1+**

If you're upgrading to Django 5.1 or 5.2, check for:

✅ Replace `STATICFILES_STORAGE` with `STORAGES["staticfiles"]`  
✅ Replace `DEFAULT_FILE_STORAGE` with `STORAGES["default"]`  
✅ Change `index_together` to `indexes`  
✅ Change `unique_together` to `UniqueConstraint`  
✅ Use keyword arguments for `Model.save()`  
✅ Replace `check=` with `condition=` in CheckConstraint  
✅ Remove usage of `length_is` template filter  
✅ Update database versions (PostgreSQL 13+, MariaDB 10.5+, SQLite 3.31+)

## **How to Check What You're Using**

Run Django's system checks:
```bash
python manage.py check --deploy
```

This will warn you about deprecated features in your code.

## **The Most Important One for You**

Since you're trying to get cache busting to work, the **STORAGES setting** is your issue. In Django 5.1+, you MUST use:

```python
STORAGES = {
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
    },
}
```

The old `STATICFILES_STORAGE` setting is completely removed and ignored in Django 5.1+, which is why your configuration isn't working!
