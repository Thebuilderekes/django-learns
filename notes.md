## What is Django?

Django is s web framework that allows users to build full fledge apps with front end, backend and database control. It is written in Python and is suitable for apps that need to be robust, fast and manageable.
Django follows the MVC pattern but has its own slightly modified version called MVT standing for Model, view, template. In this type, the view communicates with the model and renders a template

## manage.py

When a basic Django app is created, it is created with a mange.py script available for use.
All commands that can run with the `manage.py` script are called management commands

## **MVT in Python (Django Framework)**

**MVT** stands for **Model-View-Template**, a software design pattern used by Django to organize code efficiently.

### **1. Model**

- Represents the **data layer**.
- Defines the structure of your database tables using Python classes.
- Handles all data-related logic: creation, retrieval, update, and deletion (CRUD).
- Example: A `User` model representing users in the database.

### **2. View**

- Acts as the **business logic layer**.
- Receives user requests, processes them (with help from Models), and returns a response.
- Decides **what data** to send to the template.
- Example: A view that fetches all blog posts and passes them to a template.
- Views do not always need the model for it to work. You can have a view just send data directly to the template

### **3. Template**

- The **presentation layer**.
- Handles the front-end (HTML) and is responsible for **how data is displayed**.
- Uses Django's template language to dynamically insert data.
- Example: An HTML file that loops through blog posts and displays them.

### In Summary:

- **Model** = Data
- **View** = Logic
- **Template** = Presentation

Django's MVT is similar to MVC, but Django handles the controller part internally via its URL dispatcher and framework logic.

## HTTP requests

When a user types in a URL into a browser, they create a HTTP request that is sent to the web server. The server sees this request and checks to see if has the resource being requested. If it has it, it retrieves the resource and sends it back to the user's browser as a HTTP response

An HTTP request consists of 4 parts

- Method
- Path
- Headers
- body

### 1. **request.method**

- The HTTP method used (e.g., `'GET'`, `'POST'`, `'PUT'`, `'DELETE'`, etc.)

```python
request.method  # 'GET' or 'POST'
```

### 2. **request.GET**

- A dictionary-like object containing **GET parameters** from the query string.

```python
request.GET['search']  # ?search=django
```

### 3. **request.POST**

- A dictionary-like object containing **POST parameters** (usually from forms).

```python
request.POST['username']
```

### 4. **request.FILES**

- A dictionary-like object containing uploaded **files**.

```python
request.FILES['profile_picture']
```

### 5. **request.path**

- The **full path** of the request (without the domain).

```python
request.path  # '/blog/5/'
```

### 6. **request.path_info**

- Same as `request.path`, but without URL resolving middleware interference.

### 7. **request.META**

- A dictionary containing all available **HTTP headers**, **server variables**, and **environment info** (like `REMOTE_ADDR`, `HTTP_USER_AGENT`, etc.)

```python
request.META['HTTP_USER_AGENT']
request.META['REMOTE_ADDR']
```

### 8. **request.COOKIES**

- A dictionary containing all cookies sent by the client.

```python
request.COOKIES['sessionid']
```

### 9. **request.session**

- A dictionary-like object representing the current user's **session** data.

```python
request.session['user_id'] = 42
```

### 10. **request.user**

- An instance of the currently authenticated **User**, if logged in.

```python
if request.user.is_authenticated:
    ...
```

### 11. **request.body**

- The **raw HTTP body** of the request (as bytes), useful for handling things like JSON or XML manually.

```python
import json
data = json.loads(request.body)
```

### 12. **request.content_type**

- The MIME type of the request body (e.g., `'application/json'`, `'multipart/form-data'`).

```python
request.content_type  # 'application/json'
```

### 13. **request.encoding**

- The character encoding used to decode the request body.

```python
request.encoding  # 'utf-8'
```

## 🧠 Summary

| Attribute     | Description                                   |
| ------------- | --------------------------------------------- |
| `method`      | HTTP method (`GET`, `POST`, etc.)             |
| `GET`, `POST` | Query and form data                           |
| `FILES`       | Uploaded files                                |
| `COOKIES`     | Cookies sent by the client                    |
| `META`        | Request headers and environment info          |
| `session`     | Session data (if middleware is enabled)       |
| `user`        | Authenticated user (if middleware is enabled) |
| `body`        | Raw request body                              |

| `path` | Path of the request URL |

## 🔍 What is a QueryDict in Django?

A **QueryDict** is a special type of dictionary used by Django to store **HTTP request data**.

It’s used internally to handle data from:

- `request.GET` → data from the URL (query string)
- `request.POST` → data from submitted forms (POST request body)

Django automatically parses incoming request data and wraps it in a `QueryDict` object, so you can easily access the values.

## 🚀 Where You'll Encounter QueryDict

### 1. **GET Parameters** (from the URL)

Example URL:

```
http://example.com/search?query=django&page=2
```

In your Django view:

```python
def my_view(request):
    search_term = request.GET['query']     # 'django'
    page_number = request.GET['page']      # '2'
```

Here, `request.GET` is a `QueryDict`.

### 2. **POST Parameters** (from a form)

Example HTML form:

