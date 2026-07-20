import pickle
import pandas as pd

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_sqlalchemy import SQLAlchemy

from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)


# =========================================
# FLASK APPLICATION
# =========================================

application = Flask(__name__)

app = application


# =========================================
# CONFIGURATION
# =========================================

app.config["SECRET_KEY"] = "change-this-secret-key"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# =========================================
# DATABASE
# =========================================

db = SQLAlchemy(app)


# =========================================
# LOGIN MANAGER
# =========================================

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"


# =========================================
# USER MODEL
# =========================================

class User(
    UserMixin,
    db.Model
):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(150),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )


# =========================================
# CREATE DATABASE TABLES
# =========================================

with app.app_context():

    db.create_all()


# =========================================
# LOAD ML MODEL
# =========================================

with open(
    "models/model.pkl",
    "rb"
) as file:

    model = pickle.load(file)


# =========================================
# USER LOADER
# =========================================

@login_manager.user_loader
def load_user(user_id):

    return User.query.get(
        int(user_id)
    )


# =========================================
# WELCOME PAGE
# =========================================

@app.route("/")
def index():

    return render_template(
        "index.html"
    )


# =========================================
# SIGNUP
# =========================================

@app.route(
    "/signup",
    methods=["GET", "POST"]
)
def signup():

    if request.method == "POST":

        username = request.form.get(
            "username"
        )

        email = request.form.get(
            "email"
        )

        password = request.form.get(
            "password"
        )


        # Check whether email already exists

        existing_email = User.query.filter_by(
            email=email
        ).first()

        if existing_email:

            flash(
                "Email already registered.",
                "error"
            )

            return redirect(
                url_for("signup")
            )


        # Check whether username already exists

        existing_username = User.query.filter_by(
            username=username
        ).first()

        if existing_username:

            flash(
                "Username already taken.",
                "error"
            )

            return redirect(
                url_for("signup")
            )


        # Hash password

        hashed_password = generate_password_hash(
            password
        )


        # Create user

        new_user = User(

            username=username,

            email=email,

            password=hashed_password

        )


        # Save user

        db.session.add(
            new_user
        )

        db.session.commit()


        flash(
            "Account created successfully. Please login.",
            "success"
        )


        return redirect(
            url_for("login")
        )


    return render_template(
        "signup.html"
    )


# =========================================
# LOGIN
# =========================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        email = request.form.get(
            "email"
        )

        password = request.form.get(
            "password"
        )


        # Find user

        user = User.query.filter_by(
            email=email
        ).first()


        # Check credentials

        if user and check_password_hash(

            user.password,

            password

        ):


            # Create login session

            login_user(
                user
            )


            flash(
                "Login successful.",
                "success"
            )


            return redirect(
                url_for("wellbeing")
            )


        flash(
            "Invalid email or password.",
            "error"
        )


        return redirect(
            url_for("login")
        )


    return render_template(
        "login.html"
    )


# =========================================
# LOGOUT
# =========================================

@app.route(
    "/logout"
)
@login_required
def logout():

    logout_user()


    flash(
        "You have been logged out.",
        "success"
    )


    return redirect(
        url_for("index")
    )


# =========================================
# MENTAL WELLBEING PAGE
# =========================================

@app.route(
    "/wellbeing"
)
@login_required
def wellbeing():

    return render_template(
        "home.html"
    )


# =========================================
# PREDICTION ROUTE
# =========================================

