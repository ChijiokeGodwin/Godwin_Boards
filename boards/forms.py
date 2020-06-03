from django import forms
from .models import Board, Topic, Post

class NewTopicForm(forms.ModelForm) :
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'What is on your mind?'}),
        max_length=4000,
        help_text='The max length of the text is 4000.')

    class Meta :
        model = Topic
        fields = ['subject', 'message']


class NewBoardForm(forms.ModelForm) :
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 3, 'placeholder': 'Describe your form.'}),
        label='Board description', max_length=100,
        help_text='The max length of the text is 1000.')

    class Meta :
        model = Board
        fields = ['name', 'description']


class PostForm(forms.ModelForm) :
    class Meta :
        model = Post
        fields = ['message']
