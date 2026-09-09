# ungoogled-chromium-windows (DLL-only build)

Windows packaging for [ungoogled-chromium](//github.com/Eloston/ungoogled-chromium) – **customized to produce only `chrome.dll` and its PDB symbol file**, without the full browser executable or installer. This is intended for debugging, integration testing, or embedding scenarios where only the core library is needed.

> **Note**: This repository is a derivative of the official [ungoogled-chromium-windows](https://github.com/ungoogled-software/ungoogled-chromium-windows) project. It **does not** produce a runnable Chromium browser. If you need the complete browser, please use the original project.

## Downloads

Since this build does not produce an installable browser, no binaries are published for end users. If you still require the output artifacts (ZIP containing `chrome.dll` and `chrome.dll.pdb`), they are available as GitHub Release assets attached to tags in this repository.

**For the official full-featured binaries**, visit the [Contributor Binaries website](//ungoogled-software.github.io/ungoogled-chromium-binaries/) or install via `winget install --id=eloston.ungoogled-chromium -e`.

## Building

This repository follows the same build environment setup as the original project, but the final build output is limited to `chrome.dll` and its PDB. The build steps are identical.

### Setting up the build environment

**IMPORTANT**: Please setup only what is referenced below. Do NOT setup other Chromium compilation tools like `depot_tools`, since we have a custom build process which avoids using Google's pre-built binaries.

#### Setting up Visual Studio

[Follow the "Visual Studio" section of the official Windows build instructions](https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/windows_build_instructions.md#visual-studio).

* Make sure to read through the entire section and install/configure all the required components.
* If your Visual Studio is installed in a directory other than the default, you'll need to set a few environment variables to point the toolchains to your installation path. (Copied from [instructions for Electron](https://electronjs.org/docs/development/build-instructions-windows))
	* `vs2019_install = DRIVE:\path\to\Microsoft Visual Studio\2019\Community` (replace `2019` and `Community` with your installed versions)
	* `WINDOWSSDKDIR = DRIVE:\path\to\Windows Kits\10`
	* `GYP_MSVS_VERSION = 2019` (replace 2019 with your installed version's year)


#### Other build requirements

**IMPORTANT**: Currently, the `MAX_PATH` path length restriction (which is 260 characters by default) must be lifted in for our Python build scripts. This can be lifted in Windows 10 (v1607 or newer) with the official installer for Python 3.11 or newer (you will see a button at the end of installation to do this). See [Issue #345](https://github.com/Eloston/ungoogled-chromium/issues/345) for other methods for older Windows versions.

1. Setup the following:
    * 7-Zip
    * Python 3.11 or above
		* Can be installed using WinGet or the Microsoft Store.
		* If you don't plan on using the Microsoft Store version of Python:
			* Check "Add python.exe to PATH" before install.
			* At the end of the Python installer, click the button to lift the `MAX_PATH` length restriction.
			* Disable the `python3.exe` and `python.exe` aliases in `Settings > Apps > Advanced app settings > App execution aliases`. They will typically be referred to as "App Installer". See [this question on stackoverflow.com](https://stackoverflow.com/questions/57485491/python-python3-executes-in-command-prompt-but-does-not-run-correctly) to understand why.
			* Ensure that your Python directory either has a copy of Python named "python3.exe" or a symlink linking to the Python executable.
		* The `httplib2` module at version 0.22.0. This can be installed using `pip install httplib2==0.22.0`.
    * Make sure to lift the `MAX_PATH` length restriction, either by clicking the button at the end of the Python installer or by [following these instructions](https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation?tabs=registry#:~:text=Enable,Later).
    * Git (to fetch all required ungoogled-chromium scripts)
        * During setup, make sure "Git from the command line and also from 3rd-party software" is selected. This is usually the recommended option.

### Building

Run in `Developer Command Prompt for VS` (as administrator):

```cmd
git clone --recurse-submodules https://github.com/your-fork/ungoogled-chromium-windows.git
cd ungoogled-chromium-windows
# Replace TAG_OR_BRANCH_HERE with a tag or branch name
git checkout --recurse-submodules TAG_OR_BRANCH_HERE
python3 build.py
python3 package.py
```

A ZIP archive containing only `chrome.dll` and `chrome.dll.pdb` will be created under `build`. No installer executable is produced.

**NOTE**: If the build fails, you must take additional steps before re-running the build:

* If the build fails while downloading the Chromium source code (which is during `build.py`), it can be fixed by removing `build\download_cache` and re-running the build instructions.
* If the build fails at any other point during `build.py`, it can be fixed by removing everything under `build` other than `build\download_cache` and re-running the build instructions. This will clear out all the code used by the build, and any files generated by the build.

An efficient way to delete large amounts of files is using `Remove-Item PATH -Recurse -Force`. Be careful however, files deleted by that command will be permanently lost.

## Developer info

The instructions for updating patches, dependencies, and Rust remain unchanged from the original project. Refer to the original [README](https://github.com/ungoogled-software/ungoogled-chromium-windows/blob/master/README.md) for detailed developer workflows.

## License

See [LICENSE](LICENSE)
