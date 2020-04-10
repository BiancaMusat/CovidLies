"""
Abstract base class for misconception detectors
"""
from typing import Any, Dict, List, Union

import numpy as np

from backend.ml.misconception import MisconceptionDataset


class Detector:
    """
    Abstract base class for a misconception detector.
    """
    def __init__(self):
        self._cache: Dict[str, Any] = {}

    def _encode(self, sentences: List[str]):
        raise NotImplementedError

    def _score(self, sentences, misconceptions) -> np.ndarray:
        raise NotImplementedError

    def score(self,
              sentences: Union[str, List[str]],
              misconceptions: MisconceptionDataset) -> np.ndarray:
        """
        Scores whether or not a given piece of text corresponds to a misconception.

        # Parameters
        sentences : str or List[str]
            The text to score. Can either be a string or a list of strings.
        misconceptions : MisconceptionDataset
            The misconceptions to score against.

        # Returns
        scores : np.ndarray
            An array with shape (num_sentences, num_misconceptions) containing the scores.
        """
        # encode misconceptions and cache to avoid needless recomputation.
        if misconceptions not in self._cache:
            self.cache_[misconceptions] = misconceptions
        encoded_misconceptions = self._cache[misconceptions]

        if isinstance(sentences, str):
            sentences = [sentences]
        encoded_sentences = self._encode(sentences)

        scores = self._score(encoded_sentences, encoded_misconceptions)
        return scores

    def refresh_cache(self) -> None:
        """
        Refresh (clear) the misconception cache.
        """
        self._cache = {}
