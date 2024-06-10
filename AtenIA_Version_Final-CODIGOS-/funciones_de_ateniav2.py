import pyaudio  # Importar la biblioteca PyAudio para la grabación de audio
import wave  # Importar la biblioteca Wave para trabajar con archivos de audio
import speech_recognition as sr  # Importar la biblioteca SpeechRecognition para el reconocimiento de voz
import pyttsx3  # Importar la biblioteca pyttsx3 para la síntesis de voz
import requests  # Importamos la biblioteca requests para realizar solicitudes HTTP
from bs4 import BeautifulSoup  # Importamos BeautifulSoup para hacer scrapping de datos HTML
import webbrowser # importamos la libreria para abrir el navegador
from deep_translator import GoogleTranslator
from ctypes import cast, POINTER  # Importar las funciones necesarias desde ctypes
from comtypes import CLSCTX_ALL  # Importar el contexto de todas las clases desde comtypes
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume  # Importar las clases necesarias desde pycaw
import wikipedia  # Importa la librería wikipedia
import pyjokes  # Importar la biblioteca pyjokes
from moviepy.editor import VideoFileClip # Importar la clase VideoFileClip del módulo moviepy.editor para la manipulación de archivos de video
from threading import Thread # Importar la clase Thread del módulo threading para la ejecución de múltiples tareas en paralelo
import os
import sys
import subprocess
# Guarda la salida estándar actual
stdout_original = sys.stdout
# Redirige la salida estándar a un archivo vacío
sys.stdout = open('nul', 'w')
# Importa Pygame (esto evitará que se impriman las líneas)
import pygame # Importar el módulo pygame para la manipulación de gráficos y eventos
# Restaura la salida estándar original
sys.stdout = stdout_original
# Inicializar el motor de síntesis de voz
engine = pyttsx3.init()
# Función para que el asistente hable

def speak(text):
    """
La función "speak" se utiliza para convertir texto a voz utilizando un motor de síntesis de voz.

Argumentos:
texto: El parámetro texto en la función speak es el texto que se desea que el asistente vocalice 
en voz alta utilizando la síntesis de texto a voz. Cuando se llama a la función speak y se pasa una 
cadena de texto como argumento texto, el asistente convertirá ese texto en voz y lo reproducirá.
"""
    engine.say(text)  # Decir el texto
    engine.runAndWait()  # Esperar a que se complete la síntesis de voz

# Función para grabar audio y procesarlo
def grabar_audio(file_name="grabacion.wav", duration=5):
    """
función en Python llamada grabar_audio que graba audio durante una duración especificada y lo guarda en un archivo WAV. 
La función toma dos argumentos:  
   Argumentos:
file_name: El parámetro file_name en la función grabar_audio se utiliza para especificar el nombre del
 archivo donde se guardará la grabación de audio. De forma predeterminada, si no se proporciona ningún 
 file_name al llamar a la función, se guardará la grabación como "grabacion.wav".

duration: El parámetro duration en la función grabar_audio representa la duración en segundos durante 
la cual se grabará el audio. Este parámetro determina cuánto tiempo durará la grabación antes de detenerse 
automáticamente. El valor predeterminado es de 5 segundos.
    """
    CHUNK = 1024  # Tamaño de los fragmentos de audio
    FORMAT = pyaudio.paInt16  # Formato de audio
    CHANNELS = 1  # Número de canales de audio (mono)
    RATE = 44100  # Tasa de muestreo (número de muestras por segundo)

    audio = pyaudio.PyAudio()  # Inicializar PyAudio

    # Abrir el stream de audio para la grabación
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("Grabando...")

    frames = []  # Lista para almacenar los fragmentos de audio

    # Grabar audio durante el tiempo especificado
    for i in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)  # Leer datos del stream de audio
        frames.append(data)  # Agregar los datos al listado de frames

    print("Terminado de grabar")

    # Detener y cerrar el stream de audio
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Guardar la grabación en un archivo WAV
    with wave.open(file_name, 'wb') as wf:
        wf.setnchannels(CHANNELS)  # Configurar el número de canales
        wf.setsampwidth(audio.get_sample_size(FORMAT))  # Configurar el ancho de muestra
        wf.setframerate(RATE)  # Configurar la tasa de muestreo
        wf.writeframes(b''.join(frames))  # Escribir los frames al archivo WAV

