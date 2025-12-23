- Create a model with needed fields: body, title, slug, created, updated,
published
- Create an ordering pattern
- Index ordering is not supported on MySQL. If you use MySQL for the database, a
descending index will be created as a normal index.
- create an enumeration class `Status` to track the state of ta post which is
either going to be in draft or published
- We can access ``Post.Status.choices`` to obtain the available choices,
``Post.Status.names`` to obtain the names of the choices, ``Post.Status.labels``
to obtain the human-readable names, and ``Post.Status.values`` to obtain the
actual values of the choices.
- `raw_id_fields` attribute is responsible for making it to that you can choose
an author in by the `id` as set in the model

> [!NOTE]
Don't mess up initial fields definition in models or you might have to write raw
sql to change the column names in models

## Creating Objects The default manager for models is the `objects` manager Lets
see how `objects` is being used with an example:

``` ``` ``` user = Users.objects.get(user="admin") posts =
Posts.objects.filter(title="today django") print(posts.query) # prints the SQL
for the filtering ``` The `.get()` acts like a `SELECT` in SQL The `.filter()`
acts like a `WHERE` in SQL *more on this on page 67 and 69 DBE book* ## 📝
Comprehensive Guide to Django QuerySet Operations

A **QuerySet** is the core mechanism in Django for interacting with your
database. It represents a collection of objects that are retrieved from your
database and allows you to filter, order, and manipulate that data using Python
code that is translated into efficient SQL queries. Understanding these
operations is fundamental to writing performant and effective Django
applications.

-----

## 🎯 The Principle of Laziness and Evaluation

The most important concept regarding QuerySets is **laziness**.

### What is Laziness?

When you construct a QuerySet—for example, by calling `filter()`, `exclude()`,
or `order_by()`—Django **does not immediately execute the database query**. It
simply builds an internal representation of the query.

### When is a QuerySet Evaluated?

The database query is only executed (the QuerySet is **evaluated**) when the
results are actually needed. This usually happens when:

1.  **Iterating:** You loop over the QuerySet (e.g., in a `for` loop).
2.  **Slicing (Non-Stepped):** You use Python slicing that is not a simple step
(`QuerySet[0:5]`).
3.  **Pickling/Caching:** You call `repr()`, `len()`, `list()`, or `cache()`.
4.  **Specific Methods:** You call methods that must retrieve data, such as
`.get()`, `.count()`, or `.latest()`.

This lazy design allows Django to optimize queries by chaining multiple
filtering and ordering methods before hitting the database just once.

-----

## 🔍 Fundamental Retrieval and Filtering

These methods are the primary tools for selecting subsets of data. Most of these
return a new QuerySet, allowing for **chaining**.

* ### **`.all()`** Returns a **new QuerySet** that is a copy of the model's
  default manager. It essentially selects all records from the table. ```python
  all_books = Book.objects.all() ```
  * ### **`.filter(**kwargs**)`** Returns a new QuerySet containing objects that
    **match** the given lookup parameters. Lookups use double underscores (`__`)
    to specify operations (e.g., `price__gt=50` for "price greater than 50").
    ```python available_fiction = Book.objects.filter(genre='Fiction',
    in_stock=True) ```
  * ### **`.exclude(**kwargs**)`** Returns a new QuerySet containing objects
    that **do not match** the specified lookup parameters. It's the logical
    inverse of `filter()`. ```python no_fantasy =
    Book.objects.exclude(genre='Fantasy') ```
  * ### **`.get(**kwargs**)`** Retrieves a **single model instance** matching
    the given parameters. This method forces immediate evaluation. If the query
    returns zero objects, it raises a `DoesNotExist` exception. If it returns
    more than one object, it raises a `MultipleObjectsReturned` exception. It is
    typically used for primary key lookups (`Book.objects.get(pk=1)`).
  * ### **Slicing** You can use Python's array slicing notation to limit the
    QuerySet, which translates directly to the SQL `LIMIT` clause. ```python
    top_ten = Book.objects.all()[:10] ```

-----

## 🔧 **Modification and Creation**

These operations interact directly with the database to insert, update, or
delete records.

* ### **`.create(**kwargs**)`** A convenient, one-step method that both
  instantiates the model and **saves it to the database**. It is equivalent to:
  `book = Book(**kwargs)` followed by `book.save()`. ```python new_book =
  Book.objects.create(title='The Atlas', author='K. Smith') ```
  * ### **`.update(**kwargs**)`** Performs an **SQL `UPDATE`** statement on the
    entire QuerySet. This is highly efficient as it executes a single database
    query, without loading any model instances into memory. The method returns
    the number of rows updated. ```python
    Book.objects.filter(price__lt=10).update(price=10) # Set a minimum price ```
  * ### **`.delete()`** Performs an **SQL `DELETE`** statement on the QuerySet.
    Like `.update()`, it is efficient because it executes in a single query. It
    also handles related objects according to the `on_delete` rules defined in
    your model relationships.

-----

## 📈 **Inspection, Aggregation, and Ordering**

These methods help you structure the results or perform quick checks on the
data.

