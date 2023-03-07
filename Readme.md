# Davids YouTube Archiver

1. Put Video-/Playlist-/Channel-URLs in Download List.txt
2. Run Run.bat or Downloader.py
3. ???
4. Profit, Files will land in Downloads under the channel name of the uploader.

----------------------------

If the process stops at "Trying to delete X", exit the folder Downloads and restart explorer.exe.
This is not a bug from yt-dlp, but explorer (as far as i know).

Also, right now the project is configured to my filesystem. You might want to set **save\_path**
and **list\_path** in Downloader.py first.