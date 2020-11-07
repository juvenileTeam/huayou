from django import forms

from User.models import User, Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nickname', 'gender', 'birthday', 'location']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

    def clean_max_distance(self):
        cleaned_data = super().clean()
        if cleaned_data['max_distance'] < cleaned_data['min_distance']:
            raise forms.ValidationError('最大匹配范围必须要大于最小匹配范围')
        return cleaned_data['max_distance']

    def clean_max_dating_age(self):
        cleaned_data = super().clean()
        if cleaned_data['max_dating_age'] < cleaned_data['min_dating_age']:
            raise forms.ValidationError('最大匹配年龄必须要大于最小年龄范围')
        return cleaned_data['max_distance']
