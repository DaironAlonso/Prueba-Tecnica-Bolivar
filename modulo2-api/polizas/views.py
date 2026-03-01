import logging
from datetime import date
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Poliza, Riesgo
from .serializers import PolizaSerializer, RiesgoSerializer, RenovarSerializer

logger = logging.getLogger(__name__)


# ── GET /polizas  |  POST /polizas ───────────────────────────────────────────
@api_view(['GET', 'POST'])
def listar_polizas(request):
    if request.method == 'GET':
        polizas = Poliza.objects.all()

        tipo = request.query_params.get('tipo')
        estado = request.query_params.get('estado')

        if tipo:
            polizas = polizas.filter(tipo=tipo.upper())
        if estado:
            polizas = polizas.filter(estado=estado.upper())

        serializer = PolizaSerializer(polizas, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PolizaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# ── GET /polizas/{id}/riesgos ─────────────────────────────────────────────────
@api_view(['GET'])
def listar_riesgos(request, pk):
    try:
        poliza = Poliza.objects.get(pk=pk)
    except Poliza.DoesNotExist:
        return Response({'error': 'Póliza no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    riesgos = poliza.riesgos.all()
    serializer = RiesgoSerializer(riesgos, many=True)
    return Response(serializer.data)


# ── POST /polizas/{id}/renovar ────────────────────────────────────────────────
@api_view(['POST'])
def renovar_poliza(request, pk):
    try:
        poliza = Poliza.objects.get(pk=pk)
    except Poliza.DoesNotExist:
        return Response({'error': 'Póliza no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    if poliza.estado == 'CANCELADA':
        return Response(
            {'error': 'No se puede renovar una póliza cancelada'},
            status=status.HTTP_409_CONFLICT
        )

    serializer = RenovarSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    ipc = serializer.validated_data['ipc'] / 100
    poliza.valor_canon = round(poliza.valor_canon * (1 + ipc), 2)
    poliza.valor_prima = round(poliza.valor_prima * (1 + ipc), 2)
    poliza.estado = 'RENOVADA'
    poliza.save()

    return Response(PolizaSerializer(poliza).data)


# ── POST /polizas/{id}/cancelar ───────────────────────────────────────────────
@api_view(['POST'])
def cancelar_poliza(request, pk):
    try:
        poliza = Poliza.objects.get(pk=pk)
    except Poliza.DoesNotExist:
        return Response({'error': 'Póliza no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    if poliza.estado == 'CANCELADA':
        return Response(
            {'error': 'La póliza ya está cancelada'},
            status=status.HTTP_409_CONFLICT
        )

    # Cancela todos los riesgos en cascada
    poliza.riesgos.filter(estado='ACTIVO').update(
        estado='CANCELADO',
        fecha_cancelacion=date.today()
    )
    poliza.estado = 'CANCELADA'
    poliza.save()

    return Response(PolizaSerializer(poliza).data)


# ── POST /polizas/{id}/riesgos ────────────────────────────────────────────────
@api_view(['POST'])
def agregar_riesgo(request, pk):
    try:
        poliza = Poliza.objects.get(pk=pk)
    except Poliza.DoesNotExist:
        return Response({'error': 'Póliza no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    if poliza.tipo != 'COLECTIVA':
        return Response(
            {'error': 'Solo se pueden agregar riesgos a pólizas COLECTIVAS'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if poliza.estado == 'CANCELADA':
        return Response(
            {'error': 'No se pueden agregar riesgos a una póliza cancelada'},
            status=status.HTTP_409_CONFLICT
        )

    serializer = RiesgoSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    riesgo = serializer.save(poliza=poliza)
    return Response(RiesgoSerializer(riesgo).data, status=status.HTTP_201_CREATED)


# ── POST /riesgos/{id}/cancelar ───────────────────────────────────────────────
@api_view(['POST'])
def cancelar_riesgo(request, pk):
    try:
        riesgo = Riesgo.objects.get(pk=pk)
    except Riesgo.DoesNotExist:
        return Response({'error': 'Riesgo no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    if riesgo.estado == 'CANCELADO':
        return Response(
            {'error': 'El riesgo ya está cancelado'},
            status=status.HTTP_409_CONFLICT
        )

    riesgo.estado = 'CANCELADO'
    riesgo.fecha_cancelacion = date.today()
    riesgo.save()

    return Response(RiesgoSerializer(riesgo).data)


# ── POST /core-mock/evento ────────────────────────────────────────────────────
@api_view(['POST'])
def core_mock_evento(request):
    evento = request.data.get('evento')
    poliza_id = request.data.get('polizaId')

    logger.info(f"[CORE-MOCK] Evento '{evento}' enviado al CORE para póliza ID: {poliza_id}")

    return Response({
        'mensaje': 'Evento registrado y enviado al CORE',
        'evento': evento,
        'polizaId': poliza_id
    })
