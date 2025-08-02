# Script: Downloads public YouTube videos and playlists
# Author: Josh Doss
# Version: 2.0.2

# Change log(<version> - <update>):
# 1.0.0 - Initial creation, downloads videos from playlists using pytube
# 1.1.0 - Added separate function to donwload individual videos 
# 1.1.1 - switched from using pytube to pytubefix when youtube updated url and pytube was not being updated
# 1.2.1 - Added a tools folder, developed code timer, to be developed: logger, unit tests
# 2.0.0 - Overhaul previous structure to reorganize and reduce repetition of code
# 2.0.1 - Updated perform_download parameters | perform_download(<youtube video object>,<download path>,<library>,<from a playlist>)
# 2.0.2 - videos_already_downloaded now returns a set (previously returned a list)

import os
from sys import argv
from pytubefix import YouTube, Playlist
from Tools.Timer import timer


def check_url(url: str) -> bool:
    # Currently YouTube uses 'playlist?' and 'watch?' to denote a playlist and video url respectively
    if 'playlist?' in url:
        return True
    elif 'watch?' in url:
        return False
    else:
        print(f"Input was not a valid url, copy full url from youtube webpage: {url}")
        exit(0)

def generate_download_path(parent: str, child: str) -> str:

    path = os.path.join(parent,child)
    if not os.path.exists(path):
        os.makedirs(path)
    
    return path

def format_for_windows(unclean_string: str) -> str:
    '''
    checks given string for any characters matching keys in forbidden_characters,
    replaces every instance of the key in the string with its cooresponding value.

    forbidden_characters = dictionary
        keys = forbidden characters for filenames
        values = filename safe alternative versions of each character
    '''
    # method_timer = timer()
    # method_timer.start()

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
    
    # method_timer.stop()
    # print(f'\nclean_filename Timer:\nMethod runtime = {method_timer.runtime()} sec')
    return cleaned_string

def videos_already_downloaded(path_to_check: str) -> set:
    '''
    returns a list of files names from the given directory with the file extension removed.
    '''
    # method_timer = timer()
    # method_timer.start()

    files = set()
    for file in os.listdir(path= path_to_check):
        files.add('.'.join(file.split('.')[:-1]))

    # method_timer.stop()
    # print(f'\nvideos_already_downloaded Timer:\nMethod runtime = {method_timer.runtime()} sec')
    return files

def perform_download(video,download_path: str,downloaded_videos: set,from_playlist: bool) -> None:
    if from_playlist:
        file_name = format_for_windows(f'{video.title} from {video.author}')
    else:
        file_name = format_for_windows(f'{video.title}')
    print(f'\nDownloading {file_name}...')
    
    if file_name in downloaded_videos:
        print(f'\nA file sharing the name {file_name} already exists at {download_path}\n')
        return
    try:
        video.streams.get_highest_resolution().download(output_path=download_path,filename=file_name + '.mp4',timeout=60)
    except Exception as err:
        print(f'Error: Download failed\ntype -> {type(err)}\nerror -> {err}\n')

def execute(link: str):
    # check if url is to a video or playlist
    isplaylist = check_url(url= link)
    parent_dir = r'C:\Joshua Doss Temp\Playlist' if isplaylist else r'C:\Joshua Doss Temp\Video'

    # downoad each video in playlist to <parent dir>\<playlist title>\<video name 'from' author name>
    if isplaylist:
        playlist = Playlist(url= link)
        path = generate_download_path(parent= parent_dir, child= format_for_windows(unclean_string= playlist.title))
        library = videos_already_downloaded(path)

        for each_video in playlist.videos:
            download_timer = timer()
            download_timer.start()
            perform_download(video= each_video, download_path= path, downloaded_videos= library, from_playlist= isplaylist)
            download_timer.stop()
            print(f'downloaded Timer:\nruntime = {download_timer.runtime()} sec')
        print('Finished.')
        exit(0)

    # download single video to <parent dir>\<author name>\<video name>
    else:
        youtube_video = YouTube(url= link)
        path = generate_download_path(parent= parent_dir, child= format_for_windows(unclean_string= youtube_video.author))
        library = videos_already_downloaded(path)

        perform_download(video= youtube_video, download_path= path, downloaded_videos= library, from_playlist= isplaylist)
        print('Finished.')
        exit(0)

# Standard call to main to begin program
if __name__ == '__main__':
    command_line_args = argv[1:]
    if command_line_args:
        # Run script from command line with | python ytdownload.py "<insert public youtube link>"
        execute(command_line_args[0])
    else:
        # Uncomment one of the lines below to run script manually in IDE
        link = r'https://www.youtube.com/playlist?list=PLw1qX0GZGsGE1-0T1NoBcDzD1rx3l1_OR' #| playlist
        # link = r'https://www.youtube.com/watch?v=nwSy9RJ98eo&list=PLw1qX0GZGsGE1-0T1NoBcDzD1rx3l1_OR&index=2' #| video
        execute(link)