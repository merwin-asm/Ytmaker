"""
YtMaker v 1.0.0

Autogenerate compilation videos,
by getting videos from Instagram
and upload it to Youtube.
"""



from youtube_upload.client import YoutubeUploader
from instagrapi import Client
from rich import print
from moviepy.editor import *
import time
import random
import os




print("\n[blue]  [?] The Number of videos to be compiled ?[/blue]", end="")
NUM_OF_VIDS_USED = int(input(" "))

print("[blue]  [?] The current number of videos in youtube channel ?[/blue]", end="")
VID_NUM = int(input(" ")) + 1

print("[blue]  [?] The Insta username ?[/blue]", end="")
INSTA_USERNAME = input(" ")

print("[blue]  [?] The Insta pwd ?[/blue]", end="")
INSTA_PWD = input(" ")

print("[blue]  [?] Client ID (yt API) ?[/blue]", end="")
ci = input(" ")

print("[blue]  [?] Client secret (yt API) ?[/blue]", end="")
cs = input(" ")

print("[blue]  [?] Title for the videos ?[/blue]", end="")
TITLE = input(" ")

print("[blue]  [?] Description for the videos ?[/blue]", end="")
DESC = input(" ")

print("[blue]  [?] Tags for the videos (separate using ',') ?[/blue]", end="")
TAGS = input(" ")

print("[blue]  [?] Time delay between each videos in minutes ? [/blue]", end="")
TIME_DELAY = int(input(" "))



uploader = YoutubeUploader(ci,cs)

uploader.authenticate()



def Download():

    cl = Client()

    cl.request_timeout = 20

    cl.login(INSTA_USERNAME, INSTA_PWD)
    
    print("[green]  [+] LOGGED IN TO INSTAGRAM[\green]")


    user_id = cl.user_id_from_username(INSTA_USERNAME)
    
    z = cl.user_following(user_id)
    
    time.sleep(4)
    
    URLS = []
  
    N_URLS = []

    FILES = []

    for e in z:

        time.sleep(4+random.randint(1,60)*0.05)

        medias = cl.user_medias(e, 25)
        
        for e in medias:
        
            if e.dict()["media_type"] == 2:
                URLS.append(e.dict()["video_url"])   


    for e in range(0, NUM_OF_VIDS_USED):
        N_URLS.append(random.choice(URLS))
    

    for e in N_URLS:
        time.sleep(5+random.randint(1,60)*0.05)

        FILES.append(cl.video_download_by_url(e, str(random.randint(1000000000000000,10000000000000000000000))))
    
    return FILES




def make_video(files):
    clips = []
   
    clips.append("intro.mp4")

    for e in files:
        clips.append(str(e))

    # concatenating both the clips
    concatenate(clips,f"videos/vid_{VID_NUM}.mp4")





def concatenate(video_clip_paths, output_path, method="compose"):

    # create VideoFileClip object for each video file
    clips = [VideoFileClip(c) for c in video_clip_paths]

    if method == "reduce":
        # calculate minimum width & height across all clips
        min_height = min([c.h for c in clips])
        min_width = min([c.w for c in clips])
        # resize the videos to the minimum
        clips = [c.resize(newsize=(min_width, min_height)) for c in clips]
        # concatenate the final video
        final_clip = concatenate_videoclips(clips)

    elif method == "compose":
        # concatenate the final video with the compose method provided by moviepy
        final_clip = concatenate_videoclips(clips, method="compose")

    # write the output video file
    final_clip.write_videofile(output_path)




while True:

    print("\n\n[green]  [+] DOWNLOADING VIDEOs [/green]")
    files = Download()
    
    print("[green]  [+] MAKING VIDEO [/green]")
    
    make_video(files)
    
    for e in files:
        os.system(f"rm {e}")
    

    print("[green]  [+] UPLOADING TO YT [/green]")
    

    options = { 
            "title" : f"{TITLE} - {VID_NUM}" , 
    "description" : DESC, 
    "tags" : TAGS.split(","),
    "categoryId" : "22",
    "privacyStatus" : "public",
    "kids" : False}


    # upload video
    uploader.upload(f"videos/vid_{VID_NUM}.mp4",options) 
   

    print("[dark_orange]  [+] UPLOADED [/dark_orange]")

    VID_NUM += 1

    print(f"\n[yellow]  [~] Next Upload In {TIME_DELAY} Mins[/yellow]")

    time.sleep(TIME_DELAY*60)
    


