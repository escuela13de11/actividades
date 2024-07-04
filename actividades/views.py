# actividades/views.py
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Resultado
from django.db.models import Avg
import random

ALLOWED_USERS = ['A', 'B', 'C', 'D', 'E', 'superuser']
USERS_6TO = ['A', 'B']
USERS_7MO = ['C', 'D', 'E']

# actividades/views.py

def home(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        print(f"Username received: {username}")
        if username in ALLOWED_USERS:
            if username == 'superuser':
                print("Redirecting to superuser_view")
                return HttpResponseRedirect(reverse('actividades:superuser_view'))
            print(f"Redirecting to grade_selection for user: {username}")
            return HttpResponseRedirect(reverse('actividades:grade_selection', args=(username,)))
        else:
            print("Invalid user")
            return HttpResponse("Usuario incorrecto")
    return render(request, 'home.html')



def generar_fraccion():
    numerador = random.randint(1, 9)
    denominador = random.randint(2, 9)  # El denominador no puede ser 1
    return (numerador, denominador)

def grade_selection(request, username):
    if username in USERS_6TO:
        grade = '6to'
    elif username in USERS_7MO:
        grade = '7mo'
    else:
        return HttpResponse("Usuario incorrecto")

    context = {
        'username': username,
        'grade': grade,
    }
    return render(request, 'grade_selection.html', context)

# actividades/views.py
# actividades/views.py

from django.urls import reverse

# actividades/views.py

# actividades/views.py

# actividades/views.py

# actividades/views.py

from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Resultado

# actividades/views.py

from django.shortcuts import render, redirect
from .models import Resultado

# actividades/views.py

from django.shortcuts import render, redirect
from .models import Resultado

# actividades/views.py
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Resultado

def superuser_view(request):
    # Obtener resultados de todas las actividades
    all_results = Resultado.objects.all()
    
    # Obtener respuestas a la actividad "sistema_numeracion"
    sistema_numeracion_results = Resultado.objects.filter(actividad='sistema_numeracion', estado_correccion='pendiente')

    if request.method == 'POST':
        # Procesar la corrección de una actividad
        actividad_id = int(request.POST.get('actividad_id'))
        puntaje = request.POST.get('puntaje')
        comentarios = request.POST.get('comentarios')
        resultado = Resultado.objects.get(id=actividad_id)
        resultado.puntaje = puntaje
        resultado.comentarios = comentarios
        resultado.estado_correccion = 'corregida'
        resultado.save()
        return redirect('actividades:superuser_view')
    
    return render(request, 'superuser_view.html', {
        'all_results': all_results,
        'sistema_numeracion_results': sistema_numeracion_results,
    })

def actividad1(request, username):
    if request.method == 'POST':
        correctas = 0
        detalles = []
        ventana_perdida = int(request.POST.get('ventana_perdida', 0))

        for i in range(1, 4):
            num1 = int(request.POST[f'num1_{i}'])
            den1 = int(request.POST[f'den1_{i}'])
            num2 = int(request.POST[f'num2_{i}'])
            den2 = int(request.POST[f'den2_{i}'])
            user_answer = request.POST[f'user_answer_{i}']

            if den1 == 0 or den2 == 0:
                continue  # Ignorar entrada inválida

            resultado_correcto = (num1 * den2 + num2 * den1) / (den1 * den2)

            try:
                user_num, user_den = map(int, user_answer.split('/'))
                if user_den == 0:
                    continue  # Ignorar entrada inválida
                user_resultado = user_num / user_den
            except ZeroDivisionError:
                continue  # Ignorar entrada inválida

            if round(user_resultado, 2) == round(resultado_correcto, 2):
                correctas += 1
                detalles.append(f'{num1}/{den1} + {num2}/{den2} = {user_answer} - Correcto')
            else:
                detalles.append(f'{num1}/{den1} + {num2}/{den2} = {user_answer} - Incorrecto (Correcto: {num1*den2 + num2*den1}/{den1*den2})')

        puntaje = (correctas / 3) * 100
        detalles_str = "; ".join(detalles)

        resultado = Resultado(
            usuario=username,
            actividad='Actividad 1',
            puntaje=round(puntaje, 2),
            detalles=detalles_str,
            ventana_perdida=ventana_perdida  # Guardar el número de veces que se perdió el enfoque
        )
        resultado.save()

        return redirect(reverse('actividades:index', kwargs={'username': username}))

    fracciones = [(generar_fraccion(), generar_fraccion()) for _ in range(3)]
    context = {
        'username': username,
        'num1_1': fracciones[0][0][0], 'den1_1': fracciones[0][0][1], 'num2_1': fracciones[0][1][0], 'den2_1': fracciones[0][1][1],
        'num1_2': fracciones[1][0][0], 'den1_2': fracciones[1][0][1], 'num2_2': fracciones[1][1][0], 'den2_2': fracciones[1][1][1],
        'num1_3': fracciones[2][0][0], 'den1_3': fracciones[2][0][1], 'num2_3': fracciones[2][1][0], 'den2_3': fracciones[2][1][1],
    }
    return render(request, 'actividad1.html', context)

def actividad2(request, username):
    if request.method == 'POST':
        respuestas_correctas = 0
        detalles = []
        ventana_perdida = int(request.POST.get('ventana_perdida', 0))

        for i in range(1, 4):
            try:
                num1, den1 = int(request.POST[f'num1_{i}']), int(request.POST[f'den1_{i}'])
                num2, den2 = int(request.POST[f'num2_{i}']), int(request.POST[f'den2_{i}'])
                user_answer = request.POST[f'user_answer_{i}']
            except KeyError:
                return redirect(reverse('actividades:actividad2', kwargs={'username': username}))

            fraccion1 = num1 / den1
            fraccion2 = num2 / den2

            if fraccion1 > fraccion2:
                correct_answer = 'mayor'
            elif fraccion1 < fraccion2:
                correct_answer = 'menor'
            else:
                correct_answer = 'igual'

            if user_answer == correct_answer:
                respuestas_correctas += 1
                detalles.append(f'{num1}/{den1} comparado con {num2}/{den2}: {user_answer} - Correcto')
            else:
                detalles.append(f'{num1}/{den1} comparado con {num2}/{den2}: {user_answer} - Incorrecto (Correcto: {correct_answer})')

        puntaje = (respuestas_correctas / 3) * 100
        detalles_str = "; ".join(detalles)

        resultado = Resultado(
            usuario=username,
            actividad='Actividad 2',
            puntaje=round(puntaje, 2),
            detalles=detalles_str,
            ventana_perdida=ventana_perdida  # Guardar el número de veces que se perdió el enfoque
        )
        resultado.save()

        return redirect(reverse('actividades:index', kwargs={'username': username}))

    fracciones = [(generar_fraccion(), generar_fraccion()) for _ in range(3)]
    context = {
        'username': username,
        'fracciones': fracciones
    }
    return render(request, 'actividad2.html', context)

def normalize_answer(answer):
    """Normalize the answer by converting commas to points and stripping whitespace."""
    return answer.replace(',', '.').strip()

def actividad3(request, username):
    if request.method == 'POST':
        respuestas_correctas = 0
        detalles = []
        ventana_perdida = int(request.POST.get('ventana_perdida', 0))

        # Respuestas correctas
        respuestas_correctas_dict = {
            'respuesta_1a': '0.1',
            'respuesta_1b': '0.01',
            'respuesta_1c': '0.001',
            'respuesta_2a': '4.2',  # Comparación directa como decimal
            'respuesta_2b': '2.5',  # Comparación directa como decimal
        }

        for key, correct_value in respuestas_correctas_dict.items():
            user_answer = request.POST.get(key, '')
            normalized_user_answer = normalize_answer(user_answer)
            
            try:
                user_value = float(eval(normalized_user_answer))
                correct_value_float = float(correct_value)
                if round(user_value, 2) == round(correct_value_float, 2):
                    respuestas_correctas += 1
                    detalles.append(f'{key}: {user_answer} - Correcto')
                else:
                    detalles.append(f'{key}: {user_answer} - Incorrecto (Correcto: {correct_value})')
            except (ValueError, SyntaxError):
                detalles.append(f'{key}: {user_answer} - Incorrecto (Correcto: {correct_value})')

        puntaje = (respuestas_correctas / len(respuestas_correctas_dict)) * 100
        detalles_str = "; ".join(detalles)

        resultado = Resultado(
            usuario=username,
            actividad='Actividad 3',
            puntaje=round(puntaje, 2),
            ventana_perdida=ventana_perdida,  # Guardar el número de veces que se perdió el enfoque
            detalles=detalles_str
        )
        resultado.save()

        return redirect(reverse('actividades:index', kwargs={'username': username}))

    return render(request, 'actividad3.html', {'username': username})


def index(request, username):
    if username in USERS_6TO:
        grade = '6to'
        activities = ['Actividad 1', 'Actividad 2']
    elif username in USERS_7MO:
        grade = '7mo'
        activities = ['Actividad 3']
    else:
        return HttpResponse("Usuario incorrecto")

    user_activities = Resultado.objects.filter(usuario=username, actividad__in=activities)
    
    promedio_actividad1 = user_activities.filter(actividad='Actividad 1').aggregate(Avg('puntaje'))['puntaje__avg'] or 0
    promedio_actividad2 = user_activities.filter(actividad='Actividad 2').aggregate(Avg('puntaje'))['puntaje__avg'] or 0
    promedio_actividad3 = user_activities.filter(actividad='Actividad 3').aggregate(Avg('puntaje'))['puntaje__avg'] or 0
    
    context = {
        'username': username,
        'grade': grade,
        'user_activities': user_activities,
        'promedio_actividad1': round(promedio_actividad1, 2),
        'promedio_actividad2': round(promedio_actividad2, 2),
        'promedio_actividad3': round(promedio_actividad3, 2),
    }
    return render(request, 'index.html', context)

def matematica_6to(request, username):
    return render(request, 'matematica_6to.html', {'username': username})

def lengua_6to(request, username):
    return render(request, 'lengua_6to.html', {'username': username})

def matematica_7mo(request, username):
    return render(request, 'matematica_7mo.html', {'username': username})

def lengua_7mo(request, username):
    return render(request, 'lengua_7mo.html', {'username': username})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import SistemaNumeracionForm
from .models import Actividad, Estudiante

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import SistemaNumeracionForm
from .models import Actividad, Estudiante

from django.shortcuts import render, get_object_or_404, redirect
from .models import Estudiante, Actividad
from .forms import SistemaNumeracionForm

# actividades/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Estudiante, Actividad
from .forms import SistemaNumeracionForm

# actividades/views.py

# actividades/views.py

from django.shortcuts import render, redirect
from .forms import SistemaNumeracionForm


# actividades/views.py

# actividades/views.py

# actividades/views.py

from django.shortcuts import render, redirect
from .forms import SistemaNumeracionForm

def sistema_numeracion(request, username):
    if username not in ALLOWED_USERS:
        return redirect('home')  # Redirige a una página de inicio o de error si el usuario no está permitido

    # Buscar si ya existe un resultado para esta actividad y usuario
    resultado = Resultado.objects.filter(usuario=username, actividad='sistema_numeracion').first()

    if resultado and resultado.estado_correccion == 'corregida':
        # Mostrar el puntaje y comentarios si ya fue corregida
        context = {
            'resultado': resultado,
            'username': username,
        }
        return render(request, 'actividades/sistema_numeracion_resultado.html', context)

    if request.method == 'POST':
        form = SistemaNumeracionForm(request.POST)
        if form.is_valid():
            respuesta = form.cleaned_data['respuesta']
            # Si ya existe un resultado pendiente, actualizar la respuesta
            if resultado:
                resultado.respuesta = respuesta
            else:
                # Crear un nuevo resultado si no existe
                resultado = Resultado(
                    usuario=username,
                    actividad='sistema_numeracion',
                    respuesta=respuesta,
                    estado_correccion='pendiente'
                )
            resultado.save()
            return redirect('actividades:matematica_6to', username=username)  # Redirige al listado de actividades o a una página de éxito
    else:
        form = SistemaNumeracionForm()

    return render(request, 'actividades/sistema_numeracion.html', {'form': form, 'username': username})


# actividades/views.py

from django.shortcuts import render, redirect
from django.conf import settings

# Simulación de una base de datos en memoria para almacenar actividades
actividades_pendientes = []

def corregir_actividad(request):
    if request.user.username != 'superuser':
        return redirect('home')  # Redirige a la página de inicio si no es superuser

    if request.method == 'POST':
        actividad_id = int(request.POST.get('actividad_id'))
        actividad = actividades_pendientes[actividad_id]
        actividad['puntaje'] = request.POST.get('puntaje')
        actividad['comentarios'] = request.POST.get('comentarios')
        actividad['estado_correccion'] = 'corregida'
        return redirect('corregir_actividad')
    
    return render(request, 'actividades/corregir_actividad.html', {'actividades': actividades_pendientes})


# actividades/views.py
from django.shortcuts import render

from django.shortcuts import render
import random

def multiplos_y_divisores_i(request, username):
    actividad = {
        'titulo': "Múltiplos y Divisores I",
        'preguntas': [
            {
                'numero': 1,
                'texto': "Si en la calculadora vas sumando de 8 en 8 a partir de 0, ¿cuáles de los siguientes números van a aparecer? Primero decidí y luego comprobá con la calculadora.",
                'opciones': ["160", "161", "320", "322", "480", "488"],
                'correctas': ["160", "320", "480", "488"]
            },
            {
                'numero': 2,
                'texto': "Ingresá un número de 3 cifras en la calculadora.",
                'subpreguntas': [
                    {
                        'letra': 'a',
                        'texto': "Restale 6 todas las veces que puedas. Ganás si en algún momento aparece 0 en el visor. Anotá dos números que te permitan ganar.",
                        'respuesta_correcta': []  # Este campo se usará para una futura validación si es necesario
                    },
                    {
                        'letra': 'b',
                        'texto': "Marcá con una X con cuáles de los siguientes números se gana.",
                        'opciones': ["600", "540", "542", "122", "204", "240"],
                        'correctas': ["600", "540", "204", "240"]  # Múltiplos de 6
                    }
                ]
            },
            {
                'numero': 3,
                'texto': "En una calculadora, se parte de 0, se va sumando de 4 en 4 y se llega a un número mayor que 203 y menor que 218. ¿Cuál puede ser ese número? ¿Hay más de una posibilidad?",
                'correctas': [num for num in range(204, 218, 4)]  # Múltiplos de 4 entre 203 y 218
            },
            {
                'numero': 4,
                'texto': "Usando la calculadora, encontrá 3 múltiplos de 6 que tengan 4 cifras.",
                'correctas': []  # Validación manual
            },
            {
                'numero': 5,
                'texto': "Usando la calculadora, decidí cuáles de los siguientes números son múltiplos de 7. Marcalos con una X.",
                'opciones': ["1351", "1456", "6356", "4727", "5467", "2465"],
                'correctas': ["1351", "1456", "6356", "5467"]
            },
            {
                'numero': 6,
                'subpreguntas': [
                    {
                        'letra': 'a',
                        'texto': "Usando solo la calculadora, decidí si 7 es divisor de 9478 y de 2887",
                        'opciones': ["9478", "2887"],
                        'correctas': ["9478"]
                    },
                    {
                        'letra': 'b',
                        'texto': "El número 3245 no es múltiplo de 7. Haciendo cálculos solo con la calculadora, decidí cuánto hay que restarle a 3245 como mínimo para que sea múltiplo de 7.",
                        'correcta': "4"
                    }
                ]
            },
            {
                'numero': 7,
                'texto': "Usando la calculadora, encontrá todos los múltiplos de 4 que estén entre 251 y 263.",
                'correctas': ["252", "256", "260"]
            },
            {
                'numero': 8,
                'texto': "Decidí si las siguientes afirmaciones son verdaderas (V) o falsas (F) y explicá cómo te diste cuenta.",
                'afirmaciones': [
                    {'texto': "Si un número es más grande que otro, tendrá más divisores.", 'correcta': "F"},
                    {'texto': "Si un número es múltiplo de otro, entonces la división del primero por el segundo da como resto 0.", 'correcta': "V"},
                    {'texto': "La cantidad de múltiplos de un número es infinita.", 'correcta': "V"},
                    {'texto': "La cantidad de divisores de un número es infinita.", 'correcta': "F"}
                ]
            }
        ]
    }

    resultados = {
        'resultado_1': None,
        'resultado_2a': None,
        'resultado_2b': None,
        'resultado_3': None,
        'resultado_4': None,
        'resultado_5': None,
        'resultado_6a': None,
        'resultado_6b': None,
        'resultado_7': None,
        'resultado_8': None,
    }
    errores = {
        'error_message_2a': None,
        'error_message_4': None,
    }

    respuestas = {
        'respuestas_1': request.POST.getlist('pregunta_1', []),
        'respuesta_2a_1': request.POST.get('pregunta_2a_1', ''),
        'respuesta_2a_2': request.POST.get('pregunta_2a_2', ''),
        'respuestas_2b': request.POST.getlist('pregunta_2b', []),
        'respuesta_3': request.POST.get('pregunta_3', ''),
        'respuesta_4': [request.POST.get(f'pregunta_4_{i}', '') for i in range(1, 4)],
        'respuestas_5': request.POST.getlist('pregunta_5', []),
        'respuestas_6a': request.POST.getlist('pregunta_6a', []),
        'respuesta_6b': request.POST.get('pregunta_6b', ''),
        'respuestas_7': request.POST.getlist('pregunta_7', []),
        'respuestas_8': request.POST.getlist('pregunta_8', [])
    }

    if request.method == "POST":
        if 'submit_1' in request.POST:
            correctas_1 = actividad['preguntas'][0]['correctas']
            if all(item in correctas_1 for item in respuestas['respuestas_1']) and len(respuestas['respuestas_1']) == len(correctas_1):
                resultados['resultado_1'] = "Bien"
            else:
                resultados['resultado_1'] = "Mal"

        if 'submit_2a' in request.POST:
            if not respuestas['respuesta_2a_1'] or not respuestas['respuesta_2a_2']:
                errores['error_message_2a'] = "Por favor, completa ambas respuestas para la pregunta 2a."
                resultados['resultado_2a'] = None
            else:
                try:
                    respuesta_2a_1 = int(respuestas['respuesta_2a_1'])
                    respuesta_2a_2 = int(respuestas['respuesta_2a_2'])
                    if respuesta_2a_1 % 6 == 0 and respuesta_2a_2 % 6 == 0:
                        resultados['resultado_2a'] = "Bien"
                    else:
                        resultados['resultado_2a'] = "Mal"
                except ValueError:
                    errores['error_message_2a'] = "Por favor, ingresa números válidos para la pregunta 2a."
                    resultados['resultado_2a'] = None

        if 'submit_2b' in request.POST:
            correctas_2b = actividad['preguntas'][1]['subpreguntas'][1]['correctas']
            if all(item in correctas_2b for item in respuestas['respuestas_2b']) and len(respuestas['respuestas_2b']) == len(correctas_2b):
                resultados['resultado_2b'] = "Bien"
            else:
                resultados['resultado_2b'] = "Mal"

        if 'submit_3' in request.POST:
            try:
                respuesta_3 = int(respuestas['respuesta_3'])
                if respuesta_3 in actividad['preguntas'][2]['correctas']:
                    resultados['resultado_3'] = "Bien"
                else:
                    resultados['resultado_3'] = "Mal"
            except ValueError:
                resultados['resultado_3'] = "Mal"

        if 'submit_4' in request.POST:
            if all(respuestas['respuesta_4']):
                try:
                    respuestas_4_validas = all(int(resp) % 6 == 0 and 1000 <= int(resp) < 10000 for resp in respuestas['respuesta_4'])
                    if respuestas_4_validas:
                        resultados['resultado_4'] = "Bien"
                    else:
                        resultados['resultado_4'] = "Mal"
                except ValueError:
                    errores['error_message_4'] = "Por favor, ingresa números válidos de 4 cifras para la pregunta 4."
                    resultados['resultado_4'] = None
            else:
                errores['error_message_4'] = "Por favor, completa todas las respuestas para la pregunta 4."

        if 'submit_5' in request.POST:
            correctas_5 = actividad['preguntas'][4]['correctas']
            if all(item in correctas_5 for item in respuestas['respuestas_5']) and len(respuestas['respuestas_5']) == len(correctas_5):
                resultados['resultado_5'] = "Bien"
            else:
                resultados['resultado_5'] = "Mal"

        if 'submit_6' in request.POST:
            correctas_6a = actividad['preguntas'][5]['subpreguntas'][0]['correctas']
            if all(item in correctas_6a for item in respuestas['respuestas_6a']) and len(respuestas['respuestas_6a']) == len(correctas_6a):
                resultados['resultado_6a'] = "Bien"
            else:
                resultados['resultado_6a'] = "Mal"

            correcta_6b = actividad['preguntas'][5]['subpreguntas'][1]['correcta']
            if respuestas['respuesta_6b'] == correcta_6b:
                resultados['resultado_6b'] = "Bien"
            else:
                resultados['resultado_6b'] = "Mal"

        if 'submit_7' in request.POST:
            correctas_7 = actividad['preguntas'][6]['correctas']
            if all(item in correctas_7 for item in respuestas['respuestas_7']) and len(respuestas['respuestas_7']) == len(correctas_7):
                resultados['resultado_7'] = "Bien"
            else:
                resultados['resultado_7'] = "Mal"

        if 'submit_8' in request.POST:
            correctas_8 = [afirmacion['correcta'] for afirmacion in actividad['preguntas'][7]['afirmaciones']]
            respuestas_8 = respuestas['respuestas_8']
            if all(respuestas_8[i] == correctas_8[i] for i in range(len(respuestas_8))):
                resultados['resultado_8'] = "Bien"
            else:
                resultados['resultado_8'] = "Mal"

    return render(request, 'actividades/multiplos_y_divisores_i.html', {
        'actividad': actividad,
        'username': username,
        'resultados': resultados,
        'errores': errores,
        'respuestas': respuestas,
    })
