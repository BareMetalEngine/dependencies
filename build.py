import sys
import os
import argparse
import contextlib
import subprocess
import shutil
import urllib.request 
import ssl
import tarfile
import zipfile

PLATFORMS = [ 'windows', 'linux' ]
COMMANDS = ['clone', 'pull', 'configure', 'build', 'deploy', 'package', 'clean', 'purge']

SOURCE_FOLDER = '.src'
BUILD_FOLDER = '.build'
OUTPUT_FOLDER = '.out'

########################

LIBRARY_ZLIB = {
    "name": "zlib",
    "repo": "https://github.com/madler/zlib.git",
    
    "config": "",
    "build": "--build . --config Release",
    "build_tool": "cmake",
    "platforms": PLATFORMS,

    "artifacts": [
        { 
            "type": "library", 
            "location": "build", 
            "platform": ["windows"],
            "files": ["Release/zlibstatic.lib"]
        },
        { 
            "type": "library", 
            "location": "build", 
            "platform": ["linux"],
            "files": ["libz.a"]
        },
        {
            "type": "header", 
            "location": "source", 
            "platform": PLATFORMS, # all platforms
            #"target_prefix_path": "zlib/", # most apps expect the zlib to be at "zlib/zlib.h"
            "files": ["zlib.h"]
        },
        {
            "type": "header", 
            "location": "build", 
            "platform": PLATFORMS, # all platforms
            #"target_prefix_path": "zlib/", # most apps expect the zlib to be at "zlib/zlib.h"
            "files": ["zconf.h"]
        }
    ]
}

LIBRARY_ZLIB_NG = {
    "name": "zlib_ng",
    "repo": "https://github.com/zlib-ng/zlib-ng.git",
    
    "config": "",
    "build": "--build . --config Release",
    "build_tool": "cmake",
    "platforms": PLATFORMS,

    "artifacts": [
        { 
            "type": "library", 
            "location": "build", 
            "platform": ["windows"],
            "files": ["Release/zlibstatic-ng.lib"]
        },
        { 
            "type": "library", 
            "location": "build", 
            "platform": ["linux"],
            "files": ["libz-ng.a"]
        },
        {
            "type": "header", 
            "location": "build", 
            "platform": PLATFORMS, # all platforms
            "files": ["zlib-ng.h"]
        }
    ]
}

LIBRARY_LZ4 = {
    "name": "lz4",
    "repo": "https://github.com/lz4/lz4.git",
    
    "config": "-DLZ4_BUILD_CLI=false -DLZ4_BUILD_LEGACY_LZ4C=false -DBUILD_STATIC_LIBS=true -DBUILD_SHARED_LIBS=false",
    "build": "--build . --config Release",
    "build_tool": "cmake",
    "custom_build_path": "build/cmake/",
    "platforms": PLATFORMS,

    "artifacts": [
        { 
            "type": "library", 
            "location": "build", 
            "platform": ["windows"],
            "files": ["Release/lz4.lib"]
        },
        { 
            "type": "library", 
            "location": "build", 
            "platform": ["linux"],
            "files": ["liblz4.a"]
        },
        {
            "type": "header", 
            "location": "source", 
            "platform": PLATFORMS, # all platforms
            "files": ["lib/lz4.h", "lib/lz4frame.h", "lib/lz4hc.h"],
            #"target_prefix_path": "lz4/", # most apps expect the zlib to be at "lz4/lz4.h"
        }
    ]
}


LIBRARY_FREETYPE = {
    "name": "freetype",
    "repo": "https://github.com/freetype/freetype.git",
    
    "config": "-D BUILD_SHARED_LIBS=false -D CMAKE_BUILD_TYPE=Release",
    "build": "--build . --config Release",
    "build_tool": "cmake",
    "platforms": PLATFORMS,
    
    "dependencies": [
        {
            "enabled": False,
            "type": "cmake",
            "lib": "zlib",
            "lib_var": "ZLIB_LIBRARY",
            "include_var": "ZLIB_INCLUDE_DIR",
        }
    ],
    
    "artifacts": [
        { 
            "type": "library", 
            "location": "build", 
            "platform": ["windows"],
            "files": ["Release/freetype.lib"]
        },
        { 
            "type": "library", 
            "location": "build", 
            "platform": ["linux"],
            "files": ["libfreetype.a"]
        },
        {
            "type": "header", 
            "location": "source", 
            "platform": PLATFORMS, # all platforms
            "dirs": ["include"]
        },
        {
            "type": "header", 
            "location": "build", 
            "platform": PLATFORMS, # all platforms
            "dirs": ["include"]
        }
    ]
}

LIBRARY_FREEIMAGE = {
    "name": "freeimage",
    "repo": "https://github.com/WinMerge/freeimage.git",
    "hacked": True,    
    
    "config": "-DBUILD_SHARED_LIBS=false -DFREEIMAGE_LIB=true -DSUPPORT_FMT_JPEG=true -DSUPPORT_FMT_OPENEXR=true -DSUPPORT_FMT_WEBP=true -DSUPPORT_FMT_TIFF=true",
    "build": "--build . --config Release",
    "build_tool": "cmake",
    "platforms": PLATFORMS,
    
    "dependencies": [
        {
            "enabled": False,
            "type": "cmake",
            "lib": "zlib",
            "lib_var": "ZLIB_LIBRARY",
            "include_var": "ZLIB_INCLUDE_DIR",
        }
    ],
    
    "artifacts": [
        { 
            "type": "library", 
            "location": "build", 
            "platform": ["windows"],
            "files": ["Release/FreeImage.lib"]
        },
        { 
            "type": "library", 
            "location": "build", 
            "platform": ["linux"],
            "files": ["libFreeImage.a"]
        },
        {
            "type": "header", 
            "location": "source", 
            "platform": PLATFORMS, # all platforms
            "files": ["Source/FreeImage.h", "Source/config.h", "Wrapper/FreeImagePlus/FreeImagePlus.h"]
        },
    ]
}

