# server/app.py
import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from server.db import db
from .models import Exercise, Workout, WorkoutExercise
from .schemas import ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema

def create_app():
    # ----------------------
    # FLASK APP CONFIG
    # ----------------------
    app = Flask(__name__, instance_relative_config=True)
    os.makedirs(app.instance_path, exist_ok=True)

    # SQLite path (ensure migrations and app use the same file)
    DB_PATH = os.path.join(app.instance_path, "app.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize DB and Migrations
    db.init_app(app)
    Migrate(app, db)

    # Initialize Schemas
    exercise_schema = ExerciseSchema()
    exercises_schema = ExerciseSchema(many=True)
    workout_schema = WorkoutSchema()
    workouts_schema = WorkoutSchema(many=True)
    we_schema = WorkoutExerciseSchema()
    wes_schema = WorkoutExerciseSchema(many=True)

    # ----------------------
    # LANDING PAGE
    # ----------------------
    @app.route("/", methods=["GET"])
    def landing_page():
        instructions = {
            "message": "Welcome to the Workout Tracker API!",
            "resources": {
                "exercises": {
                    "GET": "/exercises",
                    "GET_SINGLE": "/exercises/<id>",
                    "POST": "/exercises",
                    "DELETE": "/exercises/<id>"
                },
                "workouts": {
                    "GET": "/workouts",
                    "GET_SINGLE": "/workouts/<id>",
                    "POST": "/workouts",
                    "DELETE": "/workouts/<id>"
                },
                "workout_exercises": {
                    "POST": "/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises"
                }
            }
        }
        return jsonify(instructions), 200

    # ----------------------
    # EXERCISE ROUTES
    # ----------------------
    @app.route("/exercises", methods=["GET"])
    def get_exercises():
        exercises = Exercise.query.all()
        return jsonify(exercises_schema.dump(exercises)), 200

    @app.route("/exercises/<int:id>", methods=["GET"])
    def get_exercise(id):
        e = Exercise.query.get_or_404(id)
        result = exercise_schema.dump(e)
        result['workouts'] = workout_schema.dump(e.workouts, many=True)
        return jsonify(result), 200

    @app.route("/exercises", methods=["POST"])
    def create_exercise():
        data = request.get_json()
        try:
            validated = exercise_schema.load(data)
            e = Exercise(**validated)
            db.session.add(e)
            db.session.commit()
            return jsonify(exercise_schema.dump(e)), 201
        except Exception as ex:
            db.session.rollback()
            return jsonify({"error": str(ex)}), 400

    @app.route("/exercises/<int:id>", methods=["DELETE"])
    def delete_exercise(id):
        e = Exercise.query.get_or_404(id)
        db.session.delete(e)
        db.session.commit()
        return jsonify({"message": "Exercise deleted"}), 200

    # ----------------------
    # WORKOUT ROUTES
    # ----------------------
    @app.route("/workouts", methods=["GET"])
    def get_workouts():
        workouts = Workout.query.all()
        return jsonify(workouts_schema.dump(workouts)), 200

    @app.route("/workouts/<int:id>", methods=["GET"])
    def get_workout(id):
        w = Workout.query.get_or_404(id)
        result = workout_schema.dump(w)
        result['exercises'] = we_schema.dump(w.workout_exercises, many=True)
        return jsonify(result), 200

    @app.route("/workouts", methods=["POST"])
    def create_workout():
        data = request.get_json()
        try:
            validated = workout_schema.load(data)
            w = Workout(**validated)
            db.session.add(w)
            db.session.commit()
            return jsonify(workout_schema.dump(w)), 201
        except Exception as ex:
            db.session.rollback()
            return jsonify({"error": str(ex)}), 400

    @app.route("/workouts/<int:id>", methods=["DELETE"])
    def delete_workout(id):
        w = Workout.query.get_or_404(id)
        db.session.delete(w)
        db.session.commit()
        return jsonify({"message": "Workout deleted"}), 200

    # ----------------------
    # ADD EXERCISE TO WORKOUT
    # ----------------------
    @app.route("/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises", methods=["POST"])
    def add_exercise_to_workout(workout_id, exercise_id):
        data = request.get_json() or {}
        workout = Workout.query.get_or_404(workout_id)
        exercise = Exercise.query.get_or_404(exercise_id)
        try:
            payload = {
                "workout_id": workout.id,
                "exercise_id": exercise.id,
                "reps": data.get("reps"),
                "sets": data.get("sets"),
                "duration_seconds": data.get("duration_seconds")
            }
            validated = we_schema.load(payload)
            we = WorkoutExercise(**validated)
            db.session.add(we)
            db.session.commit()
            return jsonify(we_schema.dump(we)), 201
        except Exception as ex:
            db.session.rollback()
            return jsonify({"error": str(ex)}), 400

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(port=5000, debug=True)
