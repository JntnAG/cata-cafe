from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from .forms import CataForm
from .models import Cata

import matplotlib.pyplot as plt
import io
import base64

from django.shortcuts import render
import matplotlib
matplotlib.use('Agg')
from io import BytesIO
import urllib, base64
import numpy as np

from django.utils import timezone
import pytz


def home(request):
    return render(request, 'home.html')


def hacer_cata(request):
    if request.method == 'POST':
        form = CataForm(request.POST)
        if form.is_valid():
            cata = form.save()
            
            # Crear gráfico de radar con los nuevos atributos
            atributos = {
                'Fragancia/Aroma': cata.fraganciaAroma,
                'Sabor': cata.sabor,
                'Residual': cata.residual,
                'Acidez': cata.acidez,
                'Cuerpo': cata.cuerpo,
                'Uniformidad': 10 - (cata.uniformidad * 2),
                'Balance': cata.balance,
                'Taza Limpia': 10 - (cata.taza_limpia * 2),
                'Dulzura': 10 - (cata.dulzura * 2),
                'Puntaje Catador': cata.puntaje_catador_final
            }
            
            labels = list(atributos.keys())
            values = list(atributos.values())
            
            # Configurar el gráfico
            fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
            angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
            angles += angles[:1]
            values += values[:1]
            
            ax.plot(angles, values, color='#6f4e37', linewidth=2, linestyle='solid')
            ax.fill(angles, values, color='#6f4e37', alpha=0.2)
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(labels)
            ax.set_yticks([2, 4, 6, 8, 10])
            ax.set_ylim(0, 10)
            # ax.set_title('Perfil Sensorial de la Cata', size=16, pad=20)
            
            # Guardar gráfico
            buffer = io.BytesIO()
            plt.tight_layout()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
            buffer.close()
            plt.close(fig)
            
            # Preparar datos para la vista
            identificacion = str(cata.identificacion)
            ultimos_digitos = identificacion[-4:] if len(identificacion) >= 4 else identificacion
            
            # fecha_hora = cata.fecha.strftime('%d/%m/%Y %H:%M')
            if not cata.fecha:
                cata.fecha = timezone.now()
            cata.save()
            
            # Configurar zona horaria para Colombia
            bogota_tz = pytz.timezone('America/Bogota')
            fecha_local = timezone.localtime(cata.fecha, bogota_tz)
            fecha_hora = fecha_local.strftime('%d/%m/%Y %H:%M')

            return render(request, 'cata_exitosa.html', {
                'puntuacion': cata.puntuacion_total,
                'grafico': image_base64,
                'catador': cata.nombre,
                'fecha': fecha_hora,
                'matricula_cafe': cata.matricula_cafe,
                'ultimos_digitos': ultimos_digitos,
                'tueste': cata.get_tueste_display(),
                'tazas': cata.tazas
            })
        else:
            print(form.errors) 
    else:
        form = CataForm()
        
    return render(request, 'hacer_cata.html', {'form': form})



def cata_exitosa(request):
    # Esta vista ahora solo es accesible mediante hacer_cata
    return redirect('hacer_cata')

def ver_mis_catas(request):
    if request.method == 'POST' or request.GET.get('identificacion'):
        identificacion = request.POST.get('identificacion', request.GET.get('identificacion'))
        if identificacion:
            catas = Cata.objects.filter(identificacion=identificacion).order_by('-fecha')
            return render(request, 'ver_mis_catas.html', {
                'catas': catas,
                'identificacion': identificacion,
                'mostrar_resultados': True
            })
    
    return render(request, 'ver_mis_catas.html')

