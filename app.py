from flask import Flask, request,jsonify
from flask_cors import CORS, cross_origin
import replicate
from os import environ
from flask_pymongo import PyMongo,MongoClient

from dotenv import load_dotenv
# import io
# from getpass import getpass
# from pydub.playback import play
# from pydub import AudioSegment
# from gtts import gTTS
# import REPLICATE_API_TOKEN



# path=find_dotenv()
load_dotenv()



app = Flask(
    __name__,
    static_url_path='',
    static_folder='../frontend/build',
    template_folder='../frontend/build'
)

cors = CORS(app)

REPLICATE_API_TOKEN = environ.get('key')
# print(REPLICATE_API_TOKEN)
# print (os.environ)
environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

app.config['MONG_DBNAME'] = 'TTS'
app.config["MONGO_URI"] = "mongodb+srv://alikhansikandar007:sCRny95r8CS0vxfS@cluster0.xpits74.mongodb.net/TTS?retryWrites=true&w=majority"
mongo = PyMongo(app)


try:
    print(mongo.db.users)

    print({"message": "Database connection successful"})
except Exception as e:
    print({"error": "Failed to connect to the database", "details": str(e)})

# client = MongoClient('localhost', 27017)

# Route for receiving text
@app.route("/",methods=["POST", "GET"])
@cross_origin()

def receive_text():

    # Getting the text from the request
    if request.method == "POST":
        req = request.json["text"]
        wave_temp = float(request.json.get("waveform", 0.5))
        text_temp = float(request.json.get("rate", 0.5))
        # language = request.json.get("language")["value"]
        # speaker = language + request.json.get("speaker")["value"]
        # gender = request.json.get("selectedGender")["value"]
        # print(gender)
        
        print("wave_temp:",  wave_temp)
        print("text_temp:", text_temp)
        # print("Speaker:", speaker)

        # if gender == "male":
        #     req = "[MAN]:" + req
        # elif gender == "female":
        #     req = "[WOMAN]:" + req

        print(req)
        try:
            output = replicate.run(
                "suno-ai/bark:b76242b40d67c76ab6742e987628a2a9ac019e11d56ab96c4e91ce03b79b2787",
                input = {
                    "prompt": req,
                    # "history_prompt": speaker,
                    "sample_rate": 4 ,
                    "text_temp": text_temp,
                    "wave_temp": wave_temp,
                }
            )

            print(output["audio_out"])

            return output["audio_out"]

            # audio_link = output["audio_out"]
            # audio_file = "output.mp3"
            # audio_output.save(os.path.join(os.path.dirname(__file__), audio_file))
            # return send_file(audio_file, mimetype="audio/mpeg",as_attachment=True)

            # engine = pyttsx3.init()
            # engine.setProperty("voice", "en-us")
            # voices = engine.getProperty("voices")

            # if gender == "male1":
            #     engine.setProperty("voice", voices[0].id)
            # elif gender == "male2":
            #     engine.setProperty("voice", voices[11].id)
            # elif gender == "female1":
            #     engine.setProperty("voice", voices[41].id)
            # elif gender == "female2":
            #     engine.setProperty("voice", voices[10].id)
            

            # engine.setProperty("pitch", pitch)
            # engine.setProperty("rate", rate)

            # audio_file = "output.mp3"

            # engine.save_to_file(req , os.path.join(os.path.dirname(__file__), audio_file))
            # engine.runAndWait()
          
            # audio_output = gTTS(req)
            
            # audio_output.save(os.path.join(os.path.dirname(__file__), audio_file))
            # return send_file(audio_file, mimetype="audio/mpeg",as_attachment=True)
        

        except Exception as e:
            print("Error:", e)
            return {"error": str(e)}
        
    elif request.method == "GET":
        return "This is the GET endpoint. Send a POST request with JSON data."


@app.route("/login", methods=["POST"])
@cross_origin()
def login():
    # Logic to handle login request
    # Retrieve data from request
    data = request.json
    username = data.get("username")
    password = data.get("password")

    print(username, password)
    
    # Query MongoDB to check if user exists and credentials are correct
    user = mongo.db.users.find_one({"username": username, "password": password})
    if user:
        print("login successful")
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "invalid"}), 401

@app.route("/signup", methods=["POST"])
@cross_origin()
def signup():
    # Logic to handle signup request
    # Retrieve data from request
    data = request.json
    username = data.get("username")
    password = data.get("password")

    print("sign",username, password)
    
    # Check if user already exists
    existing_user = mongo.db.users.find_one({"username": username})
    if existing_user:

        return jsonify({"error": "Username already exists"}), 400
    
    # Add user to MongoDB
    new_user = {"username": username, "password": password}
    mongo.db.users.insert_one(new_user)
    print("user signed up successfully")
    return jsonify({"message": "Success"}), 201

# # Running app
if __name__ == "__main__":
    app.run(debug=True)
