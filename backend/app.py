# app.py (Updated Version)

from flask import Flask, request, jsonify
import json
from prompt_builder import create_meal_suggestion_prompt, create_meal_plan_prompt
from services import get_nutrition_data
from llm_service import get_llm_completion  # <--- ADD THIS IMPORT

app = Flask(__name__)

@app.route('/meal-suggestion', methods=['POST'])
def get_meal_suggestion():
    # 1. Request Initiation
    request_data = request.get_json()
    if not request_data or 'user_profile' not in request_data:
        return jsonify({"error": "A 'user_profile' object is required in the request body."}), 400
    
    user_profile = request_data.get('user_profile')
    available_ingredients = request_data.get('available_ingredients')

    # 2. LLM Interaction
    prompt = create_meal_suggestion_prompt(user_profile, available_ingredients)
    
    # --- THIS IS THE KEY CHANGE ---
    # Replace the hardcoded string with a call to your new function
    llm_response_str = get_llm_completion(prompt)
    # ----------------------------
    
    try:
        llm_data = json.loads(llm_response_str)
    except json.JSONDecodeError:
        return jsonify({"error": "Failed to parse response from LLM.", "raw_response": llm_response_str}), 500

    # Check if the LLM returned an error inside its JSON
    if 'error' in llm_data:
         return jsonify({"error": "An error occurred with the LLM service.", "details": llm_data.get('details')}), 500

    meal_option_a = llm_data.get('meal_option_a')
    meal_option_b = llm_data.get('meal_option_b')

    # 3. Data Enrichment
    if meal_option_a:
        nutrition_a = get_nutrition_data(meal_option_a['ingredients'])
        meal_option_a['nutritional_breakdown'] = nutrition_a

    if meal_option_b:
        nutrition_b = get_nutrition_data(meal_option_b['ingredients'])
        meal_option_b['nutritional_breakdown'] = nutrition_b

    # 4. Response Assembly
    final_response = {
        "meal_option_a": meal_option_a,
        "meal_option_b": meal_option_b
    }

    return jsonify(final_response), 200

# --- NEW FUNCTION ADDED HERE ---

@app.route('/meal-plan', methods=['POST'])
def get_meal_plan():
    # 1. Request Initiation
    request_data = request.get_json()
    if not request_data:
        return jsonify({"error": "Request body is required."}), 400
    
    user_profile = request_data.get('user_profile')
    plan_duration_days = request_data.get('plan_duration_days')

    if not user_profile:
        return jsonify({"error": "A 'user_profile' object is required."}), 400
    if not plan_duration_days or plan_duration_days not in [1, 3]:
        return jsonify({"error": "A 'plan_duration_days' field (1 or 3) is required."}), 400

    # 2. LLM Interaction
    prompt = create_meal_plan_prompt(user_profile, plan_duration_days)
    llm_response_str = get_llm_completion(prompt)
    
    try:
        llm_data = json.loads(llm_response_str)
    except json.JSONDecodeError:
        return jsonify({"error": "Failed to parse response from LLM.", "raw_response": llm_response_str}), 500

    if 'error' in llm_data:
        return jsonify({"error": "An error occurred with the LLM service.", "details": llm_data.get('details')}), 500

    # 3. Data Enrichment & Aggregation
    try:
        # Loop through each day in the plan
        for day in llm_data.get('days', []):
            meals_of_the_day = ['breakfast', 'lunch', 'dinner', 'snack']
            daily_nutrition = {
                "calories": 0, "protein_g": 0, "carbohydrates_g": 0, "fat_g": 0
            }

            # Loop through each meal of the day
            for meal_name in meals_of_the_day:
                if meal_name in day:
                    # Get nutrition data for this one meal
                    meal_nutrition = get_nutrition_data(day[meal_name]['ingredients'])
                    
                    # Add the breakdown to the meal object
                    day[meal_name]['nutritional_breakdown'] = meal_nutrition
                    
                    # Add this meal's nutrition to the daily total
                    daily_nutrition["calories"] += meal_nutrition['calories']
                    daily_nutrition["protein_g"] += meal_nutrition['macros']['protein_g']
                    daily_nutrition["carbohydrates_g"] += meal_nutrition['macros']['carbohydrates_g']
                    daily_nutrition["fat_g"] += meal_nutrition['macros']['fat_g']

            # Add the calculated daily summary to the day object
            day['daily_nutritional_summary'] = {
                "calories": int(daily_nutrition["calories"]),
                "macros": {
                    "protein_g": int(daily_nutrition["protein_g"]),
                    "carbohydrates_g": int(daily_nutrition["carbohydrates_g"]),
                    "fat_g": int(daily_nutrition["fat_g"])
                }
            }
    
    except Exception as e:
        # This catches errors during the complex loop (e.g., if LLM's JSON was malformed)
        return jsonify({"error": f"Failed to process and enrich LLM data: {str(e)}", "llm_data": llm_data}), 500

    # 4. Response Assembly
    return jsonify(llm_data), 200

# --- END OF NEW FUNCTION ---

if __name__ == '__main__':
    app.run(debug=True)
