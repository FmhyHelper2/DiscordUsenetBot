# FCDiscordUsenetBot

This is a fork of [sanjit's tg-usenetbot](https://github.com/sanjit-sinha/Tg-UsenetBot).
It was ported to discord.py by [jsmsj](https://github.com/jsmsj), and was modified by me for our needs.

**Note: This bot doesn't download any NZB files or content. It simply interacts with various APIs such as Sabnzbd and NZBHydra to display progress and allow user to control them via Discord.**

---

## Bot commands

`>search [search_term]` - Searches Indexers.  
`>search movie OR movies [imdbId]` - Searches for a movie with imdbId.  
`>search series OR tv [imdbId]` - Searches for a tv show with tvmazeId(if it could be found) or else will use the imdbId.  
  
`>grab [ID] [ID] [ID]` - Grabs the file to download (allows multiple IDs separated by space and remember to add "-" if it's there).  
`>grab -p [ID]` - Use this **ONLY** if you are grabbing packs like courses, tv show packs.  
  
`>nzbmirror` - Use this if you want to upload your own nzb and mirror it using the bot, make sure **that the file is sent as an attachment** and you use the command in the caption.  
`>nzbmirror --pass=password` - Use this **ONLY** if the nzb uploaded doesn't have the password embed in it.  
  
`>status` - Shows the downloading queue.  
`>pause [NZB-ID]` - Pauses the file in the queue.  
`>resume [NZB-ID]` - Resumes the file in the queue.  
`>delete [TASK-ID]` - Deletes the file from the queue.  

---

## Deployment

### Program Settings

1. You are expected to have sabnzbd and nzbhydra installed.
2. For sabnzbd, you will have to make sure you have a **category with the name `pack`** so that the `-p` will be used when grabbing packs.
3. Search for `Post-Process Only Verified Jobs` in **sabnzbd settings** and untick it.
4. Search for `Deobfuscate final filenames` in **sabnzbd settings** and put a tick it.
5. For **sabnzbd sorting** you can use the following strings:  
   movies: `%title (%y)/%dn.%ext`  
   tv shows: `%sn (%y)/Season %s/%dn.%ext`  
   **Note:** This will always make sure that the final name of the files will be the same as nzb name.

### Docker deployment

1. `git clone https://github.com/progamerz-dev/FCDiscordUsenetBot`
2. `cd FCDiscordUsenetBot`
3. `cp sample.config.env config.env`
4. `nano config.env` - edit the configuration and when done use ctrl + x and save modifications.
5. `sudo docker build . -t usenetbot`
6. `sudo docker run usenetbot`

---
