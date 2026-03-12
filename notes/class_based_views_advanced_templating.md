 # Class based views CBV
Django’s Class-Based Views (CBVs) are built using a hierarchy of **Mixins**. This means that a single view class like `CreateView` actually inherits variables from many different parents (like `ModelFormMixin`, `ProcessFormView`, and `TemplateResponseMixin`).

Below is a breakdown of the primary view classes you can inherit from, grouped by their purpose, along with the most important variables (attributes) they provide.

---

## 1. Base Views

These are the building blocks used for simple pages or custom logic.

| View Class | Key Variables / Attributes |
| --- | --- |
| **`View`** | `http_method_names` (e.g., `['get', 'post', 'put', ...]`) |
| **`TemplateView`** | `template_name`, `extra_context`, `content_type`, `template_engine` |
| **`RedirectView`** | `url`, `pattern_name` (URL name), `permanent` (bool), `query_string` (bool) |

---

## 2. Generic Display Views

Used for presenting data from your database.

### **`ListView`** (For lists of objects)

* **`model`**: The model class to use.
* **`queryset`**: A custom QuerySet (replaces `model`).
* **`context_object_name`**: The name used in the template (defaults to `object_list` or `model_name_list`).
* **`paginate_by`**: Number of items per page.
* **`ordering`**: String or list defining the sort order.
* **`template_name_suffix`**: Defaults to `_list`.

### **`DetailView`** (For a single object)

* **`model` / `queryset**`: Define where to get the data.
* **`context_object_name`**: The template variable (defaults to `object` or `model_name`).
* **`pk_url_kwarg`**: The name of the PK in the URL (defaults to `'pk'`).
* **`slug_url_kwarg`**: The name of the slug in the URL (defaults to `'slug'`).
* **`slug_field`**: The name of the slug field in the model (defaults to `'slug'`).

---

## 3. Generic Editing Views

Used for handling forms and database changes.

### **`FormView`** (Standard Form)

* **`form_class`**: The Form class to instantiate.
* **`success_url`**: Where to redirect after a valid submission.
* **`initial`**: A dictionary of initial data for the form.
* **`prefix`**: String prefix for form fields.

### **`CreateView` & `UpdateView**` (Model Forms)

* *Inherits all `FormView` variables, plus:*
* **`fields`**: A list of model fields to include (if `form_class` is not provided).
* **`template_name_suffix`**: Defaults to `_form`.

### **`DeleteView`** (Object Deletion)

* **`model` / `queryset**`: The object to delete.
* **`success_url`**: Where to go after deletion.
* **`template_name_suffix`**: Defaults to `_confirm_delete`.

---

## 4. Date-Based Views

Used for "drill-down" archives (e.g., a blog archive by year/month).

* **Common Classes:** `ArchiveIndexView`, `YearArchiveView`, `MonthArchiveView`, `WeekArchiveView`, `DayArchiveView`, `TodayArchiveView`, `DateDetailView`.
* **Shared Variables:**
* **`date_field`**: The name of the `DateField` or `DateTimeField` in the model.
* **`allow_future`**: Boolean allowing the view to show items with future dates.
* **`year_format` / `month_format` / `day_format**`: String formats for parsing the URL (e.g., `'%Y'`, `'%b'`).
* **`date_list_period`**: Defines the "drill-down" level (e.g., `'year'`, `'month'`).



---

## 💡 The "Secret" to Navigating CBVs

Because Django uses deep multiple inheritance, it is nearly impossible to remember every variable. The industry-standard tool for this is **[CCBV.co.uk (Classy Class-Based Views)](https://ccbv.co.uk/)**.

It provides a "flattened" view of every class, showing you exactly which variables and methods are inherited from which Mixins.

Would you like me to show you an example of how to **override** one of these variables using a method like `get_context_data()`?
- To use a CBV you have to map, it to a url path in urls.py using `.as_view()`
 appended to the class name
