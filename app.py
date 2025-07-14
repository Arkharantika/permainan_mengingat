from flask import Flask, render_template, request, jsonify
from gtts import gTTS
import random
from playsound import playsound

app = Flask(__name__)
globalstring = ""


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/input", methods=["POST"])
def submit():
    data = request.get_json()
    user_input = data.get("user_input")
    user_input = int(user_input)
    print(f"Received input: {user_input}")

    def listTostring(listnya):
        list = " "
        for kata in listnya:
            list = list + kata
        return list

    filename = open("datanya.txt", "r")
    kata = filename.read().splitlines()

    randomnya = random.sample(kata, user_input)
    convert = listTostring([word + " " for word in randomnya])
    print(convert)

    global globalstring
    globalstring = convert.strip()

    tts = gTTS(convert, lang="id")
    tts.save("static/wow.mp3")

    return jsonify({"message": f"berhasil generate sebanyak {user_input}"})


@app.route("/jawaban", methods=["POST"])
def answer():
    data = request.get_json()
    user_input = data.get("user_input")

    print(f"jawaban yang ditererima : {user_input}")
    print(f"jawaban yang seharusnya : {globalstring}")

    if user_input == globalstring:
        return jsonify({"message": "jawaban benar !!"})
    else:
        return jsonify({"message": "jawaban SALAH !!!"})


if __name__ == "__main__":
    app.run(debug=True)
