# I. Information
SPN stands for Service Principal Name in Windows. It is a unique identifier for a service instance used in Kerberos authentication. SPNs allow clients to identify and authenticate services within a network.
## Key features
### Purpose: 
- SPNs are used to associate a specific service instance with a service account (like a computer or user account) in Active Directory.
### Usage:
- Authentication: They enable Kerberos to authenticate services securely without needing passwords to be directly transmitted.
- Delegation: SPNs are critical for features like Kerberos constrained delegation.
### Format: An SPN typically includes:
- The service class (e.g., HTTP, MSSQLSvc).
- The host name or fully qualified domain name (FQDN) of the server.
- Optionally, a port number. Example: HTTP/www.example.com or MSSQLSvc/host.example.com:1433.
## How SPN work
- A client application looks up the SPN for the target service it wants to access.
- The SPN is used to request a Kerberos ticket from the Key Distribution Center (KDC).
- The KDC issues a service ticket, allowing the client to securely communicate with the service.
## Managing SPN
Setspn Command: Administrators can manage SPNs using the setspn command in Windows.
- Add SPN: setspn -A <SPN> <account>
- Delete SPN: setspn -D <SPN> <account>
- List SPNs: setspn -L <account>
```bash
setspn -A MSSQLSvc/sqlserver01.example.com sqlserviceaccount
setspn -A MSSQLSvc/sqlserver01.example.com:1500 sqlserviceaccount
```
## Step by step SPN Flow
### 1. User Authenticates with the KDC:
- The user logs into the domain and authenticates with the KDC using their credentials.
The KDC issues a Ticket Granting Ticket (TGT) to the user. This TGT allows the user to request TGS tickets without re-entering credentials.
### 2. Client Requests a TGS Ticket for the SPN:
- When the client application needs to access a service, it sends a request to the KDC for a TGS ticket for the SPN (e.g., MSSQLSvc/sqlserver01.example.com).
The client includes its TGT in this request to prove its identity.
### 3. KDC Issues the TGS Ticket:
- The KDC locates the account associated with the SPN in Active Directory (e.g., sqlserviceaccount@example.com).
It generates a TGS ticket encrypted with the service account's secret key (derived from its password or machine credentials).
The KDC sends this TGS ticket back to the client.
Client Presents the TGS Ticket to the Service:

### 4. The client connects to the service (e.g., SQL Server) and presents the TGS ticket.
- The service decrypts the ticket using its secret key and validates the client’s identity.
### 5. Authentication Success:
- If the ticket is valid, the service grants the client access.

# Note
- If a client or program runs on local system on machine wants to connect to remote service, SPN will be resolved for computer accounts
## Computer account credentials
### 1. Password for the Computer Account:
- Each computer account (e.g., COMP01$) in Active Directory has a secret password stored in the AD database.
- This password is automatically generated and managed by Windows.
By default, the password is 120 characters long and is regularly rotated (every 30 days, though this can be configured).
<table border="1" cellpadding="5" cellspacing="0">
    <thead>
        <tr>
            <th>Aspect</th>
            <th>SPN Linked to Machine Account</th>
            <th>SPN Linked to Service Account</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Object Type</strong></td>
            <td>Machine account (e.g., <code>MACHINE01$</code>).</td>
            <td>User or service account (e.g., <code>SQLServiceAccount</code>).</td>
        </tr>
        <tr>
            <td><strong>Ownership</strong></td>
            <td>The SPN is automatically registered for the computer.</td>
            <td>The SPN is manually registered to the service account.</td>
        </tr>
        <tr>
            <td><strong>Account Context</strong></td>
            <td>Services running as Local System, Network Service, etc.</td>
            <td>Services running as the specified service account.</td>
        </tr>
        <tr>
            <td><strong>Credential Management</strong></td>
            <td>Credentials managed automatically by the domain.</td>
            <td>Credentials managed manually or via MSAs.</td>
        </tr>
        <tr>
            <td><strong>Use Case</strong></td>
            <td>Default Windows services, file sharing, remote access.</td>
            <td>Applications like SQL Server, IIS, or third-party services.</td>
        </tr>
        <tr>
            <td><strong>SPN Registration</strong></td>
            <td>Automatic during domain join or by default for services.</td>
            <td>Requires manual registration or automation via MSAs.</td>
        </tr>
        <tr>
            <td><strong>Flexibility</strong></td>
            <td>Tied to the computer’s identity.</td>
            <td>Provides better isolation and customization for services.</td>
        </tr>
    </tbody>
</table>

### 2. How the Computer Uses Its Credentials:
- When a computer joins a domain, it establishes a trust relationship with the domain controller using its computer account.
- The computer securely stores its password in the Local Security Authority (LSA) subsystem.
- The password is used during authentication requests, like obtaining a TGT from the KDC.

