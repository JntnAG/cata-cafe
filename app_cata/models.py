from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Cata(models.Model):
    # Opciones para el tueste
    TUESTE_CHOICES = [
        ('claro', 'Claro'),
        ('medio', 'Medio'),
        ('medio_oscuro', 'Medio Oscuro'),
        ('oscuro', 'Oscuro'),
    ]
    
    # Información del catador y café
    nombre = models.CharField(max_length=50)
    identificacion = models.CharField(max_length=20)
    matricula_cafe = models.CharField(max_length=10)
    tueste = models.CharField(max_length=15, choices=TUESTE_CHOICES, default='medio')

    # Atributos sensoriales (valores flotantes de 6.00 a 10.00 en incrementos de 0.25)
    fraganciaAroma = models.FloatField(
        validators=[MinValueValidator(6.0), MaxValueValidator(10.0)],
        help_text="Valor entre 6.00 y 10.00 en incrementos de 0.25",
    )

    sabor = models.FloatField(
        validators=[MinValueValidator(6.0), MaxValueValidator(10.0)],
        help_text="Valor entre 6.00 y 10.00 en incrementos de 0.25"
    )
    residual = models.FloatField(
        validators=[MinValueValidator(6.0), MaxValueValidator(10.0)],
        help_text="Valor entre 6.00 y 10.00 en incrementos de 0.25"
    )
    acidez = models.FloatField(
        validators=[MinValueValidator(6.0), MaxValueValidator(10.0)],
        help_text="Valor entre 6.00 y 10.00 en incrementos de 0.25"
    )
    cuerpo = models.FloatField(
        validators=[MinValueValidator(6.0), MaxValueValidator(10.0)],
        help_text="Valor entre 6.00 y 10.00 en incrementos de 0.25"
    )
    balance = models.FloatField(
        validators=[MinValueValidator(6.0), MaxValueValidator(10.0)],
        help_text="Valor entre 6.00 y 10.00 en incrementos de 0.25"
    )
    puntaje_catador = models.FloatField(
        validators=[MinValueValidator(6.0), MaxValueValidator(10.0)],
        help_text="Valor entre 6.00 y 10.00 en incrementos de 0.25"
    )

    # Intensidades (0-10)
    intensidad_fragancia = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="Intensidad de 0 a 10"
    )
    intensidad_aroma = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="Intensidad de 0 a 10"
    )
    intensidad_acidez = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="Intensidad de 0 a 10"
    )
    intensidad_cuerpo = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="Intensidad de 0 a 10"
    )

    # Checkboxes (cada uno resta 2 puntos)
    uniformidad = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Número de checkboxes marcados (0-5)",
        default=0
    )
    taza_limpia = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Número de checkboxes marcados (0-5)",
        default=0
    )
    dulzura = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Número de checkboxes marcados (0-5)",
        default=0
    )

    # Tazas y defectos
    tazas = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Número de tazas (1-10)",
        default=5
    )
    defectos_ligero = models.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Cantidad de defectos ligeros (cada uno resta 2 puntos)",
        default=0
    )
    defectos_rechazo = models.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Cantidad de defectos de rechazo (cada uno resta 4 puntos)",
        default=0
    )
    
    # Puntaje final calculado
    puntaje_catador_final = models.FloatField(editable=False)
    puntuacion_total = models.FloatField(editable=False)

    # Otros campos
    observaciones = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.defectos_ligero = self.defectos_ligero or 0
        self.defectos_rechazo = self.defectos_rechazo or 0
        # Calcular puntaje_catador_final
        self.puntaje_catador_final = self.puntaje_catador - (self.defectos_ligero * 2) - (self.defectos_rechazo * 4)
        
        # Calcular puntuación total ajustando los checkboxes (cada checkbox resta 2 puntos)
        self.puntuacion_total = (
            self.fraganciaAroma + self.sabor + self.residual + self.acidez +
            self.cuerpo + (10 - (self.uniformidad * 2)) + 
            (10 - (self.taza_limpia * 2)) + (10 - (self.dulzura * 2)) + 
            self.balance + self.puntaje_catador_final
        )
        print("Calculando puntajes:", self.puntaje_catador_final, self.puntuacion_total)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Cata de {self.nombre} - {self.matricula_cafe} ({self.fecha.date()})"