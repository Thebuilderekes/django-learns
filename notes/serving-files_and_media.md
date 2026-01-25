
 ## Uploading media

- Create form to upload media
- Input element for uploading file

-Example of save function that allows for saving and uploaded file to an output
file. Using Django Model and ModelForm will make it so you do not need to
manually handle upload with such functions

``````
def save_file_upload(upload, save_path):
with open(save_path, "wb+") as output_file:
        for chunk in upload.chunks(): output_file.write(chunk)


uploaded_file = request.FILES["file-upload-name"] #where file-upload-name is the
name value of the input element save_file_upload(uploaded_file,
"/path/to/output.jpg") ``````


- Don't forget `<form method="post" enctype="multipart/form-data">` enctype and
csrf token when using a form to upload data


## Security check
[] Check the file types being uploaded so that they match the
expected file type of that input. Find out about Pillow library and python-magic
package and their uses when it comes to operations like these.
[] Make sure your base `DIR` is limited so that hackers cannot go back up folders to reach a
resource that you don't want then to reach using `../.../` in the URL search bar
[] use `cleaned_data` to get data from a form field when it is necessary
[] When DO you need `cleaned_data`? Even when using a ModelForm, you would only manually
reach into `cleaned_data` if you wanted to do something extra with the data
before it hits the database.


## ImageField in python

The `ImageField` is one of Django’s most powerful model
fields, but it has a few "hidden" requirements and behaviors that often trip up
developers. You can serve a file that doesn't intend to be stored into a model
instance, in that case is is stored and Django go doesn't remember it or you can
store it in a Model instance by creating a model and using a model form where
files will be remembered through out the app.

Here is a summary of everything you need to know about the `ImageField`:

### 1. The Core Purpose

An `ImageField` is essentially a `FileField` with a built-in brain. While a
`FileField` allows any file (PDF, ZIP, TXT), an `ImageField` specifically
validates that the uploaded file is a **valid image** (JPEG, PNG, GIF, etc.).

### 2. The Absolute Requirement: Pillow

Django does not handle image processing on its own. You **must** install the
**Pillow** library, or your project will throw an error immediately upon adding
the field.

```bash
pip install Pillow

```

You can use Pillow to do things like resize photos for thumbnails and many more
see page 461

### 3. Key Model Arguments

When defining the field in `models.py`, there are three arguments you should
know:

* **`upload_to`**: Defines the subfolder inside your `MEDIA_ROOT` where files
are stored. It can be a string (`'photos/'`) or even a dynamic path based on the
date (`'photos/%Y/%m/%d/'`).
* **`height_field` & `width_field**`: You can link these to other
`IntegerFields` in your model. Django will automatically calculate the image's
dimensions and save them there every time you upload.
* **`blank=True`**: If you want the image to be optional in your forms, you must
set this.

### 4. How Data is Stored

* **Database:** Only stores a **string** (the path to the file, like
`"photos/my_pic.jpg"`).
* **Filesystem:** The actual file is stored in your `MEDIA_ROOT`.
* You can store in a subfolder by using the ``upload_to ="/folder"`` to upload
into a sub folder in `MEDIA_ROOT` so ``media/folder/``

`upload_to` can also allow fro string that contains `strftime` formatting
directives
* **Accessing it:** In your templates, you use `.url` to get the full path:
`<img src="{{ hotel.hotel_Main_Img.url }}">`.

---

### 5. Important Security & Validation

* **Extension Filtering:** Django checks the file extension against those
supported by Pillow.
* **Corrupt File Check:** If a user uploads a `.jpg` that is actually a renamed
text file, `ImageField` will catch it and throw an "Invalid Image" error during
`is_valid()`.
* **Duplicate Names:** If you upload `test.jpg` twice, Django automatically
renames the second one to `test_1.jpg` so nothing is overwritten.

### 6. The "Gotchas"

* **Serving Files:** Django **does not** serve media files in production. You
usually need a separate service (like AWS S3 or WhiteNoise) or a web server
config (Nginx) to actually show the images to users.
* **Deletion:** By default, deleting a model instance in Django **does not**
delete the physical file from your hard drive. The file stays there as an
"orphan" unless you use a library like `django-cleanup`.
