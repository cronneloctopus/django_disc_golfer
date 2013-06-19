from django.forms import ModelForm
from .models import ScoreCard


class ScoreModelForm(ModelForm):
    """
    Form for entering Score.
    """

    class Meta:
        model = ScoreCard
        fields = (
            'created',
            'score',
            'baskets',
        )

    def __init__(self, *args, **kwargs):

        super(ScoreModelForm, self).__init__(*args, **kwargs)

        self.fields['created'].label = 'Date'
