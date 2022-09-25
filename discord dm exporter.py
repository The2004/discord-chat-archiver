import discord
import os
import sys

client = discord.Client()
currentdir = os.path.dirname(os.path.realpath(__file__))
token = "" # put your discord token in quotes
userid = 0 #user id of dm you want to log
found = False
if token == "":
 token = input(">>> Please Enter your token")
if userid == 0:
 userid = int(input(">>> Please Enter ID of user DM you want to export"))
messageblock = """<div class="messageblock">
            <p class="reply">╔═══ <strong>$rname</strong> $rcontent</p>
            <img align="top" class="pfp" src="$pfp"></img>
            <div class="userandtime"><p class="username">$user <span class="time"> $timestamp</span></p></div>
            """
vid = """<video class="center-fit mrgin" controls>
  <source src="$vid" type="video/mp4"></video>"""
img = "<img class=\"center-fit mrgin\" src=\"$img\"></img>"
msg = "<p class=\"message\">$message</p>"
hyperlink = "<a href=\"link\" style=\"color: rgb(35, 163, 244);\">link</a>"
htmlsourceraw = """<!DOCTYPE html>
<html>
    <head>
        <style>
            body{
                background-color: rgb(54, 57, 63);
            }

            .pfp{
                width: 40px;
                height: 40px;
                border-radius: 50%;
                margin-right: 5px;
                position: relative;
                float: left;
            }

            .username{
                display: block;
                font-size: 1rem;
                font-weight: 500;
                line-height: 1.375rem;
                position: relative;
                overflow: hidden;
                flex-shrink: 0;
                color: white;
                word-break: keep-all;
                font-family: Whitney,"Helvetica Neue",Helvetica,Arial,sans-serif;
                top:0px;
            }

            .userandtime{
                width: min-content;
                display: contents;
            }

            .time{
                color: rgb(163, 166, 170);
                font-size: 0.8rem;
            }

            .message{
                color: rgb(209, 221, 222);
                font-size: 0.9rem;
                font-family: Whitney,"Helvetica Neue",Helvetica,Arial,sans-serif;
                margin: 0%;
                display: inline-block;
                text-align: left;
                position: relative;
                clear:both;
                top:-16px;
            }

            
            .imgbox {
                display: grid;
                height: 100%;
            }
            .center-fit {
                max-width:35%;
                max-height: 100vh;
                border-radius: 10px;
                position: relative;
                top: 0px;
                display: block;
            }

            .mrgin{
              margin-left: 45px;
            }

            .messageblock{
                position: relative;
                display: block;
                margin-top: 20px;
            }

            .reply{
                color: rgb(149, 150, 153);
                position: relative;
                left: 15px;
                font-family: Whitney,"Helvetica Neue",Helvetica,Arial,sans-serif;
            }
        </style>
    </head>
    <body>"""

htmlend = "</body></html>"
msgend = "</div>"
@client.event
async def on_ready():
 global found
 print(u"Logged in as "+client.user.name)
 for chan in client.private_channels:
  if str(chan.type) == "private":
   if chan.recipient.id == userid:
    #print(u"User with id "+str(userid)+" was found named: " + chan.recipient.name)
    found = True
    htmlsource = htmlsourceraw
    messages = []
    async for message in chan.history(limit=None):
     messages.append(message)
    messages = messages[::-1]
    for message in messages:
     wasmessage = False
     if message.reference is not None:

      replyid =  message.reference.message_id
      replymessage = None
      for replymsg in messages:
        
       if replymsg.id == replyid:
        replymessage = replymsg
        break
       if replymsg.id == message.id:
        break
      htmlsource += messageblock.replace("$pfp", str(message.author.avatar_url)).replace("$user", message.author.name).replace("$timestamp", str(message.created_at)).replace("$rname", replymessage.author.name).replace("$rcontent",  replymessage.content)
     else:
      htmlsource += messageblock.replace("$pfp", str(message.author.avatar_url)).replace("$user", message.author.name).replace("$timestamp", str(message.created_at)).replace("<p class=\"reply\">╔═══ <strong>$rname</strong> $rcontent</p>", "")
     if message.content != "":
      wasmessage = True
      if "http" not in message.content and "://" not in message.content:
       htmlsource += msg.replace("$message", message.content.replace("\n", "<br>"))
      else:
       words = message.content.split(" ")
       embeds = ""
       i = 0
       for word in words:
        if "http" in word and "://" in word:
         if word.endswith(".mp4") or word.endswith(".mov") or word.endswith(".webm"):
          embeds += vid.replace("$vid", word)
         else:
          if word.endswith(".png") or word.endswith(".jpg") or word.endswith(".jpeg") or word.endswith(".webp")or word.endswith(".gif"):
           embeds += img.replace("$img", word)
         words[i] = hyperlink.replace("link", word)
        
        i += 1 
       htmlsource += msg.replace("$message", " ".join(words)) + embeds
        
       
        
     if len(message.attachments) > 0:
      for attach in message.attachments:
       if attach.url.endswith(".png") or attach.url.endswith(".jpg") or attach.url.endswith(".jpeg") or attach.url.endswith(".webp") or attach.url.endswith(".gif"):
        if wasmessage == False:
         htmlsource += img.replace("$img", attach.url).replace(" mrgin", "")
        else:
         htmlsource += img.replace("$img", attach.url)
       else:
        if attach.url.startswith("http") and (attach.url.endswith(".mp4") or attach.url.endswith(".mov") or attach.url.endswith(".webm")):
         if wasmessage == False:
          htmlsource += vid.replace("$vid", attach.url).replace(" mrgin", "")
         else:
          htmlsource += vid.replace("$vid", attach.url)
        else:
         htmlsource += msg.replace("$message", "["+attach.url+"]")
     htmlsource += msgend
    htmlsource += htmlend
    filename = chan.recipient.name.encode("ascii", 'xmlcharrefreplace').decode().replace("*","").replace("<","").replace(">","").replace(":","").replace("\"","").replace("/","").replace("|","").replace("\\","")
    open(currentdir+"\\" + filename +".html", "w+", encoding="utf-8").write(htmlsource)
    print(u"done, log written to "+currentdir+"\\" + filename +".html")
    break
 if found == False:
  print(u"user id " + str(userid) + " could not be found.")

   
 
@client.event
async def on_message(message):
 pass
 #async for message in message.channel.history(limit=1):
  #print(message.content)

client.run(token, bot=False)
