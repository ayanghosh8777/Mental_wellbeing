import pickle
import pandas as pd

from flask import (
    Flask,
    render_template,
    request
)


application = Flask(__name__)

app = application


# Load the complete pipeline
# This contains:
# Imputer
# StandardScaler
# OneHotEncoder
# SVC

with open(
    "models/best_model.pkl",
    "rb"
) as file:

    model = pickle.load(file)


@app.route("/")
def home():

    return render_template(
        "home.html"
    )


@app.route(
    "/predict",
    methods=["POST"]
)
def predict():

    try:

        # Get values from HTML form

        age = float(
            request.form["age"]
        )

        daily_screen_time = float(
            request.form["daily_screen_time"]
        )

        sleep_duration = float(
            request.form["sleep_duration"]
        )

        stress_level = float(
            request.form["stress_level"]
        )


        gender = request.form["gender"]

        occupation = request.form["occupation"]

        device_type = request.form["device_type"]


        # Create DataFrame

        features = pd.DataFrame({

            "age": [age],

            "daily_screen_time": [
                daily_screen_time
            ],

            "sleep_duration": [
                sleep_duration
            ],

            "stress_level": [
                stress_level
            ],

            "gender": [
                gender
            ],

            "occupation": [
                occupation
            ],

            "device_type": [
                device_type
            ]

        })


        # Predict

        prediction = model.predict(
            features
        )


        # Optional probability

        if hasattr(
            model,
            "predict_proba"
        ):

            probability = model.predict_proba(
                features
            )

            confidence = (
                max(probability[0]) * 100
            )

        else:

            confidence = None


        return render_template(

            "result.html",

            prediction=prediction[0],

            confidence=confidence

        )


    except Exception as e:

        return f"Error: {e}"


if __name__ == "__main__":

    app.run(
        debug=True
    )



