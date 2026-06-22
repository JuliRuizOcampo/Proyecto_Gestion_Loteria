from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import RegistroLoteria

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'admin',
                'autocomplete': 'username',
            }
        )
    )
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'admin123',
                'autocomplete': 'current-password',
            }
        ),
    )

# ModelForm genera automáticamente el formulario basado en el modelo
class RegistroLoteriaForm(forms.ModelForm):

    class Meta:
        # Le decimos a Django en qué modelo se basa este formulario
        model = RegistroLoteria

        # Qué campos del modelo incluir en el formulario
        fields = ['numero', 'fecha']

        # Personalizar los widgets (cómo se renderiza cada campo en HTML)
        widgets = {
            'numero': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 4521'
            }),
            'fecha': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'  # Activa el selector de fecha del navegador
            }),
        }

    def clean_numero(self):
        numero = self.cleaned_data.get('numero')
        if numero is None or numero <= 0:
            raise forms.ValidationError(
                'Ingrese un número ganador válido mayor que cero.'
            )
        return numero

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if fecha:
            # Excluir el registro actual si se está editando
            query = RegistroLoteria.objects.filter(fecha=fecha)
            if self.instance.pk:
                query = query.exclude(pk=self.instance.pk)
            
            if query.exists():
                raise forms.ValidationError(
                    'Ya existe un número ganador registrado para la fecha seleccionada.'
                )
        return fecha
