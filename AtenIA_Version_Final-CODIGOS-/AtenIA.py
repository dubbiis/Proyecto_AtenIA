import funciones_de_ateniav2 as af  # Importar el archivo de funciones del asistente
import analisisv4
import sys #Acceso a argumentos de línea de comandos
import os  # Para manejo de rutas

def atenia():
    """

    La función atenia define un programa de asistente virtual que interactúa con 
    el usuario a través de entrada y salida de audio, procesando los comandos del 
    usuario y proporcionando respuestas en consecuencia.
    """

   # Definir la ruta base del proyecto
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Construir rutas relativas a los recursos
    video_speak_path = os.path.join(BASE_DIR, 'resources', 'speak.mp4')
    video_escuchar_path = os.path.join(BASE_DIR, 'resources', 'escuchar.mp4')
    video_procesar_path = os.path.join(BASE_DIR, 'resources', 'procesar.mp4')
    af.video(video_speak_path)

    
    #af.video("C:\\Users\\dubi\\Desktop\\vissual\\AtenIA_Version_Final\\speak.mp4")
    af.speak("!Hola¡, soy atenia, tu asistente. ¿en que puedo ayudarte?")
  


    while True:  # Bucle infinito
       # af.video("C:\\Users\\dubi\\Desktop\\vissual\\AtenIA_Version_Final\\escuchar.mp4")
        af.video(video_escuchar_path)
        af.grabar_audio()  # Llamar a la función para grabar audio
        #af.video("C:\\Users\\dubi\\Desktop\\vissual\\AtenIA_Version_Final\\procesar.mp4")
        af.video(video_procesar_path)
        mensaje_usuario = af.procesar_audio()  # Llamar a la función para procesar el audio grabado
        if mensaje_usuario:  # Si se reconoció correctamente el audio
            print("Usuario:", mensaje_usuario)  # Imprimir el texto reconocido
            respuesta = analisisv4.analizar_accion(mensaje_usuario)  # Analizar la acción y obtener la respuesta
            print("Asistente:", respuesta)  # Imprimir la respuesta del asistente
            #af.video("C:\\Users\\dubi\\Desktop\\vissual\\AtenIA_Version_Final\\speak.mp4")
            af.video(video_speak_path)
            af.speak(f"{respuesta}")
            
            if respuesta == "Hasta luego ¡Espero haber sido útil!":  # Verificar si la respuesta indica salir del bucle
                sys.exit()
                

               
        else:  # Si hubo un error al procesar el audio
            print("Error al procesar el audio.")  # Imprimir un mensaje de error

if __name__ == "__main__":
    atenia()  # Llamar a la función principal al ejecutar el archivo

