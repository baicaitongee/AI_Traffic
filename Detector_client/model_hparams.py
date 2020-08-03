
"""Hyperparameters for the object detection model in TF.learn.

This file consolidates and documents the hyperparameters used by the model.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf


def create_hparams(hparams_overrides=None):
  """Returns hyperparameters, including any flag value overrides.

  Args:
    hparams_overrides: Optional hparams overrides, represented as a
      string containing comma-separated hparam_name=value pairs.

  Returns:
    The hyperparameters as a tf.HParams object.
  """
  hparams = tf.contrib.training.HParams(
      # Whether a fine tuning checkpoint (provided in the pipeline config)
      # should be loaded for training.
      load_pretrained=True)
  # Override any of the preceding hyperparameter values.
  if hparams_overrides:
    hparams = hparams.parse(hparams_overrides)
  return hparams
