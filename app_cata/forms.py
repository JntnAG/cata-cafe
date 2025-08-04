from django import forms
from django.core.exceptions import ValidationError
from .models import Cata
from django.core.validators import MinValueValidator, MaxValueValidator

# Función de validador personalizado
def validar_entre_0_y_10(valor):
    if valor is None or not (0 <= valor <= 10):
        raise ValidationError("Ingrese un número entero entre 0 y 10.")

# Lista de atributos sensoriales
atributos_sensoriales = [
    'fragancia', 'aroma', 'sabor', 'acidez', 'cuerpo',
    'uniformidad', 'dulzura', 'taza_limpia', 'balance', 'residual'
]

class CataForm(forms.ModelForm):
    nombre = forms.CharField(
    widget=forms.TextInput(attrs={
        'placeholder': 'Nombre Completo',
    }))
    identificacion = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Número de Identificación',}))
    matricula_cafe = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Id. del Café',}))
    class Meta:
        model = Cata
        fields = '__all__'
        widgets = {
            'tueste': forms.RadioSelect(choices=Cata.TUESTE_CHOICES),
            'fraganciaAroma': forms.NumberInput(attrs={'step': '0.25', 'min': '6', 'max': '10','placeholder': '6.0 a 10.0',}),            
            'sabor': forms.NumberInput(attrs={'step': '0.25', 'min': '6', 'max': '10','placeholder': '6.0 a 10.0',}),
            'residual': forms.NumberInput(attrs={'step': '0.25', 'min': '6', 'max': '10','placeholder': '6.0 a 10.0'}),
            'acidez': forms.NumberInput(attrs={'step': '0.25', 'min': '6', 'max': '10','placeholder': '6.0 a 10.0'}),
            'cuerpo': forms.NumberInput(attrs={'step': '0.25', 'min': '6', 'max': '10','placeholder': '6.0 a 10.0'}),
            'balance': forms.NumberInput(attrs={'step': '0.25', 'min': '6', 'max': '10','placeholder': '6.0 a 10.0'}),
            'puntaje_catador': forms.NumberInput(attrs={'step': '0.25', 'min': '6', 'max': '10','placeholder': '6.0 a 10.0'}),


            
            'intensidad_fragancia': forms.NumberInput(attrs={'type':'range','min': '0', 'max': '10', 'step':'1','class':'vertical-slider'}),
            'intensidad_aroma': forms.NumberInput(attrs={'type':'range','min': '0', 'max': '10', 'step':'1','class':'vertical-slider'}),
            'intensidad_acidez': forms.NumberInput(attrs={'type':'range','min': '0', 'max': '10', 'step':'1','class':'vertical-slider'}),
            'intensidad_cuerpo': forms.NumberInput(attrs={'type':'range','min': '0', 'max': '10', 'step':'1','class':'vertical-slider'}),
            
            'uniformidad': forms.NumberInput(attrs={'min': '0', 'max': '5','placeholder': '0 a 5'}),
            'taza_limpia': forms.NumberInput(attrs={'min': '0', 'max': '5','placeholder': '0 a 5'}),
            'dulzura': forms.NumberInput(attrs={'min': '0', 'max': '5','placeholder': '0 a 5'}),
            'tazas': forms.NumberInput(attrs={'min': '1', 'max': '10',}),
            'defectos_ligero': forms.NumberInput(attrs={'min': '0', 'max': '10'}),
            'defectos_rechazo': forms.NumberInput(attrs={'min': '0', 'max': '10'}),
            'observaciones': forms.Textarea(attrs={'rows': 3, 'style': 'width: 100%;'}),
        }

    # Validaciones personalizadas
    def clean(self):
        cleaned_data = super().clean()
        for campo in atributos_sensoriales:
            valor = cleaned_data.get(campo)
            if valor is not None and not (0 <= valor <= 10):
                self.add_error(campo, "Ingrese un número entero entre 0 y 10.")
