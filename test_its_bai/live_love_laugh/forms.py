from django import forms
from .models import Quote

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['text', 'source', 'weight', 'author']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
            'weight': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }