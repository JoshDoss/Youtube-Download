# Script: Downloads YouTube public youtube videos and playlists
# Author: Josh Doss
# Version: 1.2.1

# Change log(<version> - <update>):
# 1.0.0 - Initial creation, downloads videos from playlists using pytube
# 1.1.0 - Added separate function to donwload individual videos 
# 1.1.1 - switched from using pytube to pytubefix when youtube updated url and pytube was not being updated
# 1.2.1 - Added a tools folder, developed code timer, to be developed: logger, unit tests
# 2.0.0 - Overhaul previous structure to reorganize and reduce repetition of code

import os
from sys import argv
from pytubefix import YouTube, Playlist
from Tools.Timer import timer


def handle_video(link_to_video,parent_dir,subfolder):
    '''
    Main function for handling individual youtube video downloads
    '''
    method_timer = timer()
    method_timer.start()

    print(f'handled as video: {link_to_video}')
    video = YouTube(link_to_video)

    if not subfolder:
        subfolder = clean_filename(video.author)
        video_file_name = clean_filename(f'{video.title}')
    else:
        video_file_name = clean_filename(f'{video.title} from {video.author}')

    video_download_path = os.path.join(parent_dir,subfolder)
    if not os.path.exists(video_download_path):
        os.makedirs(video_download_path)
    
    library = videos_already_downloaded(video_download_path)
    if video_file_name in library:
        print(f'\n\nA file sharing the name {video_file_name} already exists at {video_download_path}\n')
        method_timer.stop()
        print(f'\nhandle_video timer:\nmethod runtime = {method_timer.runtime()} sec')
        return
    
    print(f'\nSaving file to {video_download_path}')
    print(f'Downloading {video_file_name} ...')
    donwload_timer = timer()
    try:
        donwload_timer.start()
        video.streams.get_highest_resolution().download(output_path=video_download_path,filename=video_file_name + '.mp4',timeout=60)
        donwload_timer.stop()
        print('Finished.')
    except Exception as err:
        print(f'Error Type: {type(err)}\nError: {err}')

    method_timer.stop()
    print(f'\nTimers:\nhandle_video method timer = {method_timer.runtime()} sec\ndonwload_timer runtime = {donwload_timer.runtime()} sec')
    return

def handle_playlist(link_to_playlist,parent_dir):
    '''
    Defines output directory and iterates through playlist videos,
    also checks for matches in naming convention between new file and any exisitng files,
    skips any matches and only downlaods files with unique names.
    
    playlist = pytube playlist object
    playlist_download_path = \\[parent dir]\\[playlist title]
    library = list of filenames in download path
    cleaned_file_name = [video title] from [channel name] with illegal characters replaced with legal ones for file names
    '''

    # define playlist object
    print(f'handled as playlist: {link_to_playlist}')
    playlist = Playlist(link_to_playlist)

    # define path to output directory, check if it exists and create it if it doesnt 
    playlist_download_path = os.path.join(parent_dir,playlist.title)
    if not os.path.exists(playlist_download_path):
        os.makedirs(playlist_download_path)
    
    # list of filenames without extensions that are in the output directory before downloading
    library = videos_already_downloaded(playlist_download_path)

    # Programs main workflow loop, iterates across pytube playlist object where eaach item in the iteration is a pytube Youtube object 
    print(f'Beginning download: {playlist.title}')
    for video in playlist.videos:
        # set naming convention and replace illegal characters
        video_file_name = clean_filename(f'{video.title} from {video.author}')
        # check if file name already exists
        if video_file_name in library:
            print(f'Skipping {video_file_name}: File with this name existed before download start.')
            continue
        print(f'Downloading {video_file_name} ...')
        # perform the download, timesout after 60 seconds and moves to next video
        try:
            video.streams.get_highest_resolution().download(output_path=playlist_download_path,filename=video_file_name + '.mp4',timeout=60)
        except Exception as err:
            print(f'Error: {type(err)} caused failure during download')
    print('Finished.')
    return

