import datetime
import random
import webbrowser
import pyttsx3
import requests
from bs4 import BeautifulSoup
import os
import pywhatkit
import speech_recognition as sr
import wikipedia

# create instance of Recognizer class
r = sr.Recognizer()

# initialize our virtual assistant
assistant = pyttsx3.init()

assistant.say("Welcome back.")
assistant.runAndWait()

def get_audio():
    # use default microphone as the source
    with sr.Microphone() as source:
        print("Speak now...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        # use Google Speech Recognition to convert audio to text
        print("Recognizing...")
        text = r.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I didn't understand.")
    except sr.RequestError as e:
        print(f"Request error from Google Speech Recognition service: {e}")

def tell_joke():
    joke_url = "https://official-joke-api.appspot.com/random_joke"
    response = requests.get(joke_url)
    joke_data = response.json()
    setup = joke_data["setup"]
    punchline = joke_data["punchline"]
    print("Setup: " + setup)
    print("Punchline: " + punchline)
    assistant.say(setup)
    assistant.runAndWait()
    assistant.say(punchline)
    assistant.runAndWait()

#############


def get_recommendation():
    base_url = "https://api.tvmaze.com/search/shows?q=random"
    response = requests.get(base_url)
    data = response.json()
    recommendation = data[random.randint(0, len(data)-1)]
    name = recommendation["show"]["name"]
    summary = recommendation["show"]["summary"]
    print(f"I suggest {name}. Here's a brief summary: {summary}")
    assistant.say(f"I suggest {name}. Here's a brief summary: {summary}")
    assistant.runAndWait()



def process_input():
    print("I'm listening you. ")
    assistant.say("I'm listening you. ")
    assistant.runAndWait()
    user_input = get_audio()

    if not user_input:  # user_input None veya boş bir dize ise
        print("Sorry, recognition list is empty.")
        assistant.say("Sorry, recognition list is empty.")
        assistant.runAndWait()
        process_input()  # Ana fonksiyonu tekrar çağır
        return  # Çıkış yap, işlemi tekrarlamadan önce
    
    # if the user wants to quit, break the loop
    if user_input and user_input.lower() in ["goodbye", "quit", "exit", "see you", "bye"]:
        print("Goodbye. ")
        assistant.say("Goodbye. ")
        assistant.runAndWait()
        exit()

    # if the user asks "what time is it", tell them the time
    elif "what time is it" in user_input.lower() and user_input:
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(f"The current time is {current_time}")
        assistant.say(f"The current time is {current_time}")
        assistant.runAndWait()

    # if the user wants to open an application, open it
    elif "open" in user_input.lower():
        app = ' '.join(user_input.split()[1:])
        os.startfile(app)
        print(f"Opening {app}.")
        assistant.say(f"Opening {app}.")
        assistant.runAndWait()

    # if the user wants to search something on Google, do it
    elif "google" in user_input.lower():
        query = user_input.lower().replace("google", "").strip()
        print(f"Searching Google for {query}")
        assistant.say(f"Searching Google for {query}")
        assistant.runAndWait()
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)

#########


    # Call the tell_joke() function when the user says "joke"
    elif "joke" in user_input.lower():
        tell_joke()
    
    elif "suggest" in user_input.lower() and ("movie" in user_input.lower() or "show" in user_input.lower()):
        print("Sure, here's a random movie/TV show recommendation.")
        assistant.say("Sure, here's a random movie/TV show recommendation.")
        assistant.runAndWait()
        get_recommendation()

    elif "dice" in user_input.lower():
        rand_num = random.randint(1, 6)
        print(f"The randomly generated number is {rand_num}")
        assistant.say(f"The randomly generated number is {rand_num}")
        assistant.runAndWait()

    elif "wikipedia" in user_input.lower():
        search_term = user_input.lower().replace("wikipedia", "").strip()
        try:
            page = wikipedia.page(search_term)
            summary = wikipedia.summary(search_term)
            print("Summary: " + summary)
            assistant.say(summary)
            assistant.runAndWait()
        except wikipedia.DisambiguationError as e:
            options = ", ".join(e.options[:5])
            print(f"Multiple results were found for {search_term}. Here are the top 5: {options}")
            assistant.say(f"Multiple results were found for {search_term}. Here are the top 5: {options}")
            assistant.runAndWait()
        except wikipedia.PageError:
            print(f"No results were found for {search_term}.")
            assistant.say(f"No results were found for {search_term}.")
            assistant.runAndWait()



    # if the user wants to know the weather, get the current weather data
    elif "weather" in user_input.lower():
        assistant.say("Which city's weather do you want to know?")
        assistant.runAndWait()
        city_name = get_audio()
        weather_url = f"https://wttr.in/{city_name}?format=%C+%t"
        response = requests.get(weather_url)
        weather_data = response.text.strip()
        print(f"The current weather in {city_name} is {weather_data}")
        assistant.say(f"The current weather in {city_name} is {weather_data}")
        assistant.runAndWait()

    # if the user wants to know the news, get the latest news
    elif "news" in user_input.lower():
        news_url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=6aedad43c9fe4064a5a577d707d8f64d"
        response = requests.get(news_url)
        news_data = response.json()
        articles = news_data["articles"]
        for article in articles:
            title = article["title"]
            description = article["description"]
            print("Title: " + title)
            print("Description: " + description)
            assistant.say(title)
            assistant.runAndWait()
            assistant.say(description)
            assistant.runAndWait()

    # if the user wants to play a song on YouTube, do it
    elif "play" in user_input.lower() and "youtube" in user_input.lower():
        song = user_input.lower().replace("play", "").replace("youtube", "").strip()
        pywhatkit.playonyt(song)
        print(f"Playing {song} on YouTube.")
        assistant.say(f"Playing {song} on YouTube.")
        assistant.runAndWait()

    # if the user wants to know the meaning of a word, get the definition
    elif "meaning" in user_input.lower():
        word = user_input.split("meaning of ")[1].strip()
        definition_url = f"https://www.dictionary.com/browse/{word}"
        response = requests.get(definition_url)
        soup = BeautifulSoup(response.text, "html.parser")
        definition = soup.find(class_="e1wg9v5m0").text
        print(f"The meaning of {word} is: {definition}")
        assistant.say(f"The meaning of {word} is: {definition}")
        assistant.runAndWait()

    elif "thank" in user_input.lower():
        print("You're welcome! Do you need any help with something else?")
        assistant.say("You're welcome! Do you need any help with something else?")
        assistant.runAndWait()

    # if the user wants to calculate something, calculate it
    elif "calculate" in user_input.lower():
        if "calculate" not in user_input.lower():
            print("I'm sorry, I didn't catch the calculation you wanted to perform.")
            assistant.say("I'm sorry, I didn't catch the calculation you wanted to perform.")
        else:
            try:
                expression = user_input.split("calculate", 1)[1].strip()
                result = eval(expression)
                print(f"The result of {expression} is {result}")
                assistant.say(f"The result of {expression} is {result}")
            except:
                print("I'm sorry, I couldn't perform that calculation. Please try again with a valid expression.")
                assistant.say("I'm sorry, I couldn't perform that calculation. Please try again with a valid expression.")
        assistant.runAndWait()


    # if we can't understand the user, provide a random response
    else:
        responses = [
            "I'm sorry, I didn't understand that.",
            "Can you please repeat that?",
            "I didn't quite catch that.",
            "Please say that again"
        ]
        print(random.choice(responses))
        assistant.say(random.choice(responses))
        assistant.runAndWait()
# Start the assistant
while True:
    user_input = get_audio()
    process_input(user_input)
