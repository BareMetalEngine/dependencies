@ECHO OFF

SET PLATFORM=windows
SET ONION="..\onion_tool\bin\onion.exe"

REM %ONION% library -commit -library=scripts/zlib.onion
REM %ONION% library -commit -library=scripts/lz4.onion
%ONION% library -commit -library=scripts/freetype.onion

