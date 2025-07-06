from flask import Flask, request, render_template, send_file
from pytube import YouTube
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        try:
            yt = YouTube(url)
            stream = yt.streams.filter(file_extension="mp4", resolution="144p").first()
            if not stream:
                return "Error: No se encontró video compatible."
            
            # Descargar temporalmente
            temp_path = stream.download(filename="temp_video.mp4")
            
            # Convertir a 3GP con FFmpeg (comando directo)
            output_path = "video.3gp"
            os.system(
                f'ffmpeg -i "{temp_path}" -s 176x144 -r 15 -b:v 128k '
                f'-acodec libopencore-amrnb -ar 8000 -ac 1 -ab 12.2k '
                f'"{output_path}"'
            )
            
            # Enviar el archivo al usuario
            return send_file(output_path, as_attachment=True)
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)