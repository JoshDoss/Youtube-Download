# YouTube-Download

ytdownload.py is a script that downloads PUBLIC playlists and videos from YouTube

## Modules

ytdownload.py makes use of pytube and can be installed via pip
```bash
pip install pytube
```
also uses `sys.argv` to pass YouTube url to script

## Usage

ytdownload.py runs in the command line and takes up to 2 args 

where `argv[1]` is a YouTube url and `argv[2]` is optional and specifies a subfolder for videos not from a playlist to save to

```bat
python ytdownload.py "URL to public YouTube playlist or video" "optional subfolder name"
```

## Basic Workflow
```
- Ccollect args passed via command line:
    - pass argv[1] as YouTube url
    - pass argv[2] as a string to be used as an optional subfolder name for videos not from a playlist
- Assign parent directories
- check if url is to a playlist or video: 
    -YouTube urls currently contain "watch?" or "playlist?" to denote a video or playlist respectively
    Playlists
        - create pytube Playlist object from url
        - check for and create sub directory in parent dir with playlist title as directory name if not already existing
        - store the names of any files that exist in the playlist directory
        - iterate across pytube Playlist.vidoes object
        - generate file name with shared convention for each video: at this step replace any characters that are illegal for file names that are in video titles
        - check if video from playlist shares a name that has been stored: skip download if a match is found
        - save videos to [parent directory]\\[Playlist title]\\[[video title] from [channel name]]
        - timeout after 60 seconds and move onto next video
    Videos:
        - create pytube YouTube object
        - check command line args for a specified folder and create it if not already existing
        - if no sub folder specified set channel name as sub folder
        - store all file names from sub folder
        - generate filename
            - remove illegal characters from video titles first
            - if sub folder is specified set file name to [video title] from [channel name]
            - if no sub folder specified set file name to [video title]
        - check stored files for matching file names: if match found count how many files with that name have been stored and append count + 1 to end of file name 
        - save videos to [parent directory]\\[sub folder]\\[filename]
        - timeout after 60 seconds and display download failed
```