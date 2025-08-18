from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Quote

class QuoteForm(forms.ModelForm):
    """
    Форма для добавления циаты
    """
    class Meta:
        model = Quote
        fields = ['text', 'source', 'weight', 'author']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
            'weight': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }
    
    def clean_text(self):
        """ 
        Обработка повторного введения цитаты 
        """
        text = self.cleaned_data['text'].strip()
        if Quote.objects.filter(text__iexact=text).exists():
            raise forms.ValidationError(_("Ваши вкусы с кем-то совпадают! Цитата была уже добавлена ранее."))
        return text

    def clean_source(self):
        """ 
        Обработка введения цитаты из популярного источника 
        """
        source = self.cleaned_data['source'].strip()
        count = Quote.objects.filter(source__iexact=source).count()
        if count >= 3:
            raise forms.ValidationError(_("Вау! Этот источник очень популярен! Добавить больше цитат не получится :("))
        return source
