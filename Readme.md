# Davids YouTube Archiver

1. Put Video-/Playlist-/Channel-URLs in Download List.txt
2. Run Run.bat or Downloader.py
3. ???
4. Profit, Files will land in Downloads under the channel name of the uploader.

----------------------------

If the process stops at "Trying to delete X", exit the folder Downloads and restart explorer.exe.
This is not a bug from yt-dlp, but explorer (as far as i know).

Also, right now the project is configured to my filesystem. You might want to set `save_path`
and `list_path` in Downloader.py first.

----------------------------

Theres also a Song Splitter script in here that takes in an album .mp4 file,
timestamps of the songs and then splits the album into its songs. How the
songs get split is determined by Timestamps.txt.

The album goes in `Song Splitter/Input`, single songs get saved to Output.

Timestamps.txt has the following format:

```
ALBUM NAME
ARTIST
TIMESTAMP,SONGNAME
TIMESTAMP,SONGNAME
TIMESTAMP,SONGNAME
...
```

TIMESTAMPs have the format MM:SS or HH:MM:SS, which stands for the time
at which the associated song starts.
