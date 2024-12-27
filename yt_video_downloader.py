from flask import Flask, request, render_template, send_file
import yt_dlp
import os

app = Flask(__name__)

def download_video(video_url, download_dir, file_format):
    if file_format == "mp3":
        options = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'ffmpeg_location': r'C:\ffmpeg',
        }
    else:  # Default to mp4
        options = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
            'ffmpeg_location': r'C:\ffmpeg',
        }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(video_url, download=True)
            file_name = ydl.prepare_filename(info)
            if file_format == "mp3":
                file_name = os.path.splitext(file_name)[0] + ".mp3"
            return file_name
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    video_url = request.form.get("video_url")
    file_format = request.form.get("format")
    if not video_url or not file_format:
        return "Invalid input provided", 400

    download_dir = os.path.expanduser("~/Downloads")  

    video_path = download_video(video_url, download_dir, file_format)

    if video_path:
        return send_file(video_path, as_attachment=True)
    else:
        return "Error occurred during download", 500

if __name__ == "__main__":
    app.run(debug=True)