import discord
from discord.ext import commands
import os
import glob
import pandas as pd
pd.set_option('display.max_columns', 10)
from itertools import takewhile
import requests
import datetime
embed = discord.Embed
import instaloader
from instaloader import Profile
intents = discord.Intents.default()
intents.all()
client = commands.Bot(command_prefix="!", intents=intents)
client = discord.Client()

@client.event
async def on_ready():
  print("Bot is online!")

profile = ('thv')
PROFILE = profile
profile_name = PROFILE

#profile = set('rkive', 'thv', 'j.m', 'agustd', 'jin', 'abcdefghi__lmnopqrstuvwxyz', 'uarmyhope')
# Technically it is supposed to be a set of profiles, something that Instaloader can do but if I can't even make one profile work anymore, 
#there isn't much of a point trying to figure out how to program a ser.

      L = instaloader.Instaloader(
      filename_pattern="{profile}_{shortcode}_{date_utc}_UTC"
           )
      #USER = os.environ['USER']
      #PASSWORD = os.environ['PASSWORD']
      #L.login(USER, PASSWORD)
      #L.save_session_to_file(USER)
    
 ############# DL PROFILE ############
      profile = Profile.from_username(L.context, PROFILE)
      B = profile.profile_pic_url
      profile_df = pd.read_csv('thv_profile.csv')
      if B not in profile_df.values:
        L.download_profilepic_if_new(profile, latest_stamps=None)
        
 ############# Profile DF save to CSV #############
        member_profile_dict = {
            'User ID': [profile.userid],
            'Username': [profile.username],
            'Fullname': [profile.full_name],
            'Biography': [profile.biography],
            'Avatar URL': [profile.profile_pic_url]
            }
        key = member_profile_dict
        member_profile_df = pd.DataFrame(member_profile_dict)
        for keys in member_profile_dict:
          if key not in profile_df.values:
            
 #Below is code for first instance
 #member_profile_df.to_csv('thv_profile.csv', header=['User ID', 'Username', 'Fullname', 'Biography', 'Avatar URL'], index=False, mode='w')
    
            member_profile_df.to_csv('thv_profile.csv', header=False, index=False, mode='a')
            print("Profile data updated")    
            
################# POST ###################        
        posts = instaloader.Profile.from_username(L.context, PROFILE).get_posts()
        DATE_MARKER = datetime.datetime(2021, 12, 25) #JM
        for post in takewhile(lambda p: p.date > DATE_MARKER, posts):

          A = post.shortcode
          posts_df = pd.read_csv('thv_posts.csv')
   
          if A not in posts_df.values:
            L.download_post(post, profile)
            
############# Post DF save to CSV #############
            member_posts_dict = {
                'PROFILE': [post.profile],
                'shortcode': [post.shortcode],
                'Caption': [post.caption],
                'Post_URL': [post.url],
                'Video_URL': [post.video_url],
                'Media_ID': [post.mediaid],
                'Post_date': [post.date_utc],
                'mediaCount': [post.mediacount]
                }

            member_posts_df = pd.DataFrame(member_posts_dict)  
 
            member_posts_df.to_csv('thv_posts.csv', header=False, index=False, mode='a')

            print("Post data updated")

            content = f"<:Tae_bell:929446734977982494> **New Post from {profile.full_name}** \nhttps://www.instagram.com/p/{post.shortcode}"

            my_files = [
              discord.File('thv/2021-12-04_07-50-44_UTC_profile_pic.jpg', filename='2021-12-04_07-50-44_UTC_profile_pic.jpg'),
              discord.File('xtra/Insta_icons/Tae_Insta_Logo.png', filename='Tae_Insta_Logo.png'),
              discord.File('xtra/Emojis/tiger-emoji-tae.png', filename='tiger-emoji-tae.png')
            ]
            embed = discord.Embed(title='', description=f'<:Tae_User:929449211785793576> {profile.biography} \n\n {post.caption}', colour=0x02db15, timestamp=datetime.datetime.utcnow())
            embed.set_thumbnail(url="attachment://2021-12-04_07-50-44_UTC_profile_pic.jpg")
            embed.set_author(name=f"{profile.username}", url="https://www.instagram.com/thv/", icon_url="attachment://Tae_Insta_Logo.png")
            embed.set_footer(text='Posted this', icon_url="attachment://tiger-emoji-tae.png") 

            await message.channel.send(embed=embed, files=my_files, content=content)
 
########### RUNNUNG THIS CODE AFTER THE CODE ABOVE HAS NOT BEEN SUCCESSFUL THUS FAR ########
# I'm sure it has something to do with the await code but I don't know how to do it differently
# I have to use discord api for the embed but can't use it to upload the photos without a filename.
# Hence I had to use post request. Sending a webhook also didn't work because it sent it as me whereas I need
# it to send as the bot. These processes work fine in isolation but I can't connect the two.
# Will defining a completely new async function work? I can't really do it with a message because I need it
# to follow immediately after the embed without an extra trigger.
# There are so many other little things that I need to program but can't unless I get this working in order :(
# Also, I don't know what is going on with commands. No matter what I do, they just don't work for me.
# Or maybe I shoul put this before, the await although I'm afraid that will lead to the images going up first. 
# I don't know but at least writing this out has has given me some new ideas to try.

            mediapath = glob.glob("thv/*.jpg")
            mediapath.extend(glob.glob("thv/*.mp4"))

            for media in mediapath:
          
              discord_df = pd.read_csv('thv_posts.csv')

              C = post.shortcode

              if C not in discord_df.values:
  
                mediapost = open(media, 'rb')

                url = os.environ['api_channel']

                files = {'image': mediapost} 
                headers = {
                "Authorization":"Bot {}".format(os.environ['Token'])
                        }

                r = requests.post(url=url, content=content, files=files, embed=discord.Embed, headers=headers)
                print(r.text, file=open("thv_discord.csv", 'w'))
              else:
                print('Post already in channel')
                
my_secret = os.environ['Token']
client.run(my_secret)
