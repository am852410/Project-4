import models
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict

dogs = Blueprint('dogs', 'dogs')

@dogs.route('', methods=['GET'])
def dogs_index():
    result = models.Dog.select()

    print("")
    print('result of dog select query')
    print(result) #hmm looks like SQL

    dog_dicts = [model_to_dict(dog) for dog in result]

    return jsonify({
        'data': dog_dicts,
        'message': f"Successfully found {len(dog_dicts)} dogs",
        'status': 200
    }), 200

@dogs.route('', methods=['POST'])
def create_dog():
    # .get_json() attached to request will extract JSON from the request body
    payload = request.get_json() # this is like req.body in express
    print(payload) # you should see request body in your terminal :)

    new_dog = models.Dog.create(name=payload['name'], breed=payload['breed'], age=payload['age'], weight=payload['weight'], additionalComments=payload['additionalComments'])
    print(new_dog)
    dog_dict = model_to_dict(new_dog)

    return jsonify(
        data=dog_dict,
        message='Successfully created dog!',
        status=201
    ), 201
