'''
Downloads public playlists from youtube using pytube

Basic Info:
    - Runs in terminal and takes playlist link as arg after program name
    - The name of the playlist on youtube will be used as the directory name for all the videos in the playlist
    - The playlist directory will be saved in a parent directopry defiend by: parent_dir_for_playlist_downloads
    - All videos are saved as .mp4
    - Filename convention is: [title of video on youtube] from [youtube channel that posted the video]

    - Working on adding functionality for individual youtube videos
'''
import os
from sys import argv
from pytube import YouTube, Playlist



def handle_video(link_to_video,parent_dir):
    pass

def generate_filename(video_file_name):
    '''
    returns a string, checks given string for any characters matching keys in forbidden_characters_replacements,
    replaces every instance of the key in the string with its cooresponding value.

    forbidden_characters_replacements = dictionary, keys = forbidden characters for filenames, values = filename safe alternative versions of each character
    '''
    forbidden_characters_replacements = {
                                        '<' : '＜',
                                        '>' : '＞',
                                        ':' : '：',
                                        '"' : '＂',
                                        '*' : '＊',
                                        '?' : '？',
                                        '|' : '｜',
                                        '/' : '／',
                                        '\\' : '＼',
                                        '.' : '．'
                                        }
    for char in forbidden_characters_replacements:
        # if the current char isnt found skip it and check for the next one
        if not char in video_file_name:
            continue
        # updates the string everytime a illegal char is found and replace every instasnce of it 
        video_file_name = forbidden_characters_replacements[char].join(video_file_name.split(char))
    return video_file_name

def videos_already_downloaded(path_to_check):
    '''
    returns a list of files names from the given directory with the file extension removed.
    '''
    # list files in dir and remove file type extension, rejoin by '.' incase there are any '.' in the filename other than one to denote the extension
    return ['.'.join(file.split('.')[:-1]) for file in os.listdir(path_to_check)]

def handle_playlist(link_to_playlist,parent_dir):
    '''
    Defines output directory and iterates through playlist videos,
    also checks for matches in naming convention between new file and any exisitng files,
    skips any matches and only downlaods files with unique names.
    
    playlist = pytube playlist object
    download_path = \\[parent dir]\\[playlist title]
    library = list of filenames in download path
    video_file_name = [video title] from [channel name] with illegal characters replaced with legal ones for file names
    '''

    print(f'handled as playlist: {link_to_playlist}')
    playlist = Playlist(link_to_playlist)

    # define path to output directory, check if it exists and create it if it doesnt 
    download_path = os.path.join(parent_dir,playlist.title)
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    
    # list of filenames without extensions that are in the output directory before downloading
    library = videos_already_downloaded(download_path)

    # Programs main workflow loop, iterates across pytube playlist object where eaach item in the iteration is a pytube Youtube object 
    print(f'Beginning download: {playlist.title}')
    for video in playlist.videos:
        # set naming convention and replace illegal characters
        video_file_name = generate_filename(f'{video.title} from {video.author}')
        # check if file name already exists
        if video_file_name in library:
            print(f'Skipping {video_file_name}: File with this name existed before download start.')
            continue
        print(f'Downloading {video_file_name}...')
        # perform the download, timesout after 60 seconds and moves to next video
        try:
            video.streams.get_highest_resolution().download(output_path=download_path,filename=video_file_name + '.mp4',timeout=60)
        except Exception as err:
            print(f'Error: {type(err)} caused failure during download')
    print('Finished.')
    return True

def main(url = ''):
    '''
    Defines parent directory and checks the contents of the url provided.

    url = command line arguemnts index postion [1]: argv[1] 
    parent_dir_for_playlist_downloads = directory location to save downloaded videos to
    '''
    parent_dir_for_playlist_downloads = r'D:\Personal\Media\Music'
    parent_dir_for_video_downloads = r''

    if not 'playlist?' in url:
            print(f"Input was not a valid url: {url}")
            exit(1)
    if handle_playlist(url,parent_dir_for_playlist_downloads):
        exit(0)

# Standard call to main() to begin program
if __name__ == '__main__':
    # Pass in the command line argument after the program name from the terminal, needs to be a youtube link to public playlist
    main(argv[1])