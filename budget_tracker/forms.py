from django import forms
from django.utils import formats
from .models import Budget, Transaction 
from datetime import timedelta

BUDGET_DURATION_CHOICES = {
    timedelta(weeks=1).total_seconds(): "Week",
    timedelta(weeks=4).total_seconds(): "Month",
    timedelta(days=365).total_seconds(): "Year",
    0: "Custom",
}

TAG_CHOICES = {
    "income": "Income",
    "interest": "Interest",
    "food": "Food",
    "rent": "Rent",
    "debt": "Debt",
    "utilities": "Utilities",
    "other": "Other",
}

FILTER_CHOICES = {
    "": "-----",
    "name": "Name",
    "less": "Less than",
    "more": "Greater than",
    "date": "Date",
    "tag": "Tag",  
}

class TransForm(forms.ModelForm):
    other = forms.CharField(required=False, max_length=20)
    class Meta: 
        model = Transaction 
        fields = ['name', 'amount', 'timestamp', 'tag', 'other', 'budget']
        widgets = {
            "tag": forms.Select(choices=TAG_CHOICES),
            "budget": forms.HiddenInput()
        }

    def __init__(self, *args, budget_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['budget'].initial = budget_id

    def clean(self):
        tag = self.cleaned_data.get("tag")
        other = self.cleaned_data.get("other")
        if tag == "other":
            if other == '':
                self.add_error("other", "Please provide a tag")
            else:
                self.cleaned_data["tag"] = other

class FilterTrans(forms.Form):
    template_name = 'search_html'
    filter_by = forms.ChoiceField(required=False,choices=FILTER_CHOICES)
    tag = forms.ChoiceField(required=False,choices=TAG_CHOICES)
    search = forms.CharField(required=False,max_length=100)

    def clean(self):
        filter_by = self.cleaned_data.get("filter_by")
        search = self.cleaned_data.get("search")
        tag = self.cleaned_data.get("tag")
        if (search == ''):
            match filter_by:
                case "name": 
                    self.add_error("search", "Please provide a name")
                case "less": 
                    self.add_error("search", "Please provide a comparison value")
                case "great": 
                    self.add_error("search", "Please provide a comparison value")
                case "date": 
                    self.add_error("search", "Please provide a date and time")
                case "tag":
                    if tag == "other":
                        if search == '':
                            self.add_error("search", "Please provide a tag")
                        else:
                            self.cleaned_data["tag"] = search
            

class BudgetForm(forms.ModelForm):
    duration = forms.ChoiceField(required=True,
    choices=BUDGET_DURATION_CHOICES, help_text = "7, 28, or 365 days")
    custom = forms.DateField(required=False)
    class Meta: 
        model = Budget 
        fields = ['goal', 'start', 'duration', 'custom']

    def clean(self):
        duration = self.cleaned_data.get("duration")
        custom = self.cleaned_data.get("custom")
        if duration == '0' and custom == None:
            self.add_error("custom", "Please fill out this field")