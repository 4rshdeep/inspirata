import facebook
import os
import requests

app_id = "340963926402035"
app_secret = "b9c46f67e14f5d69c343e0df06bea0bd"

def get_fb_token(app_id, app_secret):           
    payload = {'grant_type': 'client_credentials', 'client_id': app_id, 'client_secret': app_secret}
    file = requests.post('https://graph.facebook.com/oauth/access_token?', params = payload)
    #print file.text #to test what the FB api responded with    
    result = file.json()['access_token']
    #print file.text #to test the TOKEN
    return result

graph = facebook.GraphAPI(access_token='EAACEdEose0cBAAUoPkaEZBZADr1W5xpcHoMioICVaVbkWZBYB9ciclWZAZBsyF0KEZBZAslc8EICxChAsUdoSBytirO3gTYfACEEI5qQCVx88QsT1fuHZBl9ZBkTZB3pxvZBCP0A88TWpz0NlDeS0zQ1oOs8Pw36LJcvB3kINwO90fdq8dETIPoE5cQZCOeg15Kgqzo0CvngqJXlLAZDZD', version="2.10")
# get_app_access_token(app_id, app_secret)

# users = graph.search(type='user', q='4rshdeep')

# for user in users['data']:
#     print('%s %s' % (user['id'],user['name'].encode()))




graph.put_comment(object_id='531752773523381_1767214209977225', message='Great post...')
