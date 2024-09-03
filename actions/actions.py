import json
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Dict, Text, List

class ActionAskQuestion(Action):
    def name(self) -> Text:
        return "action_ask_question"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Load the course data from the JSON file
        try:
            with open('data/course_data.json', 'r') as f:
                course_data = json.load(f)
        except FileNotFoundError:
            dispatcher.utter_message(text="Sorry, the course data file is missing.")
            return []
        except json.JSONDecodeError:
            dispatcher.utter_message(text="Sorry, there was an error reading the course data file.")
            return []
        except Exception as e:
            dispatcher.utter_message(text=f"An unexpected error occurred: {e}")
            return []

        # Get the user query from Rasa
        user_question = tracker.latest_message.get('text', '').lower()

        # Determine what the user is asking for
        if "entry requirement" in user_question or "eligibilty" in user_question or "apply" in user_question:
            topic = "entry_requirements"
        elif "overview" in user_question or "details" in user_question:
            topic = "overview"
        elif "fees" in user_question or "fee" in user_question:
            topic = "fees"
        elif "teaching" in user_question or "research" in user_question:
            topic = "teaching_and_research"
        elif "careers" in user_question:
            topic = "careers"
        else:
            topic = None

        # Initialize the default answer
        answer = "Sorry, I couldn't find the information you're looking for."

        # Search for the relevant course and topic
        for item in course_data:
            if isinstance(item, dict):  # Ensure item is a dictionary
                course = item.get("course", "").lower()
                if course in user_question:
                    if topic:
                        description = item.get(topic, {}).get('description', 'No description available')
                        link = item.get(topic, {}).get('link', 'No link available')
                        # Using HTML for clickable link
                        answer = f"{description}<br>For more details, visit: <a href='{link}' target='_blank'>Click here</a>"

                    else:
                        answer = f"I found information about {course}, but I couldn't identify what you're asking for."
            else:
                dispatcher.utter_message(text=f"Unexpected data format: {item}")
                return []

        # Send the answer back to the user
        dispatcher.utter_message(text=f"Here's what I found: {answer}", parse_mode='html')

        return []
