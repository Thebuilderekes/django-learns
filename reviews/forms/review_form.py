from django import forms

class ExampleForm(forms.Form):
    # This will generate inputs and Labels will
    # automatically be generated as the form inputs are generated
    RADIO_CHOICES = (
        ("Value One", "Value One Display"),\
        ("Value Two", "Text For Value Two"),\
        ("Value Three", "Value Three's Display Text")
    )


    BOOK_CHOICES = (
        ('fiction', (
            ("1", "harry potter"),
            ('2', "The conjuring"),
            ('3', "fantastic Four")
        )),
    )
    
    text_input = forms.CharField()
    password_input = forms.CharField(widget=forms.PasswordInput)
    checkbox_on = forms.BooleanField()
    radio_input = forms.ChoiceField(
        choices=RADIO_CHOICES,
        widget=forms.RadioSelect
    )
    favorite_book = forms.ChoiceField(choices=BOOK_CHOICES)
    books_you_own = forms.MultipleChoiceField(choices=BOOK_CHOICES)
    text_area = forms.CharField(widget=forms.Textarea)
    integer_input = forms.IntegerField()
    float_input = forms.FloatField()
    decimal_input = forms.DecimalField(max_digits=3)
    email_input = forms.EmailField()
    date_input = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    hidden_input = forms.CharField(
        widget=forms.HiddenInput,
        initial="Hidden Value"
    )

