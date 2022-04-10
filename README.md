# RexDex Dependencies
Gathered dependencies for my projects

# How To Build
Use the provided scripts to build and package all libraries

```
build_linux.sh
build_windows.bat
```

# How To Build individual libs
All building is done via the build.py script, examples:

```
python3 build.py -p linux -l zlib build
```

Where:
-p selects platform (windows, linux, macos, etc)
-l selects project to build (if skipped ALL projects are affected)

Last argument specifies the action to run:
 pull - Get source code from git or other places
 configure - Run configuration script
 build - Build library
 deploy - Copy library artifacts

# Hacks
Not all libraries can be always build directly from sources, in that case some override files are placed in the "hacks" folder. Those files are modified copies of original files changed to get the project to compile. 

# Known Issues
1) There are dependencies between libraries that require some of them to be built and deployed before other starts building, notable example is the zlib and the mbedtls that must be compiled and deployed first before any other libs can be built.

2) Hack files must be kept up to date manually

3) Probably we are outputting way to many artifacts for LLVM project.
