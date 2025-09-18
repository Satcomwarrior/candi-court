@echo off

chcp 65001 > NUL

@set "tune_dir=%ProgramData%\Logitech\Tune"

REM optional script param: [final zip path with collected info] [tmp_output_dir]
@if [%1]==[] (set final_archive="%HOMEDRIVE%%HOMEPATH%\Logitune-report.zip") else (set final_archive="%~1")
@if [%2]==[] (
	@set "tmp_output_dir=%tune_dir%\logitune_logs"
) else (
	@set "tmp_output_dir=%~2"
)
@echo temp dir is "%tmp_output_dir%"
@rd /s /q "%tmp_output_dir%"
@mkdir "%tmp_output_dir%"

pushd "%~dp0"
@echo Enumerating USB devices
"%~dp0backend\EnumUSBDevices.exe" > "%tmp_output_dir%\enum_usb_devices.txt"
@echo Preparing backend settings
"%~dp0backend\LogiTuneAgent.exe" --decrypt-settings "%tmp_output_dir%\backend-settings.json"
popd

@echo Collecting system info
@systeminfo > "%tmp_output_dir%\system_info.txt"
@tasklist > "%tmp_output_dir%\tasklist.txt"

@echo Collecting services info
@sc queryex type= service state= all > "%tmp_output_dir%\services_info.txt"

REM @echo Checking internet connection:
REM @echo - Ping Google DNS
REM @ping 8.8.8.8 > "%tmp_output_dir%\ping.txt"
REM @echo - Ping Logitech.com
REM @ping logitech.com >> "%tmp_output_dir%\ping.txt"

REM @echo Checking logitech network services
REM @call domains-diagnostic.cmd -verbose > "%tmp_output_dir%\network_services.txt"

@echo Collecting logs and settings from:
@echo "%tune_dir%":
xcopy "%tune_dir%\settings.json" "%tmp_output_dir%"

@echo "%ProgramFiles%\Logitech\LogiTune\data\logs":
xcopy "%ProgramFiles%\Logitech\LogiTune\data\logs" "%tmp_output_dir%" /s

REM do not make empty folders in %tmp_output_dir%, otherwise zip shows message box that they are ignored

IF EXIST "%appdata%\LogiTune\LogiTuneLogs" (
	dir /a /s "%appdata%\LogiTune\LogiTuneLogs" | findstr /r /c:"^ *[1-9][0-9]* File(s)" > NUL && GOTO logitune_logs
)
GOTO verify_UI_logs

:logitune_logs
@echo "%appdata%\LogiTune\LogiTuneLogs":
@mkdir "%tmp_output_dir%\LogiTuneLogs"
xcopy "%appdata%\LogiTune\LogiTuneLogs\*" "%tmp_output_dir%\LogiTuneLogs" /s

:verify_UI_logs
IF EXIST "%appdata%\LogiTune\UILogs" (
	dir /a /s "%appdata%\LogiTune\UILogs" | findstr /r /c:"^ *[1-9][0-9]* File(s)" > NUL && GOTO UI_logs
)
GOTO crash_dumps

:UI_logs
@echo "%appdata%\LogiTune\UILogs":
@mkdir "%tmp_output_dir%\UILogs"
xcopy "%appdata%\LogiTune\UILogs\*" "%tmp_output_dir%\UILogs" /s

:crash_dumps
@set crashdumps_dirs="%appdata%\LogiTune\dumps","%ProgramFiles%\Logitech\LogiTune\data\dumps"
FOR %%i in (%crashdumps_dirs%) do (
    IF EXIST %%i (
        FOR /F %%j in ('dir /B /A:D %%i') do (
            IF EXIST %%i\"%%j"\*dmp (
                @mkdir %tmp_output_dir%\dumps\"%%j"
                @xcopy  %%i\"%%j"\*dmp %tmp_output_dir%\dumps\"%%j" /s
            )
        )
    )
)

@set "features_cfg_64=%ProgramFiles%\tune-features.cfg"
@set "features_dest_64=%tmp_output_dir%\Program Files"
IF EXIST "%features_cfg_64%" (
	@mkdir "%features_dest_64%"
	xcopy "%features_cfg_64%" "%features_dest_64%"
)

@set "features_cfg_32=%ProgramFiles(x86)%\tune-features.cfg"
@set "features_dest_32=%tmp_output_dir%\Program Files (x86)"
IF EXIST "%features_cfg_32%" (
	@mkdir "%features_dest_32%"
	xcopy "%features_cfg_32%" "%features_dest_32%"
)

@echo Preparing zip
@set zipper_script="%tmp%\Logitech-zip.vbs"
@echo Set objArgs = WScript.Arguments > %zipper_script%
@echo Set FS = CreateObject("Scripting.FileSystemObject") >> %zipper_script%
@echo InputFolder = FS.GetAbsolutePathName(objArgs(0)) >> %zipper_script%
@echo ZipFile = FS.GetAbsolutePathName(objArgs(1)) >> %zipper_script%
@echo|set /p="CreateObject("Scripting.FileSystemObject").CreateTextFile(ZipFile, True).Write "PK" & Chr(5) & Chr(6) & String(18, vbNullChar)" >> %zipper_script%
@echo. >> %zipper_script%
@echo Set objShell = CreateObject("Shell.Application") >> %zipper_script%
@echo Set source = objShell.NameSpace(InputFolder).Items >> %zipper_script%
REM sleep removal code from https://superuser.com/questions/110991/can-you-zip-a-file-from-the-command-prompt-using-only-windows-built-in-capabili
@echo Set ZipDest = objShell.NameSpace(ZipFile) >> %zipper_script%
REM Count gets 0 if no archive existed bedore
@echo Count=ZipDest.Items().Count >> %zipper_script%
@echo objShell.NameSpace(ZipFile).CopyHere(source) >> %zipper_script%
REM ZipDest.Items().Count will also contain 0 untill archive is updated
@echo Count=ZipDest.Items().Count >> %zipper_script%
@echo Do While Count = ZipDest.Items().Count >> %zipper_script%
@echo     wScript.Sleep 100 >> %zipper_script%
@echo Loop >> %zipper_script%

@cscript %zipper_script% "%tmp_output_dir%" %final_archive%
@if exist %final_archive% (
	@echo A zip file %final_archive% generated. Send it to developers.
) else (
	@echo Can't find generated file %final_archive%. Please send this info to developers.
)

@del %zipper_script%
@rd /s /q "%tmp_output_dir%"
if [%1]==[] pause
@echo Done
