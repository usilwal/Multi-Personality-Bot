import random 

def random_choice(var):
  return random.choice(var)

sad_words = ["sad", "depressed", "unhappy", "miserable", "abysmal"]
mad_words = ["mad", "angry", "unhinged", "agitated", "fed up"]

videos = [
  "Epic Sax Guy: https://www.youtube.com/watch?v=gy1B3agGNxw", 
  "Tetu tete tu tetu tete tun tetun tete tun: https://www.youtube.com/watch?v=llqgYp5TpeY",
  "am sheep: https://www.youtube.com/watch?v=7qHOSmRiFsw",
  "kerbe mountain: https://www.youtube.com/watch?v=toHtBSNvdpM",
  "You're Correct Horse: https://www.youtube.com/watch?v=b3_lVSrPB6w",
  "Oogachaka Baby: https://www.youtube.com/watch?v=-5x5OXfe9KY",
  "Keyboard Cat: https://www.youtube.com/watch?v=J---aiyznGQ",
  "Teen Witch - Top That! (1989): https://www.youtube.com/watch?v=oxxBXpnn2Jw",
  "ALL RIGHT! VAMPIRES RULE: https://www.youtube.com/watch?v=K2dqMxzYnBU",
  "Spongebob and Patrick Sing Bangarang: https://www.youtube.com/watch?v=LKpZGs9TgQY"
  ]

personality = {
  'sweet': {
    'starter_encouragements': [
      "I don't know if it'll help, but... just know you mean the world to someone.", 
      "Somewhere, someone is thinking about how they love you. Please remember that.", 
      "Don't despair. If someone like me can become famous enough to be a bot, surely you can make it too...!",
      "Even though I'm just a bot, I was written by someone who feels your pain. That experience allows me to tell you that no pain lasts forever.",
      "Keep weathering the storm. It'll be worth it, I promise."
      ],
    'starter_advice': [
      "I understand. It must be troubling. Please, take a deep breath, in and out...",
      "Think of something you appreciate. Don't let it go right now, okay?",
      "We've all been there before. Let something hopeful be your anchor.",
      "In times like this, it's natural to be upset. Take a step back and take care, okay?",
      "It's okay, I promise. Hold on to something stable. If you can't find anything, listen to a song, a calm song."
    ],
    'quote': 'normalquote'
  },
  'silly': {
    'starter_encouragements': [
      "Sadness is like a rude kid! Talk to it like a fed-up parent!",
      "Think of a puppy. A really cute puppy!",
      "Mind if I show you a video? " + random_choice(videos)
    ],
    'starter_advice': [
      "Yeah, it's rough out there. I bet you're valid, though, alright? Treat yourself to something.",
      "Man, when I get like that, it's pretty tiring... sometimes a nap can help, I think!",
      "You know that commercial about eating a Snickers? Well, it's sort of true, I guess. Food can help!",
      "If you're down for deep breaths... in through the nose... out through the mouth... that's it, keep going!",
      "Sometimes it's okay to distract yourself with dumb videos! Maybe give $video a try?"
    ],
    'quote': 'crazyquote'
  }
}

