from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Facet, UserFacetPreference


class CustomUserCreationForm(UserCreationForm):
    """Formulario de registro personalizado."""
    email = forms.EmailField(
        required=True,
        label="Correo electrónico",
        error_messages={
            'required': 'El correo electrónico es obligatorio.',
            'invalid': 'Por favor, ingresa un correo electrónico válido.',
            'unique': 'Este correo electrónico ya está registrado.',
        },
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'tu@email.com'
        })
    )
    username = forms.CharField(
        label="Nombre de usuario",
        min_length=3,
        max_length=150,
        error_messages={
            'required': 'El nombre de usuario es obligatorio.',
            'min_length': 'El nombre de usuario debe tener al menos 3 caracteres.',
            'max_length': 'El nombre de usuario no puede exceder 150 caracteres.',
            'unique': 'Este nombre de usuario ya está en uso.',
            'invalid': 'El nombre de usuario solo puede contener letras, números y los caracteres @/./+/-/_.',
        },
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Nombre de usuario'
        }),
        help_text='Requerido. 3-150 caracteres. Solo letras, números y @/./+/-/_.'
    )
    password1 = forms.CharField(
        label="Contraseña",
        error_messages={
            'required': 'La contraseña es obligatoria.',
        },
        widget=forms.PasswordInput(attrs={
            'class': 'form-input password-input',
            'placeholder': 'Contraseña'
        }),
        help_text='Mínimo 8 caracteres. No puede ser completamente numérica ni muy similar a tu información personal.'
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        error_messages={
            'required': 'Debes confirmar tu contraseña.',
            'password_mismatch': 'Las contraseñas no coinciden.',
        },
        widget=forms.PasswordInput(attrs={
            'class': 'form-input password-input',
            'placeholder': 'Confirma tu contraseña'
        }),
        help_text='Ingresa la misma contraseña que antes para verificación.'
    )
    rol = forms.ChoiceField(
        choices=[
            ('visitante', 'Visitante'),
            ('estudiante', 'Estudiante'),
        ],
        required=True,
        label="Rol",
        help_text="Selecciona tu rol: Visitante (acceso general) o Estudiante (acceso a material exclusivo)",
        widget=forms.Select(attrs={
            'class': 'form-input form-select'
        })
    )
    # Campos adicionales del perfil
    nombre = forms.CharField(
        required=False,
        label="Nombre",
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Tu nombre completo'
        })
    )
    id_usuario = forms.CharField(
        required=False,
        label="ID",
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'RUT, DNI, etc.'
        })
    )
    ciudad = forms.CharField(
        required=False,
        label="Ciudad",
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Santiago'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'rol')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Obtener facetas activas para el formulario
        self.facets = Facet.objects.filter(activo=True).order_by('orden')
        
    def save(self, commit=True):
        from .models import UserProfile
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        rol = self.cleaned_data.get('rol', 'visitante')
        if commit:
            user.save()
            # Crear o actualizar el perfil del usuario
            profile, created = UserProfile.objects.get_or_create(usuario=user)
            profile.rol = rol
            profile.nombre = self.cleaned_data.get('nombre', '')
            profile.id_usuario = self.cleaned_data.get('id_usuario', '')
            profile.ciudad = self.cleaned_data.get('ciudad', '')
            profile.save()
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
