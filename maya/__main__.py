from os import makedirs
from tqdm import tqdm

from pytube.contrib.playlist import Playlist
from pytube import YouTube
from click import group, option, argument


@group()
def main():
    pass


@main.command()
@argument('playlist', type = str)
@option('--output-path', '-o', type = str, required = True)
@option('--authenticate', '-a', is_flag = True)
@option('--audio', '-u', is_flag = True)
@option('--bit-rate', '-b', type = int, default = 160)
def pull(playlist: str, output_path: str, authenticate: bool, audio: bool, bit_rate: int):
    playlist = Playlist(playlist)
    # youtube = YouTube('https://www.youtube.com/watch?v=FqKAlH-4F70')
    # yt = YouTube('https://www.youtube.com/watch?v=FqKAlH-4F70', use_oauth = authenticate, allow_oauth_cache = True)
    # playlist = ['https://www.youtube.com/watch?v=FqKAlH-4F70']

    abr = f'{bit_rate}kbps' if audio else None

    for url in tqdm(playlist, desc = 'Downloading media from playlist'):
        yt = YouTube(url, use_oauth = authenticate, allow_oauth_cache = True)

        makedirs(output_path, exist_ok = True)

        # print(yt.title)
        if audio:
            (
                yt.streams
                .filter(only_audio = True, abr = abr)
                .first()
                .download(output_path = output_path, filename = f'{yt.title}.mp3')
            )
        else:
            (
                yt.streams
                .filter(progressive = True, file_extension = 'mp4')
                .order_by('resolution')
                .desc()
                .first()
                .download(output_path = output_path, filename = f'{yt.title}.mp4')
            )

    # print(len(playlist))


if __name__ == '__main__':
    main()
