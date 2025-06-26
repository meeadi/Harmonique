# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Colab widgets for Magenta RT."""

import base64
import concurrent.futures
import functools
import importlib
import uuid
import ipywidgets as ipw
import numpy as np
import resampy
from . import utils

colab = importlib.import_module('google.colab')


class Prompt:
  """Text prompt widget.

  This widget allows to input a text prompt, a slider value and a text value
  linked to the slider.
  """

  def __init__(self):
    self.slider = ipw.FloatSlider(
        value=0,
        min=0,
        max=2,
        step=0.001,
        readout=False,
        layout=ipw.Layout(
            display='flex',
            width='auto',
            flex='16 1 0%',
        ),
    )
    self.text = ipw.Text(
        value='',
        placeholder='Enter a style',
        layout=ipw.Layout(
            display='flex',
            width='auto',
            flex='16 1 0%',
        ),
    )
    self.label = ipw.FloatText(
        value=0,
        disabled=False,
        layout=ipw.Layout(
            display='flex',
            width='4em',
        ),
    )
    ipw.link((self.slider, 'value'), (self.label, 'value'))

  def get_widget(self):
    """Shows the widget in the current cell."""
    return ipw.HBox(
        children=[
            self.text,
            self.slider,
            self.label,
        ],
        layout=ipw.Layout(display='flex', width='50em'),
    )

  @property
  def prompt_value(self):
    return self.text


class AudioPrompt(Prompt):
  """Audio prompt widget.

  This widget allows to upload an audio file, a slider value and a text value
  linked to the slider.
  """

  def __init__(self):
    super().__init__()
    utils._load_js('static/js/upload_audio.js')  # pylint: disable=protected-access

    self.upload_button = ipw.Button(
        value='Upload',
        description='Upload audio file',
        layout=ipw.Layout(
            display='flex',
            width='auto',
            flex='16 1 0%',
        ),
    )
    callback_name = f'notebook.uploadAudio/{uuid.uuid4()}'

    self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    colab.output.register_callback(
        callback_name,
        functools.partial(self.executor.submit, self.audio_callback),
    )

    def _on_click(*args, **kwargs):
      del args, kwargs
      utils._call_js('uploadAudio', callback_name)  # pylint: disable=protected-access

    self.upload_button.on_click(_on_click)
    self.value = None
    self.parameter_callback = None

  def observe(self, callback):
    self.parameter_callback = callback

  def audio_callback(
      self, filename: str, audio_data_b64: str, sample_rate: int, **kwargs
  ):
    """Callback for audio upload."""
    del kwargs
    x = np.frombuffer(base64.b64decode(audio_data_b64), dtype=np.float32)
    x = x.copy()

    self.upload_button.description = filename
    audio = resampy.resample(x, sample_rate, 16_000)
    if self.parameter_callback is None:
      return

    self.parameter_callback(dict(name='value', new=audio))

  def get_widget(self):
    """Shows the widget in the current cell."""
    return ipw.HBox(
        children=[
            self.upload_button,
            self.slider,
            self.label,
        ],
        layout=ipw.Layout(display='flex', width='50em'),
    )

  @property
  def prompt_value(self):
    return self


def area(name: str, *childrens: ipw.Widget) -> ipw.Widget:
  """Groups multiple widgets inside a box with an explicit label.

  Args:
    name: label to display
    *childrens: list of ipw.Widget to display

  Returns:
    An ipw.Widget containing all childrens.
  """
  return ipw.Box(
      children=[ipw.HTML(f'<h3>{name}</h3>')] + list(childrens),
      layout=ipw.Layout(
          border='solid 1px',
          padding='.2em',
          margin='.2em',
          display='flex',
          flex_flow='column',
      ),
  )
