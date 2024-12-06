[References](https://www.labofapenetrationtester.com/2018/10/domain-enumeration-from-PowerShell-CLM.html)
- We can use Micorosft's PowerShell ActiveDirectory module without RSAT and administrative privileges.
- If you have access to a Server which has the module installed (like a DC), copy the Microsoft.ActiveDirectory.Management.dll from C:\Windows\Microsoft.NET\assembly\GAC_64\Microsoft.ActiveDirectory.Management to your own machine and then use the Import-Module cmdlet to import the DLL
```bash
PS C:\> Import-Module C:\ADModule\Microsoft.ActiveDirectory.Management.dll -Verbose
```
- Or automatically import into memory by [ADModule](https://github.com/samratashok/ADModule)