@app.route(
    "/predict",
    methods=["POST"]
)
@login_required
def predict():

    try:


        # =====================================
        # NUMERICAL FEATURES
        # =====================================

        age = int(
            request.form["age"]
        )

        platforms_used_count = int(
            request.form[
                "platforms_used_count"
            ]
        )

        daily_screen_hours = float(
            request.form[
                "daily_screen_hours"
            ]
        )

        daily_notifications = int(
            request.form[
                "daily_notifications"
            ]
        )

        minutes_to_first_check_after_waking = int(
            request.form[
                "minutes_to_first_check_after_waking"
            ]
        )

        avg_sleep_hours = float(
            request.form[
                "avg_sleep_hours"
            ]
        )

        anxiety_score_0to27 = int(
            request.form[
                "anxiety_score_0to27"
            ]
        )

        low_mood_score_0to27 = int(
            request.form[
                "low_mood_score_0to27"
            ]
        )

        life_satisfaction_1to10 = int(
            request.form[
                "life_satisfaction_1to10"
            ]
        )

        loneliness_1to10 = int(
            request.form[
                "loneliness_1to10"
            ]
        )

        self_esteem_1to10 = int(
            request.form[
                "self_esteem_1to10"
            ]
        )

        fomo_1to10 = int(
            request.form[
                "fomo_1to10"
            ]
        )

        social_comparison_1to10 = int(
            request.form[
                "social_comparison_1to10"
            ]
        )

        physical_activity_days_per_week = int(
            request.form[
                "physical_activity_days_per_week"
            ]
        )


        # =====================================
        # CATEGORICAL FEATURES
        # =====================================

        gender = request.form[
            "gender"
        ]

        occupation = request.form[
            "occupation"
        ]

        region = request.form[
            "region"
        ]

        most_used_platform = request.form[
            "most_used_platform"
        ]

        night_time_use = request.form[
            "night_time_use"
        ]

        primary_purpose = request.form[
            "primary_purpose"
        ]

        uses_screen_time_limits = request.form[
            "uses_screen_time_limits"
        ]

        attempted_digital_detox = request.form[
            "attempted_digital_detox"
        ]

        seeks_mental_health_support = request.form[
            "seeks_mental_health_support"
        ]


        # =====================================
        # CREATE DATAFRAME
        # =====================================

        features = pd.DataFrame({

            "age": [age],

            "gender": [gender],

            "occupation": [occupation],

            "region": [region],

            "most_used_platform": [
                most_used_platform
            ],

            "platforms_used_count": [
                platforms_used_count
            ],

            "daily_screen_hours": [
                daily_screen_hours
            ],

            "daily_notifications": [
                daily_notifications
            ],

            "night_time_use": [
                night_time_use
            ],

            "minutes_to_first_check_after_waking": [

                minutes_to_first_check_after_waking

            ],

            "primary_purpose": [
                primary_purpose
            ],

            "avg_sleep_hours": [
                avg_sleep_hours
            ],

            "anxiety_score_0to27": [
                anxiety_score_0to27
            ],

            "low_mood_score_0to27": [
                low_mood_score_0to27
            ],

            "life_satisfaction_1to10": [
                life_satisfaction_1to10
            ],

            "loneliness_1to10": [
                loneliness_1to10
            ],

            "self_esteem_1to10": [
                self_esteem_1to10
            ],

            "fomo_1to10": [
                fomo_1to10
            ],

            "social_comparison_1to10": [
                social_comparison_1to10
            ],

            "physical_activity_days_per_week": [

                physical_activity_days_per_week

            ],

            "uses_screen_time_limits": [

                uses_screen_time_limits

            ],

            "attempted_digital_detox": [

                attempted_digital_detox

            ],

            "seeks_mental_health_support": [

                seeks_mental_health_support

            ]

        })


        # =====================================
        # PREDICTION
        # =====================================

        prediction = model.predict(
            features
        )[0]


        # =====================================
        # PREDICTION PROBABILITY
        # =====================================

        probabilities = model.predict_proba(
            features
        )[0]


        classes = model.classes_


        probability_dict = dict(
            zip(
                classes,
                probabilities
            )
        )


        # =====================================
        # RISK PERCENTAGE
        # =====================================

        risk_percentage = (

            probability_dict.get(
                "At-risk",
                0
            ) * 100

        )


        # =====================================
        # CONSULTATION RECOMMENDATION
        # =====================================

        if risk_percentage >= 70:

            consultation_message = (

                "A professional mental health "
                "consultation is strongly recommended."

            )

            consultation_level = (
                "High Priority"
            )


        elif risk_percentage >= 40:

            consultation_message = (

                "Consider speaking with a "
                "mental health professional."

            )

            consultation_level = (
                "Recommended"
            )


        else:

            consultation_message = (

                "No immediate consultation "
                "indication based on this model."

            )

            consultation_level = (
                "Low Priority"
            )


        # =====================================
        # RETURN RESULT
        # =====================================

        return render_template(

            "result.html",

            prediction=prediction,

            risk_percentage=round(
                risk_percentage,
                2
            ),

            consultation_message=(
                consultation_message
            ),

            consultation_level=(
                consultation_level
            ),

            probabilities=probability_dict

        )


    except Exception as e:

        return f"Error: {e}"


# =========================================
# RUN APPLICATION
# =========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )