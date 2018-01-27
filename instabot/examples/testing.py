import argparse
import os
import sys
from tqdm import tqdm

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot
import delay

bot = Bot()
bot.login(username='_inspirata', password='inspirata001')

# def downloadPhoto(self, media_id, filename, media=False, path='photos/'):
#     if not media:
#         self.mediaInfo(media_id)
#         media = self.LastJson['items'][0]
#     filename = '{0}_{1}.jpg'.format(media['user']['username'], media_id) if not filename else '{0}.jpg'.format(filename)
#     images = media['image_versions2']['candidates']
#     if os.path.exists(path + filename):
#         return os.path.abspath(path + filename)
#     response = self.session.get(images[0]['url'], stream=True)
#     if response.status_code == 200:
#         with open(path + filename, 'wb') as f:
#             response.raw.decode_content = True
#             shutil.copyfileobj(response.raw, f)
#     return os.path.abspath(path + filename)


# def download_photos(self, medias, path='photos/', description=False):
#     broken_items = []
#     if not medias:
#         self.logger.info("Nothing to downloads.")
#         return broken_items
#     self.logger.info("Going to download %d medias." % (len(medias)))
#     for media in tqdm(medias):
#         if not download_photo(media, path, description=description):
#             delay.error_delay(self)
#             broken_items = medias[medias.index(media):]
#             break
#     return broken_items

# def download_photo(self, media_id, path='photos/', filename=None, description=False):
#     delay.small_delay(self)
#     if not os.path.exists(path):
#         os.makedirs(path)
#     if description:
#         media = self.get_media_info(media_id)[0]
#         caption = media['caption']['text']
#         with open('{path}{0}_{1}.txt'.format(media['user']['username'], media_id, path=path), encoding='utf8', mode='w') as file_descriptor:
#             file_descriptor.write(caption)
#     photo = super(self.__class__, self).downloadPhoto(media_id, filename, False, path)
#     if photo:
#         return photo
#     self.logger.info("Media with %s is not %s ." % (media_id, 'downloaded'))
#     return False


hashtags = ['sad']
for hashtag in hashtags:
    medias = bot.get_hashtag_medias(hashtag)
    bot.download_photos(medias)
