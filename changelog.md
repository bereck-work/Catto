# Version Release 1.0.5
### Summary
This is the latest release of catto ( version `1.0.5` ) which has a lot of improvements, changes, major updates, 
and new features.
This will be the final release of catto, as most of the required improvements have been made, and tests are properly
written.

### Added
* Added `setup.cfg` file, for the new packaging conventions, as setup.py has been deprecated.
* Added `pytest.ini` file for pytest configuration.
* Running pytest will log the console output for the command that is being tested.
* Updated `LICENSE` from BSD-3-CLAUSE to `GNU` license.
* Moved the entire `catto` directory inside `src` directory as per python packaging convention.
* Created `changelog.md` for semantic versioning ( although this is not a good way to do that.)
* __Update__: Catto's help command has been upgraded as, `Typer` has been upgraded to version `0.6.1` featuring new UI changes.
* Test assertions have been improved greatly, and they also make assertion checks based on command output and more.
* Catto now uses `httpx` library to make API requests over using `requests`.
* Catto has a new command called `healthcheck` that tests catto's various features, incase a bug or some code error has been detected.
* Added a new file called `nox_testing.py` which uses `nox` for standalone testing.
* __Major Update__: Catto now uses python 3.11, and it requires python 3.11 to work.
* `show-all-animals` command has been renamed to `show-all-categories` and its corresponding code has been changed to reflect this change.

### Removed
* `requests` library has been removed.
* The commands that are tested using pytest and `Clirunner` object do not run in standalone mode.
* Removed `NoConnectionFoundException` class from exceptions.py.
* Removed the function `log` and enum `LogLevelEnum` and removed the creation of log files at application startup.



### Code Changes
* The functions attached to the command decorator now return command data, instead of returning None.
* Pytest functions now use regex to remove unnecessary ansi characters for better string search.
* The file with name `downloader.py` has been renamed to `api.py`.
* class `Client`'s attributes are now private.
* Loguru's logger object that was an attribute in class `Client` is now removed.
* `download` method of the class `Client` now returns a dictionary containing the name of the images that where saved and the path to directory as a pathlib.Path object.
* Renamed AnimalAPIEndpointEnum class to CategoryEnum in enums.py
* Removed exception NoConnectionFound as it has no uses and added `DataFetchFailed` and `ImageDownloadFailed` exceptions in exceptions.py
* Fixed a stupid bug in method `save_image_from_url` in class `Client`, where the hex code of the image that was saved is different and when it is returned as data in the dict, it was different, as it was called seperately and generated different hex value, now the hex value is generated once and is assigned to a variable.
* Rewrote the logic of function `interactive_print`.
* Changed `with underline` to `underline` in ColorEnum class.
