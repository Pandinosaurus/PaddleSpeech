# Copyright (c) 2021 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import collections
import os
from typing import List
from typing import Tuple

from ..utils.download import download_and_decompress
from ..utils.env import DATA_HOME
from .dataset import AudioClassificationDataset

__all__ = ['ESC50']


class ESC50(AudioClassificationDataset):
    """
    The ESC-50 dataset is a labeled collection of 2000 environmental audio recordings
    suitable for benchmarking methods of environmental sound classification. The dataset
    consists of 5-second-long recordings organized into 50 semantical classes (with
    40 examples per class)

    Reference:
        ESC: Dataset for Environmental Sound Classification
        http://dx.doi.org/10.1145/2733373.2806390
    """

    archives = [
        {
            'url':
            'https://paddleaudio.bj.bcebos.com/datasets/ESC-50-master.zip',
            'md5': '7771e4b9d86d0945acce719c7a59305a',
        },
    ]
    label_list = [
        # Animals
        'Dog',
        'Rooster',
        'Pig',
        'Cow',
        'Frog',
        'Cat',
        'Hen',
        'Insects (flying)',
        'Sheep',
        'Crow',
        # Natural soundscapes & water sounds
        'Rain',
        'Sea waves',
        'Crackling fire',
        'Crickets',
        'Chirping birds',
        'Water drops',
        'Wind',
        'Pouring water',
        'Toilet flush',
        'Thunderstorm',
        # Human, non-speech sounds
        'Crying baby',
        'Sneezing',
        'Clapping',
        'Breathing',
        'Coughing',
        'Footsteps',
        'Laughing',
        'Brushing teeth',
        'Snoring',
        'Drinking, sipping',
        # Interior/domestic sounds
        'Door knock',
        'Mouse click',
        'Keyboard typing',
        'Door, wood creaks',
        'Can opening',
        'Washing machine',
        'Vacuum cleaner',
        'Clock alarm',
        'Clock tick',
        'Glass breaking',
        # Exterior/urban noises
        'Helicopter',
        'Chainsaw',
        'Siren',
        'Car horn',
        'Engine',
        'Train',
        'Church bells',
        'Airplane',
        'Fireworks',
        'Hand saw',
    ]
    meta = os.path.join('ESC-50-master', 'meta', 'esc50.csv')
    meta_info = collections.namedtuple(
        'META_INFO',
        ('filename', 'fold', 'target', 'category', 'esc10', 'src_file', 'take'))
    audio_path = os.path.join('ESC-50-master', 'audio')

    def __init__(self,
                 mode: str='train',
                 split: int=1,
                 feat_type: str='raw',
                 **kwargs):
        """
        Args:
            mode (:obj:`str`, `optional`, defaults to `train`):
                It identifies the dataset mode (train or dev).
            split (:obj:`int`, `optional`, defaults to 1):
                It specify the fold of dev dataset.
            feat_type (:obj:`str`, `optional`, defaults to `raw`):
                It identifies the feature type that user wants to extract of an audio file.
        """
        files, labels = self._get_data(mode, split)
        super(ESC50, self).__init__(
            files=files, labels=labels, feat_type=feat_type, **kwargs)

    def _get_meta_info(self) -> List[collections.namedtuple]:
        ret = []
        with open(os.path.join(DATA_HOME, self.meta), 'r') as rf:
            for line in rf.readlines()[1:]:
                ret.append(self.meta_info(*line.strip().split(',')))
        return ret

    def _get_data(self, mode: str, split: int) -> Tuple[List[str], List[int]]:
        if not os.path.isdir(os.path.join(DATA_HOME, self.audio_path)) or \
            not os.path.isfile(os.path.join(DATA_HOME, self.meta)):
            download_and_decompress(self.archives, DATA_HOME)

        meta_info = self._get_meta_info()

        files = []
        labels = []
        for sample in meta_info:
            filename, fold, target, _, _, _, _ = sample
            if mode == 'train' and int(fold) != split:
                files.append(os.path.join(DATA_HOME, self.audio_path, filename))
                labels.append(int(target))

            if mode != 'train' and int(fold) == split:
                files.append(os.path.join(DATA_HOME, self.audio_path, filename))
                labels.append(int(target))

        return files, labels
