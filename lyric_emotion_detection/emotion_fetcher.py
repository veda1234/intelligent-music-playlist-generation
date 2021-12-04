import torch
import numpy as np
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
import torch.nn.functional as F
from transformers import BertTokenizer, BertConfig,AdamW, BertForSequenceClassification,get_linear_schedule_with_warmup

import os
import sys
cur_dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(cur_dir_path)
model = BertForSequenceClassification.from_pretrained('{0}/model'.format(cur_dir_path))
tokenizer = BertTokenizer.from_pretrained('{0}/tokenizer'.format(cur_dir_path))
import traceback 
from lyric_scrapper import get_lyrics

## emotion labels
label2int = {
  "sadness": 4,
  "joy": 2,
  "anger": 0,
  "fear": 1,
  "love": 3,
  "surprise": 5
}
MAX_LEN = 256


def get_lyric_emotion(lyrics):
    try:
        input_id = tokenizer.encode(lyrics, add_special_tokens=True,max_length=MAX_LEN,padding='max_length', truncation=True)
        attention_mask = [int(i>0) for i in input_id]
        input_id = torch.unsqueeze(torch.LongTensor(input_id),0)
        attention_mask = torch.unsqueeze(torch.LongTensor(attention_mask),0)
        int2label = {v: k for k, v in label2int.items()} 
        with torch.no_grad():
            logits = model(input_id, token_type_ids=None, attention_mask=attention_mask)
            pred_flat = np.argmax(logits[0].to('cpu').numpy(), axis=1).flatten()
        return int2label[pred_flat[0]]
    except:
        print("error while detecting emotion for lyrics")
        raise

def get_song_emotion(song_name, artist_name):
    try:
        lyrics = get_lyrics(song_name, artist_name)
        if lyrics:
            return { 'lyrics': lyrics, 'emotion': get_lyric_emotion(lyrics) }
        else:
            return None
    except:
        print("error occured while fetching emotion of song {0} by {1}".format(song_name, artist_name))
        traceback.print_exc()
        raise

if __name__ == '__main__':
    song_name = input("Enter song name : ")
    artist_name = input("Enter artist name : ")
    print(get_song_emotion(song_name, artist_name))