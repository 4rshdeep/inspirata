import facebook
import os

app_id = os.environ['APP_ID']
app_secret = os.environ['APP_SECRET']

graph = facebook.GraphAPI(access_token='EAACEdEose0cBADJY4EEZCKw86CA5LFt5NXelh7weB0F6EHKVodV6Jb2Vt6nmtuqZB2ZCwCuf486Gsfw0rcJruSLZARlaJlH7I52mIYanPJPgyiFZBt9acFr9AQCdktKt99R52inH9cG1sMyZA5MvuOZAcxwfUF1P3Q0VUiBvmhzeJlIrFNsEV9BuMsGfHE1wBvUy2SkYZBiBOgZDZD', version="2.10")
# get_app_access_token(app_id, app_secret)

users = graph.search(type='user', q='4rshdeep')

for user in users['data']:
    print('%s %s' % (user['id'],user['name'].encode()))
