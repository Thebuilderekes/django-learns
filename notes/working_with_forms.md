
We have seen forms in action in the admin page using functionality already provided by Django admin, but now we want to create our own forms that can be used to do CRUD

## what is idempotency
idempotency is when data is the same at every request sent to the server. So if a request for a page is made by refreshing the page to find that the data that comes back is the same every time, that request is said to be idempotent.

## POST VS GET
The default method of a form that does not have an explicit method attribute set to POST is GET
A request with a POST method has its 

**POST**: Sends data in the body of the HTTP request. This is the method typically used for forms that change data on the server (e.g., creating, updating, or deleting records). Django requires a CSRF token for POST requests.

**GET**: Appends the data to the URL as query parameters. This is typically used for forms that only retrieve or search for data and do not change server state. Django does not require a CSRF token for GET requests

### When to use POST OR GET

## Using CSRF tokens for form security ``{%csrf token%}``
CSRF token put into forms ensures that the form is unique to one particular user

The CSRF token is unique to every visitor on the site and periodically changes. If an attacker were to copy the HTML from our site, they would get their own CSRF token that would not match that of any other user, so Django would reject the form when it was posted by someone else.


## Validating data using Django form library
Before Django converts form input values to objects, the input values are all string format

Django has some built in functionality for form validation that we are going to be looking into.

## Bound vs Unbound forms
Forms are of two types, bound and unbound. If a form is bound it means it contains data that will be sent to it for validation like `form = ExampleForm(request.POST)`. Unbound is for without data like ``form = ExampleForm()``
``is_valid()`` and `cleaned_data()` are some methods associated with bound form that allows for good form validation.
For example:

```python
form = ExampleForm(request.POST)
if form.is_valid():
  if form.cleaned_data["integer_input"] > 5:
    do_something() 
  `````

```is_valid()``` method is particularly important to use because it ensure that all data provided to the form is correct before any thing else can be done to it.

Each form method have argument that allow you set the properties of the form element getting displayed in the template.
