import funciones_de_ateniav2 as af  
import os  # Para manejo de rutas
# Definir la ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construir rutas relativas a los recursos
video_speak_path = os.path.join(BASE_DIR, 'resources', 'speak.mp4')
video_escuchar_path = os.path.join(BASE_DIR, 'resources', 'escuchar.mp4')
video_procesar_path = os.path.join(BASE_DIR, 'resources', 'procesar.mp4')
def analizar_accion(mensaje_usuario):
    """
    La función analizar_accion analiza la entrada 
    del usuario para determinar la acción apropiada 
    a tomar en función de palabras clave, como obtener 
    información meteorológica, traducir texto, reproducir
    videos de YouTube, ajustar el volumen,
    buscar en Wikipedia, contar chistes y manejar consultas relacionadas con el usuario.

    Argumentos:

    mensaje_usuario: Es el objeto que nos llegaradespues
    de que se haya transcrito.
    
    Retornos:

    La función analizar_accion devuelve la acción
    correspondiente basada en el mensaje del usuario.
    Verifica palabras clave relacionadas con varias acciones,
    como obtener información meteorológica, traducción, 
    reproducción de videos de YouTube, ajuste de volumen, búsqueda en Wikipedia, 
    contar chistes, preguntar por el nombre del usuario y activar un modo especial.
    Si no se reconocen ninguna de las acciones específicas, devolverá la acción predeterminada.
    """
    # Diccionario que mapea palabras clave con funciones correspondientes
    acciones = {
        'tiempo': af.obtener_tiempo,
        'salir': af.decir_despedida,
       'traductor': af.traducir_texto,
        'youtube': af.reproducir_video,
        'volumen': af.ajustar_volumen,
        'wiki': af.wiki,
        'chiste': af.contar_chiste_aleatorio,
        'usuario': af.obtener_nombre_usuario,
        'x': af.cmd
         
    }

    mensaje = mensaje_usuario.lower()  # Convertir el mensaje a minúsculas para una comparación más fácil
# Verificar si el mensaje es de salida
    es_salida = True
    palabras_clave_salida = ['eso', 'todo', 'asistente','es']
    for palabra in palabras_clave_salida:
       if palabra not in mensaje:
        es_salida = False
        break
    if es_salida:
       return acciones['salir']()  # Pasar la ciudad como argumento    

# Verificar si el mensaje contiene palabras clave relacionadas con la solicitud de información sobre el tiempo 
    es_tiempo = True
    palabras_clave_viaje = ['tiempo', 'dime']
    palabras_clave_viaje_2 =['tiempo', 'hace']
    if not any(palabra in mensaje for palabra in palabras_clave_viaje) and \
       not any(palabra in mensaje for palabra in palabras_clave_viaje_2):
         es_tiempo = False

    if es_tiempo:
       # Dividir el mensaje en palabras
        palabras = mensaje.split()
        ciudad = palabras[-1]
        return acciones['tiempo'](ciudad)  # Pasar la ciudad como argumento
             
       


 # Verificar si el mensaje contiene palabras clave relacionadas con traducir
    es_traductor = True
    palabras_clave_traductor = ['traduce']
    palabras_clave_traductor_2 = ['como', 'dice']

    if not any(palabra in mensaje for palabra in palabras_clave_traductor) and \
       not any(palabra in mensaje for palabra in palabras_clave_traductor_2):
            es_traductor = False 
             
    if es_traductor:       
        # Dividir el mensaje en palabras
        palabras = mensaje.split()
        idioma = palabras[-1]
        if "traduce" in mensaje:
            indice_traduce = palabras.index("traduce")
            lista_a_traducir = palabras[indice_traduce +1:-2]
        else:
            indice_traduce = palabras.index("dice")
            lista_a_traducir = palabras[indice_traduce +1:-2]
            frase_a_traducir = ' '.join(map(str, lista_a_traducir))
        return acciones['traductor'](frase_a_traducir, idioma)  # Llamar a la función de traducción con la frase y el idioma
    
   
