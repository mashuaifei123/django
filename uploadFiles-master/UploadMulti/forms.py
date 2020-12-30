from django import forms
from .models import Photo, tsmcode, spss, xzx, word


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('file', )


class tsmForm(forms.ModelForm):
    class Meta:
        model = tsmcode
        fields = ('file', )


class spssForm(forms.ModelForm):
    class Meta:
        model = spss
        fields = ('file', )


class xzxForm(forms.ModelForm):
    class Meta:
        model = xzx
        fields = ('file', )

class wordForm(forms.ModelForm):
    class Meta:
        model = word
        fields = ('file', )