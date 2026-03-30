from django import forms

class ColumnMappingForm(forms.Form):
    def __init__(self, *args, columns=None, data_types=None, **kwargs):
        super().__init__(*args, **kwargs)

        for column in columns:
            self.fields[column] = forms.ChoiceField(
                choices=[(v, k) for k, v in data_types.items()],
                widget=forms.Select(attrs={"class": "form-select"}),
                label=column,
                required = False
            )