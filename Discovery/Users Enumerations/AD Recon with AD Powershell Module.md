[References](https://adsecurity.org/?p=3719)
- Microsoft provided several Active Directory PowerShell cmdlets with Windows Server 2008 R2 (and newer) which greatly simplify tasks which previously required putting together lengthy lines of code involving ADSI.
- On a Windows client, install the Remote Sever Administration Tools (RSAT) and ensure the Active Directory PowerShell module is installed.
- On a Windows server (2008 R2 or newer), run the following commands in a PowerShell console (as an Adminsitrator):
```bash
Import-Module ServerManager ; Add-WindowsFeature RSAT-AD-PowerShell
```