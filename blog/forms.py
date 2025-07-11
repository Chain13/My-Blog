from django import forms
from .models import Post, Comment, ContactMessage
from ckeditor.widgets import CKEditorWidget
from .models import Profile
from taggit.forms import TagWidget
import json

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'content': forms.Textarea(attrs={'style': 'display:none;'}),
            'category': forms.Select(attrs={'class': 'w-full border rounded px-3 py-2'}),
            'tags': TagWidget(attrs={'id': 'tags-hidden', 'style': 'display:none;'}),
        }

    def clean_tags(self):
        raw = self.data.get('tags')

        # ✅ ตรวจสอบก่อนว่า raw เป็น list อยู่แล้วหรือไม่
        if isinstance(raw, list):
            return raw
        elif isinstance(raw, str):
            try:
                tag_data = json.loads(raw)
                if isinstance(tag_data, list):
                    return tag_data
                else:
                    raise forms.ValidationError("Invalid format for tags.")
            except json.JSONDecodeError:
                raise forms.ValidationError("Tags must be a valid JSON list.")
        else:
            return []

class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'w-full px-3 py-2 border border-gray-300 rounded',
    }))
    class Meta:
        model = Comment
        fields = ['body']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'w-full p-2 border rounded'}),
        }
        
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']  # ✅ เพิ่ม 'subject'