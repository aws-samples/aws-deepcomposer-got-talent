# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import os
import sys
import glob
import argparse
import pickle

import numpy as np
import matplotlib.pylab as plt
import torch
from torch.nn import Softmax

from pypianoroll.track import Track
import pypianoroll as piano
from pypianoroll import Multitrack

from model import CNN
from scipy import stats

## Input: array of MIDI files
## Output: corresponding similarity score

def sample_midi(midi, offset=0, step=2, bar_num=8, bar_len=96, num_samples=1):
    '''
    Sample fixed length from midi file
    8 bars = 768 -> 1 bar = 96
    '''
    
    samples = []
    
    count = 0
    total_midi_len = len(midi)
    sample_len = bar_num * bar_len
    
    while count < num_samples:
        # Beginning timestep of new sample
        cur_begin = count * step * bar_len + offset
        if cur_begin + sample_len <= total_midi_len:
            samples.append(midi[cur_begin : cur_begin + sample_len])
            count += 1
        else:
            break
    
    return samples
    

def load_model(gpu=False):
    '''Load pretrained pytorch model'''
    model = CNN()
    model = model.double()
    model.load_state_dict(torch.load('pretrained_model'))
    if gpu:
        model = model.cuda()
        
    return model

def load_midi(file):
    '''
    Load single midi file
    
    Return:
    List containting a single midi in shape [768, 128]
    '''
    try:
        midi = piano.read(file)
    except ValueError:
        print("Midi file does not exist")
        
    # Binarize merged track
    merged = midi.blend(mode='sum')
    binary = np.array(merged > 0).astype(int)
    # Sample beginning of the 8 bars if input too long
    sample = sample_midi(binary)
    
    return sample, file.split('/')[-1]
        
    
def load_midi_folder(path):
    '''
    Load all midi files in specified folder
    
    Arguments:
    path : folder path containing midi files
    
    Return:
    midi: list of midi files in shape [768, 128]
    '''
    midi_list = []
    midi_name = []
    
    for f in glob.glob(path + '*.mid'):
        print(f)
        sample, name = load_midi(f)
        # Skip if input midi does not have at least 8 bars
        if not sample:
            print(f'File {f} does not have at least 8 bars! Exiting..')
            continue
        midi_list.append(sample[0])
        midi_name.append(name)
       
    return midi_list, midi_name

def get_class_score(midis, model):
    '''Get classification score to bach music on selected midis'''
    sm = Softmax(dim=1)
    outputs = model(midis)
    probs = sm(outputs)
    scores = (probs[:,1] - probs[:,0] + 1) * 50
    return scores

def pch(track):
    '''Get the pitch density of a track'''
    density = []

    for i in range(track.shape[1]):
        density.extend([i] * int(np.sum(track[:, i])))
    
    return density


def get_ks_dist(midis, bach_pdf):
    '''Calculate KS similarity'''
    ks = []
    for midi in midis:
        midi = midi[0, :, :]
        density = pch(midi)
        d, p = stats.ks_2samp(density, bach_pdf)
        ks.append(d)
    return ks

def combine_score(cls_score, ks_dist, w=0.5):
    '''Combine classification score and KS distance to construct final score'''
    final_score = []
    for s, d in zip(cls_score, ks_dist):
        score = (w * s / 100 + (1 - w) * (1 - d)) * 100
        final_score.append(score)
    
    return final_score


def parse_args():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--midi_file', type=str, dest='midi_file')
    group.add_argument('--midi_folder', type=str, dest='midi_folder')
    parser.add_argument('--save_path', type=str, dest='save_path')
    args = parser.parse_args()

    # test arguments
    if not args.midi_folder and not args.midi_file:
        assert 0, print("Please specify the midi file or a folder of midi files")

    return args

def main():
    gpu = False
    batch_size = 8
    num_workers = 2
    f_names = None
    
    # load bach pdf
    bach_pdf = pickle.load(open('bach_pdf.p', 'rb'))
    
    # load midi files
    args = parse_args()
    save_path = args.save_path
    if args.midi_file:
        f = args.midi_file
        midi, f_names = load_midi(f)
    elif args.midi_folder:
        path = args.midi_folder
        print(path)
        midi, f_names = load_midi_folder(path)
        print('Loaded files from folder.')
        print('Files: ', f_names)
    print(f'Midi file is loaded! There are {len(midi)} tracks')
    
    # If no track
    if len(midi) == 0:
        print('No midi files to calculate score')
        sys.exit()
    
    if torch.cuda.is_available():
        gpu = True
       
    # load model
    model = load_model(gpu)
    print('Model is loaded!')
    
    # transform and merge track
    midi_ready = np.array(midi, dtype=float)
    midi_ready = torch.tensor(np.expand_dims(midi_ready, axis=1))
    midi_loader = torch.utils.data.DataLoader(
        midi_ready,
        batch_size=batch_size,
        num_workers=num_workers,
        shuffle=False
    )
    
    final_scores = []
    
    for midi_set in midi_loader:
        # calculate classification score and KS distance
        np_midi_set = midi_set.numpy()
        ks_dist = get_ks_dist(np_midi_set, bach_pdf)
        if gpu:
            midi_set = midi_set.to('cuda')
        cls_score = get_class_score(midi_set, model)
        cls_score = cls_score.cpu().detach().numpy()
        
        # combine score together to output the final score
        combined_score = combine_score(cls_score, ks_dist)
        final_scores.extend(combined_score)
    
    # Write the final scores to output csv
    output = {f:s for f,s in zip(f_names, final_scores)}
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    pickle.dump(output, open(save_path + 'score_results.p', 'wb'))
    print(f'Calculation is completed! Scores are saved at {save_path}')
    
if __name__ == '__main__':
    main()
    
    
    
