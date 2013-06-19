from django.forms import ModelForm
from .models import ScoreCard


class ScoreModelForm(ModelForm):
    """
    Form for entering Score.
    """

    class Meta:
        model = ScoreCard
        fields = (
            'score',
            'baskets',
        )