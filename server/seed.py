#!/usr/bin/env python3

from datetime import date
from server.app import create_app
from server.models import db, Exercise, Workout, WorkoutExercise

app = create_app()

with app.app_context():

    # Clear existing data
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    # --------------------------
    # Seed Exercises
    # --------------------------
    exercises = [
        Exercise(name="Push Up", category="Strength", equipment_needed=False),
        Exercise(name="Squat", category="Strength", equipment_needed=False),
        Exercise(name="Plank", category="Strength", equipment_needed=False),  # Fixed category
        Exercise(name="Running", category="Cardio", equipment_needed=False),
        Exercise(name="Dumbbell Curl", category="Strength", equipment_needed=True),
    ]

    db.session.add_all(exercises)
    db.session.commit()

    # --------------------------
    # Seed Workouts
    # --------------------------
    workouts = [
        Workout(date=date(2025, 11, 22), duration_minutes=45, notes="Morning strength training"),
        Workout(date=date(2025, 11, 23), duration_minutes=30, notes="Quick cardio session"),
    ]

    db.session.add_all(workouts)
    db.session.commit()

    # --------------------------
    # Seed WorkoutExercises (associations)
    # --------------------------
    workout_exercises = [
        WorkoutExercise(workout_id=workouts[0].id, exercise_id=exercises[0].id, reps=15, sets=3),
        WorkoutExercise(workout_id=workouts[0].id, exercise_id=exercises[1].id, reps=20, sets=3),
        WorkoutExercise(workout_id=workouts[1].id, exercise_id=exercises[3].id, duration_seconds=1200),
    ]

    db.session.add_all(workout_exercises)
    db.session.commit()

    print("Database seeded successfully!")
