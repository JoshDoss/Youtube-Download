# Script: Downloads YouTube public youtube videos and playlists
# Author: Josh Doss
# Version: 1.2.1

# Change log(<version> - <update>):
# 1.0.0 - Initial creation, downloads videos from playlists using pytube
# 1.1.0 - Added separate function to donwload individual videos 
# 1.1.1 - switched from using pytube to pytubefix when youtube updated url and pytube was not being updated
# 1.2.1 - Added a tools folder, developed code timer, to be developed: logger, unit tests
# 2.0.0 - Overhaul previous structure to reorganize and reduce repetition of code
# 2.0.1 - Updated perform_download parameters | perform_download(<youtube video object>,<download path>,<library>,<from a playlist>)

import os
from sys import argv
from pytubefix import YouTube, Playlist
from Tools.Timer import timer


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
def videos_already_downloaded(path_to_check: str) -> list:
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

def perform_download(video,download_path: str,downloaded_videos: list,from_playlist: bool) -> None:

    if from_playlist:
        file_name = format_for_windows(f'{video.title} from {video.author}')
    else:
        file_name = format_for_windows(f'{video.title}')
    print(f'Downloading {file_name}...')

    if file_name in downloaded_videos:
        print(f'\nA file sharing the name {file_name} already exists at {download_path}\n')
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
    parent_dir = r'D:\Personal\Media\Music' if isplaylist else r'D:\Personal\Media\Youtube Vault'
    print(parent_dir)

    if isplaylist:
        print(isplaylist)
        playlist = Playlist(url= link)
        path = generate_download_path(parent= parent_dir, child= format_for_windows(unclean_string= playlist.title))
        library = videos_already_downloaded(path)
        for file in library:
            print(f'already downloaded -> {file}')
        for each_video in playlist.videos:
            perform_download(video= each_video, download_path= path, downloaded_videos= library, from_playlist= isplaylist)
        print('Finished.')
        exit(0)
    else:
        youtube_video = YouTube(url= link)
        path = generate_download_path(parent= parent_dir, child= format_for_windows(unclean_string= youtube_video.author))
        library = videos_already_downloaded(path)
        perform_download(video= youtube_video, parent_dir= path, download_path= library, from_playlist= isplaylist)
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