# WIP
import requests, re, sys, json, os
from platformdirs import user_config_dir
from twisv.version import versioning
def downloadMedia(link,file_name):
    with open(file_name, "wb") as f:
        print("Downloading %s" % file_name)
        response = requests.get(link, stream=True)
        total_length = response.headers.get('content-length')
        if total_length is None: # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
                sys.stdout.flush()
    print("✅")

def isExist(folder,file):
    if os.path.isdir(folder):
        if os.path.isfile(folder+'/'+file):
            return True
        else:
            return False
    else:
        os.makedirs(folder)
        return False

def get_config():
    conf_dir = user_config_dir('twisv','soviena')
    if not os.path.isdir(conf_dir):
        os.makedirs(conf_dir)
    if not os.path.isfile(conf_dir+'/'+'config.json'):
        with open(conf_dir+'/'+'config.json','w',encoding='utf-8') as config:
            setup = {}
            print("First time setup")
            setup['token'] = input("Paste your twitter bot token : ")
            setup['dl_dir'] = input("Media download directory : ")
            config.write(str(setup))
    else:
        with open(conf_dir+'/'+'config.json','r',encoding='utf-8') as config:
            return eval(config.read())

def get_Tweet(api_request):
    global head,config
    data = requests.get(api_request,headers=head).json()
    user = str(data['includes']['users'][0]['name']).replace(r'/', r'-')
    username = data['includes']['users'][0]['username']
    if data['includes']['media'][0]['type'] == 'video':
        if not isExist(config['dl_dir']+user+' ('+username+')', data['includes']['media'][0]['media_key']+'.mp4'):
            downloadMedia(data['includes']['media'][0]['variants'][0]['url'],config['dl_dir']+user+' ('+username+')/'+data['includes']['media'][0]['media_key']+'.mp4')
        else:
            print("Already exist!")
    else:
        for i in data['includes']['media']:
            if not isExist(config['dl_dir']+user+' ('+username+')', i['media_key']+'.jpg'):
                downloadMedia(i['url'],config['dl_dir']+user+' ('+username+')/'+i['media_key']+'.jpg')
            else:
                print("Already exist!")

def twisv():
    pass

def checkUpdate():
    r = requests.get("https://raw.githubusercontent.com/Soviena/twisv/main/twisv/version.py")
    ver = re.findall(r'=(["\d.]*)', str(r.content))
    if versioning.ver_int < int(ver[1]):
        return True
    else:
        return False    

logo = r""" ___  _ _ _  _  __  _ _ 
|_ _|| | | || |/ _|| | |
 | | | V V || |\_ \| V |
 |_|  \_n_/ |_||__/ \_/ """
config = get_config()
prefix = "https://api.twitter.com/2/tweets/"
head = {
    "Authorization": "Bearer "+config['token']
}
if len(sys.argv) > 1:
    get_Tweet(prefix+re.findall(r'\/(\d*)\?', sys.argv[1])[0]+"?expansions=author_id,attachments.media_keys&media.fields=variants,url")
    quit()
else:
    print(logo,end=" ")
    if checkUpdate():
        print("New Update Available!")
    else:
        print(versioning.ver)
    print("\nType exit to quit")
    while True:
        tw_link = input("Tweet link : ")
        if tw_link == 'exit':
            quit()
        else:
            get_Tweet(prefix+re.findall(r'\/(\d*)\?', tw_link)[0]+"?expansions=author_id,attachments.media_keys&media.fields=variants,url")