# Función para procesar el audio grabado
def procesar_audio(file_name="grabacion.wav", language='es-ES'):
    """
    La función `procesar_audio` procesa la entrada de audio desde un archivo
    utilizando el reconocimiento de voz para convertirla en texto en el
    idioma especificado.

    Argumentos:
    file_name: El parámetro `file_name` en la función `procesar_audio` es una cadena que
    representa el nombre del archivo de audio que se desea procesar. De forma predeterminada,
    está configurado como "grabacion.wav", pero se puede proporcionar un nombre de archivo 
    diferente al llamar a la función si se tiene otro archivo de audio. El valor predeterminado 
    es "grabacion.wav".
    language: El parámetro `language` en la función `procesar_audio` especifica el idioma 
    en el que se realizará el reconocimiento de voz. En este caso, el idioma predeterminado está establecido en 'es-ES', que corresponde al español (España). Esto significa que la función intentará reconocer y transcribir el audio en español. El valor predeterminado es 'es-ES'.

    Returns:
    - La función `procesar_audio` devuelve el texto reconocido a partir del archivo de audio si el reconocimiento es exitoso. Si se produce un `sr.UnknownValueError`, imprime un mensaje y devuelve `None`. Si hay un `sr.RequestError`, también imprime un mensaje y devuelve `None`.
    """
    recognizer = sr.Recognizer()  # Inicializar el reconocedor de voz
    with sr.AudioFile(file_name) as source:  # Abrir el archivo de audio grabado
        print("Procesando audio...")
        audio = recognizer.record(source)  # Leer el audio del archivo

    try:
        mensaje_usuario = recognizer.recognize_google(audio, language=language)  # Reconocer el texto a partir del audio
        return mensaje_usuario  # Retornar el texto reconocido

    except sr.UnknownValueError:  # Si el reconocedor no pudo entender el audio
        print("Asistente: Lo siento, no entendí lo que dijiste.")  # Imprimir un mensaje de error
        return None  # Retornar None en caso de error
    except sr.RequestError:  # Si hubo un error al procesar la solicitud del reconocedor
        print("Asistente: Lo siento, no pude completar la solicitud en este momento.")  # Imprimir un mensaje de error
        return None  # Retornar None en caso de error


############### Función para decir una despedida al usuario    #############
def decir_despedida():
 
    return "Hasta luego ¡Espero haber sido útil!"

########## Función para manejar acciones que no corresponden a las anteriores   ###########
def accion_predeterminada(file_path):
    return "Lo siento pero algo ha salido mal, vamos a intentarlo con otra pregunta"
    

########################  FUNCION NOMBRE USUARIO  ##########################################################

def obtener_nombre_usuario():
    """
    Esta funcion capta el nombre de usuario del sistema.
    """
    nombre = f" Este ordenador es de  {os.getlogin()}"
    return nombre

########################  FUNCION TIEMPO  ##########################################################
def obtener_tiempo(ciudad):
    """
    La función "obtener_tiempo" recupera datos meteorológicos para una ciudad especificada 
    utilizando la API de OpenWeatherMap y traduce la descripción del clima al español.

    Argumentos:
    ciudad: objeto necesario para la funcion obtener_tiempo(ciudad) que recupera datos
    meteorológicos para una ciudad específica utilizando la API de OpenWeatherMap. La función
    toma el nombre de una ciudad como entrada y devuelve una cadena formateada con información 
    meteorológica como la descripción, la temperatura, la sensación térmica, la humedad y el viento.

    Returns:
    La función obtener_tiempo(ciudad) devuelve una cadena que proporciona información sobre el
    clima en la ciudad especificada. La cadena incluye detalles como la descripción del clima, 
    la temperatura, la sensación térmica, la humedad y la velocidad del viento. Si hay un error 
    al obtener los datos meteorológicos, se devuelve un mensaje de error en su lugar.
    """
   
    api_key = "cfd0aad97796a302d11caaeec31a9070"
   
   
    url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()
        #recogemos el contenido del json y comprovamos que tiene datos, despues extraemos los datos que queremos del .json 
        if response.status_code == 200:
            descripcion = data['weather'][0]['description']
            temperatura = data['main']['temp']
            sensacion_termica = data['main']['feels_like']
            humedad = data['main']['humidity']
            velocidad_viento = data['wind']['speed']

            clima = GoogleTranslator(source='auto', target='es').translate(descripcion).lower()

            tiempo = f"El tiempo en {ciudad} es {clima}. La temperatura es {temperatura}°C, " \
                     f"la sensación térmica es {sensacion_termica}°C, la humedad es {humedad}% " \
                     f"y la velocidad del viento es {velocidad_viento} m/s."

            return tiempo
        else:
            return "Error al obtener los datos del tiempo."

    except Exception as e:
        print(f"Error al obtener datos del tiempo: {e}")
        return "Ha ocurrido un error al obtener los datos del tiempo."