LIBRARY_SQUISH = {
    "name": "squish",
    "wget": "https://netix.dl.sourceforge.net/project/libsquish/libsquish-1.15.tgz",
    
    "config": "-DBUILD_SHARED_LIBS=false -DBUILD_SQUISH_WITH_SSE2=true",
    "build": "--build . --config Release",
    "build_tool": "cmake",
    "platforms": PLATFORMS,
   
    "artifacts": [
        { 
            "type": "library", 
            "location": "build", 
            "platform": ["windows"],
            "files": ["Release/squish.lib"]
        },
        { 
            "type": "library", 
            "location": "build", 
            "platform": ["linux"],
            "files": ["libsquish.a"]
        },
        {
            "type": "header", 
            "location": "source", 
            "platform": PLATFORMS, # all platforms
            "files": ["squish.h"]
        },
    ]
}

LIBRARY_D3DCOMPILER = {
    "name": "dxc",
    "wget": "https://github.com/microsoft/DirectXShaderCompiler/releases/download/v1.6.2112/dxc_2021_12_08.zip",
    
    "platforms": ['windows'],
    
    "artifacts": [
        { 
            "type": "library", 
            "location": "source", 
            "platform": ["windows"],
            "files": ["lib/x64/dxcompiler.lib"]
        },
        { 
            "type": "deploy", 
            "location": "source", 
            "platform": ["windows"],
            "files": ["bin/x64/dxcompiler.dll"]
        },
        {
            "type": "header", 
            "location": "source", 
            "platform": ['windows'],
            "files": ["inc/dxcapi.h", "inc/d3d12shader.h"]
        },
    ]
}

LIBRARY_D3DCOMPILER_LINUX = {
    "name": "dxc",
    "repo": "https://github.com/microsoft/DirectXShaderCompiler.git",
    
    "config": "-GNinja -C {source_path}/cmake/caches/PredefinedParams.cmake -DSPIRV_BUILD_TESTS=ON -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ -DCMAKE_CXX_FLAGS=-Wno-error -DENABLE_DXIL2SPV=ON",
    "build_tool": "ninja",
    "platforms": ['linux'],
    
    "artifacts": [
        { 
            "type": "library", 
            "location": "build", 
            "platform": ["linux"],
            "files": ["lib/libdxcompiler.so.3.7"]
        },
        { 
            "type": "deploy", 
            "location": "build", 
            "platform": ["linux"],
            "files": ["lib/libdxcompiler.so.3.7"]
        },
        {
            "type": "header", 
            "location": "source", 
            "platform": ['linux'],
            "files": ["include/dxc/dxcapi.h"]
        },
    ]
}

LIBRARY_MBEDTLS = {
    "name": "mbedtls",
    "repo": "https://github.com/ARMmbed/mbedtls.git",
    
    "config": " -DENABLE_TESTING=false -DUSE_SHARED_MBEDTLS_LIBRARY=true -DGEN_FILES=true -DENABLE_PROGRAMS=false -DUSE_STATIC_MBEDTLS_LIBRARY=true -DUSE_SHARED_MBEDTLS_LIBRARY=false",
    "build": "--build . --config Release",
    "build_tool": "cmake",
    "platforms": PLATFORMS,   
    
    "artifacts": [
        { 
            "type": "library", 
            "location": "build", 
            "platform": ["windows"],
            "files": ["library/Release/mbedcrypto.lib", "library/Release/mbedtls.lib", "library/Release/mbedx509.lib"]
        },
        { 
            "type": "library", 
            "location": "build", 
            "platform": ["linux"],
            "files": ["library/libmbedcrypto.a", "library/libmbedtls.a", "library/libmbedx509.a"]
        },
        {
            "type": "header", 
            "location": "source", 
            "platform": PLATFORMS, # all platforms
            "dirs": ["include"]
        },
    ]
}

LIBRARY_CURL = {
    "name": "curl",
    "repo": "https://github.com/curl/curl.git",
    
    "config": "-DBUILD_SHARED_LIBS=false -DHTTP_ONLY=true -DCURL_ENABLE_SSL=true -DCURL_USE_MBEDTLS=true",
    "build": "--build . --config Release",
    "build_tool": "cmake",
    "platforms": PLATFORMS,
    
    "dependencies": [
        # MbedTLS
        {
            "type": "cmake",
            "lib": "mbedtls",
            "platform": "linux",
            "include_var": "MBEDTLS_INCLUDE_DIRS",
            "lib_vars": [
                {"var": "MBEDTLS_LIBRARY", "file": "libmbedtls.a" },
                {"var": "MBEDX509_LIBRARY", "file": "libmbedx509.a" },
                {"var": "MBEDCRYPTO_LIBRARY", "file": "libmbedcrypto.a" },
            ]
        },
        # MbedTLS
        {
            "type": "cmake",
            "lib": "mbedtls",
            "platform": "windows",
            "include_var": "MBEDTLS_INCLUDE_DIRS",
            "lib_vars": [
                {"var": "MBEDTLS_LIBRARY", "file": "mbedtls.lib" },
                {"var": "MBEDX509_LIBRARY", "file": "mbedx509.lib" },
                {"var": "MBEDCRYPTO_LIBRARY", "file": "mbedcrypto.lib" },
            ]
        },
        # ZLIB
        {
            "type": "cmake",
            "lib": "zlib",
            "lib_var": "ZLIB_LIBRARY",
            "include_var": "ZLIB_INCLUDE_DIR",
        }
    ],
    
    "artifacts": [
        { 
            "type": "library", 
            "location": "build", 
            "platform": ["windows"],
            "files": ["lib/Release/libcurl.lib"]
        },
        { 
            "type": "library", 
            "location": "build", 
            "platform": ["linux"],
            "files": ["lib/libcurl.a"]
        },
        {
            "type": "header", 
            "location": "source", 
            "platform": PLATFORMS, # all platforms
            "dirs": ["include"]
        },
    ]
}

LIBRARY_OFBX = {
    "name": "ofbx",
    "repo": "https://github.com/nem0/OpenFBX.git",
    "hacked": True,
    
    "config": "",
    "build": "--build . --config Release",
    "build_tool": "cmake",
    "platforms": PLATFORMS,   
    
    "artifacts": [
        { 
            "type": "library", 
            "location": "build", 
            "platform": ["windows"],
            "files": ["Release/OFBX.lib"]
        },
        { 
            "type": "library", 
            "location": "build", 
            "platform": ["linux"],
            "files": ["libOFBX.a"]
        },        
        {
            "type": "header", 
            "location": "source", 
            "platform": PLATFORMS, # all platforms
            "files": ["src/ofbx.h"]
        },
    ]
}

