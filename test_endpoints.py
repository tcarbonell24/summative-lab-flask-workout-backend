# test_endpoints.py
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def print_response(resp):
    print(f"Status: {resp.status_code}")
    try:
        print(json.dumps(resp.json(), indent=2))
    except:
        print(resp.text)
    print("-" * 50)

def test_exercises():
    print("== TESTING EXERCISES ==")

    # GET all exercises
    print("GET /exercises")
    resp = requests.get(f"{BASE_URL}/exercises")
    print_response(resp)
    exercises = resp.json()
    first_ex_id = exercises[0]['id'] if exercises else None

    # GET single exercise
    if first_ex_id:
        print(f"GET /exercises/{first_ex_id}")
        resp = requests.get(f"{BASE_URL}/exercises/{first_ex_id}")
        print_response(resp)

    # POST new exercise
    print("POST /exercises")
    new_ex = {"name":"Lunges","category":"Strength","equipment_needed":False}
    resp = requests.post(f"{BASE_URL}/exercises", json=new_ex)
    print_response(resp)
    new_ex_id = resp.json().get("id")

    # DELETE exercise
    if new_ex_id:
        print(f"DELETE /exercises/{new_ex_id}")
        resp = requests.delete(f"{BASE_URL}/exercises/{new_ex_id}")
        print_response(resp)

def test_workouts():
    print("== TESTING WORKOUTS ==")

    # GET all workouts
    print("GET /workouts")
    resp = requests.get(f"{BASE_URL}/workouts")
    print_response(resp)
    workouts = resp.json()
    first_w_id = workouts[0]['id'] if workouts else None

    # GET single workout
    if first_w_id:
        print(f"GET /workouts/{first_w_id}")
        resp = requests.get(f"{BASE_URL}/workouts/{first_w_id}")
        print_response(resp)

    # POST new workout
    print("POST /workouts")
    new_w = {"date":"2025-11-24","duration_minutes":40,"notes":"Evening session"}
    resp = requests.post(f"{BASE_URL}/workouts", json=new_w)
    print_response(resp)
    new_w_id = resp.json().get("id")

    # DELETE workout
    if new_w_id:
        print(f"DELETE /workouts/{new_w_id}")
        resp = requests.delete(f"{BASE_URL}/workouts/{new_w_id}")
        print_response(resp)

def test_add_exercise_to_workout():
    print("== TESTING ADD EXERCISE TO WORKOUT ==")

    # GET first workout and exercise
    w_resp = requests.get(f"{BASE_URL}/workouts")
    e_resp = requests.get(f"{BASE_URL}/exercises")
    workouts = w_resp.json()
    exercises = e_resp.json()
    if workouts and exercises:
        w_id = workouts[0]['id']
        e_id = exercises[0]['id']
        print(f"POST /workouts/{w_id}/exercises/{e_id}/workout_exercises")
        payload = {"reps": 10, "sets": 2}
        resp = requests.post(f"{BASE_URL}/workouts/{w_id}/exercises/{e_id}/workout_exercises", json=payload)
        print_response(resp)

def main():
    test_exercises()
    test_workouts()
    test_add_exercise_to_workout()

if __name__ == "__main__":
    main()
