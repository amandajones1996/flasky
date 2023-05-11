from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.crystal import Crystal
from app.models.healer import Healer

# class Crystal():
#     def __init__ (self, id, name, color, powers):
#         self.id = id
#         self.name = name
#         self.color = color
#         self.powers = powers


# crystals = [
#     Crystal(1, "Amethyst", "Purple", "Infinite Knowledge and wisdom"),
#     Crystal(2, "Tigers Eye", "Gold", "Confidence, Strength"),
#     Crystal(3, "Rose Quartz", "Pink", "Love")
# ]

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"messgae": f"{model_id} invalid"}, 400))
    
    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"messgae": f"{cls.__name__} {model_id} not found"}, 404))
    return model

crystal_bp = Blueprint("crystals", __name__, url_prefix="/crystals")

# @crystal_bp.route("", methods=["GET"])
# def handle_crystals():
#     crystal_response = []
#     for crystal in crystals:
#         crystal_response.append({
#             "id": crystal.id,
#             "name": crystal.name,
#             "color": crystal.color,
#             "power": crystal.powers
#         })

#     return jsonify(crystal_response)

# @crystal_bp.route("/<crystal_id>", methods=["GET"])
# def handle_crystal(crystal_id):
#     crystal = validate_crystal(crystal_id)
#     return {
#         "id": crystal.id,
#         "name": crystal.name,
#         "color": crystal.color,
#         "power": crystal.powers
#         }
@crystal_bp.route("", methods=['POST'])
# define route for creating a crystal resource
def create_crystal():
    request_body = request.get_json()
    new_crystal = Crystal.from_dict(request_body)

    db.session.add(new_crystal)
    db.session.commit()

    return jsonify(f"Crystal {new_crystal.name} successfully created!"), 201

@crystal_bp.route("", methods=['GET'])
def read_all_crystals():
    color_query = request.args.get("color")
    powers_query = request.args.get("powers")

    crystals_response = []
    
    if color_query:
        crystals = Crystal.query.filter_by(color=color_query)
    elif powers_query:
        crystals = Crystal.query.filter_by(powers=powers_query)
    else:
        crystals = Crystal.query.all()
    
    for crystal in crystals:
        crystals_response.append(crystal.to_dic())
    return jsonify(crystals_response)

@crystal_bp.route("/<crystal_id>", methods=['GET'])
def read_one_crystal(crystal_id):
    crystal = validate_model(Crystal, crystal_id)
    return crystal.to_dic(), 200

@crystal_bp.route("/<crystal_id>", methods=['PUT'])
def update_crystal(crystal_id):
    crystal = validate_model(Crystal, crystal_id)
    request_body = request.get_json()

    crystal.name = request_body["name"]
    crystal.color = request_body["color"]
    crystal.powers = request_body["powers"]

    db.session.commit()

    return crystal.to_dic(), 200

@crystal_bp.route("/<crystal_id>", methods=['DELETE'])
def delete_crystal(crystal_id):
    crystal = validate_model(Crystal, crystal_id)

    db.session.delete(crystal)
    db.session.commit()

    return make_response(f"Crystal #{crystal_id} successfully deleted")

healer_bp = Blueprint("healers", __name__, url_prefix="/healers")

@healer_bp.route("", methods=['POST'])
# define a route for creating a crystal resource
def create_healer():
    request_body = request.get_json()
    
    new_healer = Healer(
        name=request_body["name"]
    )
    
    db.session.add(new_healer)
    db.session.commit()
    
    return jsonify(f"Yayyyy Healer {new_healer.name} successfully created!"), 201


@healer_bp.route("", methods=["GET"])
def read_all_healers():
    
    healers = Healer.query.all()
        
    healers_response = []
    
    for healer in healers:
        healers_response.append({ 
            "name": healer.name,
            "id": healer.id
            })
    
    return jsonify(healers_response)

@healer_bp.route("/<healer_id>/crystals", methods=['POST'])
def create_crystal_by_id(healer_id):
    healer = validate_model(Healer, healer_id)
    request_body = request.get_json()

    new_crystal = Crystal(
        name = request_body["name"],
        color = request_body["color"],
        powers = request_body["powers"],
        healer=healer
    )
    db.session.add(new_crystal)
    db.session.commit()
    return jsonify(f"Crystal {new_crystal.name} owned by {new_crystal.healer.name} was successfully created."), 201

@healer_bp.route("/<healer_id>/crystals", methods=['GET'])
def get_all_crystals_with_id(healer_id):
    healer = validate_model(Healer, healer_id)

    crystals_response = []
    for crystal in healer.crystals:
        crystals_response.append(crystal.to_dic())

    return jsonify(crystals_response), 200
