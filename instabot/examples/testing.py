import argparse
import os
import sys
from tqdm import tqdm

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot
import delay

bot = Bot()
bot.login(username='_inspirata', password='inspirata001')

hashtags = ['sad']
for hashtag in hashtags:
    medias = bot.get_hashtag_medias(hashtag)
    bot.download_photos(medias)
