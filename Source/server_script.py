import os
import subprocess
import sys
import json
import random
from io import BytesIO

try:
    import pip
except ImportError:
    os.system('sudo apt install python3-venv python3-pip')

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import tweepy
except ImportError:
    install("tweepy")
    import tweepy

try:
    from stegano import lsb
except ImportError:
    install("Stegano")
    from stegano import lsb

try:
    import PIL
except ImportError:
    install("Pillow")
    import PIL

try:
    import requests
except ImportError:
    install("requests")
    import requests

try:
    import tweepy
except ImportError:
    install("tweepy")
    import tweepy


def getConfig():
    #TODO get information from configuration file
    pass

def updateConfig():
    #TODO update configuration file
    pass

#hide message into image
def stenographizeImage(ImagePath,NewImagePath,Text):
    secret_image = lsb.hide(ImagePath,message=Text)
    secret_image.save(NewImagePath)

#reveal hidden message from image
def deStenographizeImage(ImagePath):
    revealedMessage = lsb.reveal(ImagePath)
    #remove b'' strings from message
    revealedMessage = revealedMessage[2:len(revealedMessage)-1]
    return revealedMessage

def encrypt(password, logged_file, encrypted_file):
    enc_scheme = "-aes-128-cbc"
    opts = "-a -A -nosalt"
    openssl_cmd = 'openssl enc -pass pass:{} {} {} -in {} -out {} -nosalt 2> /dev/null '.format(password, enc_scheme, opts, logged_file, encrypted_file)

    try:
        os.system(openssl_cmd)
    except Exception as e:
        print(e)

def decrypt(password, encrypted_file, logged_file):
    enc_scheme = "-aes-128-cbc"
    opts = "-d -a -A -nosalt"
    openssl_cmd = 'openssl enc -pass pass:{} {} {} -in {} -out {} -nosalt 2> /dev/null '.format(password, enc_scheme, opts, encrypted_file, logged_file)

    try:
        os.system(openssl_cmd)
    except Exception as e:
        print(e)

# Setup dir structure
def setup_dir():
    if not os.path.exists("temp"):
        os.mkdir("temp")
    if not os.path.exists("data"):
        os.mkdir("data")

# Delete temp files
def cleanup(files):
    for eaFile in files:
        if os.path.exists(eaFile):
            os.remove(eaFile)

# tweet image
def tweetSetup():
    consumer_key = '94lE6CQUO1NcpfGUjbY7a2D32'
    consumer_key_secret = 'BSkoyZTEIm3oMIPvLWSOcCqnFd0w9n1WagP0SY43ztGxI8cOlz'
    access_token = '1265315199197736960-WCposgyu6MQ3y1hlAJj8enfRbwyLBI'
    access_token_secret = 'oJ9K73Fw3E5GZiAB9ftqvlGsopbexqi2n2OoYISxjqfdA'

    auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)

def getTweets(tw_api, image_path, data_path):
    username = "Lemon12776532"
    tweets = tw_api.user_timeline(username, count=10)
    new_tweets_id = []
    new_tweets_media = []
    for tweet in tweets:
        tweet_data = tweet._json
        # Use id as filename (so there are no duplicates)
        tw_id = tweet_data["id"]
        tw_media = tweet_data["entities"]["media"][0]["media_url"]

        if not os.path.exists(data_path.format(tw_id)):
            new_tweets_id.append(tw_id)
            new_tweets_media.append(tw_media)
    return (new_tweets_id, new_tweets_media)

def main():
    setup_dir()

    image_path = './data/{}.png'
    data_path = './data/{}.txt'
    password = "password"

    tw_api = tweetSetup()
    new_tweets = getTweets(tw_api, image_path, data_path)

    tweet_ids = new_tweets[0]
    tweet_medias = new_tweets[1]

    for idx in range(len(tweet_ids)):
        tweet_id = tweet_ids[idx]
        tweet_media = tweet_medias[idx]
        
        # Save image from url
        image = requests.get(tweet_media)
        cur_image_path = image_path.format(tweet_id)
        PIL.Image.open(BytesIO(image.content)).save(cur_image_path)

        # Data file paths
        logged_file = data_path.format(tweet_id)
        encrypted_file = data_path.format(str(tweet_id) + "_enc")

        # Save message to file
        enc_message = deStenographizeImage(cur_image_path)
        file_enc = open(encrypted_file, 'w')
        file_enc.write(enc_message);
        file_enc.close();

        # Decrypt
        decrypt(password, encrypted_file, logged_file)

        # Cleanup
        files = [encrypted_file, image_path]
        cleanup(files)


main()
