import requests, urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from key import ACCESS_TOKEN

BASE_URL = 'https://api.instagram.com/v1/'

comment=""
maximum_likes = -1
maximum_likes_id = ""
minimum_likes = 10000000
minimum_likes_id = ""
'''
Function declaration to get your own info
'''

def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!'


'''
Function declaration to get the ID of a user by username
'''

def get_user_id(insta_username):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit()


'''
Function declaration to get the info of a user by username
'''

def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'


'''
Function declaration to get your recent post
'''

def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded! with post id - '+ own_media['data'][0]['id']
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'


'''
Function declaration to get the recent post of a user by username
'''

def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded! with post id - '+ user_media['data'][0]['id']
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'


'''
Function declaration to get the ID of the recent post of a user by username
'''

def get_post_id(insta_username,code):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()
    i=0
    j=0
    if user_media['meta']['code'] == 200:
        if code == 2:
            global maximum_likes_id
            global minimum_likes_id
            global maximum_likes
            global minimum_likes
            while len(user_media['data']) > i and i < 10:
                if user_media['data'][i]['likes']['count'] >maximum_likes:
                    maximum_likes = user_media['data'][i]['likes']['count']
                    maximum_likes_id = user_media['data'][i]['id']
                if user_media['data'][i]['likes']['count'] < minimum_likes:
                    minimum_likes = user_media['data'][i]['likes']['count']
                    minimum_likes_id = user_media['data'][i]['id']
                i += 1
        elif code ==0:
          if len(user_media['data']):
            return user_media['data'][0]['id']
          else:
            print 'Status code other than 200 received!'
            exit()


'''
Function declaration to like the recent post of a user
'''

def like_a_post(insta_username,code):
   if code == 0:
    media_id = get_post_id(insta_username,0)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
   elif code == 1:
    request_url = (BASE_URL + 'media/%s/likes') % (insta_username)

   payload = {"access_token": ACCESS_TOKEN}
   print 'POST request url : %s' % (request_url)
   post_a_like = requests.post(request_url, payload).json()
   if post_a_like['meta']['code'] == 200:
     print 'Like was successful!'
   else:
     print 'Your like was unsuccessful. Try again!'


'''
Function declaration to make a comment on the recent post of the user
'''

def post_a_comment(insta_username,code):
  if code ==0:
    media_id = get_post_id(insta_username,0)
    comment_text = raw_input("Your comment: ")
    payload = {"access_token": ACCESS_TOKEN, "text": comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)
  elif code ==1:
      payload = {"access_token": ACCESS_TOKEN, "text": comment}
      request_url = (BASE_URL + 'media/%s/comments') % (insta_username)

  make_comment = requests.post(request_url, payload).json()

  if make_comment['meta']['code'] == 200:
    print "Successfully added a new comment!"
  else:
    print "Unable to add comment. Try again!"

