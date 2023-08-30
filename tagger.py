import os, mutagen
from mutagen.flac import Picture

# Initial variables
music_folder = os.path.abspath('.' + '/music')
music_files = os.listdir(music_folder)
mutagen_files = []

# Generate user-defined variables containing album information
composer = input('Name of the composer:\n')
artist = input('Name of the artist(s):\n')
album = input('Name of the album:\n')
year = input('Year of the recording:\n')
genre = input('Genre of the album:\n').title()

# Import TXT file containing track titles and store titles in a list
with open('titles.txt', 'r') as file:
    titles = file.readlines()
    titles = [title.strip() for title in titles]
    file.close()

# Initialise Mutagen music files and append to a list
for file_name in music_files:
    music_file = os.path.join(music_folder, file_name)
    mutagen_files.append(mutagen.File(music_file))

# Ensure length of track titles list is equal to that of mutagen files list
if len(titles) != len(mutagen_files):
    print('ERROR: There are %s track titles for %s files', (len(titles),
                                                            len(mutagen_files)))
    quit()

# Order list of music files by ascending track number
mutagen_files.sort(key=lambda x: x['tracknumber'])

# Locate album artwork within folder
for file in os.listdir():
    if file.startswith('folder'):
        artwork_file = file

# Instantiate album artwork
artwork = Picture()
artwork.type = 3
artwork.mime = u'image/jpeg'
with open(artwork_file, 'rb') as art:
    artwork.data = art.read()
    art.close()

# Delete and replace all metadata of music files
track_number = 1
for file in mutagen_files:
    file.clear()
    file.clear_pictures()
    file['title'] = titles.pop(0)
    file['composer'] = [composer]
    file['album artist'] = [composer]
    file['artist'] = [artist]
    file['album'] = [album]
    file['date'] = [year]
    file['genre'] = [genre]
    file['tracknumber'] = [f'{track_number:02d}']
    file.add_picture(artwork)
    track_number += 1
    file.save()