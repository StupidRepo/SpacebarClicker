# Spacebar Clicker
A free and fun game made in [Python][py], using the [`pygame`][pg] library.
## Description
Think of Cookie Clicker, but you have to press your space(bar) key to get 'spaces' (which are like cookies, but Spacebar Clicker's version).
## Custom In-Game Statuses
You can make your own in-game statuses by editing the `assets/core/descriptions.json` file.
Formatting goes as follows:
```
{clicks} - how many spaces you have
{cpc} - how many spaces you get per click
{chanceToClick} - the chance to get a space (hard mode only)
{version} - the current version of the game
{space} - is either 'spaces' if you have more than 1 space, or 'space' if you have 1 space
{intlimit} - the limit of an integer
{untilintlimit} - the amount of spaces until you reach the integer limit
```
## Installing
Warning: Most files here haven't been made yet. Wait until next commit or something.
### macOS
Download the latest [build][rel] of the game and run the `.app` file.
### Windows
Download the [source code][source], extract it, and run the `run_windows.bat` file.
You will need Python 3 installed on your computer to run the game.
### Linux
Same as Windows, but run `run_linux.sh` instead.
Just like Windows, you will need Python 3 installed on your computer to run the game.
## Building
### macOS
Download the [source code](https://github.com/StupidRepo/SpacebarClicker/archive/refs/heads/main.zip), extract it, and run the `build_macos.sh` file.
You will need Python 3 installed on your computer to build the game.
### Windows
Same as macOS, but run `build_windows.bat` instead.
### Linux
Same as Windows, but run `build_linux.sh` instead.
## Contributing
I recommend you contribute to the game, as it's made in Python and the code is pretty simple. You can contribute by making forking the repository, making your changes and then making a pull request.
## Credits/Contributors
- Bradlee Barnes ([StupidRepo][bb-sr])
## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE.md) file for more information.

[py]: https://www.python.org/
[pg]: https://www.pygame.org/
[source]: https://github.com/StupidRepo/SpacebarClicker/archive/refs/heads/main.zip
[rel]: https://github.com/StupidRepo/SpacebarClicker/releases/latest
[bb-sr]: https://github.com/StupidRepo/