def target_comment():
    tag = raw_input("tag you want to search for")
    request_url = (BASE_URL + 'tags/%s/media/recent?access_token=%s') % (tag, ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()
    if len(user_media['data'])>0:
        global comment
        comment =raw_input("comment you want to put")
        i=0
        while len(user_media['data'])>i:
            post_a_comment(user_media['data'][i]['id'],1)
            i=i+1
        start_bot()
    else:
        print 'Tag not found!'
        start_bot()
'''
Function declaration to get the list of user's who liked your post
'''

def get_like_list(insta_username):
    media_id = get_post_id(insta_username,0)
    request_url = (BASE_URL + 'media/%s/likes?access_token=%s') % (media_id, ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    likes = requests.get(request_url).json()
    if likes['meta']['code'] == 200:
        if len(likes['data']):
            print "\npeople who liked your post : - "
            for x in range(0, len(likes['data'])):
                print likes['data'][x]['username'] + '\n'
        else:
            print 'post has no comments\n'


'''
Function declaration to get the list of comments on user's recent post
'''

def get_comment_list(insta_username):
    media_id = get_post_id(insta_username,0)
    request_url = (BASE_URL + 'media/%s/comments?access_token=%s') % (media_id, ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comments = requests.get(request_url).json()
    if comments['meta']['code'] == 200:
        if len(comments['data']):
            for x in range(0, len(comments['data'])):
               print '\n'+comments['data'][x]['from']['username']+ " -: "+ comments['data'][x]['text']
        else:
            print 'post has no comments\n'



'''
Function declaration to make delete negative comments from the recent post
'''

def delete_negative_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            # Here's a naive implementation of how to delete the negative comments :)
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (
                    media_id, comment_id, ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print 'Positive comment : %s\n' % (comment_text)
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'


'''function to show own action menu'''
def own_action(user_name):
    while True:
        print '\n'
        print "a.Get your details"
        print "b.Get your recent post"
        print "c.Get a list of people who have liked your recent post"
        print "d.Like your post"
        print "e.Get a list of comments on your recent post"
        print "f.Make a comment on your recent post of"
        print "g.Delete negative comments from your recent post"
        print "h.Go to main menu"

        choice = raw_input("Enter you choice: ")
        if choice == "a":
            self_info()
        elif choice == "b":
            get_own_post()
        elif choice == "c":
            get_like_list(user_name)
        elif choice == "d":
          while True:
            print "\n1. Like your recent post"
            print "2. Like your post which has minimum likes"
            print "3. Like your post which has maximum likes"
            print "4. Go to previous menu"
            choice = raw_input("\nEnter your choice : ")
            if choice == "1":
                like_a_post(user_name,0)
            elif choice == "2":
                get_post_id(user_name,2)
                print "Minimum like %d" % minimum_likes
                like_a_post(minimum_likes_id,1)
            elif choice == "3":
                get_post_id(user_name, 2)
                print "Maximum like %d" % maximum_likes
                like_a_post(maximum_likes_id,1)
            elif choice == "4":
                own_action(user_name)
            else:
                print "Wrong choice"
        elif choice == "e":
            get_comment_list(user_name)
        elif choice == "f":
            post_a_comment(user_name,0)
        elif choice == "g":
            delete_negative_comment(user_name)
        elif choice == "h":
            start_bot()
        else:
            print "wrong choice"


'''Function to show action on other menu'''

def action_on_other(user_name):
    user_id = get_user_id(user_name)
    if user_id == None:
        print 'User does not exist!'
        start_bot()
    else:
     while True:
        print '\n'
        print "a.Get %s's details" % user_name
        print "b.Get %s's recent post" % user_name
        print "c.Get a list of people who have liked %s's recent post" % user_name
        print "d.Like %s's post" % user_name
        print "e.Get a list of comments on %s's recent post" % user_name
        print "f.Make a comment on %s's recent post of" % user_name
        print "g.Delete negative comments from %s's recent post" % user_name
        print "h.Go to main menu"

        choice = raw_input("Enter you choice: ")
        if choice == "a":
            get_user_info(user_name)
        elif choice == "b":
            get_user_post(user_name)
        elif choice == "c":
            get_like_list(user_name)
        elif choice == "d":
            while True:
                print "\n1. Like %s's recent post"
                print "2. Like %s's post which has minimum likes"
                print "3. Like %s's post which has maximum likes"
                print "4. Go to previous menu"
                choice = raw_input("\nEnter your choice : ")
                if choice == "1":
                    like_a_post(user_name,0)
                elif choice == "2":
                    get_post_id(user_name,2)
                    print "Minimum like %d" % minimum_likes
                    like_a_post(minimum_likes_id,1)
                elif choice == "3":
                    get_post_id(user_name,2)
                    print "Maximum like %d" % maximum_likes
                    like_a_post(maximum_likes_id, 1)
                elif choice == "4":
                    action_on_other(user_name)
                else:
                    print "Wrong choice"
        elif choice == "e":
            get_comment_list(user_name)
        elif choice == "f":
            post_a_comment(user_name,0)
        elif choice == "g":
            delete_negative_comment(user_name)
        elif choice == "h":
            start_bot()
        else:
            print "wrong choice"


'''function to show main menu'''

def start_bot():
    while True:
        print '\n'
        print 'Hey! Welcome to instaBot!'
        print 'Here are your menu options:'
        print "a.Perform actions on own\n"
        print "b.Perform actions on other user\n"
        print "c.Perform target commenting\n"
        print "d.Exit"

        choice = raw_input("Enter you choice: ")
        if choice == "a":
            user_name = raw_input("Enter your user name : ")
            own_action(user_name)
        elif choice == "b":
            user_name = raw_input("Enter the user name of the user : ")
            action_on_other(user_name)
        elif choice == "c":
            target_comment()
        elif choice == "d":
            exit()
        else:
            print "wrong choice"


start_bot()
