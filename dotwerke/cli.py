# -*- coding: utf-8 -*-

"""
The dotwerk CLI.

This is the main entry point of the public API.
"""
from argparse import ArgumentParser
import glob
import os

from .config import ConfigReader, ReadingError
from .dispatcher import Dispatcher, DispatchError
from .logging import Level
from .logging import Logger
from .util import module


def add_options(parser):
  """
  Adds all options to the specified parser.

  :param parser: The parser to add all options to
  :return: None
  """
  parser.add_argument('-Q', '--super-quiet', action='store_true', help='suppress almost all output')
  parser.add_argument('-q', '--quiet', action='store_true', help='suppress most output')
  parser.add_argument('-v', '--verbose', action='store_true', help='enable verbose output')
  parser.add_argument('-b', '--base-directory', default='.', dest='base', help='base directory of dotfiles repository (default=\'.\')', metavar='BASE_DIR')
  parser.add_argument('configs', nargs='*', help='dotwerke package configurations, relative to base (default=all)', metavar='PACKAGE_DIR')
  parser.add_argument('-p', '--plugin', action='append', dest='plugins', default=[], help='load PLUGIN as a plugin', metavar='PLUGIN')
  parser.add_argument('--disable-core-plugins', action='store_true', help='disable all core plugins')
  parser.add_argument('--plugin-dir', action='append', dest='plugin_dirs', default=[], metavar='PLUGIN_DIR', help='load all plugins in PLUGIN_DIR')


def read_config(config_file):
  """
  Reads the specified configuration file.

  :param config_file: The configuration file to read
  :return: The read configuration data
  """
  reader = ConfigReader(config_file)
  return reader.get_config()


def find_configs(base, filenames):
  """
  finds list of dotwerke configuration files

  :param base: The base directory to begin search
  :filename: The filename to search for
  :return: List of configuration files
  """
  result = []
  for root, subs, files in os.walk(base):
    for file in filenames:
      if file in files:
        result.append(os.path.join(root, file))
  return result


def main():
  """
  Processes all parsed options and hands it over to the dispatcher for each package configuration.

  :return: True if all tasks have been executed successfully, False otherwise
team  """
  log = Logger()
  try:
    cfg_filenames = ['dotwerke.json']
    parser = ArgumentParser()
    add_options(parser)
    options = parser.parse_args()

    if options.super_quiet:
      log.set_level(Level.WARNING)
    if options.quiet:
      log.set_level(Level.INFO)
    if options.verbose:
      log.set_level(Level.DEBUG)

    plugin_directories = list(options.plugin_dirs)
    if not options.disable_core_plugins:
      plugin_directories.append(os.path.join(os.path.dirname(__file__), "plugins"))
    plugin_paths = []
    for directory in plugin_directories:
      for plugin_path in glob.glob(os.path.join(directory, "*.py")):
        plugin_paths.append(plugin_path)
    for plugin_path in options.plugins:
      plugin_paths.append(plugin_path)
    for plugin_path in plugin_paths:
      abspath = os.path.abspath(plugin_path)
      module.load(abspath)

    configs = []
    if options.configs is None or len(options.configs) == 0:
      configs.extend(find_configs(options.base, cfg_filenames))
    else:
      for cfg in options.configs:
        found = False
        for file in cfg_filenames:
          if os.path.isfile(os.path.join(options.base, cfg, file)):
            configs.append(os.path.join(cfg, file))
            found = True
            break
        if not found:
          log.warning("dotwerke configuration file in \'{}\' not found".format(cfg))

    if len(configs) == 0:
      log.error("dotwerke configuration files not found")
      exit(1)

    for cfg in configs:
      log.info("running {}".format(cfg))
      tasks = read_config(os.path.join(options.base, cfg))

      if not isinstance(tasks, list):
        raise ReadingError("Failed to read configuration file \"{}\"".format(cfg))

      dispatcher = Dispatcher(os.path.join(options.base, os.path.split(cfg)[0]))
      success = dispatcher.dispatch(tasks)
      if success:
        log.info("All tasks succeeded")
      else:
        raise DispatchError("Some tasks failed")

  except (ReadingError, DispatchError) as e:
    log.error("{}".format(e))
    exit(1)
  except KeyboardInterrupt:
    log.error("Operation aborted")
    exit(1)
