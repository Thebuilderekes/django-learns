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

* The HTTP method used (e.g., `'GET'`, `'POST'`, `'PUT'`, `'DELETE'`, etc.)

```python
request.method  # 'GET' or 'POST'
```


### 2. **request.GET**

* A dictionary-like object containing **GET parameters** from the query string.

```python
request.GET['search']  # ?search=django
```


### 3. **request.POST**

* A dictionary-like object containing **POST parameters** (usually from forms).

```python
request.POST['username']
```


### 4. **request.FILES**

* A dictionary-like object containing uploaded **files**.

```python
request.FILES['profile_picture']
```


### 5. **request.path**

* The **full path** of the request (without the domain).

```python
request.path  # '/blog/5/'
```


### 6. **request.path\_info**

* Same as `request.path`, but without URL resolving middleware interference.


### 7. **request.META**

* A dictionary containing all available **HTTP headers**, **server variables**, and **environment info** (like `REMOTE_ADDR`, `HTTP_USER_AGENT`, etc.)

```python
request.META['HTTP_USER_AGENT']
request.META['REMOTE_ADDR']
```


### 8. **request.COOKIES**

* A dictionary containing all cookies sent by the client.

```python
request.COOKIES['sessionid']
```


### 9. **request.session**

* A dictionary-like object representing the current user's **session** data.

```python
request.session['user_id'] = 42
```


### 10. **request.user**

* An instance of the currently authenticated **User**, if logged in.

```python
if request.user.is_authenticated:
    ...
```


### 11. **request.body**

* The **raw HTTP body** of the request (as bytes), useful for handling things like JSON or XML manually.

```python
import json
data = json.loads(request.body)
```


### 12. **request.content\_type**

* The MIME type of the request body (e.g., `'application/json'`, `'multipart/form-data'`).

```python
request.content_type  # 'application/json'
```


### 13. **request.encoding**

* The character encoding used to decode the request body.

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
| `path`        | Path of the request URL                       |



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




