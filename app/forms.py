from django.forms import ModelForm
from .models import Constat


class ConstatForm(ModelForm):
    class Meta:
        model = Constat
        fields = '__all__'