* ### **`.order_by(*fields*)`** Orders the QuerySet according to the given
  field(s). The order is **ascending** by default. To specify **descending**
  order, prefix the field name with a minus sign (`-`). ```python # Order by
  price ascending, then title descending ordered_books =
  Book.objects.order_by('price', '-title') ```
  * ### **`.count()`** Forces evaluation and returns the number of objects in
    the QuerySet as an integer. This translates to an efficient `SELECT
    COUNT(*)` query.
  * ### **`.exists()`** Returns **`True`** if the QuerySet contains one or more
    results, and **`False`** otherwise. This is the **most efficient way** to
    check for the presence of an object, as it executes a minimal query (`SELECT
    1... LIMIT 1`) instead of fetching all records. ```python if
    Book.objects.filter(author='Tolkien').exists(): # Do something only if
    Tolkien books are present pass ```
  * ### **`.values()` and `.values_list()`** These methods are used for
    optimization when you only need specific data fields rather than full model
    objects.
      * **`.values()`** returns a QuerySet of **dictionaries**, with keys
      corresponding to field names.
      * **`.values_list()`** returns a QuerySet of **tuples**, which is slightly
      more memory-efficient if you only need the raw field data.

Would you like to explore how to combine these QuerySet methods into complex,
chained queries for advanced data retrieval?

## Creating custom managers A **Custom Manager** is a class that inherits from
`django.db.models.Manager` and is attached to a Django Model. The manager is the
**interface** through which database query operations are provided to a Model.

By default, every model automatically gets a standard manager named
**`objects`**. When you define a custom manager, you are replacing or augmenting
the model's default manager.

-----

## ✨ Key Benefits of Custom Managers

Creating custom managers provides significant benefits, primarily centering
around **query encapsulation** and **code reusability**:

### 1\. Encapsulating Query Logic

Instead of repeating complex or common filter operations across different views,
templates, or logic files, you can define them once in a manager.

* **Before (Repetitive):** ```python published_posts =
Post.objects.filter(status='PB', publish_date__lte=timezone.now()) ```
  * **After (Encapsulated):** ```python published_posts = Post.published.all() #
  Assuming 'published' is the custom manager ```

This makes your application code cleaner, more readable, and less prone to
copy-paste errors.

### 2\. Modifying Initial QuerySets (Default Filtering)

You can use a custom manager to override the base `get_queryset()` method. This
allows you to apply default filtering to **every single query** made through
that manager.

* A common example is creating a **`PublishedManager`** (as seen in your
previous code) that always restricts results to objects with `status='PB'`. Any
call made via this manager (`Post.published.all()`, `Post.published.get(...)`)
will *automatically* include that filter.

### 3\. Creating Reusable Utility Methods

Managers are an ideal place to define complex **data-access methods** that don't
fit well on the Model instance itself.

* For example, you could add a method like
`Post.objects.get_posts_by_author(user)` or
`Product.objects.available_in_stock()`. This keeps your view logic focused on
HTTP concerns and business logic, while keeping database concerns neatly
organized in the manager.

### 4\. Handling Cross-Cutting Concerns

Managers can be used for things like adding custom select clauses, annotations,
or performing bulk operations specific to a certain data type, ensuring
consistency across your application's data layer.

## Enhancing blog with social features
- We start by creating the `get_asbsolute_url()` method on Post model so we can
use the `reverse()` function in the method to make a canonical URL like the
``blog/post/list/2`` in the address bar when you visit using the details link in
`post_list.html` page.
- We want the canonical link to be SEO friendly so we create a slug-publish date
combination so that it is unique for each post. So we alter slug field to only
allow to be unique for publish date By doing this we have to alter the path URL
to follow this pattern
**NOTE** Watch how the ``get_asbsolute_url`` method interacts with the body of
the `PostDetailView`

## NOTE
- Make sure the arguments of the parameters match the same arrangement in the
URLS and in the models
-
## Adding pagination
We  use the `Paginator` built in module from Django
`from django.core.paginator import Paginator` to add pagination


### Key Features of Django's Built-in Paginator
- Core Logic: The Paginator class handles the logic of splitting a large
QuerySet, list, or other sliceable object into smaller Page objects.
- Ease of Use: It can be implemented in both function-based views and
class-based views (specifically the `ListView` generic class-based view) with
minimal code.
- Template Integration: It passes a `page_obj` to the template, which provides
essential attributes and methods for navigation links, such as `has_next``,
`has_previous``, ``next_page_number``, ``previous_page_number``, and
``paginator.num_pages``.
- Error Handli g: It includes built-in exceptions like `EmptyPage` and
`PageNotAnInteger` to handle cases where a user requests an invalid page.

## Adding exceptions to pagination
You have access to `EmptyPage` exception with `PageNotAnInteger` exception among
others.

## Using class based views
use `page=page_obj` as value for the pagination include tag because template comes
with it to point to what is needed when using class based view

## Setting up forms for message sending using email
The email config has been made to work with gmail.


## Setting up Comment system
- Created `Comment` model
- Created `Comment` model admin
- Created a `Comment` form that matches the `Comment` model
- Create a ``post_comment`` view

In this view, we have implemented the following actions:
1. We retrieve a published post by its id using the get_object_or_404() shortcut.

2. We define a comment variable with the initial value None. This variable will be used to store the comment object when it is created.

3. We instantiate the form using the submitted POST data and validate it using the is_valid() method. If the form is invalid, the template is rendered with the validation errors.

4. If the form is valid, we create a new Comment object by calling the form’s save() method and assign it to the comment variable, as follows: comment = form.save(commit=False)

5. The save() method creates an instance of the model that the form is linked to and saves it to the database. If you call it using commit=False, the model instance is created but not saved to the database. This allows us to modify the object before finally saving it. The save() method is available for ModelForm but not for Form instances since they are not linked to any model.



## Setting up tagging for blog posts
- install django-taggit
- By adding django-taggit, you can now add a TaggableManager to your Post model. This will allow you to:
 - Tag posts (e.g., "Python", "Django", "Tutorial").
 - Filter posts by tags.
 - Show "Similar Posts" based on shared tags.

