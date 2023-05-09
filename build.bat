python -m PyInstaller graph.spec
xcopy .\resources .\dist\resources /E /I /Y
xcopy readme.md .\dist\readme.md /I /Y 
echo ENV=PROD > dist\.env
del dist\resources\nodes\debug.json /Q
del dist\resources\nodes\examples /Q
del dist\resources\nodes\examples-pro /Q
ren dist ChatGraph-Beta
start .