from django.views.generic.list import ListView

from .forms import ExpenseSearchForm
from .models import Expense, Category
from .reports import summary_per_category


class ExpenseListView(ListView):
    model = Expense
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list

        form = ExpenseSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get('name', '').strip()
            date = form.cleaned_data.get('date', '')
            date_to = form.cleaned_data.get('date_to', '')
            category = form.cleaned_data.get('category', '')
            if name:
                queryset = queryset.filter(name__icontains=name)
            if date and date_to:
                queryset = queryset.filter(date__range=(date,date_to))
            elif date:
                queryset = queryset.filter(date=date)
            elif date_to:
                queryset = queryset.filter(date=date_to)
            if category:
                queryset = queryset.filter(category=category)
        return super().get_context_data(
            form=form,
            object_list=queryset,
            summary_per_category=summary_per_category(queryset),
            **kwargs)

class CategoryListView(ListView):
    model = Category
    paginate_by = 5

