import pytest
from sqlalchemy.exc import IntegrityError
from server.app import create_app
from server.models import db, Exercise, Workout, WorkoutExercise

@pytest.fixture(scope="module")
def test_app():
    """Create app context for tests."""
    app = create_app()
    with app.app_context():
        yield app

# --------------------------
# Exercise Tests
# --------------------------
def test_exercise_data(test_app):
    exercises = Exercise.query.all()
    assert len(exercises) >= 5  # Ensure at least 5 exercises seeded

    names = [ex.name for ex in exercises]
    assert "Push Up" in names
    assert "Squat" in names

def test_exercise_fields(test_app):
    ex = Exercise.query.filter_by(name="Dumbbell Curl").first()
    assert ex.category == "Strength"
    assert ex.equipment_needed is True

# --------------------------
# Workout Tests
# --------------------------
def test_workout_data(test_app):
    workouts = Workout.query.all()
    assert len(workouts) >= 2  # Ensure at least 2 workouts seeded

def test_workout_fields(test_app):
    workout = Workout.query.filter_by(duration_minutes=45).first()
    assert workout.notes == "Morning strength training"

# --------------------------
# WorkoutExercise Tests
# --------------------------
def test_workout_exercise_association(test_app):
    we = WorkoutExercise.query.first()
    assert we.workout is not None
    assert we.exercise is not None

def test_workout_exercise_fields(test_app):
    we = WorkoutExercise.query.filter_by(reps=15).first()
    assert we.sets == 3
    assert we.duration_seconds is None

# --------------------------
# ORM Relationship Tests
# --------------------------
def test_workout_exercises_relationship(test_app):
    workout = Workout.query.filter_by(duration_minutes=45).first()
    exercise_names = [ex.name for ex in workout.exercises]
    assert "Push Up" in exercise_names
    assert "Squat" in exercise_names

def test_exercise_workouts_relationship(test_app):
    exercise = Exercise.query.filter_by(name="Push Up").first()
    workout_dates = [w.date for w in exercise.workouts]
    assert any(date.isoformat() == "2025-11-22" for date in workout_dates)

# --------------------------
# Constraints and Validations
# --------------------------
def test_unique_exercise_name(test_app):
    """Test unique constraint on Exercise name."""
    ex1 = Exercise(name="Push Up", category="Strength", equipment_needed=False)
    db.session.add(ex1)
    with pytest.raises(IntegrityError):
        db.session.commit()
    db.session.rollback()

def test_workout_exercise_unique_constraint(test_app):
    """Test unique_workout_exercise constraint."""
    we1 = WorkoutExercise.query.first()
    duplicate = WorkoutExercise(
        workout_id=we1.workout_id,
        exercise_id=we1.exercise_id,
        reps=10,
        sets=2
    )
    db.session.add(duplicate)
    with pytest.raises(IntegrityError):
        db.session.commit()
    db.session.rollback()
