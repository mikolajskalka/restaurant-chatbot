# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import json
import datetime

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.events import AllSlotsReset



class ActionGetMenu(Action):
    def name(self) -> Text:
        return "action_get_menu"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        with open("menu.json") as menu_file:
            menu_data = json.load(menu_file)

        menu_items = [f"{item['name']} (${item['price']})" for item in menu_data["items"]]
        dispatcher.utter_message(text="We offer:\n" + "\n".join(menu_items))

        return []


class ActionPlaceOrder(Action):
    def name(self) -> Text:
        return "action_place_order"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    
        dishes = tracker.get_slot("dish")
        
        if not dishes:
            dispatcher.utter_message(text="I'm sorry, I didn't catch what you'd like to order. Could you please repeat?")
            return []

        if not isinstance(dishes, list):
            dishes = [dishes]

        # Load menu data
        with open("menu.json") as menu_file:
            menu_data = json.load(menu_file)
            menu_items = {item["name"].lower() for item in menu_data["items"]}

        # Separate valid and invalid dishes
        valid_dishes = []
        invalid_dishes = []
        
        for dish in dishes:
            if dish.lower() in menu_items:
                valid_dishes.append(dish)
            else:
                invalid_dishes.append(dish)

        # Handle invalid dishes
        if invalid_dishes:
            invalid_str = ", ".join(invalid_dishes)
            dispatcher.utter_message(text=f"I'm sorry, but we don't serve {invalid_str}. Would you like to see our menu?")
            return []

        # Process valid order
        if valid_dishes:
            if len(valid_dishes) > 1:
                dishes_str = ", ".join(valid_dishes[:-1]) + " and " + valid_dishes[-1]
            else:
                dishes_str = valid_dishes[0]
            confirmation = f"Your order for {dishes_str} has been placed successfully!"
            dispatcher.utter_message(text=confirmation)
            return [SlotSet('dish', valid_dishes)]

        return []
    
class ActionGetOpeningHours(Action):
    def name(self) -> Text:
        return "action_is_restaurant_open"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Determine today's day name, e.g., "Monday"
        today = datetime.datetime.now().strftime('%A')

        # Read the opening hours from file
        with open("opening_hours.json") as oh_file:
            opening_hours_data = json.load(oh_file)

        # Retrieve today's hours from the json data
        hours = opening_hours_data["items"].get(today)
        if hours:
            open_time = hours["open"]
            close_time = hours["close"]
            if open_time == 0 and close_time == 0:
                message = f"Today is {today}. The restaurant is closed."
            else:
                message = f"Today is {today}. We are open from {open_time} to {close_time}."
        else:
            message = "I'm sorry, I couldn't retrieve today's opening hours."

        dispatcher.utter_message(text=message)
        return []
    

class ActionGetOrderReadyTime(Action):
    def name(self) -> Text:
        return "action_get_order_ready_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dishes = tracker.get_slot("dish")
        
        if not dishes:
            dispatcher.utter_message(text="I don't see any active orders.")
            return []

        if not isinstance(dishes, list):
            dishes = [dishes]

        # Load menu data and create a lookup dictionary
        with open("menu.json") as menu_file:
            menu_data = json.load(menu_file)
            menu_lookup = {item["name"].lower(): item for item in menu_data["items"]}

        # Find preparation time for each dish
        prep_times = {}
        not_found_dishes = []
        for dish in dishes:
            menu_item = menu_lookup.get(dish.lower())
            if menu_item:
                prep_times[dish] = menu_item["preparation_time"]
            else:
                not_found_dishes.append(dish)

        if not_found_dishes:
            dishes_str = ", ".join(not_found_dishes)
            message = f"I'm sorry, I couldn't find {dishes_str} in our menu."
        elif prep_times:
            max_prep_time = max(prep_times.values())
            if len(dishes) > 1:
                dishes_str = ", ".join(dishes[:-1]) + " and " + dishes[-1]
                message = f"Your order of {dishes_str} will be ready in approximately {max_prep_time} hours."
            else:
                message = f"Your {dishes[0]} will be ready in approximately {max_prep_time} hours."

        dispatcher.utter_message(text=message)
        return []
    
class ActionGetOpeningHours(Action):
    def name(self) -> Text:
        return "action_get_opening_hours"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Read the opening hours from file
        with open("opening_hours.json") as oh_file:
            opening_hours_data = json.load(oh_file)

        # Create a formatted schedule message
        schedule = ["Our opening hours:"]
        for day, hours in opening_hours_data["items"].items():
            if hours["open"] == 0 and hours["close"] == 0:
                schedule.append(f"{day}: Closed")
            else:
                schedule.append(f"{day}: {hours['open']} - {hours['close']}")

        message = "\n".join(schedule)
        dispatcher.utter_message(text=message)

        return []
    

class ActionResetSlots(Action):
    def name(self) -> Text:
        return "action_reset_slots"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [AllSlotsReset()]
    

class ValidateDishSlot(Action):
    def name(self) -> Text:
        return "action_validate_dish"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dishes = tracker.get_slot("dish")
        
        if not dishes:
            return [SlotSet("dish_valid", False)]

        if not isinstance(dishes, list):
            dishes = [dishes]

        # Load menu data
        with open("menu.json") as menu_file:
            menu_data = json.load(menu_file)
            menu_items = {item["name"].lower() for item in menu_data["items"]}

        # Check if all dishes are valid
        all_valid = all(any(dish.lower().startswith(menu_item) 
                          for menu_item in menu_items) 
                       for dish in dishes)

        return [SlotSet("dish_valid", all_valid)]