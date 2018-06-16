from django import forms



class ClassifyForm(forms.Form):
    text = forms.CharField(label='Enter some text to classify:', widget=forms.Textarea, max_length=1000)