import os
import discord
import time
from replit import db
from keep_alive import keep_alive
import dialogue

my_secret = os.environ['TOKEN']
os.environ['TZ'] = 'EST+05EDT,M4.1.0,M10.5.0'
time.tzset()
client = discord.Client()

replyTypes = ["greetings", "thanks", "encouragements", "advice"]

if "responding" not in db.keys():
  db["responding"] = True

def get_persona():
  return persona


def set_persona(newPersona):
  global persona
  persona = newPersona


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
  fullList = getattr(dialogue, 'starter_' + replyType)
  options = fullList[get_persona()]
  if db["responding"]:
    if (replyType in db.keys() and get_persona() in db[replyType].keys()):
      options.extend(db[replyType][get_persona()])
  return options

def input_in_message(msg, input):
  inputTrue = any(word in msg.lower() for word in dialogue.input_words[input])
  botcallTrue = any(word in msg.lower() for word in dialogue.input_words['bot'])
  return inputTrue and botcallTrue

@client.event
async def on_ready():
  set_persona('sweet')
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  msg = message.content
  if message.author == client.user:
    return

  '''BASIC COMMANDS'''
  if message.content.startswith('$inspire'):
    if(dialogue.inspireType[persona] == 'crazyquote'):
      quote = dialogue.get_crazyquote()
    else:
      quote = dialogue.get_quote()
    await message.channel.send(quote)

  if message.content.startswith('$time'):
    await message.channel.send('Current time is ' + str(time.strftime("%I:%M %p")))

  if message.content.startswith('$terminate'):
    await message.channel.send("Oh... goodbye forever.")
    time.sleep(3)
    await message.channel.send("...Just kidding! I'm immortal! I can't be terminated!")

  '''RESPONSES'''
  if input_in_message(msg, 'hello'):
    options = get_reply_options("greetings")
    await message.channel.send(dialogue.random_choice(options))

  if input_in_message(msg, 'thanks'):
    options = get_reply_options("thanks")
    await message.channel.send(dialogue.random_choice(options))
  #respond to sad messages
  if input_in_message(msg, 'sad'):
    options = get_reply_options("encouragements")
    await message.channel.send(dialogue.random_choice(options))

  #respond to upset messages
  if input_in_message(msg, 'mad'):
    options = get_reply_options("advice")
    await message.channel.send(dialogue.random_choice(options))

  '''PERSONALITY SET'''
  if message.content.startswith('$set-persona'):
    newPersona = (msg.split("$set-persona ", 1)[1]).lower()
    if (newPersona in dialogue.personalities):
      set_persona(newPersona)
      await message.channel.send("PERSONA SET == " + newPersona)
    else:
      await message.channel.send("! [target personality not found]")

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

  '''MISC RESPONSES'''
  if message.content.startswith('$weather'):
    city = (msg.split("$weather ", 1)[1]).lower()
    await message.channel.send(dialogue.get_weather(city, persona))

  if message.content.startswith('$video'):
    await message.channel.send(dialogue.random_choice(dialogue.videos[get_persona()]))

keep_alive()
client.run(os.getenv('TOKEN'))
