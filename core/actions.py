import os
import datetime
import subprocess
import webbrowser
import urllib.parse
import pyautogui
import requests

class JarvisActions:
    def __init__(self):
        """Initializes the unified execution engine for local actions and utilities."""
        # Setup for screenshot directory
        self.screenshot_dir = os.path.join(os.path.expanduser("~"), "Pictures", "Jarvis_Screenshots")
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)
            
        # Free weather API endpoint
        self.weather_api_url = "https://wttr.in/{}?format=j1"

    # =====================================================================
    # NAVIGATION ACTIONS 
    # =====================================================================
    def get_time(self):
        """Fetches the current system time."""
        now = datetime.datetime.now()
        return f"The current time is {now.strftime('%I:%M %p')}."

    def open_website(self, spoken_text):
        """Dynamically opens websites or searches Google based on spoken text."""
        target = spoken_text.lower().replace("open", "").strip()
        
        if "dot" in target:
            url = f"https://www.{target.replace(' dot ', '.')}"
            webbrowser.open(url)
            return f"Opening {url}, Sir."
        elif " " not in target:
            url = f"https://www.{target}.com"
            webbrowser.open(url)
            return f"Opening {target.capitalize()}, Sir."
        else:
            safe_query = urllib.parse.quote(target)
            search_url = f"https://www.google.com/search?q={safe_query}"
            webbrowser.open(search_url)
            return f"Searching the web for {target}."

    def open_calculator(self):
        """Opens the system calculator."""
        try:
            subprocess.Popen('calc') 
            return "Opening the calculator, Sir."
        except Exception:
            return "I was unable to open the calculator."

    # =====================================================================
    # UTILITY ACTIONS 
    # =====================================================================
    def get_weather(self, spoken_text):
        """Dynamically extracts the city from speech and fetches weather data."""
        # 1. Set your fallback default city (for when you just say "what's the weather?")
        target_city = "Chandigarh" 
        
        # 2. Clean the input string
        command = spoken_text.lower().strip()
        
        # 3. Dynamic Extraction Logic
        # We split the sentence at prepositions and grab whatever comes after them
        if " in " in command:
            target_city = command.split(" in ")[-1].strip()
        elif " for " in command:
            target_city = command.split(" for ")[-1].strip()
        elif " of " in command:
            target_city = command.split(" of ")[-1].strip()
            
        # Clean up any trailing punctuation the speech-to-text might have added
        target_city = target_city.replace("?", "").replace(".", "")

        try:
            # 4. Inject the dynamically extracted city into the API URL
            response = requests.get(self.weather_api_url.format(target_city)).json()
            
            current_temp = response['current_condition']['temp_C']
            feels_like = response['current_condition']['FeelsLikeC']
            description = response['current_condition']['weatherDesc']['value']
            
            # Format the output so Jarvis pronounces the target city
            return (f"The current temperature in {target_city.capitalize()} is {current_temp} degrees Celsius. "
                    f"It feels like {feels_like} degrees, and the sky shows {description.lower()}.")
        except Exception:
            return f"I am currently unable to fetch the weather data for {target_city.capitalize()}, Sir."
        
    def take_screenshot(self):
        """Captures the current screen and saves it to the Pictures folder."""
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"screenshot_{timestamp}.png"
            filepath = os.path.join(self.screenshot_dir, filename)
            
            screenshot = pyautogui.screenshot()
            screenshot.save(filepath)
            return f"Screenshot successfully saved as {filename}."
        except Exception as e:
            return f"Failed to capture the screen. Error: {str(e)}"