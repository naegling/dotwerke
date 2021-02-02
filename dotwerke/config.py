# -*- coding: utf-8 -*-

import os.path
import json

class ConfigReader(object):
  """
  dotwerke configuration file reader.
  """
  def __init__(self, config_file_path):
    self._config = self._read(config_file_path)

  def _read(self, config_file_path):
    """
    Reads the specified configuration file.

    :param config_file_path: The path to the configuration file to read
    :return: The read configuration data
    """
    try:
      with open(config_file_path) as infile:
        data = json.load(infile)
        return data
    except Exception as e:
      raise ReadingError('Could not read config file:\n{}'.format(e))


  def get_config(self):
    """
    Gets the dotwerke configuration data.

    :return: The read dotwerke configuration data
    """
    return self._config


class ReadingError(Exception):
    pass
