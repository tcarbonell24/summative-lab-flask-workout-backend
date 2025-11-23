#!/usr/bin/env python3

from server.app import create_app
from server.models import db, Exercise, Workout, WorkoutExercise

app = create_app()

with app.app_context():
    session = db.session

    # --------------------------
    # Verify Exercises
    # --------------------------
    exercises = session.execute(session.select(Exercise)).scalars().all()
    print("Exercises:")
    for ex in exercises:
        print(f"  {ex.id}: {ex.name}, Category: {ex.category}, Equipment Needed: {ex.equipment_needed}")

    # --------------------------
    # Verify Workouts
    # --------------------------
    workouts = session.execute(session.select(Workout)).scalars().all()
    print("\nWorkouts:")
    for w in workouts:
        print(f"  {w.id}: Date: {w.date}, Duration: {w.duration_minutes} mins, Notes: {w.notes}")

    # --------------------------
    # Verify WorkoutExercises (Associations)
    # --------------------------
    workout_exercises = session.execute(session.select(WorkoutExercise)).scalars().all()
    print("\nWorkoutExercises:")
    for we in workout_exercises:
        exercise = session.get(Exercise, we.exercise_id)
        workout = session.get(Workout, we.workout_id)
        print(
            f"  Workout {workout.id} ({workout.date}) -> Exercise {exercise.name}: "
            f"Reps: {we.reps}, Sets: {we.sets}, Duration (sec): {we.duration_seconds}"
        )

    # --------------------------
    # Verify relationships via ORM
    # --------------------------
    print("\nVerify relationships via ORM:")
    for w in workouts:
        print(f"Workout {w.id} has exercises:")
        for ex in w.exercises:
            print(f"  - {ex.name}")
    for ex in exercises:
        print(f"Exercise {ex.name} belongs to workouts:")
        for w in ex.workouts:
            print(f"  - {w.date}")
