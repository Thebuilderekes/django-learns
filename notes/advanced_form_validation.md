
## Review forms
`form` in `views.py` of class type ``CreateReview`` as defined in ``reviews.forms.create_review.py``
Every form field has its own attributes that can be used to customized the behaviour of the field

##Encourage better Vim habits. A simple toggle to enable/disable arrow keys in Normal, Insert, and Visual modes. Forms and best practices
Django forms are a powerful system that handles the tedious, repetitive work of data validation, cleaning, and rendering. Mastering them comes down to understanding the **ModelForm vs. Form** distinction, the **request-response cycle**, and **where to put your custom logic**.

Here are the key things to note, including best practices and common quirks.

-----

## 1\. Core Distinction: `Form` vs. `ModelForm`

This is the most crucial decision when starting a new form.

| Feature | `forms.Form` | `forms.ModelForm` |
| :--- | :--- | :--- |
| **Purpose** | For data that **doesn't map directly** to a database model. | For data used to **create or update** a single database model instance. |
| **Fields** | You **must** manually define every field (`CharField`, `EmailField`, etc.). | Fields are **automatically generated** from the specified `Model`'s fields. |
| **Saving** | Has **NO** built-in `.save()` method. You handle the data processing yourself. | Has a built-in **`.save()`** method to create/update the model instance. |
| **Use Case** | Login forms, contact forms, search forms, data wizards. | Create Post, Edit Profile, Update Product details. |

### Best Practice

  * **Always use `ModelForm`** if the form's sole purpose is CRUD (Create, Read, Update, Delete) on a single model. It saves you from redefining fields and manually writing `Model.objects.create(...)` logic.
  * Use the **`fields`** or **`exclude`** attribute in the `Meta` class to explicitly control which fields are included, rather than relying on Django to include everything.

-----

## 2\. The View Logic Flow 🔄

In your Django view, all forms follow a standard, secure pattern to handle GET (display) and POST (submission) requests.

### Key Things to Note

1.  **GET Request (Unbound Form):**

      * The user first requests the page (via GET).
      * You create an **unbound** form instance (e.g., `form = MyForm()`).
      * The form is rendered in the template, usually using `{{ form.as_p }}` or manual field rendering.

2.  **POST Request (Bound Form):**

      * The user submits the form data (via POST).
      * You create a **bound** form instance, passing in the submitted data: `form = MyForm(request.POST, request.FILES)`.
      * **Always include `request.FILES`** if your form handles file uploads.

3.  **The Validation Gate:**

      * Call `if form.is_valid():`. This triggers all field-level and form-level validation/cleaning methods.

4.  **Accessing Data:**

      * **Quirk:** **NEVER** use `request.POST.get('field_name')` inside the `if form.is_valid():` block.
      * **Best Practice:** Always access the data via **`form.cleaned_data`**. This dictionary contains data that has been:
          * Validated against constraints (required, max length, etc.).
          * Sanitized (safe from malicious input).
          * Converted into the correct Python type (e.g., `'10'` becomes the integer `10`).

5.  **Redirect on Success:**

      * **Best Practice:** After successful processing (e.g., `form.save()`), you **must** use `return redirect('some_success_url')`. This prevents the user from hitting the browser's back button and accidentally submitting the form a second time ("double-submit" problem).

-----

## 3\. Validation and Cleaning 🧼

Django provides three main places to add custom validation, running in a specific order:

| Method | Where is it defined? | Purpose |
| :--- | :--- | :--- |
| **1. Field-Specific Clean** | `def clean_field_name(self):` | For validating and normalizing a **single field**. |
| **2. Form-Level Clean** | `def clean(self):` | For validating **multiple fields** that depend on each other (e.g., confirming password matches password). |
| **3. Model Validation** | `Model.clean_fields()` | Validation that should run regardless of where the data comes from (Forms, API, Django Admin, etc.). (ModelForms inherit this). |

### Quirks & Best Practices

  * **Dependencies in `clean()`:** When implementing `def clean(self):`, remember that the data for *all* fields has already been cleaned and is available in **`self.cleaned_data`**. You must check for a field's presence in `self.cleaned_data` before using it, as previous cleaning steps might have removed it due to errors.

  * **Raising Errors:** To signal an error, raise a **`forms.ValidationError`**.

      * In a field-specific method (`clean_field_name`), raising `ValidationError` automatically associates the error with that field.
      * In the form-level `clean()` method, you must raise a non-field error OR use `self.add_error('field_name', 'Message')` to attach it to a specific field.

## Multi form validation
You can grab and validate all form fields at a time so you can be able to handle situation where one field's input depends on the value of another and if ``add_error()`` runs during field validation in a form, it causes ``is_valid()`` to return `False`. 1``add_error("field", "message")`` is used when you want to handle field specific errors but when you want to use a more general error with it you can use

```add_error(None, "message)```


## TO remove empty field error lists
``````    
<script>
document.addEventListener("DOMContentLoaded", function () {
    // Find all error lists
    document.querySelectorAll("ul.errorlist").forEach(function (ul) {

        // Check if all <li> inside are empty ("" or whitespace)
        const allEmpty = [...ul.querySelectorAll("li")].every(li => li.textContent.trim() === "");

        if (allEmpty) {
            ul.remove();   // Remove it from the DOM
        }
    });
});
</script>
```````

## How to create and run a Validator on a field

Create a validation function
``
def validationFunction(value):
   --- write code for if conditions on ``value``
        raise ValidationError("error message")
``  
Apply validation function on the field 
``field = form.CharField(validators=[validationFunction])``



## 4. ModelForm Quirk: `commit=False`

When using `ModelForm.save()`, the default behavior is to save the object directly to the database.

  * **Quirk:** If you need to set a value **before** saving the model that is **not** included in the form fields (e.g., setting the `user` field to `request.user` on a blog post), you must use **`commit=False`**.

<!-- end list -->

```python
# In your view.py
if form.is_valid():
    # 1. Save the model instance to a variable, but DO NOT commit to DB yet
    post = form.save(commit=False)

    # 2. Set the extra, required fields
    post.author = request.user

    # 3. Now commit the save to the database
    post.save()

    # 4. Save Many-to-Many data if applicable (ModelForm handles this)
    form.save_m2m()

    return redirect('success_page')
```

