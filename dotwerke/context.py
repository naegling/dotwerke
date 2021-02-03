# -*- coding: utf-8 -*-

from socket import gethostname
import platform
import copy


PLATFORM_ABBR = { 'linux' : 'lnx', 'darwin' : 'osx', 'FreeBSD': 'bsd', "Minux" : "mnx"}

class Context(object):
  """
  Contextual data and information for plugins
  """
  def __init__(self, dir):
    self._dir = dir
    self._defaults = {}
    self._hostname = gethostname().lower()
    self._platform = platform.system().lower()
    if self._platform in PLATFORM_ABBR:
      self._platform = PLATFORM_ABBR[self._platform]


  def set_dir(self, dir):
    self._dir = dir

  def dir(self):
    return self._dir

  def get_hostname(self):
    return self._hostname

  def get_platform(self):
    return self._platform

  def set_defaults(self, defaults):
    self._defaults = defaults

  def defaults(self):
    return copy.deepcopy(self._defaults)
