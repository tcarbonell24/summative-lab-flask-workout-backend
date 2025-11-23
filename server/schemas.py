# server/schemas.py
from marshmallow import Schema, fields, validate, ValidationError, post_load
from server.models import Exercise, Workout, WorkoutExercise

# -----------------------
# EXERCISE SCHEMA
# -----------------------
class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(
        required=True,
        validate=validate.Length(min=3, error="Exercise name must be at least 3 characters long")
    )
    category = fields.Str(
        required=True,
        validate=validate.OneOf(["Strength", "Cardio", "Mobility", "Flexibility"])
    )
    equipment_needed = fields.Bool(missing=False)
    
    # Nested workouts for GET /exercises/<id>
    workouts = fields.List(fields.Nested(lambda: WorkoutSchema(only=("id", "date"))), dump_only=True)

# -----------------------
# WORKOUT SCHEMA
# -----------------------
class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(
        required=True,
        validate=validate.Range(min=1, error="Workout duration must be greater than 0")
    )
    notes = fields.Str(allow_none=True)
    
    # Nested exercises for GET /workouts/<id>
    exercises = fields.List(fields.Nested(lambda: WorkoutExerciseSchema(exclude=("workout_id",))), dump_only=True)

# -----------------------
# WORKOUT EXERCISE SCHEMA
# -----------------------
class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    reps = fields.Int(validate=validate.Range(min=0))
    sets = fields.Int(validate=validate.Range(min=0))
    duration_seconds = fields.Int(validate=validate.Range(min=0))
    
    # Nested references
    workout = fields.Nested(WorkoutSchema, dump_only=True, exclude=("exercises",))
    exercise = fields.Nested(ExerciseSchema, dump_only=True, exclude=("workouts",))

    @post_load
    def check_reps_sets_or_duration(self, data, **kwargs):
        # Ensure at least one of reps/sets/duration is provided
        if not any([data.get("reps"), data.get("sets"), data.get("duration_seconds")]):
            raise ValidationError(
                "Must provide at least one of reps, sets, or duration_seconds"
            )
        return data
