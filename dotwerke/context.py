# -*- coding: utf-8 -*-

import copy


class Context(object):
  """
  Contextual data and information for plugins
  """
  def __init__(self, dir):
    self._dir = dir
    self._defaults = {}
    pass

  def set_dir(self, dir):
    self._dir = dir

  def dir(self):
    return self._dir

  def set_defaults(self, defaults):
    self._defaults = defaults

  def defaults(self):
    return copy.deepcopy(self._defaults)
