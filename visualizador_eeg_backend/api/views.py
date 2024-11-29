from rest_framework import viewsets
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Paciente, Sesion, Canal, Frecuencia, Enfermedad
from .serializers import PacienteSerializer, SesionSerializer, CanalSerializer, FrecuenciaSerializer, EnfermedadSerializer
from .edf_processor import cargar_archivo_edf, guardar_datos_en_base_de_datos
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Frecuencia, Canal, Paciente, Sesion, Enfermedad



class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer

class SesionViewSet(viewsets.ModelViewSet):
    queryset = Sesion.objects.all()
    serializer_class = SesionSerializer

class CanalViewSet(viewsets.ModelViewSet):
    queryset = Canal.objects.all()
    serializer_class = CanalSerializer

class FrecuenciaViewSet(viewsets.ModelViewSet):
    queryset = Frecuencia.objects.all()
    serializer_class = FrecuenciaSerializer

class EnfermedadViewSet(viewsets.ModelViewSet):
    queryset = Enfermedad.objects.all()
    serializer_class = EnfermedadSerializer


@csrf_exempt
def subir_edf(request):

    if request.method == 'POST':

         
        enfermedad_id = request.POST.get('enfermedad')
        print("Enfermedad ID recibido en el backend:", enfermedad_id)
        
        archivo = request.FILES.get('archivo_edf')  

        if archivo and archivo.name.endswith('.edf'):  
            ruta_archivo = f'uploads/{archivo.name}'
            print(f"Guardando archivo en: {ruta_archivo}") 
            with open(ruta_archivo, 'wb+') as f:
                for chunk in archivo.chunks():
                    f.write(chunk)

            
            datos_eeg = cargar_archivo_edf(ruta_archivo)  
            if datos_eeg:
                print("Datos del archivo EDF cargados correctamente.") 
               
                guardar_datos_en_base_de_datos(datos_eeg, datos_eeg['frecuencias'], enfermedad_id)
                return JsonResponse({'mensaje': 'Archivo procesado y datos insertados correctamente'})
            else:
                print("Error al procesar los datos del archivo EDF.")  
                return JsonResponse({'error': 'Error al procesar el archivo .edf'}, status=400)
        else:
            print("Archivo no válido o no proporcionado.")  
            return JsonResponse({'error': 'No se ha proporcionado un archivo válido'}, status=400)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@api_view(['GET'])
def obtener_frecuencias(request, sesion_id):
    canales = Canal.objects.filter(sesion__id=sesion_id)
    
    if not canales.exists():
        print("No se encontraron canales para esta sesión.") 
        return Response([])

    respuesta = []
    for canal in canales:

        
        frecuencias = Frecuencia.objects.filter(canal=canal).values_list('frecuencia', flat=True)
        
        if not frecuencias:
            print(f"No se encontraron frecuencias para el canal {canal.nombre_canal}.") 
        
        respuesta.append({
            'canal': canal.nombre_canal,
            'frecuencias': list(frecuencias)
        })

    return Response(respuesta)

@api_view(['GET'])
def obtener_sesiones(request):
    pacientes = Paciente.objects.all()

    respuesta = []

    for paciente in pacientes:
        sesiones = Sesion.objects.filter(paciente=paciente)
        
        sesiones_fecha = [sesion.fecha_sesion for sesion in sesiones]
        
        respuesta.append({
            'enfermedad': paciente.enfermedad.descripcion,  
            'paciente': paciente.nombre_paciente,  
            'sesiones': sesiones_fecha 
        })

    return Response(respuesta)

@api_view(['GET'])
def obtener_enfermedades_y_sesiones(request):
    try:
      
        respuesta = {}

 
        enfermedades = Enfermedad.objects.all()

        for enfermedad in enfermedades:
          
            pacientes = Paciente.objects.filter(enfermedad=enfermedad)

       
            sesiones_enfermedad = []
            for paciente in pacientes:
                sesiones = Sesion.objects.filter(paciente=paciente)
               
                for sesion in sesiones:
                    sesion_info = f"{paciente.nombre_paciente} - {sesion.fecha_sesion.strftime('%Y-%m-%d')}"
                    sesiones_enfermedad.append(sesion_info)


            respuesta[enfermedad.descripcion] = sesiones_enfermedad

        return Response(respuesta)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    
@api_view(['GET'])
def obtener_sesion_id(request):
    sesiones = Sesion.objects.all()

    respuesta = []

    for sesion in sesiones:
        respuesta.append({
            'sesionId': sesion.id,
            'pacienteId': sesion.paciente_id,
            'sesionesFecha': sesion.fecha_sesion
        })

    return Response(respuesta)