LIBRARY_LUA = {
    "name": "lua",
    "repo": "https://github.com/lua/lua.git",
    "hacked": True,
    
    "config": "",
    "build": "--build . --config Release",
    "build_tool": "cmake",
    "platforms": PLATFORMS,   
    
    "artifacts": [
        { 
            "type": "library", 
            "location": "build", 
            "platform": ["windows"],
            "files": ["Release/lua.lib"]
        },
        { 
            "type": "library", 
            "location": "build", 
            "platform": ["linux"],
            "files": ["liblua.a"]
        },
        {
            "type": "header", 
            "location": "source", 
            "platform": PLATFORMS, # all platforms
            "target_prefix_path": "lua/", # most apps expect the lua to be at "lua/" folder
            "files": ["lua.h", "lualib.h", "luaconf.h", "lauxlib.h"]
        },
    ]
}

LIBRARY_GTEST = {
    "name": "gtest",
    "repo": "https://github.com/google/googletest.git",
    
    "config": "-DBUILD_GMOCK=false -Dgtest_force_shared_crt=true -DBUILD_SHARED_LIBS=false",
    "build": "--build . --config Release",
    "build_tool": "cmake",
    "platforms": PLATFORMS,   
    
    "artifacts": [
        { 
            "type": "library", 
            "location": "build", 
            "platform": ["windows"],
            "files": ["lib/Release/gtest.lib"]
        },
        { 
            "type": "library", 
            "location": "build", 
            "platform": ["linux"],
            "files": ["lib/libgtest.a"]
        },
        {
            "type": "header", 
            "location": "source", 
            "platform": PLATFORMS, # all platforms
            "dirs": ["googletest/include"]
        },
    ]
}

LIBRARY_EMBREE = {
    "name": "embree",
    "repo": "https://github.com/embree/embree.git",
    
    "config": " -DEMBREE_STATIC_LIB=true -DEMBREE_ISPC_SUPPORT=false -DEMBREE_TUTORIALS=false -DEMBREE_ISA_AVX512=false -DEMBREE_TASKING_SYSTEM=internal ..",
    "build": "--build . --config Release",
    "build_tool": "cmake",
    "platforms": PLATFORMS,   
    
    "artifacts": [
        { 
            "type": "library", 
            "location": "build", 
            "platform": ["windows"],
            "files": ["Release/embree_avx.lib", "Release/embree_avx2.lib", "Release/embree_sse42.lib", "Release/embree3.lib", "Release/lexers.lib", "Release/math.lib", "Release/simd.lib", "Release/sys.lib", "Release/tasking.lib"]
        },
        { 
            "type": "library", 
            "location": "build", 
            "platform": ["linux"],
            "files": ["libembree3.a", "libembree_avx.a", "libembree_avx2.a", "libembree_sse42.a", "liblexers.a", "libmath.a", "libsimd.a", "libsys.a", "libtasking.a"]
        },
        {
            "type": "header", 
            "location": "source", 
            "platform": PLATFORMS, # all platforms
            "dirs": ["include"]
        },
    ]
}