```html
<form method="post">
  {% csrf_token %}
  <input type="text" name="username" />
  <input type="password" name="password" />
  <button type="submit">Login</button>
</form>
```

In your Django view:

```python
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
```

Here, `request.POST` is also a `QueryDict`.

## 🧠 Key Features of QueryDict

### ✅ 1. **Supports Multiple Values for the Same Key**

Unlike normal Python dictionaries, a `QueryDict` can store **multiple values** for a single key.

Example query string:

```
/filter?tag=python&tag=django&tag=web
```

In Django:

```python
tags = request.GET.getlist('tag')  # ['python', 'django', 'web']
```

### ✅ 2. **Immutable by Default**

`QueryDict` objects are **immutable** — meaning you can’t change them unless you make a copy:

```python
mutable_data = request.POST.copy()
mutable_data['new_key'] = 'value'
```

## 🧩 Summary

| Attribute            | Details                                           |
| -------------------- | ------------------------------------------------- |
| **Type**             | Django's `QueryDict` (like a dictionary)          |
| **Where**            | `request.GET` and `request.POST`                  |
| **Supports**         | Multiple values per key (`getlist()`)             |
| **Default Behavior** | Immutable (must `.copy()` to modify)              |
| **Purpose**          | Clean, structured access to incoming request data |

Let me know if you’d like code examples for custom forms or working with files (which also use a `QueryDict`-like object: `request.FILES`).

## HTTP response

An HTTP response consists of 3 parts

- Status
- Headers
- body

## Request and response flow

1. Match URL request against URL routes
2. Call view method with HTTP request object
3. Perform logic inside view method
4. Return HTTP response object
5. Send response to client

## urls.py

This file is responsible for the communication between URLs and the view. It contains the pattern variables that is a list of URL paths and the view that concerns each path. Hello.

## Settings.py

It is important to have a `settings.py` file in your code made by you or else Django will always fall back to it's default setting, especially when it comes to `DEBUG` setting in the `settings.py`

## Templates

When it comes to rendering html templates, Django already knows to look into any folder called template when you refer to it in the view. So there is no need to target the template file from its parent folder, simply insert the name of the template file directly in the render function and it will refer to it.
Variables can be loaded into a template using the render function located in
the view. The variables are set as key-value arguments in the render function
and this allows them to be processed by Django.

## Exceptions

Exceptions are errors that have to be caught, otherwise they bubble up into
your code and cause the program to crash,most times with an error message that
tells you what went wrong. Some errors are python specific errors while others
are Django specific errors. DEBUG= True makes it so that you can see these
errors during development but the quality is different in production as you will
find a less detailed error log, only an internal service error page that has
less sensitive information.

## Debugging

Code can be debugged using the built in debugger that comes with Django. This
will make it easy for you to tell when the error is coming from the
fetching of data or from your template.

## static files

Static files are files like CSS, JavaScript and media that need to be referred to in the templates.
They are require `DEBUG = True` in other to be loaded successfully and are handles by server during production
when `DEBUG = False`

## MODELS AND MIGRATIONS

Models are python classes that hold the blueprint for creating database tables.

Models call from the `django.db` module

Migration is the process of turning python code into database structures such as database fields and tables.

## Migration process
The `sqlmigrate` command in Django is not a mandatory step for migrations because its purpose is to show you the SQL code that will be executed, not to run the migration itself.

Here's a breakdown of the typical Django migration workflow and why `sqlmigrate` is an optional step:

1.  **`python manage.py makemigrations`**: This is the first and essential step. When you change your Django models (e.g., add a new field, change a field's properties, or create a new model), this command tells Django to "look for changes" and generate a migration file. This file is a Python script that describes the changes to be made to the database schema. It's a declarative, human-readable record of your model changes.

2.  **`python manage.py migrate`**: This is the command that actually applies the changes to your database. It reads the migration files created by `makemigrations` and executes the necessary SQL commands to update the database schema. This is the core command for keeping your database in sync with your models.

3.  **`python manage.py sqlmigrate <app_name> <migration_name>`**: This is the optional step. It's a utility command that takes a migration file as an argument and prints the raw SQL code that the `migrate` command would run. It **does not** modify your database.

**Why would you use `sqlmigrate`?**

* **Reviewing the SQL**: It's a great way to double-check what Django is about to do to your database. This is particularly useful for complex migrations, in production environments, or on databases with specific performance characteristics (like large tables or many rows). You can review the generated SQL to ensure it's what you intended, and that it won't cause unexpected issues.
* **Manual Application**: In some highly regulated or specific production environments, you might not have the permissions to run `python manage.py migrate` directly. In these cases, a database administrator might require you to provide the SQL queries to run manually. The `sqlmigrate` command allows you to generate these queries.
* **Debugging**: If a migration is failing, looking at the raw SQL can often help you understand why. It gives you a direct view into what the database is complaining about.

In summary, `makemigrations` and `migrate` are the core commands for the Django migration system, automating the process of schema changes. The `sqlmigrate` command is a tool for developers and administrators to inspect and understand the generated SQL, providing transparency and control without being a required part of the standard, automated workflow.