############################ Función traductor   #############################

def traducir_texto(texto, idioma):
    """
    La función traducir_texto intenta primero capturar el texto y el idioma y despues
    traducir un texto dado al idioma especificado utilizando 
    la API de Google Translate, manejando excepciones 
    y devolviendo la traducción o mensajes de error correspondientes.

    Argumentos:
    texto: El parámetro texto es el texto que se 
    desea traducir a un idioma diferente.
    idioma: El parámetro idioma en la función traducir_texto representa el
    idioma al que se desea traducir el texto de entrada. Es el idioma objetivo para la traducción.
    
    Retunrs:
    La función traducir_texto devuelve una cadena que proporciona la traducción
    del texto de entrada al idioma deseado. Si la traducción es exitosa, devuelve 
    un mensaje con el texto traducido. Si hay un error durante el proceso de traducción,
    devuelve un mensaje de error indicando el problema encontrado.





    """
    
    try:
        idioma_ingles = GoogleTranslator(source='auto', target='en').translate(idioma).lower()
    except Exception as e:
        return f"Error al traducir el idioma: {e}"

    # Traducir el texto al idioma deseado
    try:
        traduccion = GoogleTranslator(source='auto', target=idioma_ingles).translate(texto)
        print (f"{traduccion}")
        print (f"{idioma_ingles}")
        return f"Claro, aquí tienes la traducción de '{texto}' al '{idioma}': '{traduccion}'"
    except Exception as e:
        return f"Disculpa pero el idioma {idioma} no lo conozco todavia."

########## Función youtube musica   ###########        
def reproducir_video(video):
    # Construir la URL de búsqueda en YouTube
    url = f"https://www.youtube.com/results?search_query={video.replace(' ', '+')}"

    # Abrir el navegador con la URL de búsqueda
    webbrowser.open(url)
    return f"listo aqui tienes el resultado para que elijas el video que mas te guste sobre...{video}"



################################## Función volumen   ###################################
def ajustar_volumen(ajuste):
    # Obtener el control de volumen del dispositivo de reproducción predeterminado
    devices = AudioUtilities.GetSpeakers()  # Obtener el objeto de interfaz de los altavoces
    interfaces = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None) # Obtencia
    volumen = cast(interfaces, POINTER(IAudioEndpointVolume))  # Convertir la interfaz en un objeto de control de volumen

    # Obtener el volumen actual y ajustarlo
    current_volume = volumen.GetMasterVolumeLevelScalar()  # Obtener el volumen actual como un valor entre 0.0 y 1.0
    new_volume = max(0.0, min(1.0, current_volume + ajuste))  # Calcular el nuevo volumen ajustado
    volumen.SetMasterVolumeLevelScalar(new_volume, None)  # Establecer el nuevo volumen

    # Devolver el nuevo volumen
    return f"he modificado el volumen a tu gusto "


