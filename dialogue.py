import random 
import requests
import os
import json

WEATHER_API = os.environ['WEATHER_API']

personalities = ['sweet', 'silly']

input_words = {
  'hello': ["hi", "hello", "hey", "ay", "ola", "yo", "excuse me"],
  'sad': ["sad", "depressed", "unhappy", "miserable", "abysmal"],
  'mad': ["mad", "angry", "unhinged", "agitated", "fed up"],
  'bot': ["multipersona", "multi-personality", "bot"]
}

videos = {
  'sweet': [
    "Dream - Motivational Video: https://www.youtube.com/watch?v=g-jwWYX7Jlo",
    "NEVER GIVE UP!!: https://www.youtube.com/watch?v=KxGRhd_iWuE",
    "Grit: the power of passion and perseverance: https://www.youtube.com/watch?v=H14bBuluwB8",
    "Mr Rogers' Advice: https://www.youtube.com/watch?v=J9O48kKG4MI",
    "Collection Of Inspirational & Moving Film Scenes: https://www.youtube.com/watch?v=vdRNQLi5Mqw",
    "Cat politely declines being removed from blanket pile: https://www.youtube.com/watch?v=Oyx3xkdi4uw",
    "Dog and Capybara: https://www.youtube.com/watch?v=SCwcJsBYL3o",
    "Keyboard Cat: https://www.youtube.com/watch?v=J---aiyznGQ",
    "A Trip Through New York City in 1911: https://www.youtube.com/watch?v=hZ1OgQL9_Cw"
  ],
  'silly': [
  "Epic Sax Guy: https://www.youtube.com/watch?v=gy1B3agGNxw", 
  "Tetu tete tu tetu tete tun tetun tete tun: https://www.youtube.com/watch?v=llqgYp5TpeY",
  "am sheep: https://www.youtube.com/watch?v=7qHOSmRiFsw",
  "kerbe mountain: https://www.youtube.com/watch?v=toHtBSNvdpM",
  "You're Correct Horse: https://www.youtube.com/watch?v=b3_lVSrPB6w",
  "Oogachaka Baby: https://www.youtube.com/watch?v=-5x5OXfe9KY",
  "Teen Witch - Top That! (1989): https://www.youtube.com/watch?v=oxxBXpnn2Jw",
  "ALL RIGHT! VAMPIRES RULE: https://www.youtube.com/watch?v=K2dqMxzYnBU",
  "Spongebob and Patrick Sing Bangarang: https://www.youtube.com/watch?v=LKpZGs9TgQY"
  ]
}

starter_encouragements = {
  'sweet': [
      "I don't know if it'll help, but... just know you mean the world to someone.", 
      "Somewhere, someone is thinking about how they love you. Please remember that.", 
      "Don't despair. If someone like me can become famous enough to be a bot, surely you can make it too...!",
      "Even though I'm just a bot, I was written by someone who feels your pain. That experience allows me to tell you that no pain lasts forever.",
      "Keep weathering the storm. It'll be worth it, I promise."
      ],
  'silly': [
      "Sadness is like a rude kid! Talk to it like a fed-up parent!",
      "Think of a puppy. A really cute puppy!",
      "Want to see a $video?",
      "Don't despair! You're almost there!"
    ],
}

starter_advice = {
  'sweet': [
      "I understand. It must be troubling. Please, take a deep breath, in and out...",
      "Think of something you appreciate. Don't let it go right now, okay?",
      "We've all been there before. Let something hopeful be your anchor.",
      "In times like this, it's natural to be upset. Take a step back and take care, okay?",
      "It's okay, I promise. Hold on to something stable. If you can't find anything, listen to a song, a calm song."
    ],
  'silly': [
      "Yeah, it's rough out there. Nothing to do but try to bring the tension down, eh? Treat yourself to something.",
      "Man, when I get like that, it's pretty tiring... sometimes a nap can help, I think!",
      "You know that commercial about eating a Snickers? Well, it's sort of true, I guess. Food can help!",
      "If you're down for deep breaths... in through the nose... out through the mouth... that's it, keep going!",
      "Sometimes it's okay to distract yourself with dumb videos! Maybe give $video a try?"
    ],
}

hello = {
  'sweet': [
      "Good day!",
      "Hello! It's always a good time to calm our nerves.",
      "Hello to you too!",
      "Hello, hello!"
    ],
    'silly': [
      "Hey hey hey!",
      "Good day, good day, good day, I'm glad you came my way!",
      "Good morning, day, afternoon, evening or night!",
      "What's up, doc?"
    ],
}

inspireType = {
  'sweet': 'normalquote',
  'silly': 'crazyquote'
}

def random_choice(var):
  return random.choice(var)

def get_quote():
  #zenquotes api returns inspiring quote
  response = requests.get("https://zenquotes.io/api/random")
  data = json.loads(response.text)
  quote = data[0]['q'] + " -" + data[0]['a']
  return quote


def get_crazyquote():
  #inspirobot api returns nonsense quote
  response = requests.get("https://inspirobot.me/api?generate=true")
  quote = response.text
  return quote


def kelvinToCelsius(temp):
  return round(temp - 273.15, 2)

def get_weather(city, persona):
  base_url = "http://api.openweathermap.org/data/2.5/weather?appid=" + \
      WEATHER_API + "&q=" + city
  response = requests.get(base_url)
  data = json.loads(response.text)
  country = data["sys"]["country"].lower()
  message = (f'__Here\'s the current weather in **{data["name"]}**__ :flag_{country}:\n'
             f'*Coordinates at ({data["coord"]["lon"]},{data["coord"]["lat"]})*\n'
             f'**Temperature:** {kelvinToCelsius(data["main"]["temp"])}° C\n'
             f'**Feels like:** {kelvinToCelsius(data["main"]["feels_like"])}° C\n'
             f'**Status:** {data["weather"][0]["description"]}\n')
  return message


