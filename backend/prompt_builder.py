# prompt_builder.py

#Meal Suggestion
def create_meal_suggestion_prompt(user_profile, available_ingredients=None):
    """Constructs a detailed prompt for the LLM based on user data."""
    
    # User profile data from the request 
    diet = user_profile.get('dietary_preferences', 'any')
    allergies = user_profile.get('allergies', [])
    goal = user_profile.get('goal', 'general_health')

    prompt = f"You are a helpful nutrition planning assistant. Generate two distinct and varied meal suggestions for a user with the following profile:\n"
    prompt += f"- Dietary Preference: {diet}\n"
    prompt += f"- Health Goal: {goal}\n"
    
    if allergies:
        # Allergies must be strictly avoided 
        prompt += f"- Must Avoid (Allergies): {', '.join(allergies)}\n"
    
    if available_ingredients:
        # Optional list of ingredients on hand 
        prompt += f"- Try to use some of these available ingredients: {', '.join(available_ingredients)}\n"

    prompt += "\nFor each meal, provide a unique title, a list of ingredients with quantities, and step-by-step instructions."
    prompt += " Also, provide a brief 'goal_justification' explaining how the meal supports the user's goal."
    prompt += " Please format the response as a JSON object with two keys: 'meal_option_a' and 'meal_option_b'."
    
    return prompt

#Meal Planning
def create_meal_plan_prompt(user_profile, duration_days):
    """Constructs a detailed prompt for the LLM for a multi-day meal plan."""
    
    diet = user_profile.get('dietary_preferences', 'any')
    allergies = user_profile.get('allergies', [])
    goal = user_profile.get('goal', 'general_health')

    # Start building the prompt
    prompt = f"You are a helpful nutrition planning assistant. Generate a {duration_days}-day meal plan for a user with the following profile:\n"
    prompt += f"- Dietary Preference: {diet}\n"
    prompt += f"- Health Goal: {goal}\n"
    
    if allergies:
        prompt += f"- Must Avoid (Allergies): {', '.join(allergies)}\n"

    prompt += "\nRespond with a JSON object. The root object must have two keys:\n"
    prompt += f"1. 'plan_title' (a creative title for the plan, e.g., '{duration_days}-Day {goal.title()} Plan').\n"
    prompt += "2. 'days' (a list of day objects).\n"
    
    prompt += "\nEach day object in the 'days' list must have the following keys:\n"
    prompt += "1. 'day' (the day number, starting from 1).\n"
    prompt += "2. 'breakfast' (a meal object).\n"
    prompt += "3. 'lunch' (a meal object).\n"
    prompt += "4. 'dinner' (a meal object).\n"
    prompt += "5. 'snack' (a meal object).\n"
    prompt += "6. 'daily_goal_justification' (a brief string explaining how this day's meals support the user's goal).\n"

    prompt += "\nEach meal object (breakfast, lunch, dinner, snack) must have these keys:\n"
    prompt += "1. 'title' (a unique title for the meal).\n"
    prompt += "2. 'ingredients' (a list of strings with quantities).\n"
    prompt += "3. 'instructions' (a list of strings with step-by-step instructions).\n"
    prompt += "4. 'goal_justification' (a brief string explaining how this specific meal supports the goal).\n"
    
    prompt += "\nDo NOT include 'nutritional_breakdown' or 'daily_nutritional_summary', as I will calculate those myself."
    
    return prompt
