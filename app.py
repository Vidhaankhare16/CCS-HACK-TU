import uvicorn
from fastapi import FastAPI
import joblib
import tensorflow as tf
from tensorflow import keras
from fastapi import File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io

app = FastAPI()
#joblib_in = open()
model = tf.keras.models.load_model('model.keras')

@app.get('/')
def index():
    return {'message': 'Crack Identifier ML API'}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/image/predict') #post banao
def predict_crack_type():
    def predict_crack(image_path):
        img = tf.keras.preprocessing.image.load_img(
            image_path, target_size=(300, 300)
        )
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0) / 255.0
        prediction = model.predict(img_array)
        return "Crack Detected" if prediction[0][0] > 0.5 else "No Crack Found"
    text = predict_crack('/home/harsh/Desktop/hacktu6/Broken_railroad_tracks_1.jpg')
    #data = data.model_dump()
    #Image = Image

    #prediction = model.predict([Image])
    #return {
    #    'prediction': prediction[0]
    #}
    return {'message': text}

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    def predict_crack(image_bytes):
        img = Image.open(io.BytesIO(image_bytes))
        img = img.resize((300, 300))  # Resize to match model input shape
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0) / 255.0
        prediction = model.predict(img_array)
        return "Crack Detected" if prediction[0][0] > 0.5 else "No Crack Found"
    image_bytes = await file.read()
    result = predict_crack(image_bytes)
    return {"filename": file.filename, "prediction": result}

    #prediction = model.predict([Image])
    #return {
    #    'prediction': prediction[0]
    #}
    return {'message': text}
    return {"filename": file.filename, "message": "Image processed successfully"}

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8080)