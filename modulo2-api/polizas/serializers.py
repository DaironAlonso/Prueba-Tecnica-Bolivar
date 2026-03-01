from rest_framework import serializers
from .models import Poliza, Riesgo


class RiesgoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Riesgo
        fields = ['id', 'descripcion', 'estado', 'fecha_cancelacion', 'created_at']
        read_only_fields = ['estado', 'fecha_cancelacion', 'created_at']


class PolizaSerializer(serializers.ModelSerializer):
    riesgos = RiesgoSerializer(many=True, read_only=True)

    class Meta:
        model = Poliza
        fields = [
            'id', 'tipo', 'estado', 'fecha_inicio', 'fecha_fin',
            'valor_canon', 'valor_prima', 'tomador', 'asegurado',
            'beneficiario', 'created_at', 'riesgos'
        ]
        read_only_fields = ['estado', 'created_at']


class RenovarSerializer(serializers.Serializer):
    ipc = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Porcentaje IPC, ejemplo: 9.28 para 9.28%"
    )