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
- `raw_id_fields` attribute is responsible for making it to that you can choose an
  author in by the `id` as set in the model

> [!NOTE]
Don't mess up initial fields definition in models or you might have to write raw
sql to change the column names in models

## Creating Objects
```
```
```
user = Users.objects.get(user="admin")
posts = Posts.objects.filter(title="today django")
print(posts.query) # prints the SQL for the filtering
```
The `.get()` acts like a `SELECT` in SQL
The `.filter()` acts like a `WHERE` in SQL
*more on this on page 67 and 69 DBE book*


