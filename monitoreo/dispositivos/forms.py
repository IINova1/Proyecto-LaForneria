from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Device, Organization, CustomUser, Zone

class DispositivoForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['name', 'category', 'max_consumption', 'zone', 'status', 'organization', 'imagen']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'max_consumption': forms.NumberInput(attrs={'class': 'form-control'}),
            'zone': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(choices=[("ACTIVO", 'Activo'), ("INACTIVO", 'Inactivo')], attrs={'class': 'form-select'}),
            'organization': forms.Select(attrs={'class': 'form-select'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'})
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres")
        return name

class CustomRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    organization_name = forms.CharField(label='Organization Name')

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'organization_name']

    def save(self, commit=True):
        user = super().save(commit=False)
        org_name = self.cleaned_data['organization_name']

        # Asignar zona por defecto
        default_zone = Zone.objects.first()
        if not default_zone:
            raise forms.ValidationError("No hay zonas disponibles para asignar a la organización.")

        organization, created = Organization.objects.get_or_create(name=org_name, defaults={'zone': default_zone})
        user.organization = organization

        if commit:
            organization.save()
            user.save()
        return user