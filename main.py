import os
import discord
import requests
import json
import random
import time
from replit import db
from keep_alive import keep_alive
import dialogue

my_secret = os.environ['TOKEN']
WEATHER_API = os.environ['WEATHER_API']
os.environ['TZ'] = 'EST+05EDT,M4.1.0,M10.5.0'
time.tzset()
client = discord.Client()

replyTypes = ["encouragements", "advice"]

if "responding" not in db.keys():
  db["responding"] = True


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


def get_weather(city):
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


def get_behavior():
  return behavior


def get_persona():
  return persona


def set_persona(newPersona):
  global persona
  persona = newPersona
  global behavior
  behavior = dialogue.personality[newPersona]


def update_replies(reply, replyType):
  '''Create or add to a dictionary where each key will be a type of reply (e.g. encouragement, advice).
  The values of each key contain a dict; the reply is added to an array for an inner key, the current personality.
  Each array therefore stores replies specific to both the type of reply and the personality.'''
  if replyType in db.keys() and get_persona() in db[replyType].keys():
    resList = db[replyType][get_persona()]
    resList.append(reply)
    db[replyType][get_persona()] = resList
  elif replyType in db.keys():
    db[replyType][get_persona()] = [reply]
  else:
    db[replyType] = {get_persona(): [reply]}


def delete_reply(index, replyType):
  resList = db[replyType][get_persona()]
  if len(resList) > index:
    del resList[index]
  db[replyType][get_persona()] = resList


def get_reply_options(replyType):
  behavior = get_behavior()
  options = behavior['starter_' + replyType]
  if db["responding"]:
    if replyType in db.keys():
      options.extend(db[replyType][get_persona()])
  return options


@client.event
async def on_ready():
  set_persona('sweet')
  print('We have logged in as {0.user}'.format(client))
  global behavior
  behavior = dialogue.personality[get_persona()]


@client.event
async def on_message(message):
  msg = message.content
  if message.author == client.user:
    return

  '''BASIC COMMANDS'''
  if message.content.startswith('$hello'):
    await message.channel.send("Good day, good day, good day, I'm glad you came my way!")

  if message.content.startswith('$inspire'):
    if(behavior['quote'] == 'crazyquote'):
      quote = get_crazyquote()
    else:
      quote = get_quote()
    await message.channel.send(quote)

  if message.content.startswith('$weather'):
    city = (msg.split("$weather ", 1)[1]).lower()
    await message.channel.send(get_weather(city))

  if message.content.startswith('$video'):
    await message.channel.send(dialogue.random_choice(dialogue.videos))

  if message.content.startswith('$time'):
    await message.channel.send('Current time is ' + str(time.strftime("%I:%M %p")))

  if message.content.startswith('$terminate'):
    await message.channel.send("Oh... goodbye forever.")
    time.sleep(3)
    await message.channel.send("...Just kidding! I'm immortal! I can't be terminated!")

  '''RESPONSES'''
  #respond to sad messages
  if any(word in msg for word in dialogue.sad_words):
    options = get_reply_options("encouragements")
    await message.channel.send(random.choice(options))

  #respond to upset messages
  if any(word in msg for word in dialogue.mad_words):
    options = get_reply_options("advice")
    await message.channel.send(random.choice(options))

  '''PERSONALITY SET'''
  if message.content.startswith('$set-persona'):
    newPersona = (msg.split("$set-persona ", 1)[1]).lower()
    if (newPersona in dialogue.personality.keys()):
      set_persona(newPersona)
      await message.channel.send("PERSONA SET == " + newPersona)
    else:
      await message.channel.send("Seems like I don't have that personality yet.")

  '''REPLY DB COMMANDS'''
  if msg.startswith("$add"):
    msgArr = msg.split(" ", 2)
    replyType = msgArr[1]
    reply = msgArr[2]
    if replyType in replyTypes:
      update_replies(reply, replyType)
      await message.channel.send("Thank you. I'll add that to my database.")
    else:
      await message.channel.send("Sorry, I don't think I get it.")

  if msg.startswith("$remove"):
    msgArr = msg.split(" ", 2)
    replyType = msgArr[1]
    index = int(msgArr[2])
    if replyType in db.keys():
      delete_reply(index, replyType)
      replyArr = []
      replyArr = db[replyType][get_persona()]
      await message.channel.send("Alright. Here's the new list of encouragements for this type.")
      await message.channel.send(replyArr)
    else:
      await message.channel.send("Sorry, I can't find what you want me to remove.")

  if msg.startswith("$list"):
    msgArr = msg.split(" ", 1)
    replyType = msgArr[1]
    replyArr = []
    if replyType in db.keys():
      replyArr = db[replyType]
      await message.channel.send(replyArr)
    else:
      await message.channel.send("Sorry, I can't find that in the database.")

  '''TOGGLE RESPONSES'''
  if msg.startswith("$responding"):
    if db["responding"] == True:
      db["responding"] = False
      await message.channel.send("Good night. Zzzzz...")
    else:
      db["responding"] = True
      await message.channel.send("Oh! Good morning! I think...")

keep_alive()
client.run(os.getenv('TOKEN'))
