# check_db.py
from sqlalchemy import text
from server.app import create_app
from server.models import db

app = create_app()

with app.app_context():
    # Use a connection context
    with db.engine.connect() as conn:
        # List all tables
        tables = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';")).all()
        print("Tables in database:")
        for table in tables:
            print(" -", table[0])

        print("\nSample data from each table:")

        # Exercises
        print("\nExercises:")
        exercises = conn.execute(text("SELECT * FROM exercises;")).all()
        for row in exercises:
            print(row)

        # Workouts
        print("\nWorkouts:")
        workouts = conn.execute(text("SELECT * FROM workouts;")).all()
        for row in workouts:
            print(row)

        # WorkoutExercises
        print("\nWorkoutExercises:")
        workout_exercises = conn.execute(text("SELECT * FROM workout_exercises;")).all()
        for row in workout_exercises:
            print(row)