***If computer is not joined domain, local accounts will be save on SAM (C:/Windows/system32/config/SAM), otherwise cache domains accounts will be saved on SECURITY hive (C:/Windows/system32/config/SECURITY). SYSTEM hive, which contains encryption keys for the SAM database is saved on %SystemRoot%\System32\config\SYSTEM***
***Sensitive information managed by LSA, such as cached credentials and service account passwords, is saved in the registry under HKEY_LOCAL_MACHINE\SECURITY\Policy\Secrets***
<table border="1">
  <thead>
    <tr>
      <th>Account Type</th>
      <th>Registry Hive</th>
      <th>Details</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Local Account</td>
      <td>HKEY_LOCAL_MACHINE\SAM</td>
      <td>Names, SIDs, encrypted password hashes.</td>
    </tr>
    <tr>
      <td>Domain Account</td>
      <td>HKEY_LOCAL_MACHINE\SECURITY\Cache</td>
      <td>Cached credentials for offline logins.</td>
    </tr>
  </tbody>
</table>

# II. Resources
## 1. [SPN discovery](https://pentestlab.blog/2018/06/04/spn-discovery/)
### [SetSPN](https://learn.microsoft.com/en-us/archive/technet-wiki/18996.active-directory-powershell-script-to-list-all-spns-used#setspn)
- Using setspn to find SPNs linked to a certain computer:
```bash
setspn -L <ServerName>
```
- Using setspn to find SPNs linked to a certain user account:
```bash
setspn -L <domain\user>
```
- List all SPNs in domain:
```bash
setspn -Q */*
```
### [Ldifde](https://learn.microsoft.com/en-us/archive/technet-wiki/18996.active-directory-powershell-script-to-list-all-spns-used#ldifde)
***Note that ldifde only works on window server, not in windows 10 or 11***
```bash
Ldifde -d "DC=Contoso,DC=Com" -l ServicePrincipalName -F C:\SPN.txt
```
### [Pure powershell](https://learn.microsoft.com/en-us/archive/technet-wiki/18996.active-directory-powershell-script-to-list-all-spns-used#powershell)
```powershell
$search = New-Object DirectoryServices.DirectorySearcher([ADSI]"")
$search.filter = "(servicePrincipalName=*)"
$results = $search.Findall()
foreach($result in $results)
{
    $userEntry = $result.GetDirectoryEntry()
    Write-host "Object Name = " $userEntry.name -backgroundcolor "yellow" -foregroundcolor "black"
    Write-host "DN = " $userEntry.distinguishedName
    Write-host "Object Cat. = " $userEntry.objectCategory
    Write-host "servicePrincipalNames"
    $i=1
    foreach($SPN in $userEntry.servicePrincipalName){
        Write-host "SPN(" $i ") = " $SPN
        $i+=1
    }
    Write-host ""
}
```
### [GetUserSPNs](https://github.com/fortra/impacket/blob/master/examples/GetUserSPNs.py)
### [GetUserSPNs vbs](https://github.com/nidem/kerberoast/blob/master/GetUserSPNs.vbs)
```bash
cscript.exe GetUserSPNs.vbs
```
### [PowerShell AD Recon](https://github.com/PyroTek3/PowerShell-AD-Recon)
### [Empire](https://github.com/EmpireProject/Empire)
```bash
usemodule situational_awareness/network/get_spn
```
### [PowerShellery](https://github.com/nullbind/Powershellery)
```bash
Import-Module .\Get-SPN.psm1
Get-SPN -type service -search "*" -List yes | Format-Table
```
### Impacket (GetUserSPNs.py)
```bash
./GetUserSPNs.py -dc-ip 10.0.0.1 pentestlab.local/test
```
## 2. [All class names of SPN](https://adsecurity.org/?page_id=183)

# III. Hunting for suspicious SPN discovery
- After examinating code from multiple sources, including Empire, impacket, PS AD Recon, or even native binary of Window, my custom python script. I realize that all tools must contains filter **servicePrincipalName**, this means LDAP queries required.
- Therefore, as my opinion, hunt for any LDAP connection on port 389 or 636, and initiated from suspicious process like powershell, cmd, python, cscript,... maybe reveal some odd activities which are potential Keberoasting attack or network scanning.
- This is core idea, but hunting queries must be changed base on organization environment.
## 1. MDE hunt
- hunt for odd powershell process
```bash
DeviceNetworkEvents
| where RemotePort == 389 or RemotePort == 636  // LDAP ports (389 - LDAP, 636 - LDAPS)
| where (InitiatingProcessCommandLine contains "powershell" or InitiatingProcessCommandLine contains "cmd" InitiatingProcessCommandLine contains "python" ) and (InitiatingProcessCommandLine !contains "defender")
| where tolower(InitiatingProcessAccountName) !contains "system" and tolower(InitiatingProcessAccountName) !contains "local"
| summarize by InitiatingProcessCommandLine, InitiatingProcessFolderPath, InitiatingProcessAccountName
```
- hunt for any executable files which initiate LDAP connection is not located on system folders
```bash
DeviceNetworkEvents
| where RemotePort == 389 or RemotePort == 636  // LDAP ports (389 - LDAP, 636 - LDAPS)
| where InitiatingProcessFileName != ""
| where InitiatingProcessFolderPath !contains "system32" and InitiatingProcessFolderPath !contains "program files" and InitiatingProcessFolderPath !contains "teams"
and InitiatingProcessFolderPath !contains "windows"
| summarize by InitiatingProcessCommandLine, InitiatingProcessFolderPath, RemoteIP, RemotePort
```