# Verificar si el mensaje contiene palabras clave relacionadas con youtube
    es_youtube = True
    palabras_clave_youtube = ['youtube']
    for palabra in palabras_clave_youtube:
        if palabra not in mensaje:  
            es_youtube = False 
            break 
    if es_youtube:       
        # Dividir el mensaje en palabras
        palabras = mensaje.split()
        indice_youtube = palabras.index("youtube")
        video_lista = palabras[indice_youtube +1:]
        video = ' '.join(map(str, video_lista))
        return acciones['youtube'](video)  # Llamar a la función de traducción con la frase y el idioma
    
     
 # Verificar si el mensaje contiene palabras clave relacionadas con volumen
    es_volumen = True
    palabras_clave_volumen = ['volumen']
    for palabra in palabras_clave_volumen:
        if palabra not in mensaje:  
            es_volumen = False 
            break 
    if es_volumen:       
        # Dividir el mensaje en palabras
        palabras = mensaje.split()
        indice_el = palabras.index("el")
        accion = palabras[indice_el -1]
        
        if accion == "sube" or accion == "aumenta":
            accion = 0.25 
            return acciones['volumen'](accion) # Llamar a la función de ajustar volumen   
        else:          
         accion = -0.25
         return acciones['volumen'](accion)  # Llamar a la función de ajustar volumen      

 
 # Verificar si el mensaje contiene palabras clave relacionadas con wiki
    es_wiki = True
    palabras_clave_wikipedia = ['wikipedia']
    for palabra in palabras_clave_wikipedia:
        if palabra not in mensaje:  
            es_wiki = False 
            break 
    if es_wiki: 
            #af.video("C:\\Users\\dubi\\Desktop\\vissual\\AtenIA_Version_Final\\speak.mp4")
            af.video(video_speak_path)
            af.speak("claro¡ ¿Que quieres buscar en la wikipedia?")
            #af.video("C:\\Users\\dubi\\Desktop\\vissual\\AtenIA_Version_Final\\escuchar.mp4")
            af.video(video_escuchar_path)
            af.grabar_audio()  # Llamar a la función para grabar audio y pedir la busqueda
            af.video(video_procesar_path)           
            mensaje_usuario = af.procesar_audio()  # Llamar a la función para procesar el audio grabado
            busqueda = mensaje_usuario
            af.speak(f"Muy bien, voy a buscar {busqueda} en wikipedia")
            print (busqueda)
            return acciones['wiki'](busqueda) # Llamar a la función  
           

    # Verificar si el mensaje contiene palabras clave relacionadas con chistes
    es_chiste = any(palabra in mensaje for palabra in ['chiste'])

    if es_chiste: 
        # Si el mensaje contiene palabras clave de chistes, se ejecuta este bloque
        af.speak("Claro aquí va un chiste")  # Decir al usuario que se contará un chiste
        return acciones['chiste']()  # Llamar a la función que maneja los chistes 

    # Verificar si el mensaje contiene palabras clave relacionadas con preguntas sobre el nombre de usuario
    es_usuario = any(palabra in mensaje for palabra in ['de', 'quien', 'es', 'este', 'ordenador'])

    if es_usuario:
        # Si el mensaje contiene palabras clave relacionadas con preguntas sobre el nombre de usuario, se ejecuta este bloque
        return acciones['usuario']()  # Llamar a la función que maneja las preguntas sobre el nombre de usuario

 # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    es_x = any(palabra in mensaje for palabra in ['modo', 'hacker', 'activa'])

    if es_x:
        # Si el mensaje contiene palabras clave relacionadas con preguntas sobre el nombre de usuario, se ejecuta este bloque
        return acciones['x']()  # Llamar a la función que maneja las preguntas sobre el nombre de usuario




   # Si no se reconoce ninguna acción específica, se ejecuta la acción predeterminada
    return af.accion_predeterminada()
 