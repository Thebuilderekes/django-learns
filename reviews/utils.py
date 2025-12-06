from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

def create_edit_view(Model, Form, template_name, detail_url_name, obj_name_field='name'):
    """
    Generates a generic view function for both creating and editing a model instance.
    """
    def view_func(request, pk=None):
        instance = None
        # 1. Handle Edit Case (if pk is provided)
        if pk:
            instance = get_object_or_404(Model, pk=pk)
            action = 'Update'
            title = f'Edit {getattr(instance, obj_name_field)}'
            success_message = f'{Model.__name__} "{getattr(instance, obj_name_field)}" was successfully updated.'
        # 2. Handle Create Case (if pk is NOT provided)
        else:
            action = 'Create'
            title = f'Create {Model.__name__}'
            success_message = f'{Model.__name__} was successfully created.'

        if request.method == 'POST':
            # Instantiate form with POST data, and instance if editing
            form = Form(request.POST, instance=instance)

            if form.is_valid():
                obj = form.save()

                # Update success message for 'Create' with the new object's name
                if not pk:
                    success_message = f'{Model.__name__} "{getattr(obj, obj_name_field)}" was successfully created.'

                messages.success(request, success_message)

                # Redirect to the detail view
                return redirect(detail_url_name, pk=obj.pk)
        else:
            # Instantiate form for GET request
            form = Form(instance=instance)

        # Context for the template
        context = {
            'form': form,
            'title': title,
            'submit_text': action,
            'object': instance, # Optional, for template use
        }

        return render(request, template_name, context)

    return view_func





def average_rating(rating_list):
    if not rating_list:
        return 0
    return round(sum(rating_list) / len(rating_list))
