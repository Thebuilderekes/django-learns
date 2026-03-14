
## Forms
Because the aim of CBV is to create reusable code to execute views, the  ``book_form.html`` template can be used to handle different view functionality
depending on what view is being requested by the `urls.py` and the submit
button text can be made dynamic depending on this as well.

- Each editing view provides an `object` variable that represents the model
  object. This `object` can be used in the template to render details from the
  model like `object.name``, `object.author` etc
-
