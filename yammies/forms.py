from ajax_select import make_ajax_field
from django.forms import ModelForm
from .models import ModDependency

class ModRelationForm(ModelForm):

    class Meta:
        model = ModDependency
        fields = ["relation", "dependency"]

    dependency = make_ajax_field(ModDependency, 'dependency', 'mod', help_text=None)