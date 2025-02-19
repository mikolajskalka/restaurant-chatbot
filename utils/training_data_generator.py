import random
import os

def apply_typos(text):
    """Apply common typos and mistakes to text."""
    common_typos = {
        'ready': ['redy', 'reedy', 'rady'],
        'order': ['ordr', 'orde', 'oder'],
        'restaurant': ['resturant', 'restaurent', 'restarant'],
        'open': ['opn', 'oppen', 'openn'],
        'hours': ['hrs', 'ours', 'houres'],
        'when': ['wen', 'whn'],
        'time': ['tiem', 'tym'],
        'have': ['hav', 'ave'],
        'please': ['plz', 'pls', 'plese'],
        'would': ['wud', 'wuld'],
        'like': ['liek', 'lke'],
    }
    
    words = text.split()
    result = []
    
    for word in words:
        lower_word = word.lower()
        if lower_word in common_typos and random.random() < 0.5:  # 30% chance of typo
            result.append(random.choice(common_typos[lower_word]))
        else:
            result.append(word)
    
    return ' '.join(result)

def generate_training_data():
    """Generate training data with typos and variations."""
    
    # Base templates for different intents
    place_order_templates = [
        "I would like to order {dish}",
        "Can I have {dish}",
        "I want to order {dish}",
        "Give me {dish}",
        "Id like to get {dish}",
    ]
    
    dishes = [
        "Pizza", "Burger", "Spaghetti", "Lasagne", "Sushi",
        "Pad Thai", "Tacos", "Fish and Chips", "Ramen"
    ]
    
    order_ready_templates = [
        "When will my order be ready",
        "How long until I get my order",
        "When can I get my food",
        "How much more time for my order",
        "Is my order ready yet"
    ]
    
    check_open_templates = [
        "Are you open now",
        "Is the restaurant open",
        "Are you guys still open",
        "Is this place open",
        "Do you take orders now"
    ]
    
    opening_hours_templates = [
        "What are your hours",
        "When do you open",
        "What time do you close",
        "Tell me your opening hours",
        "Until what time are you open"
    ]
    
    # Generate data with typos
    training_data = []
    
    # Place order intent
    training_data.append("\n- intent: place_order\n  examples: |")
    for template in place_order_templates:
        for dish in dishes:
            # Apply typos to the template but not to the dish name
            text_parts = template.split("{dish}")
            typo_text = apply_typos(text_parts[0])
            if len(text_parts) > 1:
                typo_text += f" [{dish}](dish)" + apply_typos(text_parts[1])
            else:
                typo_text += f" [{dish}](dish)"
            training_data.append(f"    - {typo_text}")

    # Order ready intent
    training_data.append("\n- intent: order_ready\n  examples: |")
    for template in order_ready_templates:
        training_data.append(f"    - {apply_typos(template)}")
        training_data.append(f"    - {template}")
    
    # Check restaurant open intent
    training_data.append("\n- intent: check_restaurant_open\n  examples: |")
    for template in check_open_templates:
        training_data.append(f"    - {apply_typos(template)}")
        training_data.append(f"    - {template}")
    
    # Opening hours intent
    training_data.append("\n- intent: opening_hours\n  examples: |")
    for template in opening_hours_templates:
        training_data.append(f"    - {apply_typos(template)}")
        training_data.append(f"    - {template}")
    
    return "\n".join(training_data)

if __name__ == "__main__":
    generated_data = generate_training_data()
    with open(os.path.join("tests","generated_training_data.yml"), "w") as f:
        f.write("version: \"3.1\"\n\nnlu:")
        f.write(generated_data)