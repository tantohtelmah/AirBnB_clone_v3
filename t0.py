#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.state import State

print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))

first_state_id = list(storage.all(State).values())[0].id
print(State)
print("First state: {}".format(storage.get(State, "ba13f814-e1e1-4780-92bf-dd55294f6fd8")))
