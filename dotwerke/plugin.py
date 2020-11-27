# -*- coding: utf-8 -*-

from .logging import Logger
from .context import Context


class Plugin(object):
  """
  A abstract base class for plugins that process directives.
  """
  def __init__(self, context):
    self._context = context
    self._log = Logger()

  def get_actions(self):
    """
    Returns a list of actions handled by this pluggin.

    :return: List of actions
    """
    raise NotImplementedError

  def do_handle(self, action, data):
    """
    Handles the data of the specified directive.

    :param directive: The directive to handle the data of
    :param data: The data to handle
    :return: True if the directive has been handled successfully
    """
    raise NotImplementedError