LIBRARY_LLVM = {
    "name": "llvm",
    "repo": "https://github.com/llvm/llvm-project.git",
    
    "config": "-DLLVM_BUILD_LLVM_DYLIB=false -DLLVM_BUILD_RUNTIMES=false -DLLVM_BUILD_RUNTIME=false -DLLVM_INCLUDE_TESTS=false -DLLVM_INCLUDE_TOOLS=false -DLLVM_INCLUDE_UTILS=false -DLLVM_TARGETS_TO_BUILD=X86 -DLLVM_TEMPORARILY_ALLOW_OLD_TOOLCHAIN=true ..",
    "build": "--build . --config Release",
    "build_tool": "cmake",
    "custom_build_path": "llvm/",
    "platforms": PLATFORMS,   
    
    "artifacts": [
        { 
            "type": "library", 
            "location": "build", 
            "platform": ["windows"],
            "files": ["Release/lib/LLVMAggressiveInstCombine.lib", "Release/lib/LLVMAnalysis.lib", "Release/lib/LLVMAsmParser.lib", "Release/lib/LLVMAsmPrinter.lib", "Release/lib/LLVMBinaryFormat.lib", "Release/lib/LLVMBitReader.lib", "Release/lib/LLVMBitstreamReader.lib", 
                      "Release/lib/LLVMBitWriter.lib", "Release/lib/LLVMCFGuard.lib", "Release/lib/LLVMCodeGen.lib", "Release/lib/LLVMCore.lib", "Release/lib/LLVMCoroutines.lib", "Release/lib/LLVMCoverage.lib", "Release/lib/LLVMDebugInfoCodeView.lib", "Release/lib/LLVMDebuginfod.lib", 
                      "Release/lib/LLVMDebugInfoDWARF.lib", "Release/lib/LLVMDebugInfoGSYM.lib", "Release/lib/LLVMDebugInfoMSF.lib", "Release/lib/LLVMDebugInfoPDB.lib", "Release/lib/LLVMDemangle.lib", "Release/lib/LLVMDlltoolDriver.lib", "Release/lib/LLVMDWARFLinker.lib", "Release/lib/LLVMDWP.lib", 
                      "Release/lib/LLVMExecutionEngine.lib", "Release/lib/LLVMExtensions.lib", "Release/lib/LLVMFileCheck.lib", "Release/lib/LLVMFrontendOpenACC.lib", "Release/lib/LLVMFrontendOpenMP.lib", "Release/lib/LLVMFuzzMutate.lib", "Release/lib/LLVMGlobalISel.lib", "Release/lib/LLVMInstCombine.lib", 
                      "Release/lib/LLVMInstrumentation.lib", "Release/lib/LLVMInterfaceStub.lib", "Release/lib/LLVMInterpreter.lib", "Release/lib/LLVMipo.lib", "Release/lib/LLVMIRReader.lib", "Release/lib/LLVMJITLink.lib", "Release/lib/LLVMLibDriver.lib", "Release/lib/LLVMLineEditor.lib", "Release/lib/LLVMLinker.lib", 
                      "Release/lib/LLVMLTO.lib", "Release/lib/LLVMMC.lib", "Release/lib/LLVMMCA.lib", "Release/lib/LLVMMCDisassembler.lib", "Release/lib/LLVMMCJIT.lib", "Release/lib/LLVMMCParser.lib", "Release/lib/LLVMMIRParser.lib", "Release/lib/LLVMObjCARCOpts.lib", "Release/lib/LLVMObject.lib", 
                      "Release/lib/LLVMObjectYAML.lib", "Release/lib/LLVMOption.lib", "Release/lib/LLVMOrcJIT.lib", "Release/lib/LLVMOrcShared.lib", "Release/lib/LLVMOrcTargetProcess.lib", "Release/lib/LLVMPasses.lib", "Release/lib/LLVMProfileData.lib", "Release/lib/LLVMRemarks.lib", 
                      "Release/lib/LLVMRuntimeDyld.lib", "Release/lib/LLVMScalarOpts.lib", "Release/lib/LLVMSelectionDAG.lib", "Release/lib/LLVMSupport.lib", "Release/lib/LLVMSymbolize.lib", "Release/lib/LLVMTableGen.lib", "Release/lib/LLVMTableGenGlobalISel.lib", "Release/lib/LLVMTarget.lib", 
                      "Release/lib/LLVMTextAPI.lib", "Release/lib/LLVMTransformUtils.lib", "Release/lib/LLVMVectorize.lib", "Release/lib/LLVMWindowsManifest.lib", "Release/lib/LLVMX86AsmParser.lib", "Release/lib/LLVMX86CodeGen.lib", "Release/lib/LLVMX86Desc.lib", "Release/lib/LLVMX86Disassembler.lib", 
                      "Release/lib/LLVMX86Info.lib", "Release/lib/LLVMX86TargetMCA.lib", "Release/lib/LLVMXRay.lib" ]
        },
        { 
            "type": "library", 
            "location": "build", 
            "platform": ["linux"],
            "files": ["lib/libbenchmark.a", "lib/libbenchmark_main.a", "lib/libLLVMAggressiveInstCombine.a", "lib/libLLVMAnalysis.a", "lib/libLLVMAsmParser.a",
                      "lib/libLLVMAsmPrinter.a", "lib/libLLVMBinaryFormat.a", "lib/libLLVMBitReader.a", "lib/libLLVMBitstreamReader.a", "lib/libLLVMBitWriter.a",
                      "lib/libLLVMCFGuard.a", "lib/libLLVMCodeGen.a", "lib/libLLVMCore.a", "lib/libLLVMCoroutines.a", "lib/libLLVMCoverage.a", "lib/libLLVMDebugInfoCodeView.a",
                      "lib/libLLVMDebuginfod.a", "lib/libLLVMDebugInfoDWARF.a", "lib/libLLVMDebugInfoGSYM.a", "lib/libLLVMDebugInfoMSF.a", "lib/libLLVMDebugInfoPDB.a",
                      "lib/libLLVMDemangle.a", "lib/libLLVMDlltoolDriver.a", "lib/libLLVMDWARFLinker.a", "lib/libLLVMDWP.a", "lib/libLLVMExecutionEngine.a", "lib/libLLVMExtensions.a",
                      "lib/libLLVMFileCheck.a", "lib/libLLVMFrontendOpenACC.a", "lib/libLLVMFrontendOpenMP.a", "lib/libLLVMFuzzMutate.a", "lib/libLLVMGlobalISel.a",
                      "lib/libLLVMInstCombine.a", "lib/libLLVMInstrumentation.a", "lib/libLLVMInterfaceStub.a", "lib/libLLVMInterpreter.a", "lib/libLLVMipo.a",
                      "lib/libLLVMIRReader.a", "lib/libLLVMJITLink.a", "lib/libLLVMLibDriver.a", "lib/libLLVMLineEditor.a", "lib/libLLVMLinker.a", "lib/libLLVMLTO.a",
                      "lib/libLLVMMC.a", "lib/libLLVMMCA.a", "lib/libLLVMMCDisassembler.a", "lib/libLLVMMCJIT.a", "lib/libLLVMMCParser.a", "lib/libLLVMMIRParser.a", "lib/libLLVMObjCARCOpts.a", "lib/libLLVMObjCopy.a",
                      "lib/libLLVMObject.a", "lib/libLLVMObjectYAML.a", "lib/libLLVMOption.a", "lib/libLLVMOrcJIT.a", "lib/libLLVMOrcShared.a", "lib/libLLVMOrcTargetProcess.a", "lib/libLLVMPasses.a", "lib/libLLVMProfileData.a",
                      "lib/libLLVMRemarks.a", "lib/libLLVMRuntimeDyld.a", "lib/libLLVMScalarOpts.a", "lib/libLLVMSelectionDAG.a", "lib/libLLVMSupport.a", "lib/libLLVMSymbolize.a", "lib/libLLVMTableGen.a", "lib/libLLVMTableGenGlobalISel.a",
                      "lib/libLLVMTarget.a", "lib/libLLVMTextAPI.a", "lib/libLLVMTransformUtils.a", "lib/libLLVMVectorize.a", "lib/libLLVMWindowsDriver.a", "lib/libLLVMWindowsManifest.a", "lib/libLLVMX86AsmParser.a", "lib/libLLVMX86CodeGen.a",
                      "lib/libLLVMX86Desc.a", "lib/libLLVMX86Disassembler.a", "lib/libLLVMX86Info.a", "lib/libLLVMX86TargetMCA.a", "lib/libLLVMXRay.a"]
        },
        {
            "type": "header", 
            "location": "source", 
            "platform": PLATFORMS, # all platforms
            "dirs": ["llvm/include"]
        },
        {
            "type": "header", 
            "location": "build", 
            "platform": PLATFORMS, # all platforms
            "target_prefix_path": "llvm/",
            "dirs": ["include/llvm/"],
            #"files": ["include/llvm/Config/llvm-config.h", "include/llvm/Config/config.h", "include/llvm/Config/abi-breaking.h"]
        },
    ]
}

