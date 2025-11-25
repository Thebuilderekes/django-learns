## Modifying table data using the shell

Type `python manage.py shell` to enter shell interaction mode
and then
`>>>from reviews.models import Publisher`
then
`>>>publisher=Publisher(name="Packt publishing", website="https://www.packhub.com", email="info@packthub.com")`
and then
`publisher.save()` to write the model object into the database.

To do all of this in one step, use the `create()`
for example
`>>>publisher=Publisher.object.create(name="Packt publishing", website="https://www.packhub.com", email="info@packthub.com")`
and this will create and save a record at the same time.

## NOTE

- To use a model in the shell, you must first import it from the file
- To set relationships to the value of a record that points to the primary key while creating an object you must first get that record either by using one of the record property e.g `object_name = Class.objects.get(name="value")` or by using its primary key e.g `object_name = Class.objects.get(pk=key_number)`

# example of shell commands

- To create a book

```
>>>book_object_name = Contributor.objects.create(title="", publication_date="", isbn="")
```

- To create a contributor

```
>>>contributor_object_name = Contributor.objects.create(first_names="", last-names="", email="")
```

- To create a bookContributor

```
>>>BookContributor.objects.create(
        book=[book_object_name],
        contributor=[Contributor_object_name],
        role=BookContributor.ContributionRole.[role_name]
    )
```

- To create a publisher

```
>>>publisher_object_name = Publisher(name="", website=", email="")
```

- To get a particular record `get()`

```
>>>book.objects.get(name="nameofbook")
```

- To get all records of a model `all()`

```
>>>Model_name.objects.all()
```

- To get all records that match when there are one or more having identical values `filter()`

```
>>>Model.objects.filter(name="name_of_item")
```

- Using field lookups like **gt, **lt, \_\_ghe
  It returns an empty Queryset when it doesn't see a match

```
Model.objects.filter(publication_date__gt=date(2014, 3, 4 ))
```

- query by order_by to order alphabetically or by date

` >>>book.objects.order_by('title')`
` >>>book.objects.order_by('publication_date')`

- query by negating the key to sort in reverse alphabetical order

`book.objects.order_by('-title')`

- Using pattern matching with filtering

```
>>>book = Book.objects.filter(title__contains="Addvanced Learning"

for case insensitive that contains
>>>book = Book.objects.filter(title__icontains="Advanced Learning"
```

- To exclude a member that has a certain value
  `>>>object_name = Model.objects.exlude(key="value")`

- query by model name (like book with publisher since it shares a foreign key)

`>>>Publisher.objects.get(book__title="value")`

- query by object instance

```
>>>book = Book.objects.get(title="title of book")
>>>book.publisher
```
