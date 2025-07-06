from pytube import YouTube
from moviepy.editor import VideoFileClip
import os
import sys

def download_youtube_to_3gp(video_url, output_filename="video.3gp"):
    try:
        # Descargar video de YouTube (calidad baja para Nokia)
        yt = YouTube(video_url)
        stream = yt.streams.filter(
            file_extension='mp4',
            resolution='144p'  # Resolución baja para Nokia
        ).first()
        
        if not stream:
            print("No se encontró un stream compatible.")
            return False
        
        print("Descargando video...")
        video_path = stream.download(filename="temp_video.mp4")
        
        # Convertir a 3GP con parámetros para Nokia
        print("Convirtiendo a 3GP...")
        video_clip = VideoFileClip(video_path)
        
        # Configuración para Nokia (176x144, 15fps, audio AMR-NB)
        video_clip_resized = video_clip.resize((176, 144))
        video_clip_resized.write_videofile(
            output_filename,
            codec='mpeg4',  # Códec compatible con 3GP
            audio_codec='libopencore-amrnb',  # Audio AMR para Nokia
            fps=15,
            bitrate="128k",
            ffmpeg_params=[
                '-ar', '8000',  # Frecuencia de audio baja
                '-ac', '1',     # Mono (no estéreo)
                '-ab', '12.2k'  # Bitrate de audio bajo
            ]
        )
        
        # Limpiar archivos temporales
        video_clip.close()
        os.remove(video_path)
        
        print(f"¡Listo! Video guardado como: {output_filename}")
        return True
    
    except Exception as e:
        print(f"Error: {e}")
        return False

# Ejemplo de uso:
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python youtube_to_3gp.py <URL_DE_YOUTUBE>")
        sys.exit(1)
    
    youtube_url = sys.argv[1]
    download_youtube_to_3gp(youtube_url)