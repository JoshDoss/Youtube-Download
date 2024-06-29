# Youtube-Download

ytdownload.py is a script that downlaods PUBLIC playlists and videos from youtube

## Modules

ytdownload.py uses makes use of pytube and can be installed via pip
```bash
pip install pytube
```
also uses sys.argv to pass youtube url to script

## Usage

ytdownload.py runs in the command line and takes up tp 2 args 

where argv[1] is a youtube url and argv[2] is optional and specifies a subfolder for videos not from a playlist to save to

```bat
python ytdownload.py "URL to public youtube playlist or video"
```

## Basic Workflow
```
- Check number of args passed via commadn line:
    - if one pass argv[1] as youtube url
    - if more than one also pass argv[2] as a string to be used as a subfolder name for vidoes not from a playlist
- Assign parent directories
- check if url is to a playlist or video: Youtube urls currently contain "watch?" or "playlist?" to denote a video or playlist respectively
    Playlists
        - check for and create sub directory in parent dir with playlist title as directory name if not already existing
        - store the names of any files that exist in the playlist directory
        - iterate across pytube Playlist.vidoes object
        - genreate file name with shared convention for each video: at this step replace any characters that are illegal for file names that are in viedo titles
        - check if video from playlist shares a name that has been stored: skip download if a match is found
        - save videos to [parent directory]\\[Playlist title]\\[[video title] from [channel name]]
        - timeout after 60 seconds and move onto next video
    Videos:
        - check command line args for a specified folder and create it if not already existing
        - if no sub folder specified set channel name as sub folder
        - store all file names from sub folder
        - generate filename
            - remove illegal characters from video titles first
            - if sub folder is specified set file name to [vidoe title] from [chanel name]
            - if no sub folder specified set file name to [video title]
        - check stored files for matching file names: if match found count how many files with that name have been stored and append count + 1 to end of file name 
        - save videos to [parent directory]\\[sub folder]\\[filename]
        - timout after 60 seconds and display download failed
```