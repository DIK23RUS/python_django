from django import forms
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile


class UserBioForm(forms.Form):
    name = forms.CharField()
    age = forms.IntegerField(label="Age", min_value=2, max_value=120)
    bio = forms.CharField(label="User biography", widget=forms.Textarea)


def validate_file_name(file: InMemoryUploadedFile) -> None:
    if file.name and "virus" in file.name:
        raise ValidationError("File name should not contain 'virus'")


class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[validate_file_name])
