import os
from PIL import Image
from colorama import Fore, Back, Style

# Paths to the files
timestamps_path = "F:/Youtube/Archive/Song Splitter/Timestamps.txt"
input_path = "F:/Youtube/Archive/Song Splitter/Input"
output_path = "F:/Youtube/Archive/Song Splitter/Output"
new_videos = [f for f in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, f))]

# Convert HH:MM:SS to seconds
def convert_to_seconds(time):
    # Pad the timestamp if needed
    parts = time.split(':')
    while len(parts) < 3:
        parts.insert(0, '00')
    padded_time = ':'.join(parts)
    
    hours, minutes, seconds = map(int, padded_time.split(':'))
    return hours * 3600 + minutes * 60 + seconds

# Read the Timestamps
with open(timestamps_path, 'r') as file:
    lines = file.readlines()

album_name = lines[0].strip()
artist_name = lines[1].strip()

# Removing the first two lines since they are not timestamps or song names
lines = lines[2:]

timestamps = [line.split(',', 1)[0].strip() for line in lines]
song_names = [line.split(',', 1)[1].strip() for line in lines]
timestamps.append('end')

# Create a new directory in the output folder with the album name
album_output_path = os.path.join(output_path, album_name)
if not os.path.exists(album_output_path):
    os.makedirs(album_output_path)

for i in range(len(new_videos)):
    album = new_videos[i]
    album_path = os.path.join(input_path, album)
    
    # Extract the thumbnail for the video
    thumbnail_path = os.path.join(album_output_path, 'cover.png')
    ffmpeg_thumbnail_command = f'ffmpeg -i "{album_path}" -ss 00:00:00.000 -frames:v 1 "{thumbnail_path}" -hide_banner -loglevel error'

    os.system(ffmpeg_thumbnail_command)
    print(Fore.BLUE + f"🖼 Thumbnail saved!" + Style.RESET_ALL)

    with Image.open(thumbnail_path) as img:
        width, height = img.size
        new_dimension = min(width, height)
        left = (width - new_dimension)/2
        top = (height - new_dimension)/2
        right = (width + new_dimension)/2
        bottom = (height + new_dimension)/2
        img_cropped = img.crop((left, top, right, bottom))
        img_cropped.save(thumbnail_path)
    
    print(Fore.BLUE + f"🖼 Thumbnail cropped!" + Style.RESET_ALL)
    
    for index, timestamp in enumerate(timestamps[:-1]):
        start_time = convert_to_seconds(timestamp)
        song_name_with_order = f"{index + 1:02} {song_names[index]}"
        output_song_path = os.path.join(album_output_path, song_name_with_order + '.mp3')

        # Build FFmpeg command over several lines
        common_template = f'ffmpeg -i "{album_path}" -i "{thumbnail_path}" -ss {start_time} '
        metadata_template = f'-metadata artist="{artist_name}" -metadata album="{album_name}" -metadata title="{song_names[index]}" -metadata track="{index + 1}" '
        map_template = '-map 0:a -map 1 -c:v copy '
        
        if timestamps[index + 1] != 'end':
            end_time = convert_to_seconds(timestamps[index + 1])
            duration = end_time - start_time
            duration_template = f'-t {duration} '
            ffmpeg_command = common_template + duration_template + '-q:a 0 ' + map_template + metadata_template + f'"{output_song_path}" -hide_banner -loglevel error'
        else:
            ffmpeg_command = common_template + '-q:a 0 ' + map_template + metadata_template + f'"{output_song_path}" -hide_banner -loglevel error'
        
        os.system(ffmpeg_command)
        print(Fore.GREEN + f"🎵 Extracted: {song_name_with_order}" + Style.RESET_ALL)

print(Fore.YELLOW + "Splitting complete!" + Style.RESET_ALL)
