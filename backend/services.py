# services.py
import requests
import os
from dotenv import load_dotenv

load_dotenv() # Loads variables from .env file

USDA_API_KEY = os.getenv('USDA_API_KEY')
USDA_API_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"

def get_nutrition_data(ingredients):
    """
    Queries the USDA API for nutritional data of ingredients.
    This is a simplified example. A real implementation needs to handle
    parsing quantities and summing nutrients.
    """
    # NOTE: This is a major challenge. The LLM output "1 cup chopped kale" 
    # must be parsed to query for "kale". This requires significant logic.
    # For now, we'll simulate a lookup.
    
    print(f"Querying USDA for: {ingredients}")
    # In a real app, you would loop through each ingredient, make an API call,
    # and aggregate the results for calories, protein, carbs, and fat.
    
    # Placeholder logic
    total_calories = 0
    total_protein_g = 0
    total_carbohydrates_g = 0
    total_fat_g = 0

    # This loop is a placeholder for actual API calls
    for item in ingredients:
        if "quinoa" in item:
            total_calories += 222
            total_protein_g += 8
            total_carbohydrates_g += 40
            total_fat_g += 4
        if "salmon" in item:
            total_calories += 412
            total_protein_g += 40
            total_carbohydrates_g += 0
            total_fat_g += 28

    nutritional_breakdown = {
        "calories": int(total_calories),
        "macros": {
            "protein_g": int(total_protein_g),
            "carbohydrates_g": int(total_carbohydrates_g),
            "fat_g": int(total_fat_g)
        },
        "key_micronutrients": "Data aggregated from USDA API" # Placeholder
    }
    return nutritional_breakdown
