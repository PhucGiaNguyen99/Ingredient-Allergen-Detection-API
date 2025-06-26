from flask import Flask, request, jsonify
from allergen_store import get_allergens, set_allergens
from utils.allergen_detector import detect_allergens_spacy

app = Flask(__name__)

@app.route("/set_allergens", methods=["POST"])
def set_allergen_keywords():
    data = request.get_json()
    new_allergens = data.get("allergens", [])
    if isinstance(new_allergens, list):
        set_allergens(new_allergens)
        return jsonify({"message": "Allergens updated.", "allergens": new_allergens})
    else:
        return jsonify({"error": "Expected a list of allergens."}), 400

@app.route("/detect_allergens", methods=["POST"])
def detect():
    data = request.get_json()
    text = data.get("ingredients", "")
    allergens = get_allergens()
    found = detect_allergens_spacy(text, allergens)
    return jsonify({"detected_allergens": found})

if __name__ == "__main__":
    app.run(debug=True)
