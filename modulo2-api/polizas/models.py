from django.db import models


class Poliza(models.Model):
    TIPO_CHOICES = [
        ('INDIVIDUAL', 'Individual'),
        ('COLECTIVA', 'Colectiva'),
    ]
    ESTADO_CHOICES = [
        ('ACTIVA', 'Activa'),
        ('CANCELADA', 'Cancelada'),
        ('RENOVADA', 'Renovada'),
    ]

    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='ACTIVA')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    valor_canon = models.DecimalField(max_digits=12, decimal_places=2)
    valor_prima = models.DecimalField(max_digits=12, decimal_places=2)
    tomador = models.CharField(max_length=100)
    asegurado = models.CharField(max_length=100)
    beneficiario = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Poliza {self.id} - {self.tipo} - {self.estado}"


class Riesgo(models.Model):
    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('CANCELADO', 'Cancelado'),
    ]

    poliza = models.ForeignKey(Poliza, on_delete=models.CASCADE, related_name='riesgos')
    descripcion = models.CharField(max_length=255)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='ACTIVO')
    fecha_cancelacion = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Riesgo {self.id} - Poliza {self.poliza_id} - {self.estado}"
