from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Quote

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['text', 'author', 'weight']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
            'weight': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }