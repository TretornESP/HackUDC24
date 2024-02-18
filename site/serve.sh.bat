:<<"::CMDLITERAL"
@ECHO OFF
GOTO :CMDSCRIPT
::CMDLITERAL

echo "Executing a Python http server in http://localhost:8080/site.html"
python -m http.server 8080
exit $?

:CMDSCRIPT
echo Executing a Python http server in http://localhost:8080/site.html
python.exe -m http.server 8080
