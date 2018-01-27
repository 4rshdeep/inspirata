import os
from tqdm import tqdm
from sentiment_analysis import get_sentiment, get_sentiment_val
from emotion_analysis import get_image_sentiment 
from . import delay
import markovify
import json
import re

class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        words = [ "::".join(tag) for tag in nltk.pos_tag(words) ]
        return words

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence


def upload_photo(self, photo, caption=None, upload_id=None):
    delay.small_delay(self)
    if super(self.__class__, self).uploadPhoto(photo, caption, upload_id):
        self.logger.info("Photo '%s' is %s ." % (photo, 'uploaded'))
        return True
    self.logger.info("Photo '%s' is not %s ." % (photo, 'uploaded'))
    return False


def download_photo(self, media_id, path='photos/', filename=None, description=True):
    delay.small_delay(self)
    if not os.path.exists(path):
        os.makedirs(path)
    # print(description)
    media = self.get_media_info(media_id)[0]
    caption = media['caption']['text']
        
    if caption:
        print(caption)
        caption_sentiment = get_sentiment(caption)
        print()
        print("caption_sentiment::", end="")
        print(caption_sentiment)
        if caption_sentiment < 0.3:
            model_json = json.load(open('../../examples/model.json', 'r'))
            reconstituted_model = POSifiedText.from_json(model_json)
            print("caption::"+caption)
            print("response::"+reconstituted_model.make_short_sentence(140))
        elif caption_sentiment < 0.5:
            photo = super(self.__class__, self).downloadPhoto(media_id, filename, False, path)
            if photo:
                sad_sentiment, max_key = get_image_sentiment(photo)
                if sad_sentiment == None:
                    return True
                return photo
            happy_array = ['happiness', 'surprise']
            if (max_key not in happy_array) and sad_sentiment > 0.5:
                print("caption::"+caption)
                print("response::"+reconstituted_model.make_short_sentence(140))
        else:
            return True ##
    else:
        media = self.get_media_info(media_id)[0]
        caption = media['caption']['text']
        print(caption)
        

    
    self.logger.info("Media with %s is not %s ." % (media_id, 'downloaded'))
    return False


def download_photos(self, medias, path, description=True):
    broken_items = []
    if not medias:
        self.logger.info("Nothing to downloads.")
        return broken_items
    self.logger.info("Going to download %d medias." % (len(medias)))
    for media in tqdm(medias):
        print(media)
        print(get_instagram_url_from_media_id(media))

        ######## TODO COMMENT
        # self.comment(media, "inspirata")
        if not self.download_photo(media, path, description=description):
            delay.error_delay(self)
            broken_items = medias[medias.index(media):]
            break
    return broken_items

def get_instagram_url_from_media_id(media_id, url_flag=True, only_code=None):
    media_id = int(media_id)
    if url_flag is False: return ""
    else:
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'
        shortened_id = ''
        while media_id > 0:
            media_id, idx = divmod(media_id, 64)
            shortened_id = alphabet[idx] + shortened_id
        if only_code: return shortened_id
        else: return 'instagram.com/p/' + shortened_id + '/'