LIBRARY_OPENAL = {
    "name": "openal",
    "repo": "https://github.com/kcat/openal-soft.git",
    
    "config": "-DLIBTYPE=STATIC -DALSOFT_BACKEND_WINMM=false ..",
    "build": "--build . --config Release",
    "build_tool": "cmake",
    "platforms": PLATFORMS,   
    
    "artifacts": [
        { 
            "type": "library", 
            "location": "build", 
            "platform": ["windows"],
            "files": ["Release/OpenAL32.lib"]
        },
        { 
            "type": "library", 
            "location": "build", 
            "platform": ["linux"],
            "files": ["libopenal.a"]
        },
        {
            "type": "header", 
            "location": "source", 
            "platform": PLATFORMS, # all platforms
            "dirs": ["include"]
        },
    ]    
}

LIBRARY_PHYSX = {
    "name": "physx",
    "repo": "https://github.com/NVIDIAGameWorks/PhysX.git",
    
    "hacked": True, # we copy over some of our fake configs
    "source_build": True, # TODO: configure PhysX to build from external folder
    
    "build_tool": "cmake",
    "build": {
        "windows": "--build physx/compiler/vc16win64 --config Release",
        "linux": "--build physx/compiler/linux-release --config Release",
    },

    "run": 
    {
        "windows": "{source_dir}/physx/generate_projects.bat vc16win64",
        "linux": "{source_dir}/physx/generate_projects.sh linux",
    },
    
    "platforms": PLATFORMS,
    
    "artifacts": [
        { 
            "type": "library", 
            "location": "source",  # in source build for PhysX
            "platform": ["windows"],
            "files": [
                "physx/bin/win.x86_64.vc142.md/release/PhysXCharacterKinematic_static_64.lib", 
                "physx/bin/win.x86_64.vc142.md/release/PhysXCommon_static_64.lib", 
                "physx/bin/win.x86_64.vc142.md/release/PhysXCooking_static_64.lib", 
                "physx/bin/win.x86_64.vc142.md/release/PhysXExtensions_static_64.lib", 
                "physx/bin/win.x86_64.vc142.md/release/PhysXFoundation_static_64.lib", 
                "physx/bin/win.x86_64.vc142.md/release/PhysXPvdSDK_static_64.lib", 
                "physx/bin/win.x86_64.vc142.md/release/PhysXVehicle_static_64.lib", 
                "physx/bin/win.x86_64.vc142.md/release/PhysX_static_64.lib"
            ]
        },
        { 
            "type": "library", 
            "location": "source",  # in source build for PhysX
            "platform": ["linux"],
            "files": [
                "physx/bin/linux.clang/release/libPhysX_static_64.a", 
                "physx/bin/linux.clang/release/libPhysXPvdSDK_static_64.a", 
                #"physx/bin/linux.clang/release/libPhysXGpu_64.so", 
                "physx/bin/linux.clang/release/libPhysXFoundation_static_64.a", 
                "physx/bin/linux.clang/release/libPhysXExtensions_static_64.a", 
                "physx/bin/linux.clang/release/libPhysXCooking_static_64.a", 
                "physx/bin/linux.clang/release/libPhysXCommon_static_64.a", 
                "physx/bin/linux.clang/release/libPhysXVehicle_static_64.a", 
                "physx/bin/linux.clang/release/libPhysXCharacterKinematic_static_64.a"
            ]
        },
        {
            "type": "header", 
            "location": "source", 
            "platform": PLATFORMS, # all platforms
            "dirs": ["physx/include"]
        },
        {
            "type": "header", 
            "location": "source", 
            "platform": PLATFORMS, # all platforms
            "dirs": ["pxshared/include"]
        },
    ]    
}

# 

########################
   
# order must match dependencies (ie. zlib compiled before png)
PROJECT_LIST = [
    LIBRARY_ZLIB,
    LIBRARY_ZLIB_NG,
    LIBRARY_LZ4,
    LIBRARY_FREETYPE,
    LIBRARY_FREEIMAGE,
    LIBRARY_SQUISH,
    LIBRARY_D3DCOMPILER,
    LIBRARY_D3DCOMPILER_LINUX,
    LIBRARY_MBEDTLS,
    LIBRARY_CURL,
    LIBRARY_OFBX,
    LIBRARY_LUA,
    LIBRARY_GTEST,
    LIBRARY_EMBREE, 
    LIBRARY_LLVM,
    LIBRARY_OPENAL,
    LIBRARY_PHYSX
]