def format_for_windows(unclean_string: str) -> str:
    '''
    returns a string, checks given string for any characters matching keys in forbidden_characters,
    replaces every instance of the key in the string with its cooresponding value.

    forbidden_characters = dictionary
        keys = forbidden characters for filenames
        values = filename safe alternative versions of each character
    '''
    method_timer = timer()
    method_timer.start()

    forbidden_characters = {
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
    cleaned_string = unclean_string
    for char in forbidden_characters:
        # if the current char isnt found skip it and check for the next one
        if not char in cleaned_string:
            continue
        # updates the string everytime a illegal char is found and replace every instasnce of it 
        cleaned_string = forbidden_characters[char].join(cleaned_string.split(char))
    
    method_timer.stop()
    # print(f'\nclean_filename Timer:\nMethod runtime = {method_timer.runtime()} sec')
    return cleaned_string

# update to return a dictionary | <file name> : <> 
def videos_already_downloaded(path_to_check: str):
    '''
    returns a list of files names from the given directory with the file extension removed.
    '''
    method_timer = timer()
    method_timer.start()

    # list files in dir and remove file type extension, rejoin by '.' incase there are any '.' in the filename other than one to denote the extension
    files = ['.'.join(file.split('.')[:-1]) for file in os.listdir(path_to_check)]

    method_timer.stop()
    # print(f'\nvideos_already_downloaded Timer:\nMethod runtime = {method_timer.runtime()} sec')
    return files

def generate_download_path(parent: str, child: str) -> str:

    path = os.path.join(parent,child)
    if not os.path.exists(path):
        os.makedirs(path)
    
    return path

def perform_download(video,parent_dir: str,sub_folder: str,from_playlist: bool) -> None:

    download_path = generate_download_path(parent= parent_dir, child= sub_folder)
    if from_playlist:
        file_name = format_for_windows(f'{video.title} from {video.author}')
    else:
        file_name = format_for_windows(f'{video.title}')
    print(f'Downloading {file_name}...')

    library = videos_already_downloaded(download_path)
    for file in library:
        print(f'already downloaded -> {file}')
    if file_name in library:
        print(f'\n\nA file sharing the name {file_name} already exists at {download_path}\n')
        return
    try:
        video.streams.get_highest_resolution().download(output_path=download_path,filename=file_name + '.mp4',timeout=60)
    except Exception as err:
        print(f'Error: Download failed\ntype -> {type(err)}\nerror -> {err}\n')

def check_url(url: str) -> bool:
    # Currently YouTube uses 'playlist?' and 'watch?' to denote a playlist and video url respectively
    if 'playlist?' in url:
        return True
    elif 'watch?' in url:
        return False
    else:
        print(f"Input was not a valid url, copy full url from youtube webpage: {url}")
        exit(0)

def main(link: str):

    isplaylist = check_url(url= link)
    path = r'D:\Personal\Media\Music' if isplaylist else r'D:\Personal\Media\Youtube Vault'
    print(path)

    if isplaylist:
        print(isplaylist)
        playlist = Playlist(url= link)
        for each_video in playlist.videos:
            perform_download(video= each_video, parent_dir= path, sub_folder= format_for_windows(unclean_string= playlist.title), from_playlist= isplaylist)
        print('Finished.')
        exit(0)
    else:
        youtube_video = YouTube(url= link)
        perform_download(video= youtube_video, parent_dir= path, sub_folder= format_for_windows(unclean_string= youtube_video.author), from_playlist= isplaylist)
        print('Finished.')
        exit(0)

# Standard call to main() to begin program
if __name__ == '__main__':
    command_line_args = argv[1:]
    if command_line_args:
        main(command_line_args[0])
    else:
        # playlist | https://www.youtube.com/playlist?list=PLw1qX0GZGsGE1-0T1NoBcDzD1rx3l1_OR
        # video | https://www.youtube.com/watch?v=yau-rTqV4xQ
        main('https://www.youtube.com/watch?v=yau-rTqV4xQ')