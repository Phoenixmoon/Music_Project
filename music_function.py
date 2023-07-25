# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


import numpy as np
from pydub import AudioSegment
import pandas as pd


xlpath = '/Users/joannazhang/Documents/notesheets.xlsx'
df_note_length = pd.read_excel(xlpath, sheet_name="note_length")

csv_path = '/Users/joannazhang/Downloads/note_frequency.csv'
df = pd.read_csv(csv_path)

AudioSegment.converter = '/opt/homebrew/bin/ffmpeg'

def note_creator(base_frequency, bands=4, energy_decreaser=0.5, sr=44100, note_length=10): #triple quote to allow adding explanation to function - docstring
    x = np.linspace(start=0, stop=note_length, num=sr * note_length, dtype="float")
    y = np.zeros_like(x)
    for i in range(bands):
        y += np.sin(np.pi * base_frequency * 2 * (i + 1)* x) * 0.33**i
    y_adjusted = y / np.max(y)
    return y_adjusted


def create_music(file_path, output_mp3, tempo=60, sr=44100): # tempo in bpm
    # defining vars:
    for i, note in df.iterrows():
        locals()[note['note']] = note_creator(note['frequency'])
        for _, row in df_note_length.iterrows():
            locals()[note['note']+"_"+row['name']] = locals()[note['note']][0: int(sr * row['tempo']/tempo)]

    for _, row in df_note_length.iterrows():
        locals()[row['name']+'_rest'] = np.zeros(sr * int(row['tempo']/tempo))

    sep = np.zeros(10)
    rest = np.zeros(1000)

    with open(file_path) as file:
        txt = file.read()
        txt.strip()
        notes = txt.strip().split(", ")
        notes2 = []
        for s in notes:
            x = locals().get(s, np.array([]))  # locals retrieves all previously defined variables
            if len(x):
                notes2.append(x)
            else:
                print(f'Note not found. Possible typo: {s}')
                notes2.append(rest)
        array = np.concatenate(notes2)
        scaled_data = np.int16(array / np.max(np.abs(array)) * 32767)
        audio_segment = AudioSegment(scaled_data, frame_rate=sr, sample_width=2, channels=1)

        audio_segment.export(output_mp3, format="mp3")  # save as mp3




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    create_music('new.txt', 'output1.mp3', tempo=120)