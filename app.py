from flask import Flask, render_template, request, redirect, flash
import requests
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

TELEGRAM_BOT_TOKEN = "8155990401:AAF1F2S7nlg2aUEteB8enKIE2h57PyrxUdA"
TELEGRAM_CHAT_ID = "5116463638"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("video")
        if file and file.filename != "":
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            send_to_telegram(filepath, file.filename)
            flash("Video uploaded successfully!", "success")
        else:
            flash("Please select a video to upload.", "danger")
        return redirect("/")

    return render_template("index.html")

def send_to_telegram(file_path, filename):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
    with open(file_path, "rb") as video:
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "caption": f"New LMS Video Upload: {filename}"
        }
        files = {
            "document": video
        }
        requests.post(url, data=data, files=files)

if __name__ == "__main__":
    app.run(debug=True)
