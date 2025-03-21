from django.forms import ModelForm, BooleanField
from django.core.exceptions import ValidationError

from catalog.models import Product


taboo_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance( field, BooleanField):
                field.widget.attrs['class'] = "form-check-input"
            else:
                field.widget.attrs['class'] = "form-control"


class CatalogForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Product
        exclude = ("views_counter", "owner")

class CatalogAdminForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Product
        exclude = ("views_counter",)

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 0:
            raise ValidationError ('Цена продукта не может быть отрицательной')
        return price

    def clean_name(self):
        name = self.cleaned_data.get('name')
        for word in taboo_words:
            if word in name.lower():
                raise ValidationError ('Это запрещенные слова, которые нельзя использовать в названиях продуктов')
        return name


    def clean_description(self):
        description = self.cleaned_data.get('description')
        for word in taboo_words:
            if word in description.lower():
                raise ValidationError ('Это запрещенные слова, которые нельзя использовать в описаниях продуктов')
        return description