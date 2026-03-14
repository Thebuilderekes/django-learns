# Create your views here.
# from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import DeleteView, FormView, CreateView, UpdateView
from django.views import View
from .forms import BookForm
from .models import Book
# Create your views here.
from django.views.generic import DetailView, ListView


class BookRecordDetailView(DetailView):
    model = Book
    template_name = 'book_management/book_detail.html'

class BookCreateView(CreateView):
    model = Book
    fields = ['name', 'author']
    template_name = 'book_management/book_form.html'
    success_url = '/book_management/entry_success'
    extra_context = {'button_text': 'Create Book', 'title': 'Add New Book'}

class BookUpdateView(UpdateView):
    model = Book
    fields = ['name', 'author']
    template_name = 'book_management/book_form.html'
    success_url = '/book_management/entry_success'
    extra_context = {'button_text': 'Update book', 'title': 'Edit Book'}

class BookDeleteView(SuccessMessageMixin, DeleteView):
    model = Book
    fields = ['name', 'author']
    template_name = 'book_management/book_delete_form.html'
    success_url = '/book_management/delete_success'
    extra_context = {'button_text': 'Delete Book', 'title': 'Delete book'}

class BookRecordFormView(FormView):
    template_name = 'book_management/book_form.html'
    form_class = BookForm
    success_url = '/book_management/entry_success'
    extra_context = {'button_text': 'Save record', 'title': 'Book entry'}

    def form_valid(self, form):
        #form_valid should always return an HttpResponse object
        form.save()
        return super().form_valid(form)

class BookListView(ListView):
    model = Book
    template_name = 'book_management/book_list.html'
    # Optional: Order books so the newest ones appear first
    ordering = ['-id']
    # Optional: Change the name of the variable in the template
    context_object_name = 'books'
    extra_context = {'title': 'List of books'}

class FormSuccessView(View):
    def get(self):
        save_message =  "Book record saved successfully"
        return HttpResponse(save_message)

# Create your views here.
