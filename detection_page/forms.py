from django import forms
from .models import Image
from PIL import Image as PILImage

class ImageForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = Image
        fields = ('title', 'image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'class':'image', 'id':'upload_file'})
        self.fields['title'].widget.attrs.update({'class': 'title'})
        
    def save(self, commit=True):
        instance = super().save(commit=False)

        image = self.cleaned_data.get('image')

        if image:
            # Open the uploaded image
            img = PILImage.open(image)

            # Resize the image
            resized_img = img.resize((299, 299))  # Adjust the desired width and height as needed

            # Save the resized image back to the instance
            instance.image = resized_img

        if commit:
            instance.save()

        return instance