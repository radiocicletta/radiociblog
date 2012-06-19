from djangotoolbox.fields import ListField, AbstractIterableField
from django.forms.widgets import SelectMultiple
from django.forms.fields import MultipleChoiceField
from django.contrib.auth.models import User

class ModelListField(ListField):
    def formfield(self, **kwargs):
        #return FormListField(**kwargs)
        return super(AbstractIterableField, self).formfield(**kwargs)

class ListFieldWidget(SelectMultiple):
    pass

#class FormListField(MultipleChoiceField):
#    """
#    This is a custom form field that can display a ModelListField as a Multiple Select GUI element.
#    """
#    widget = ListFieldWidget
#
#    def clean(self, value):
#        #TODO: clean your data in whatever way is correct in your case and return cleaned data instead of just the value
#        return value


