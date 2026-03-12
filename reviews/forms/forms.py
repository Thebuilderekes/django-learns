from django import forms


class NewsletterForm(forms.Form):
    signup = forms.BooleanField(
        label="Would you like to sign up for our newsletter?",
        required=False,
        label_suffix="",
    )
    email = forms.EmailField(
        help_text="Enter your email address to subscribe", required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If form has data and signup is checked, make email required
        if self.data.get("signup"):
            self.fields["email"].required = True

    def clean(self):
        cleaned_data = super().clean()
        signup = cleaned_data.get("signup")
        email = cleaned_data.get("email")

        if signup and not email:
            self.add_error(
                "email", "Email is required when signing up for the newsletter."
            )

        return cleaned_data

