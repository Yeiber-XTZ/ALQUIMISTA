from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Facet, UserFacetPreference


class CustomUserCreationForm(UserCreationForm):
    """Formulario de registro personalizado."""
    email = forms.EmailField(
        required=True,
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 bg-white/5 border border-white/20 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500 text-white placeholder-white/50',
            'placeholder': 'tu@email.com',
            'style': 'color: #FFFFFF;'
        })
    )
    username = forms.CharField(
        label="Nombre de usuario",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-white/5 border border-white/20 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500 text-white placeholder-white/50',
            'placeholder': 'Nombre de usuario',
            'style': 'color: #FFFFFF;'
        })
    )
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 pr-12 bg-white/5 border border-white/20 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500 text-white placeholder-white/50',
            'placeholder': 'Contraseña',
            'style': 'color: #FFFFFF;'
        })
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 pr-12 bg-white/5 border border-white/20 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500 text-white placeholder-white/50',
            'placeholder': 'Confirma tu contraseña',
            'style': 'color: #FFFFFF;'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Obtener facetas activas para el formulario
        self.facets = Facet.objects.filter(activo=True).order_by('orden')
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class FacetSelectionForm(forms.Form):
    """Formulario para seleccionar facetas durante el registro."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        facets = Facet.objects.filter(activo=True).order_by('orden')
        self.facets = facets  # Hacer las facetas accesibles en el template
        for facet in facets:
            self.fields[f'facet_{facet.id}'] = forms.BooleanField(
                required=False,
                label=facet.titulo,
                widget=forms.CheckboxInput(attrs={
                    'class': 'w-5 h-5 text-red-600 border-gray-300 rounded focus:ring-red-500'
                })
            )
            self.fields[f'priority_{facet.id}'] = forms.IntegerField(
                required=False,
                initial=0,
                min_value=0,
                label=f'Prioridad de {facet.titulo}',
                widget=forms.NumberInput(attrs={
                    'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500',
                    'placeholder': '0',
                    'min': '0'
                })
            )


class LoginForm(forms.Form):
    """Formulario de inicio de sesión."""
    username = forms.CharField(
        label="Nombre de usuario",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500',
            'placeholder': 'Nombre de usuario'
        })
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 pr-12 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500',
            'placeholder': 'Contraseña'
        })
    )


class FacetManagementForm(forms.Form):
    """Formulario para gestionar facetas del usuario."""
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        facets = Facet.objects.filter(activo=True).order_by('orden')
        user_preferences = {
            pref.faceta_id: pref.prioridad 
            for pref in UserFacetPreference.objects.filter(usuario=user)
        }
        
        self.facets_list = []
        for facet in facets:
            is_selected = facet.id in user_preferences
            self.fields[f'facet_{facet.id}'] = forms.BooleanField(
                required=False,
                initial=is_selected,
                label=facet.titulo,
                widget=forms.CheckboxInput(attrs={
                    'class': 'facet-checkbox w-5 h-5 text-red-600 border-gray-300 rounded focus:ring-red-500',
                    'data-facet-id': facet.id
                })
            )
            self.fields[f'priority_{facet.id}'] = forms.IntegerField(
                required=False,
                initial=user_preferences.get(facet.id, 0),
                min_value=0,
                label=f'Prioridad',
                widget=forms.NumberInput(attrs={
                    'class': 'priority-input w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-red-500 focus:border-red-500',
                    'placeholder': '0',
                    'min': '0'
                })
            )
            if not is_selected:
                self.fields[f'priority_{facet.id}'].widget.attrs['disabled'] = True
            
            self.facets_list.append({
                'facet': facet,
                'is_selected': is_selected,
                'priority': user_preferences.get(facet.id, 0)
            })