################################## FUNCION WIKI    ##################################
def wiki(consulta):
    # Configurar Wikipedia en español
    wikipedia.set_lang("es")
    try:
        resultado = wikipedia.summary(consulta)  # Busca un resumen de la consulta en Wikipedia
       
        return resultado
    except wikipedia.exceptions.DisambiguationError as e:  # Maneja errores de ambigüedad en la búsqueda
        return f"La busqueda {consulta} es ambigua. Por favor, se mas especifico."
    except wikipedia.exceptions.PageError as e:  # Maneja errores cuando no se encuentra ninguna página
        return f"No se encontro ninguna pagina para {consulta}. Intenta con otro termino."
    


################## CHISTES #################


def contar_chiste_aleatorio():
    try:
        # Obtener un chiste aleatorio en español
        chiste = pyjokes.get_joke(language='es', category='all')
        print (chiste) 
        return chiste  # Devolver el chiste obtenido
    except Exception as e:
        return f"No pude contar un chiste en este momento. Error: {str(e)}"  # Manejar cualquier error que pueda ocurrir durante la obtención del chiste


################## Videos #################
def video(ruta_video):
    """

    La función video se utiliza para reproducir
    un video utilizando Pygame al inicializar Pygame, 
    configurar la pantalla para la reproducción de video,
    cargar el video y calcular la posición para 
    centrarlo en la pantalla.

    Argumentos:
    ruta_video: El parámetro ruta_video en la función video
    es la ruta al archivo de video que se desea reproducir 
    utilizando Pygame. Esta función inicializa Pygame, configura
    la pantalla para la reproducción de video, carga el video 
    desde la ruta proporcionada y calcula la posición para centrar 
    el video en la pantalla
    """
     
    pygame.quit()  # Cerrar cualquier instancia previa de Pygame
    pygame.init()  # Inicializar Pygame en el hilo principal

    pantalla = pygame.display.set_mode((800, 600))  # Configurar el tamaño de la pantalla
    pantalla_rect = pantalla.get_rect()  # Obtener el rectángulo que representa la pantalla

    clip = VideoFileClip(ruta_video)  # Cargar el video desde la ruta proporcionada
    clip_surface = pygame.Surface(clip.size).convert()  # Crear una superficie para el video

    # Calcular la posición para centrar el video en la pantalla
    x = (pantalla_rect.width - clip.size[0]) // 2
    y = (pantalla_rect.height - clip.size[1]) // 2
    # Función para reproducir el video
    
    def reproducir():
       #Función para reproducir un video utilizando Pygame.

        #Esta función maneja la reproducción del video en un bucle,
        #gestionando eventos y actualizando la pantalla con cada frame del video.
       
        playing = True  # Variable para controlar si el video se está reproduciendo
        clock = pygame.time.Clock()  # Crear un objeto reloj para gestionar la velocidad de fotogramas

        while playing:  # Bucle principal de reproducción
            for event in pygame.event.get():  # Manejar eventos de Pygame
                if event.type == pygame.QUIT:  # Si se cierra la ventana, detener la reproducción
                    playing = False

            # Obtener el frame actual del video basado en el tiempo transcurrido
            clip_frame = clip.get_frame(pygame.time.get_ticks() / 1000)
            # Convertir el frame a una superficie de Pygame y dibujarlo en la superficie del video
            clip_surface.blit(pygame.image.frombuffer(clip_frame, clip.size, 'RGB'), (0, 0))

            pantalla.fill((0, 0, 0))  # Rellenar la pantalla con un color negro
            pantalla.blit(clip_surface, (x, y))  # Dibujar el frame del video en la posición calculada
            pygame.display.flip()  # Actualizar la pantalla para mostrar el nuevo frame

            clock.tick(clip.fps)  # Asegurar que la reproducción se mantiene a la velocidad de fotogramas del video

        pygame.quit()  # Cerrar Pygame al finalizar la reproducción

    # Iniciar la reproducción del video en un hilo separado
    thread = Thread(target=reproducir)
    thread.start()



################## cmd #################
def cmd():
    
    try:
        comandos = ["color a", "dir/s"]
        # Abrir el símbolo del sistema (cmd) y ejecutar los comandos uno por uno
        for comando in comandos:
            subprocess.run(["cmd", "/c", comando], shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando: {e}")
    except Exception as e:
        print(f"Error general: {e}")
    return f"listo modo hacker activado"


