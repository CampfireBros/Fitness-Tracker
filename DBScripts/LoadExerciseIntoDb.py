import csv
import os
import config
from pymongo import MongoClient


def load_exercises():
    client = MongoClient(config.MONGODB_URL)
    db = client.exercisedb
    exercise_collection = db.Exercises

    files = ["Abdominal", "Back", "Bicep", "Chest", "Leg", "Shoulder", "Tricep"]
    for filename in files:
        with open(os.path.join(os.path.dirname(__file__), "data/" + filename + ".csv"), "rU") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            exercise = []
            next(reader)
            for line in reader:
                name = line[0]
                primary = line[1]
                secondary = line[2].split(":")
                equipment = line[3]
                mechanics = line[4]

                exercise.append(
                    {
                        "exercise": name,
                        "primary": primary,
                        "secondary": secondary,
                        "equipment": equipment,
                        "mechanics": mechanics
                    }
                )
            exercise_collection.insert_one(
                {
                    "muscle": filename,
                    "exercises": exercise
                }
            )


if __name__ == '__main__':
    load_exercises()
