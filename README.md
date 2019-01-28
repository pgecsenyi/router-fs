# FST

FST (File System Transformer) allows you to create different views for directories. It can transform paths on-the-fly based on regular expressions.

## How does it work?

FST makes use of FUSE to implement filesystems in user mode that provide access to your files through paths defined in the configuration file. It can handle several different source directories and mount points simultaneously.

Each source directory and the corresponding mount point constitutes a _volume_. For each volume you can declare regular expression pairs that define how file paths will be transformed.

For example, let's suppose you have a directory `doc` with the following contents.

    food/
      fruits/
        content/
          apple.md
          banana.odt
        draft/
          cherry.md
      vegetables/
        content/
          aubergine.txt

Then you define the following transformation rules for this volume.

    "from_path": ".*/(?P<title>[^/]+)/(?P<category>[^/]+)/content/(?P<filename>.+)\\.(?P<extension>md|odt|txt)$",
    "to_path": "cyclopaedia/\\g<title> [\\g<category>]/\\g<filename>.\\g<extension>"

In this case you will get a virtual filesystem with the following structure.

    cyclopaedia/
      food [fruits]/
        apple.md
        banana.odt
      food [vegetables]/
        aubergine.txt

## System requirements

A modern Linux operating system is required with Python 3.6 (or later) and Pipenv installed.

## Installation and usage

  1. Copy the contents of the folder `src` to a location of your choice.
  2. Navigate to the installation folder in the _Terminal_.
  5. Run the following command.

    python -m pipenv install

  4. Generate a sample configuration file using the following command. Substitute `../data/config.json` with any path you like.

    python -m pipenv run python main.py -i -c ../data/config.json

  5. Edit the configuration file.
  6. You can execute the application with the following command.

    python -m pipenv run python main.py -c ../data/config.json

If you would like to enable other users to access the mounted filesystem, please specify the `allow_other` option in the configuration file for the given volume as well as the `user_allow_other` option in the `/etc/fuse` global configuration file. In case of transformed filesystems with the same mount point, you will have to enable this option for all affected volumes.

## Development

Install developer dependencies first by running the following command.

    python -m pipenv install --dev

_Visual Studio Code_ can be used to debug the application. In order to do that you will first need to configure the path of the Python interpreter in `.vscode/settings.json`. A sample file is provided you (`.vscode/settings_sample.json`). You can only debug one FUSE filesystem at a time.

### Environment

  * Ubuntu 18.04.1
  * Python 3.6.7, pip 9.0.1, Pipenv 8.3.2
  * Visual Studio Code 1.30.2
