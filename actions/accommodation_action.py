import json
import logging
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Dict, Text, List

# Set up the logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class ActionAccommodationInfo(Action):
    def name(self) -> Text:
        return "action_accommodation_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        logger.debug("Action 'action_accommodation_info' called.")
        
        try:
            # Load accommodation data from JSON file
            with open('data/accommodation_data.json', 'r') as f:
                accommodation_data = json.load(f)
            logger.debug(f"Accommodation data loaded: {accommodation_data}")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            # Log and inform the user if there's an issue loading the data
            error_message = f"Sorry, there was an error loading the accommodation data: {str(e)}"
            dispatcher.utter_message(text=error_message)
            logger.error(error_message)
            return []

        # Get the user's message from the tracker
        user_question = tracker.latest_message.get('text', '').lower()
        logger.debug(f"User question: {user_question}")

        # Determine what the user is asking for
        topic = None
        if "how to choose accommodation" in user_question:
            topic = "how_to_choose_accommodation"
        elif "room finder" in user_question or "find a room" in user_question or "accomodation" in user_question:
            topic = "room_finder"
        elif "applying and paying" in user_question or "apply" in user_question or "pay" in user_question:
            topic = "applying_and_paying"
        elif "moving in" in user_question or "move in" in user_question:
            topic = "moving_in"
        elif "private accommodation" in user_question:
            topic = "private_accommodation"
        elif "contact" in user_question:
            topic = "contact"

        # Default answer if no match is found
        answer = "Sorry, I couldn't find the information you're looking for."

        # Check if the accommodation data contains the relevant information
        if accommodation_data and "accommodation_information" in accommodation_data and topic:
            if topic in accommodation_data["accommodation_information"]:
                value = accommodation_data["accommodation_information"][topic]
                description = value.get("overview", "No description available")
                link = value.get("link", "No link available")
                # Using HTML for clickable link
                msg={ "type":"video", "payload":{ "title":"Link name", "src": "https://youtube.com/9C1Km6xfdMA" } }
                answer = f"{description}<br>For more details, visit: <a href='{link}' target='_blank'>Click here</a>, attachment=msg"

                logger.debug(f"Found match: {description}, {link}")
        
        # Send the response back to the user
        dispatcher.utter_message(text=f"Here's what I found: {answer}", parse_mode='html')
        logger.debug(f"Response sent: {answer}")

        return []
