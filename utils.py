import whisper
import json
import pandas as pd
from pytube import YouTube

def get_audio_from_video(url: str, file_name: str=None):
    """Obtains an audio file from a YouTube video

    Parameters:
        url (str): The URL of the video
        file_name (str): The name to be given to the file to be downloaded. Default None
    """
    print('[+] Process initiated')
    try:
        print(f'[+] Getting video from {url}')
        yt = YouTube(url)
        print(f'[+] Title: {yt.title}')
        print('[+] Getting audio...')
        streams = yt.streams.filter(only_audio=True)
        streams[0].download('./tmp', filename=file_name)
        print('[+] Successfully obtained audio!')
    except:
        print(f'[!] Something went wrong in getting the video: {url}')
  
def get_audio_from_videos(url_list: list):
    """Obtains audio files for multiple YouTube videos

    Parameters:
        url_list (list(str)): The list of URLs of the videos to download
    """

    print(f'[+] {len(url_list)} videos will be downloaded')
    for url in url_list:
        get_audio_from_video(url)
    print(f'[+] Videos have been successfully obtained')

def get_transcription(file: str, model, language: str=None) -> str:
    """Generates the transcription of an audio file

    Parameters:
        file (str): The path to the audio file to transcribe
        model: The Whisper model to be used to perform transcription
        language (str): The ISO code of the audio language. Default None
    Returns:
        transcription (str): Transcript generated for the audio file
    """

    try:
        print(f'[x] Performing transcription of {file}...')
        text = model.transcribe(file, language=language)
        print('[x] Transcription created!')
        return text['text']
    except:
        print(f'[!] Something went wrong when transcribing {file}')

def get_transcriptions(file_list: list, model, language: str=None) -> dict:
    """Generate transcripts for multiple audio files

    Parameters:
        file_list (list(str)): The path to the audio files to transcribe
        model: The Whisper model to be used to perform transcription
        language (str): The ISO code of the audio language. Default None
    Returns:
        transcriptions (dict): A dictionary with the name of the transcribed file as key and the transcription text as value
    """

    transcriptions = dict()
    print(f'[+] Making transcriptions of {len(file_list)} files')
    for file in file_list:
        text = get_transcription(file, model, language=language)
        transcriptions[file] = text
    return transcriptions

def get_segments_df(file: str, model, language: str=None):
    """Generate a Pandas dataframe with text information divided into segments.
    
    Parameters:
        file (str): The file to transcribe
        model: The Whisper model instance
        language (str): the file language. Default None
    Returns:
        df (dataframe): A Pandas dataframe with the information
    """
    try:
        print(f'[+] Performing transcription of {file}...')
        text = model.transcribe(file, language=language)
        print('[+] Transcription created!')
        segments_dict = {
            'id': [],
            'start': [],
            'end': [],
            'text': [],
            'tokens': []
        }
        for segment in text['segments']:
            segments_dict['id'].append(segment['id'])
            segments_dict['start'].append(segment['start'])
            segments_dict['end'].append(segment['end'])
            segments_dict['text'].append(segment['text'].strip())
            segments_dict['tokens'].append(segment['tokens'])
        
        return pd.DataFrame.from_dict(segments_dict)
    except:
        print(f'[!] Something went wrong when transcribing {file}')


def write_json_file(transcriptions_dict: dict, file_name: str):
    """Saves the dictionary with the transcriptions in a json file format
    
    Parameters:
        transcriptions (dict): A dictionary with the name of the transcribed file as key and the transcription text as value
        file_name (str): The name of the file to be created
    """
    try:
        with open(file_name, 'w') as f:
            f.write(json.dumps(transcriptions_dict))
        print(f'[+] File successfully created in {file_name}')
    except:
        print(f'[!] File could not be created in {file_name}')
