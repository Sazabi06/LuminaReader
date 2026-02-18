; LuminaReader Inno Setup Script
; ===============================
; This script creates a Windows installer for LuminaReader
;
; Prerequisites:
;   - Inno Setup 6.0 or higher (https://jrsoftware.org/isinfo.php)
;   - Build the executable first using build.bat
;
; Usage:
;   1. Install Inno Setup
;   2. Open this file in Inno Setup Compiler
;   3. Click Build -> Compile
;   4. Output: installer/LuminaReader_Setup.exe

#define MyAppName "LuminaReader"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "LuminaReader Team"
#define MyAppURL "https://github.com/yourusername/luminareader"
#define MyAppExeName "LuminaReader.exe"

[Setup]
; Application information
AppId={{LUMINA-READER-APP-ID-12345}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}/issues
AppUpdatesURL={#MyAppURL}/releases

; Default installation directory
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}

; Output settings
OutputDir=installer
OutputBaseFilename=LuminaReader_Setup_v{#MyAppVersion}
SetupIconFile=assets\icon.ico

; Compression
Compression=lzma2
SolidCompression=yes

; Appearance
WizardStyle=modern
WizardImageFile=assets\wizard_image.bmp
WizardSmallImageFile=assets\wizard_small_image.bmp

; Privileges
PrivilegesRequiredOverridesAllowed=dialog
PrivilegesRequired=lowest

; Other settings
DisableProgramGroupPage=yes
LicenseFile=LICENSE
InfoBeforeFile=assets\readme_before.txt
InfoAfterFile=assets\readme_after.txt

; Version info
VersionInfoVersion={#MyAppVersion}
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription={#MyAppName} - Modern Markdown and PDF Viewer
VersionInfoTextVersion={#MyAppVersion}
VersionInfoCopyright=Copyright (C) 2024 {#MyAppPublisher}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
; Create desktop shortcut
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

; Create file associations
Name: "fileassoc_md"; Description: "Associate with Markdown files (.md)"; GroupDescription: "File associations:"
Name: "fileassoc_pdf"; Description: "Associate with PDF files (.pdf)"; GroupDescription: "File associations:"

[Files]
; Main executable
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

; Add any additional files here
; Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs

[Icons]
; Start Menu shortcuts
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"

; Desktop shortcut (optional)
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
; Launch after installation
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Registry]
; File association for Markdown files
Root: HKA; Subkey: "Software\Classes\.md"; ValueType: string; ValueName: ""; ValueData: "LuminaReader.md"; Flags: uninsdeletevalue; Tasks: fileassoc_md
Root: HKA; Subkey: "Software\Classes\LuminaReader.md"; ValueType: string; ValueName: ""; ValueData: "Markdown Document"; Flags: uninsdeletekey; Tasks: fileassoc_md
Root: HKA; Subkey: "Software\Classes\LuminaReader.md\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\{#MyAppExeName},0"; Tasks: fileassoc_md
Root: HKA; Subkey: "Software\Classes\LuminaReader.md\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""; Tasks: fileassoc_md

; File association for PDF files
Root: HKA; Subkey: "Software\Classes\.pdf"; ValueType: string; ValueName: ""; ValueData: "LuminaReader.pdf"; Flags: uninsdeletevalue; Tasks: fileassoc_pdf
Root: HKA; Subkey: "Software\Classes\LuminaReader.pdf"; ValueType: string; ValueName: ""; ValueData: "PDF Document"; Flags: uninsdeletekey; Tasks: fileassoc_pdf
Root: HKA; Subkey: "Software\Classes\LuminaReader.pdf\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\{#MyAppExeName},0"; Tasks: fileassoc_pdf
Root: HKA; Subkey: "Software\Classes\LuminaReader.pdf\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""; Tasks: fileassoc_pdf

[UninstallDelete]
; Clean up any leftover files
Type: filesandordirs; Name: "{app}\assets"
Type: dirifempty; Name: "{app}"

[Code]
; Custom installation code
function InitializeSetup(): Boolean;
begin
  // Check if application is already running
  if CheckForMutexes('LuminaReader_Mutex') then
  begin
    MsgBox('LuminaReader is currently running. Please close it before continuing.', mbError, MB_OK);
    Result := false;
  end
  else
  begin
    Result := true;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Post-installation actions
    Log('Installation completed successfully');
  end;
end;
