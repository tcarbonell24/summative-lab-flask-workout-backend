# server/testing/test_imports.py

from server.app import app
from server.models import db, Exercise, Workout, WorkoutExercise

def test_seed_data():
    with app.app_context():
        print("=== Exercises ===")
        exercises = Exercise.query.all()
        for e in exercises:
            print(f"{e.id}: {e.name}")

        print("\n=== Workouts ===")
        workouts = Workout.query.all()
        for w in workouts:
            print(f"{w.id}: {w.name}")

        print("\n=== WorkoutExercises ===")
        workout_exercises = WorkoutExercise.query.all()
        for we in workout_exercises:
            print(f"Workout {we.workout_id} - Exercise {we.exercise_id} - Sets: {we.sets}, Reps: {we.reps}")

        # Optional: check relationships
        print("\n=== Exercises for each Workout ===")
        for w in workouts:
            print(f"{w.name}: {[e.name for e in w.exercises]}")

        print("\n=== Workouts for each Exercise ===")
        for e in exercises:
            print(f"{e.name}: {[w.name for w in e.workouts]}")

if __name__ == "__main__":
    test_seed_data()
