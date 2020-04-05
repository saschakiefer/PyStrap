# PyStrap

A script to bootstrap a minimal macOS development system. Big thanks to [Mike McQuaid](https://mikemcquaid.com) for his scripts! This is my port to python with some extensions.

This script works together with my [dotfiles](https://github.com/saschakiefer/dotfiles) repository.

## Features

- Disables Java in Safari (for better security)
- Enables the macOS screensaver password immediately (for better security)
- Enables the macOS application firewall (for better security)
- Adds a `Found this computer?` message to the login screen (for machine recovery)
- Enables full-disk encryption and saves the FileVault Recovery Key to the Desktop (for better security)
- Installs the Xcode Command Line Tools (for compilers and Unix tools)
- Agree to the Xcode license (for using compilers without prompts)
- Does some Finder, Dock & Menu Items setup
- Does some Keyboard Setup for editors (i.e. disable key hold and increase repeat speed )
- Enable auto update
- Installs [Homebrew](http://brew.sh) (for installing command-line software)
- Installs [Homebrew Bundle](https://github.com/Homebrew/homebrew-bundle) (for `bundler`-like `Brewfile` support)
- Installs [Homebrew Services](https://github.com/Homebrew/homebrew-services) (for managing Homebrew-installed services)
- Installs [Homebrew Cask](https://github.com/caskroom/homebrew-cask) (for installing graphical software)
- Installs the latest macOS software updates (for better security)
- Installs dotfiles from a user's `https://github.com/<username>/dotfiles` repository and runs `script/setup` to configure them.
- Runs postprocessing script `script/do-postprocessing` to do additional configurations after everything is installed
- Installs software from a user's `Brewfile` in their `https://github.com/username/homebrew-brewfile` repository or `.Brewfile` in their home directory.
- A simple web application to set Git's name, email and GitHub token (needs authorized on any organisations you wish to access)
- Idempotent

## Out of Scope Features

- Enabling any network services by default (instead enable them when needed)
- Installing Homebrew formulae by default for everyone in an organisation (install them with `Brewfile`s in project repositories instead of mandating formulae for the whole organisation)
- Opting-out of any macOS updates (Apple's security updates and macOS updates are there for a reason)
- Disabling security features (these are a minimal set of best practises)
- Add phone number to security screen message (want to avoid prompting users for information on installation)

## Usage

Open [https://pystrap.herokuapp.com/](https://pystrap.herokuapp.com/) in your web browser.

Instead, to deploy to [Heroku](https://www.heroku.com) click:

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## Web Application Configuration Environment Variables

- `GITHUB_KEY`: the GitHub.com Application Client ID.
- `GITHUB_SECRET`: the GitHub.com Application Client Secret.
- `APP_SECRET`: the secret used for cookie session storage.

## Status

Stable and in active development.

## License

Licensed under the [MIT License](http://en.wikipedia.org/wiki/MIT_License).
The full license text is available in [LICENSE.txt](https://github.com/saschakiefer/PyStrap/blob/master/LICENSE).
