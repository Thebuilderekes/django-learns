from django import forms


class MakeOrderForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=0, max_value=100,
        error_messages={ 
            "required": "",
        },
        widget=None,
    )

    signup = forms.BooleanField(
        required=False,
        label_suffix="",
    )
    email = forms.EmailField(
        help_text="Enter your email address here",
        required=True,
        widget=None,
        error_messages={
            "required": "",
        },
    )

    def clean(self):
        cleaned_data = super().clean()
        clean_signup = cleaned_data.get("signup")
        clean_email = cleaned_data.get("email")

        if clean_email and not clean_signup:
            self.add_error(None, "please check the box before providing an email")
        print(clean_email)
        print(clean_signup)

        return cleaned_data
