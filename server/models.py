from sqlalchemy.orm import validates, relationship
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Text, CheckConstraint, UniqueConstraint
from server.db import db

class Exercise(db.Model):
    __tablename__ = "exercises"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    category = Column(String, nullable=False)
    equipment_needed = Column(Boolean, nullable=False, default=False)

    # Add overlaps to prevent SAWarnings
    workout_exercises = relationship(
        "WorkoutExercise",
        back_populates="exercise",
        overlaps="workouts,exercise"
    )
    workouts = relationship(
        "Workout",
        secondary="workout_exercises",
        back_populates="exercises",
        overlaps="workout_exercises,exercise"
    )

    @validates("name")
    def validate_name(self, key, value):
        if not value or len(value.strip()) < 3:
            raise ValueError("Exercise name must be at least 3 characters long.")
        return value.strip()

    @validates("category")
    def validate_category(self, key, value):
        allowed_categories = ["Strength", "Cardio", "Mobility", "Flexibility"]
        if value not in allowed_categories:
            raise ValueError(f"Category must be one of {allowed_categories}")
        return value

class Workout(db.Model):
    __tablename__ = "workouts"
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    notes = Column(Text)

    __table_args__ = (
        CheckConstraint("duration_minutes > 0", name="check_duration_positive"),
    )

    workout_exercises = relationship(
        "WorkoutExercise",
        back_populates="workout",
        overlaps="exercises,workout"
    )
    exercises = relationship(
        "Exercise",
        secondary="workout_exercises",
        back_populates="workouts",
        overlaps="workout_exercises,workout"
    )

    @validates("duration_minutes")
    def validate_duration(self, key, value):
        if value <= 0:
            raise ValueError("Workout duration must be greater than 0.")
        return value

class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    id = Column(Integer, primary_key=True)
    workout_id = Column(Integer, ForeignKey("workouts.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    reps = Column(Integer)
    sets = Column(Integer)
    duration_seconds = Column(Integer)

    __table_args__ = (
        UniqueConstraint("workout_id", "exercise_id", name="unique_workout_exercise"),
        CheckConstraint("(reps >= 0) OR reps IS NULL", name="check_reps_non_negative"),
        CheckConstraint("(sets >= 0) OR sets IS NULL", name="check_sets_non_negative"),
        CheckConstraint("(duration_seconds >= 0) OR duration_seconds IS NULL", name="check_duration_non_negative"),
    )

    workout = relationship(
        "Workout",
        back_populates="workout_exercises",
        overlaps="exercises,workouts"
    )
    exercise = relationship(
        "Exercise",
        back_populates="workout_exercises",
        overlaps="workouts,exercises"
    )

    @validates("reps", "sets", "duration_seconds")
    def validate_positive_values(self, key, value):
        if value is not None and value < 0:
            raise ValueError(f"{key} must be zero or positive.")
        return value
