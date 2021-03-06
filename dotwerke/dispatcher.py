# -*- coding: utf-8 -*-

import os
from collections import defaultdict
from .plugin import Plugin
from .logging import Logger
from .context import Context


class Dispatcher(object):
  """
  Dispatches tasks to loaded plugins.
  """
  def __init__(self, dir, force):
    self._log = Logger()
    self._setup_context(dir)
    self._load_plugins(force)

  def _setup_context(self, dir):
    """
    Sets up the plugin context for the specified package.

    :param dir:  The directory of the package
    :return: The plugin context
    """
    path = os.path.abspath(os.path.realpath(os.path.expanduser(dir)))
    if not os.path.exists(path):
      raise DispatchError("Nonexistent package directory")
    self._context = Context(path)

  def dispatch(self, tasks):
    """
    Dispatches the specified tasks to the loaded plugins.

    :param tasks: The tasks to dispatch
    :return: True if all tasks have been handled by the loaded plugins successfully, False otherwise
    """
    success = True
    for task in tasks:
      for action in task:
        handled = False
        if action == "defaults":
          self._context.set_defaults(task[action])
          handled = True
        for plugin in self._plugins[action]:
          try:
            success &= plugin.do_handle(action, task[action])
            handled = True
          except Exception:
            self._log.error("An error was encountered while executing action \"{}\"".format(action))
        if not handled:
          success = False
          self._log.error("Action \"{}\" not handled".format(action))
    return success

  def _load_plugins(self, force):
    """
    Loads all found plugins.

    :return: None
    """
    self._plugins = defaultdict(lambda:[])
    for plugin in [plugin(self._context, force) for plugin in Plugin.__subclasses__()]:
      for action in plugin.get_actions():
        self._plugins[action].append(plugin)


class DispatchError(Exception):
  pass
