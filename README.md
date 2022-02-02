

# createurl

createurl is a Python command line application, which will create a browser independent bookmark file of a webpage.

## Demo


![Example](./readme_resources/termtosvg_jv2_awui.svg)





## Installation

Using the linux command line. Install createurl from github into a python virtual environment.

```bash
  cd ~
  python3 -m venv .venv        # create virtual environment
  source .venv/bin/activate    # activate environment
  python3 -m pip install git+https://github.com/mpflynnx/createurl.git     # install from git

```


## FAQ

#### So, I now have a file with extension .url, what can I do with it?

Sync the files to your Dropbox account and use the Dropbox app to have full access to your bookmarks on a mobile device, such as phone or tablet. The Dropbox app recognises the filetype and will open a browser tab at the webpage.


## Support

On Linux, this application makes use of the xsel command, which should come with the os. Otherwise run "sudo apt-get install xsel" or search your distrubutions package repository.

[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
[![AGPL License](https://img.shields.io/badge/license-AGPL-blue.svg)](http://www.gnu.org/licenses/agpl-3.0)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)
