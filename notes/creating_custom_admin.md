## Creating custom admin site
 In order to create custom headers and title we would need to create a custom admin model that overrides the default   `admin.site` provided by the `django.contrib.admin`. By doing so we would need a way to have access to the model that we previously had access to using the default admin.

## Admin Models
- Looking the admin models for each model, every component created in the admin page is as a result for each field defined under each model admin class

# How to refer foreign keys and manytomany relationships in ModelAdmin
the convention is to use the `foreignkeyfield__recordname` as used in the Book admin `search_field = ('publisher__name')` because of the relationship between Book and publisher. Allso you can make it so that the name starts with the first letters you type so typing "don" only matches "donald


## Excluding and Grouping Fields 
There are occasions when it is appropriate to restrict the visibility of some of the fields in the model in the admin interface. This can be achieved with the exclude attribute. This is the review form screen with the Date edited field visible. Note that the Date created field does not appear – it is already a hidden view because date_created is defined on a model with auto_now_add parameter.

I can exlude date_edited in book admin by writing:
`exlude = ('date_edited')`

I can also use `fields = ('content', 'rating', 'creator', 'book')` to set the exact editable fields you want on display in the admin page. Grouping can be don with `fieldsets` see page 253
