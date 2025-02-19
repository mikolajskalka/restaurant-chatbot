import json
import rasa

with open("opening_hours.json") as oh_file:
    opening_hours_data = json.load(oh_file)

with open("menu.json") as menu_file:
    menu_data = json.load(menu_file)

intents = {
    "opening_hours": [
        "What are your opening hours?",
        "When are you open?",
        "Give me your schedule."
    ],
    "menu_info": [
        "What do you serve?",
        "Show me the menu.",
        "What's on your menu?"
    ],
    "place_order": [
        "I'd like to order",
        "Can I get a meal?",
        "I want to buy something"
    ]
}

class RestaurantChatbot:
    def __init__(self):
        self.intents = intents

    def recognize_intent(self, user_input):
        for intent_name, phrases in self.intents.items():
            if any(phrase.lower() in user_input.lower() for phrase in phrases):
                return intent_name
        return None

    def handle_opening_hours(self):
        hours = opening_hours_data["items"]
        return "Our hours are: " + ", ".join(
            f"{day}: {info['open']} - {info['close']}" for day, info in hours.items()
        )

    def handle_menu_info(self):
        items = menu_data["items"]
        return "We offer: " + ", ".join(item["name"] for item in items)

    def handle_place_order(self, user_input):
        return f"Your order for '{user_input}' has been placed!"

    def on_message(self, user_input):
        intent = self.recognize_intent(user_input)
        if intent == "opening_hours":
            return self.handle_opening_hours()
        elif intent == "menu_info":
            return self.handle_menu_info()
        elif intent == "place_order":
            return self.handle_place_order(user_input)
        else:
            return "I’m not sure. Can you rephrase?"

if __name__ == "__main__":
    bot = RestaurantChatbot()
    while True:
        user_text = input("You: ")
        if user_text.lower() in ["exit", "quit"]:
            print("Chatbot: Goodbye!")
            break
        response = bot.on_message(user_text)
        print(f"Chatbot: {response}")