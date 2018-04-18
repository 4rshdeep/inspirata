import argparse
import os
import sys
from tqdm import tqdm

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot
import delay

bot = Bot(max_comments_per_day=10000)
bot.login(username='_inspirata', password='inspirata001')

hashtags = ['sad', 'depressed', 'suicide', 'suicidal']
for hashtag in hashtags:
    medias = bot.get_hashtag_medias(hashtag)
    bot.download_photos(medias)