class DictX(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __repr__(self):
        return '<DictX ' + dict.__repr__(self) + '>'
        
        
def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--verbose", help="Verbose output")
    ap.add_argument("-p", "--platform", choices=PLATFORMS, help="Target platform", required=True)
    ap.add_argument("-l", dest='filter', help="Process only this library", action='append')
    ap.add_argument("--root", dest='root_path', help="Custom root folder")
    ap.add_argument("--build", dest='build_path', help="Custom build folder")
    ap.add_argument("--output", dest='output_path', help="Output folder (relative to root)")
    ap.add_argument("--src", dest='source_path', help="Source folder (relative to root)")
    ap.add_argument('commands', help='Command', nargs='*', choices=COMMANDS) 
    return ap.parse_args()
    
def make_directory(path):
    try:
        if not os.path.exists(path):
            print("Creating directory: '%s'" % path)
            os.makedirs(path)
    except Exception as e:
        print("Unable to create directory: ", path)
        print(e)
        sys.exit(-1)
        
def build_args():
    args = parse_args()
    print(args)
    
    if (args.root_path is None):
        args.root_path = os.getcwd()
        
    if (args.build_path is None):
        args.build_path = os.path.join(args.root_path, BUILD_FOLDER)
        
    if (args.output_path is None):
        args.output_path = os.path.join(args.root_path, OUTPUT_FOLDER)
        
    if (args.source_path is None):
        args.source_path = os.path.join(args.root_path, SOURCE_FOLDER)
        
    print("Platform:", args.platform)
    print("Commands:", args.commands)
    print("Source path:", args.source_path)
    print("Build path:", args.build_path)
    print("Output path:", args.output_path)
    print("Filter:", args.filter)
    
    make_directory(args.source_path)
    make_directory(args.build_path)
    make_directory(args.output_path)

    args.libs = []
    args.all_libs = []
    for slib in PROJECT_LIST:
        if args.platform not in slib["platforms"]:
            print("Library '{name}' will be skipped because it's for for this platform".format(name=slib["name"]))
            continue        
        
        lib = DictX(slib)
        
        for key, value in slib.items():
            lib[key] = value;
            
        lib.source_path = os.path.join(args.source_path, lib.name)
        lib.build_path = os.path.join(args.build_path, lib.name)
        lib.output_path = os.path.join(args.output_path, lib.name)
        lib.hacked = slib.get("hacked", False)

        if args.filter and (lib.name not in args.filter):
            print("Library %s will be IGNORED" % lib.name)
            lib.muted = True
            
        else:
            lib.muted = False
            print("Library %s will be BUILD" % (lib.name))
            args.libs.append(lib)
            
        if not "dependencies" in lib:
            lib.dependencies = []
            
        if not "artifacts" in lib:
            lib.artifacts = []

        args.all_libs.append(lib)
    
    print("Found %d libraries to process" % len(args.libs))
    
    return args
   

@contextlib.contextmanager
def pushd(new_dir):
    previous_dir = os.getcwd()
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(previous_dir)
        
        
def run(command):
    print("{dir}$: {command}".format(dir=os.getcwd(), command=command))
    result = os.system(command)
    if result != 0:
        print("Previous command finished with errors")
        sys.exit(-3)
        
    return
    
        
def lib_pull_git(args, lib, cloneOnly=False):
    # no data
    if not os.path.isdir(lib.source_path):
    
        # if we don't have the data, clone it (if allowed)
        print("Cloning '%s'..." % lib.name)

        run("git clone --depth 1 {repo} {path}".format(repo=lib.repo, path=lib.source_path))

        # if we still don't have it it's a problem
        if not os.path.isdir(lib.source_path):
            print("Cloning %s failed" % lib.name)
            sys.exit(-2)
                
    # we don't want to clone
    elif cloneOnly:
        return

    # sync data to the latest
    run("git -C \"{path}\" pull".format(repo=lib.repo, path=lib.source_path))
    
    # update submodules
    run("git -C \"{path}\" submodule update --init --recursive".format(path=lib.source_path))
    
    
def unpack_tar(file_path, target_path):
    if file_path.endswith("tar.gz") or file_path.endswith("tgz"):
        tar = tarfile.open(file_path, "r:gz")
        tar.extractall(path=target_path)
        tar.close()
    elif file_path.endswith("tar"):
        tar = tarfile.open(file_path, "r:")
        tar.extractall(path=target_path)
        tar.close()
    elif file_path.endswith("zip"):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(target_path)
    else:
        print("Unsupported format of compressed file {path}".format(path=file_path))
        sys.exit(-9)
        
    
def lib_pull_wget(args, lib, cloneOnly=False):
    # local zip file
    local_file = os.path.basename(lib.wget)
    local_path = os.path.join(args.source_path, local_file) # NOTE: downloads to "sources"
    print(local_file)
    
    # download data if missing
    if not os.path.isfile(local_path):
        print("Downloading '%s'..." % lib.wget)
        ssl._create_default_https_context = ssl._create_unverified_context
        urllib.request.urlretrieve(lib.wget, local_path)
        
        # we downloaded the file, we must unpack it
        cloneOnly = False;
        
        # failed ?
        if not os.path.isfile(local_path):
            print("Failed to download {url}".format(url=lib.wget))
            sys.exit(-6)
            
    else:
        print("File {url} already downloaded".format(url=lib.wget))
        
    # no data
    if not os.path.isdir(lib.source_path):
        make_directory(lib.source_path)
        print("Unapcking '%s'..." % local_path)
        unpack_tar(local_path, lib.source_path)
        
    else:
        print("File '%s' already unpacked" % local_path)
    
    
def lib_pull(args, lib, cloneOnly=False):
    if "repo" in lib:
        lib_pull_git(args, lib, cloneOnly)
    elif "wget" in lib:
        lib_pull_wget(args, lib, cloneOnly)
    
   
def lib_verify(args, lib, clone=False):    
    if "repo" in lib:
        try:
            lib.hash = subprocess.check_output(['git', '-C', lib.source_path, 'rev-parse', 'HEAD']).decode('ascii').strip()
            
            if lib.hash is None or (len(lib.hash) != 40):
                print("Unable to verify current hash of %s", lib.name)
                
            print("Library '{name}' at {hash}".format(name=lib.name, hash=lib.hash))
                
        except Exception as e:
            print("Unable to verify proper clone of %s", lib.name)
            print(e)
            sys.exit(-1)
    
    else:
        lib.hash = "0"
        print("Library '{name}' was not cloned from git repo, no hash".format(name=lib.name))
        
    
def find_library_by_name(args, name):
    for lib in args.all_libs:
        if (lib.name == name):
            return lib;

    print("Unable to find dependency %s" % name)
    sys.exit(-1)
    
    
def find_library_lib_artifact(args, lib):
    file_artifacts = lib_gather_artifact_files(args, lib)
    
    lib_file = []
    for file in file_artifacts:
        if file["type"] == "library":
            lib_file.append(file["absolute_source_path"])
            
    if len(lib_file) == 0:
        print("Library {name} does not emit link artifact".format(name=lib.name))
        sys.exit(-1)
        
    if len(lib_file) > 1:
        print("Library {name} emits more than one library, use the lib_vars to specify EXACT dependencies".format(name=lib.name))
        sys.exit(-1)
        
    return lib_file[0]
        
def find_library_specific_lib_artifact(args, lib, file_name):
    file_artifacts = lib_gather_artifact_files(args, lib)
    
    for file in file_artifacts:
        if file["type"] == "library" and file["file_name"] == file_name:
            return file["absolute_source_path"]
            
    print("Library {name} does not emit library artifact {file}".format(name=lib.name, file=file_name))
    sys.exit(-1)
    
    
def find_library_include_artifact(args, lib):
    return os.path.join(lib.output_path, "include")
    
        
def build_cmake_config_string(args, lib):
    config = []
    
    # dependencies
    for dep in lib.dependencies:
        if not dep.get("enabled", True):
            continue
            
        if dep.get("type", "") == "cmake":

            if "platform" in dep:
                if args.platform != dep["platform"]:
                    print("Skipped dependency '{lib}' for platform '{platform}'".format(lib=dep["lib"], platform=dep["platform"]))
                    continue
                else:
                    print("Used conditional dependency '{lib}' for platform '{platform}'".format(lib=dep["lib"], platform=dep["platform"]))

            dep_lib = find_library_by_name(args, dep["lib"])
            print("Resolved internal dependency of '{src}' on '{target}'".format(src=lib.name, target=dep_lib.name))
            
            if "lib_var" in dep:
                dep_library_path = find_library_lib_artifact(args, dep_lib)
                config.append("-D{var}=\"{path}\"".format(var=dep["lib_var"], path=dep_library_path))
                
            if "lib_vars" in dep:
                for libvar in dep["lib_vars"]:
                    dep_library_path = find_library_specific_lib_artifact(args, dep_lib, libvar["file"])
                    config.append("-D{var}=\"{path}\"".format(var=libvar["var"], path=dep_library_path))
                
            if "include_var" in dep:
                dep_include_path = find_library_include_artifact(args, dep_lib)
                config.append("-D{var}=\"{path}\"".format(var=dep["include_var"], path=dep_include_path))
            
    
    # configuration items
    if lib.config:
        str = lib.config.format(source_path=lib.source_path)
        config.append(str)
    
    print(config)    
    
    return ' '.join(config)

    
def lib_configure(args, lib):
    # create build director
    make_directory(lib.build_path)
    
    # path to hack folder
    hack_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hacks")
    
    # if the build is hacked we have our own CMake script to build it
    if lib.hacked:
        target_path = lib.source_path
        source_hacked_path = os.path.join(hack_path, lib.name)
        print(target_path)
        print(source_hacked_path)
        if not os.path.isdir(source_hacked_path):
            print("Library '{name}' indicated as hacked but does not have hacked directory at '{path}'".format(name=lib.name, path=source_hacked_path))
            sys.exit(-1)
        
        shutil.copytree(source_hacked_path, target_path, dirs_exist_ok=True)
        print("HACKS copied over to library '{name}' from '{path}'".format(name=lib.name, path=source_hacked_path))

    # run configuration
    if "run" in lib:
        run_script = lib["run"][args.platform]
        with pushd(lib.build_path):
            run_script = run_script.replace("{build_dir}", lib.build_path)
            run_script = run_script.replace("{source_dir}", lib.source_path)
            run(run_script)
    
    # run CMake
    elif "config" in lib:
        with pushd(lib.build_path):
            config = build_cmake_config_string(args, lib)
            
            cmake_file_path = lib.source_path
            if ("custom_build_path" in lib) and lib.custom_build_path:
                cmake_file_path = os.path.join(lib.source_path, lib.custom_build_path)
                print("Using custom CMake build path: {path}".format(path=cmake_file_path))
            
            run("cmake \"{path}\" {extra}".format(path=cmake_file_path, extra=config))
            
    # no config
    else:
        print("Library '{name}' does not require configuration".format(name=lib.name))
    

def get_lib_build_string(args, lib):
    build_args = ""

    # use the build string if given
    if "build" in lib:
        #print("Type is: '{t}'".format(t=type(lib.build)))

        if type(lib.build) == str:
            build_args = lib.build

        elif type(lib.build) == dict:
            if args.platform in lib.build:
                build_args = lib.build[args.platform]
            else:
                print("Missing variant for platform '{platform}' in build arguments for '{name}'".format(platform=args.platform, name=lib.name))
                exit(-1)

        else:
            print("Invalid type of build arguments for '{name}'".format(name=lib.name))
            exit(-1)

    return build_args


def lib_build_cmake(args, lib):
    # determine if we have in-source build or not
    source_build = lib.get("source_build", False)

    # build command
    build_args = get_lib_build_string(args, lib)

    # extra linux hacks to run on multiple cores
    if args.platform == "linux":
        build_args += " --parallel `nproc`"
    
    # run magic
    if source_build:
        with pushd(lib.source_path):
            run("cmake {args}".format(args=build_args))
            
    else:
        with pushd(lib.build_path):
            run("cmake {args}".format(args=build_args))


def lib_build_ninja(args, lib):
    # build command
    build_args = get_lib_build_string(args, lib)

    # extra linux hacks to run on multiple cores
    if args.platform == "linux":
        build_args += " -j `nproc`"

    # run magic
    with pushd(lib.build_path):
        run("ninja {args}".format(args=build_args))


def lib_build(args, lib):
    # create directory
    make_directory(lib.build_path)

    # build type
    build_tool = lib.get('build_tool', '')

    # nothing to configure ?
    if build_tool == 'cmake':
        lib_build_cmake(args, lib)
    elif build_tool == 'ninja':
        lib_build_ninja(args, lib)
    else:
        print("Library '{name}' does not require building".format(name=lib.name))

    
def is_header_file(path):
    return path.endswith('.h') or path.endswith('.hpp') or path.endswith('.inl') or path.endswith('.inc')

def gather_artifacts_from_directories(absolute_source_directory_path, paths, headers):
    ret = []
    
    for path in paths:
    
        absolute_search_path = os.path.normpath(os.path.join(absolute_source_directory_path, path))
        
        for walk_root, walk_dirs, walk_files in os.walk(absolute_search_path):
            #print(walk_root)
            #print(walk_dirs)
            #print(walk_files)
            
            for walk_file in walk_files:
                absolute_source_file_path = os.path.join(walk_root, walk_file)
                #print(absolute_source_file_path)
                
                if headers and not is_header_file(walk_file):
                    continue
                
                entry = {
                    "absolute_source_path": absolute_source_file_path,
                    "relative_path": os.path.relpath(absolute_source_file_path, absolute_search_path)
                }
                
                #print(entry)
                ret.append(entry)

    print("Found {count} files at \"{path}\"".format(count=len(ret), path=absolute_source_directory_path))
    return ret 
    
def gather_artifacts_from_files(absolute_source_directory_path, paths):
    ret = []
    
    for path in paths:        
        entry = {
            "relative_path": os.path.basename(path),
            "absolute_source_path": os.path.normpath(os.path.join(absolute_source_directory_path, path))
        }
        print(entry)
        ret.append(entry)

    return ret 
    
    
def lib_gather_artifact_files(args, lib):
    files = []
    
    for artifact in lib.artifacts:
        
        absolute_source_directory_path = ""
        if artifact["location"] == "build": 
            absolute_source_directory_path = lib.build_path
        elif artifact["location"] == "source":
            absolute_source_directory_path = lib.source_path
            
        headers = False
        if artifact["type"] == "header":
            headers = True

        if args.platform not in artifact.get('platform', []):
            continue
            
        local_files = []
        if "dirs" in artifact:
            local_files = gather_artifacts_from_directories(absolute_source_directory_path, artifact["dirs"], headers)
        elif "files" in artifact:
            local_files = gather_artifacts_from_files(absolute_source_directory_path, artifact["files"])
        else:
            print("Library {name} has invalid artifact definition, either 'dirs' for 'files' should be specified".format(name=lib.name))
            sys.exit(-1)
            
        absolute_target_directory_path = ""
        if artifact["type"] == "header": 
            absolute_target_directory_path = os.path.join(lib.output_path, "include")
        elif artifact["type"] == "library": 
            absolute_target_directory_path = os.path.join(lib.output_path, "lib")
        elif artifact["type"] == "deploy": 
            absolute_target_directory_path = os.path.join(lib.output_path, "bin")
        else:
            print("Invalid type of artifact: " + artifact["type"])
            sys.exit(-1)

        # generate final list of artifacts that will serve as manifest and also a copy list
        # this list has resolved "source" -> "destination" paths as well as resolved type of artifact ("header", "lib", etc)
        for local_file in local_files:
           local_path = local_file["relative_path"]
           
           if "target_prefix_path" in artifact:
                local_path = os.path.join(artifact["target_prefix_path"], local_path);
        
           file = {
                "type": artifact["type"],
                "file_name": os.path.basename(local_file["relative_path"]),
                "relative_path": local_file["relative_path"],
                "absolute_source_path": local_file["absolute_source_path"],
                "absolute_target_path": os.path.join(absolute_target_directory_path, local_path)
           }
           
           print(file)
           files.append(file)
        
    print("Found {num} artifacts in library {name}".format(num=len(files), name=lib.name))
    return files

    
def lib_check_artifacts(files):
    for file in files:
        path = file["absolute_source_path"]
        
        if not os.path.isfile(path):
            print("Missing artifact file \"{path}\"".format(path=path))
            sys.exit(-4)
            
            
def lib_copy_artifacts(files):
    num_copied = 0
    num_up_to_date = 0
    
    for file in files:
        src_path = file["absolute_source_path"]
        target_path = file["absolute_target_path"]

        # copy only if newer
        if os.path.isfile(target_path):
            time_diff = os.stat(src_path).st_mtime - os.stat(target_path).st_mtime;
            if time_diff < 1:
                print("File \"{path}\" is up to date".format(path=target_path))
                num_up_to_date += 1
                continue
                
        #copy
        try:
            make_directory(os.path.dirname(target_path))
            
            print("Copying \"{src}\" to \"{target}\"".format(src=src_path, target=target_path))
            shutil.copy2(src_path, target_path)
            num_copied += 1
        except Exception as e:
            print("Unable to copy file from '{src}' to '{dest}'".format(src=src_path, dest=target_path))
            print(e)
            sys.exit(-1)

        # hack for linux - strip symbols from libraries
        if src_path.endswith(".a") or src_path.endswith(".so"):
            run("strip \"{path}\"".format(path=target_path))
    
        # check that file was copied
        if not os.path.isfile(target_path):
            print("Missing deployed artifact file \"{path}\"".format(path=target_path))
            sys.exit(-4)
            
    print("Copied {count} file(s), {x} up to date".format(count=num_copied, x=num_up_to_date))
    
    
def lib_write_manifset(args, lib, files):
    lines = []
    
    lines.append("LIB_MANIFEST")
    lines.append(lib.name)
    lines.append(args.platform)
    lines.append(lib.hash)
    
    for file in files:
        if file["type"] == "library":
            lines.append("LIBRARY")
            lines.append(file["file_name"])
        if file["type"] == "deploy":
            lines.append("DEPLOY")
            lines.append(file["file_name"])
        
    manifest_target_path = os.path.join(lib.output_path, "manifest.txt")
    try:
        with open(manifest_target_path, 'w') as f:
            f.write('\n'.join(lines))
    except Exception as e:
        print("Failed to write library manifest to '{dest}'".format(dest=manifest_target_path))
        print(e)
        sys.exit(-1)
        
    print("Written manifest for {name} at '{dest}'".format(dest=manifest_target_path, name=lib.name))
    
    
def lib_clean(args, lib):    
    if (len(lib.build_path) > 10):
        print("Cleaning build folder: {path}".format(path=lib.build_path))
        if os.path.isdir(lib.build_path):
            shutil.rmtree(lib.build_path)

    if (len(lib.output_path) > 10):
        print("Cleaning output folder: {path}".format(path=lib.output_path))
        if os.path.isdir(lib.output_path):
            shutil.rmtree(lib.output_path)
        
            
def lib_deploy(args, lib):
    make_directory(lib.output_path)
    
    # gather
    print("Deploying lib {name}".format(name=lib.name))
    file_artifacts = lib_gather_artifact_files(args, lib)
    
    # check if we even have them
    lib_check_artifacts(file_artifacts)
    
    # copy
    lib_copy_artifacts(file_artifacts)
    
    # write manifset
    lib_write_manifset(args, lib, file_artifacts)
    

def main():
    print("InfernoEngine Dependencies Compiler")
    
    args = build_args()

    for lib in args.libs:
    
        # complete removal of data
        if 'purage' in args.commands:
            lib_purge(args, lib)
    
        # get data if requested
        if 'clone' in args.commands:
            lib_clone(args, lib, True)
        elif 'pull' in args.commands: 
            lib_pull(args, lib, False)
            
        # veryfy that we have a valid version
        lib_verify(args, lib)
        
        # build
        if 'clean' in args.commands:
            lib_clean(args, lib)                    
        if 'configure' in args.commands:
            lib_configure(args, lib)
        if 'build' in args.commands:
            lib_build(args, lib)
            
        # deploy
        if 'deploy' in args.commands:
            lib_deploy(args, lib)                        
        
    return 0
    

if __name__ == "__main__":
    main()