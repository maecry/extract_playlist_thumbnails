import youtube_dl
import urllib.request
import os

playlist_url = str(input("enter playlist url: "))

# Configure youtube_dl options
ydl_opts = {
    'extract_flat': 'in_playlist',
    'ignoreerrors': False,
    'playlistend': 1000,  # Set the number of videos to retrieve from the playlist
    'verbose': True  # Enable verbose output
}

# Create a youtube_dl instance
ydl = youtube_dl.YoutubeDL(ydl_opts)

# Download the playlist info
playlist_info = ydl.extract_info(playlist_url, download=False)

# Extract playlist name from the URL
playlist_name = playlist_info.get('title', 'playlist')  # Use 'playlist' as default if name not found

# Create the download folder based on playlist name
save_folder = playlist_name.replace(' ', '_')  # Replace spaces with underscores
os.makedirs(save_folder, exist_ok=True)  # Create the folder if it doesn't exist

# Extract video IDs and titles from the playlist info
videos = {video['title']: video['id'] for video in playlist_info['entries']}

for video_title, video_id in videos.items():
    try:
        thumbnail_formats = ['maxresdefault', 'sddefault', 'hqdefault']
        image_found = False

        for thumbnail_format in thumbnail_formats:
            image_url = f'https://img.youtube.com/vi/{video_id}/{thumbnail_format}.jpg'
            save_path = os.path.join(save_folder, f'{video_id}.jpg')

            try:
                urllib.request.urlretrieve(image_url, save_path)
                print(f"Downloaded thumbnail for video: {video_title}")
                image_found = True
                break
            except urllib.error.HTTPError:
                continue

        if not image_found:
            print(f"No available thumbnail for video: {video_title}")

    except Exception as e:
        print(f"An error occurred while downloading thumbnail for video: {video_title}")
        print(e)

print(f"Total videos: {len(videos)}")
print(f"Thumbnails retrieved: {len(os.listdir(save_folder))}")
