import os

#########################################################
# Change save_path and list_path to where you want them #
#########################################################

# where the videos get saved to
save_path = "F:/Youtube/Archive/Downloads/"

# where the download list is
list_path = "F:/Youtube/Archive/Download List.txt"

# build the yt-dlp command
# output file title: "creator_title.filetype"
output_template = '-o %(uploader)s_%(title)s.%(ext)s '
save_template = '-P "' + save_path + '" '
list_template = '-a "' + list_path + '" '
thumbnail_template = '--write-thumbnail --convert-thumbnails png '
command_template = 'yt-dlp ' + list_template + save_template + output_template + thumbnail_template

# download all videos in the list
os.system(command_template)

# get all files (not directories) in the save path
# taken from https://stackoverflow.com/a/3207973/16283451
new_videos = [f for f in os.listdir(save_path) if os.path.isfile(os.path.join(save_path, f))]

# ffmpeg every video in the save path 
# first convert webm to mp4
# then set the thumbnail to the saved image
for video in new_videos:

    # get name and extension of video
    # video = video_name + video_extension
    video_name, video_extension = os.path.splitext(video)

    # only convert videos
    if video_extension in ('.mp4', '.webm', '.avi', '.flv', '.mov', '.mkv'):

        # split video_name into author and title
        # video_name = author + "_" + title
        author, title = video_name.split("_", 1)

        # create a folder for the author (if it doesn't exist)
        if not os.path.exists(save_path + author):
            os.makedirs(save_path + author)

        # move the video to the author's folder
        video_path = save_path + video_name + video_extension
        thumbnail_path = save_path + video_name + ".png"
        ffmpeg_save_path = save_path + author + "/" + title + ".mp4"

        # convert webm to mp4 and put in ffmpeg_save_path
        # also set the thumbnail to thumbnail_path
        command = 'ffmpeg -loglevel error -y -i "' + video_path + '" -i "' + thumbnail_path + '" -map 1 -map 0 -c copy -disposition:0 attached_pic "' + ffmpeg_save_path + '"'
        os.system(command)

        # delete the webm video and the thumbnail
        os.remove(video_path)
        os.remove(thumbnail_path)

        print("Finished: " + author + ", " + title)

# remove the leftover files
# for example, when downloading using a channel link, the profile picture is also downloaded
# we dont want any of that, so just delete it
leftover_files = [f for f in os.listdir(save_path) if os.path.isfile(os.path.join(save_path, f))]

for file in leftover_files:

    file_path = save_path + file

    os.remove(file_path)

    print("Deleted: " + file)