def detalle_cata(request, cata_id):
    cata = get_object_or_404(Cata, id=cata_id)

    # Crear gráfico de radar con atributos sensoriales
    atributos = {
        'Fragancia/Aroma': cata.fraganciaAroma,
        'Sabor': cata.sabor,
        'Residual': cata.residual,
        'Acidez': cata.acidez,
        'Cuerpo': cata.cuerpo,
        'Uniformidad': 10 - (cata.uniformidad * 2),
        'Balance': cata.balance,
        'Taza Limpia': 10 - (cata.taza_limpia * 2),
        'Dulzura': 10 - (cata.dulzura * 2),
        'Puntaje Catador': cata.puntaje_catador_final
    }

    labels = list(atributos.keys())
    values = list(atributos.values())
    values += values[:1]  # cerrar el radar
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    # Crear gráfico
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.plot(angles, values, color='#6f4e37', linewidth=2, linestyle='solid')
    ax.fill(angles, values, color='#6f4e37', alpha=0.2)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_ylim(0, 10)
    # ax.set_title('Perfil Sensorial de la Cata', size=16, pad=20)

    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    plt.close(fig)

    # Preparar variables para el template
    identificacion = str(cata.identificacion)
    ultimos_digitos = identificacion[-4:] if len(identificacion) >= 4 else identificacion
        # fecha_hora = cata.fecha.strftime('%d/%m/%Y %H:%M')
    if not cata.fecha:
        cata.fecha = timezone.now()
    cata.save()
    
    # Configurar zona horaria para Colombia
    bogota_tz = pytz.timezone('America/Bogota')
    fecha_local = timezone.localtime(cata.fecha, bogota_tz)
    fecha_hora = fecha_local.strftime('%d/%m/%Y %H:%M')

    return render(request, 'detalle_cata.html', {
        'puntuacion': cata.puntuacion_total,
        'grafico': image_base64,
        'catador': cata.nombre,
        'fecha': fecha_hora,
        'matricula_cafe': cata.matricula_cafe,
        'ultimos_digitos': ultimos_digitos,
        'tueste': cata.get_tueste_display(),
        'tazas': cata.tazas,
        'identificacion': cata.identificacion,
        'cata_id': cata.id,
    })

def ver_por_identificacion(request):
    identificacion = request.GET.get('identificacion')
    catas = []
    if identificacion:
        catas = Cata.objects.filter(identificacion=identificacion)
    return render(request, 'home.html', {'catas': catas})


def buscar_por_matricula(request):
    matricula = request.GET.get('matricula')

    if not matricula:
        return render(request, 'ver_por_matricula.html')

    resultados = Cata.objects.filter(matricula_cafe=matricula)

    if not resultados.exists():
        mensaje = f"No se encontró ninguna cata con la matrícula {matricula}."
        return render(request, 'ver_por_matricula.html', {'mensaje': mensaje})

    etiquetas = [
        'Fragancia/Aroma', 'Sabor', 'Residual', 'Acidez', 'Cuerpo',
        'Uniformidad', 'Balance', 'Taza Limpia', 'Dulzura', 'Puntaje Catador'
    ]

    valores_individuales = []
    nombres_catadores = []

    for cata in resultados:
        
        atributos = [
            cata.fraganciaAroma,
            cata.sabor,
            cata.residual,
            cata.acidez,
            cata.cuerpo,
            10 - (cata.uniformidad * 2),
            cata.balance,
            10 - (cata.taza_limpia * 2),
            10 - (cata.dulzura * 2),
            cata.puntaje_catador_final
        ]
        valores_individuales.append(atributos)
        nombres_catadores.append(cata.nombre)  # asegúrate de tener este campo

    valores_array = np.array(valores_individuales)
    promedio = list(np.mean(valores_array, axis=0))

    angles = np.linspace(0, 2 * np.pi, len(etiquetas), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    for valores, nombre in zip(valores_individuales, nombres_catadores):
        valores_cerrados = valores + valores[:1]
        ax.plot(angles, valores_cerrados, linewidth=1, label=nombre)
        ax.fill(angles, valores_cerrados, alpha=0.0)

    promedio += promedio[:1]
    ax.plot(angles, promedio, color='brown', linewidth=2, label='Promedio')
    ax.fill(angles, promedio, color='sienna', alpha=0.2)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(etiquetas)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_ylim(0, 10)
    fig.legend(loc='lower left',bbox_to_anchor=(0, 0), ncol=3, fontsize='small')  # fuera del gráfico si hay muchos nombres

    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    grafico_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    plt.close(fig)

    return render(request, 'ver_por_matricula.html', {
        'resultados': resultados,
        'grafico': grafico_base64,
        'matricula': matricula
    })



def editar_cata(request, cata_id):
    cata = get_object_or_404(Cata, id=cata_id)
    if request.method == 'POST':
        form = CataForm(request.POST, instance=cata)
        if form.is_valid():
            form.save()
            return redirect('detalle_cata', cata_id=cata.id)
    else:
        form = CataForm(instance=cata)
    return render(request, 'editar_cata.html', {
        'form': form,
        'identificacion': cata.identificacion  # 👈 para prellenar "volver a mis catas"
    })

def eliminar_cata(request, cata_id):
    cata = get_object_or_404(Cata, id=cata_id)
    if request.method == 'POST':
        cata.delete()
        return redirect('ver_por_identificacion')
    return render(request, 'eliminar_cata.html', {'cata': cata})

from django.shortcuts import redirect

def handler404(request, exception):
    return redirect('home')  # 'home' es el nombre de tu URL de inicio