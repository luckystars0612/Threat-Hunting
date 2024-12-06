# [References](https://adsecurity.org/?p=2535)

## I. Get Active Directory Information (powershell .NET implementations [part 1](https://adsecurity.org/?p=113), [part 2](https://adsecurity.org/?p=192))
### 1. Forest Information
```bash
PS C:\> [System.DirectoryServices.ActiveDirectory.Forest]::GetCurrentForest()

Name: lab.adsecurity.org
Sites: {Default-First-Site-Name}
Domains: {lab.adsecurity.org, child.lab.adsecurity.org}
GlobalCatalogs: {ADSDC01.lab.adsecurity.org, ADSDC02.lab.adsecurity.org, ADSDC03.lab.adsecurity.org, ADSDC11.child.lab.adsecurity.org}
ApplicationPartitions: {DC=DomainDnsZones,DC=child,DC=lab,DC=adsecurity,DC=org, DC=DomainDnsZones,DC=lab,DC=adsecurity,DC=org,
DC=ForestDnsZones,DC=lab,DC=adsecurity,DC=org}
ForestMode: Windows2008R2Forest
RootDomain: lab.adsecurity.org
Schema: CN=Schema,CN=Configuration,DC=lab,DC=adsecurity,DC=org
SchemaRoleOwner: ADSDC03.lab.adsecurity.org
NamingRoleOwner: ADSDC03.lab.adsecurity.org
```
### 2. Domain Information
```bash
PS C:\> [System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain()

Forest: lab.adsecurity.org
DomainControllers: {ADSDC01.lab.adsecurity.org, ADSDC02.lab.adsecurity.org, ADSDC03.lab.adsecurity.org}
Children: {child.lab.adsecurity.org}
DomainMode: Windows2008R2Domain
Parent:
PdcRoleOwner: ADSDC03.lab.adsecurity.org
RidRoleOwner: ADSDC03.lab.adsecurity.org
InfrastructureRoleOwner: ADSDC03.lab.adsecurity.org
Name: lab.adsecurity.org
```
### 3. Forest Trusts
```bash
$ForestRootDomain = 'lab.adsecurity.org'
([System.DirectoryServices.ActiveDirectory.Forest]::GetForest((New-Object System.DirectoryServices.ActiveDirectory.DirectoryContext('Forest', $ForestRootDomain)))).GetAllTrustRelationships()
```
### 4. Domain Trusts
```bash
PS C:\> ([System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain()).GetAllTrustRelationships()

SourceName:    lab.adsecurity.org
TargetName: child.lab.adsecurity.org
TrustType:   ParentChild
TrustDirection: Bidirectional
```
### 5. Forest Global Catalogs
```bash
PS C:\> [System.DirectoryServices.ActiveDirectory.Forest]::GetCurrentForest().GlobalCatalogs

Forest                     : lab.adsecurity.org
CurrentTime                : 1/27/2016 5:31:36 PM
HighestCommittedUsn        : 305210
OSVersion                  : Windows Server 2008 R2 Datacenter
Roles                      : {}
Domain                     : lab.adsecurity.org
IPAddress                  : 172.16.11.11
SiteName                   : Default-First-Site-Name
SyncFromAllServersCallback :
InboundConnections         : {36bfdadf-777d-4bad-9427-bc148cea256f, 48594a5d-c2a3-4cd1-a80d-bedf367cc2a9, 549871d2-e238-4423-a6b8-1bb
OutboundConnections        : {9da361fd-0eed-414a-b4ee-0a9caa1b153e, 86690811-f995-4c3e-89fe-73c61fa4a3a0, 8797cbb4-fe09-49dc-8891-952
Name                       : ADSDC01.lab.adsecurity.org
Partitions                 : {DC=lab,DC=adsecurity,DC=org, CN=Configuration,DC=lab,DC=adsecurity,DC=org,
CN=Schema,CN=Configuration,DC=lab,DC=adsecurity,DC=org, DC=DomainDnsZones,DC=lab,DC=adsecurity,DC=org…

Forest                     : lab.adsecurity.org
CurrentTime                : 1/27/2016 5:31:37 PM
HighestCommittedUsn        : 274976
OSVersion                  : Windows Server 2012 R2 Datacenter
Roles                      : {SchemaRole, NamingRole, PdcRole, RidRole…}
Domain                     : lab.adsecurity.org
IPAddress                  : fe80::1881:40d5:fc2e:e744%12
SiteName                   : Default-First-Site-Name
SyncFromAllServersCallback :
InboundConnections         : {86690811-f995-4c3e-89fe-73c61fa4a3a0, dd7b36a8-a52e-446d-95a8-318b69bd9765}
OutboundConnections        : {f901f0b5-8754-44e9-92e8-f56b3d67197b, 549871d2-e238-4423-a6b8-1bb258e2a62f}
Name                       : ADSDC03.lab.adsecurity.org
Partitions                 : {DC=lab,DC=adsecurity,DC=org, CN=Configuration,DC=lab,DC=adsecurity,DC=org,
CN=Schema,CN=Configuration,DC=lab,DC=adsecurity,DC=org, DC=DomainDnsZones,DC=lab,DC=adsecurity,DC=org…

Forest                     : lab.adsecurity.org
CurrentTime                : 1/27/2016 5:31:38 PM
HighestCommittedUsn        : 161898
OSVersion                  : Windows Server 2012 R2 Datacenter
Roles                      : {PdcRole, RidRole, InfrastructureRole}
Domain                     : child.lab.adsecurity.org
IPAddress                  : 172.16.11.21
SiteName                   : Default-First-Site-Name
SyncFromAllServersCallback :
InboundConnections         : {612c2d75-1c35-4073-a8a9-d41169665000, 8797cbb4-fe09-49dc-8891-952f38822eda}
OutboundConnections        : {71ea129f-8d56-4bd0-9b68-d80e89ae7385, 36bfdadf-777d-4bad-9427-bc148cea256f}
Name                       : ADSDC11.child.lab.adsecurity.org
Partitions                 : {CN=Configuration,DC=lab,DC=adsecurity,DC=org, CN=Schema,CN=Configuration,DC=lab,DC=adsecurity,DC=org,
DC=ForestDnsZones,DC=lab,DC=adsecurity,DC=org, DC=child,DC=lab,DC=adsecurity,DC=org…}
```

## II. Discover Enterprise Services without Network Scanning
- Use SPN method I described on **SPN Enumeration** module.
- Ex: SPN scanning can also discover what Windows computers have RDP enabled (TERMSERV), WinRM enabled (WSMAN), etc.
```bash
PS C:\> get-adcomputer -filter {ServicePrincipalName -like "*TERMSRV*"} -Properties OperatingSystem,OperatingSystemVersion,OperatingSystemServicePack,
PasswordLastSet,LastLogonDate,ServicePrincipalName,TrustedForDelegation,TrustedtoAuthForDelegation

DistinguishedName          : CN=ADSDC02,OU=Domain Controllers,DC=lab,DC=adsecurity,DC=org
DNSHostName                : ADSDC02.lab.adsecurity.org
Enabled                    : True
LastLogonDate              : 1/20/2016 6:46:18 AM
Name                       : ADSDC02
ObjectClass                : computer
ObjectGUID                 : 1efe44af-d8d9-420b-a66a-8d771d295085
OperatingSystem            : Windows Server 2008 R2 Datacenter
OperatingSystemServicePack : Service Pack 1
OperatingSystemVersion     : 6.1 (7601)
PasswordLastSet            : 12/31/2015 6:34:15 AM
SamAccountName             : ADSDC02$
ServicePrincipalName       : {DNS/ADSDC02.lab.adsecurity.org, HOST/ADSDC02/ADSECLAB, HOST/ADSDC02.lab.adsecurity.org/ADSECLAB,
GC/ADSDC02.lab.adsecurity.org/lab.adsecurity.org…}
SID                        : S-1-5-21-1581655573-3923512380-696647894-1103
TrustedForDelegation       : True
TrustedToAuthForDelegation : False
UserPrincipalName          :

DistinguishedName          : CN=ADSDC01,OU=Domain Controllers,DC=lab,DC=adsecurity,DC=org
DNSHostName                : ADSDC01.lab.adsecurity.org
Enabled                    : True
LastLogonDate              : 1/20/2016 6:47:21 AM
Name                       : ADSDC01
ObjectClass                : computer
ObjectGUID                 : 31b2038d-e63d-4cfe-b7b6-77206c325af9
OperatingSystem            : Windows Server 2008 R2 Datacenter
OperatingSystemServicePack : Service Pack 1
OperatingSystemVersion     : 6.1 (7601)
PasswordLastSet            : 12/31/2015 6:34:14 AM
SamAccountName             : ADSDC01$
ServicePrincipalName       : {ldap/ADSDC01.lab.adsecurity.org/ForestDnsZones.lab.adsecurity.org,
ldap/ADSDC01.lab.adsecurity.org/DomainDnsZones.lab.adsecurity.org, TERMSRV/ADSDC01,
TERMSRV/ADSDC01.lab.adsecurity.org…}
SID                        : S-1-5-21-1581655573-3923512380-696647894-1000
TrustedForDelegation       : True
TrustedToAuthForDelegation : False
UserPrincipalName          :
```
## III. Discover Computers without Network Scanning
```bash
PS C:\> get-adcomputer -filter {PrimaryGroupID -eq “515”} -Properties OperatingSystem,OperatingSystemVersion,OperatingSystemServicePack,Passwo
t,LastLogonDate,ServicePrincipalName,TrustedForDelegation,TrustedtoAuthForDelegation

DistinguishedName          : CN=ADSWRKWIN7,CN=Computers,DC=lab,DC=adsecurity,DC=org
DNSHostName                : ADSWRKWIN7.lab.adsecurity.org
Enabled                    : True
LastLogonDate              : 8/29/2015 6:40:16 PM
Name                       : ADSWRKWIN7
ObjectClass                : computer
ObjectGUID                 : e8b3bed2-75b4-4512-a4f0-6d9c2d975c70
OperatingSystem            : Windows 7 Enterprise
OperatingSystemServicePack : Service Pack 1
OperatingSystemVersion     : 6.1 (7601)
PasswordLastSet            : 8/29/2015 6:40:12 PM
SamAccountName             : ADSWRKWIN7$
ServicePrincipalName       : {TERMSRV/ADSWRKWin7.lab.adsecurity.org, TERMSRV/ADSWRKWIN7, RestrictedKrbHost/ADSWRKWIN7, HOST/ADSWRKWIN7…}
SID                        : S-1-5-21-1581655573-3923512380-696647894-1104
TrustedForDelegation       : False
TrustedToAuthForDelegation : False
UserPrincipalName          :

DistinguishedName          : CN=ADSAP01,CN=Computers,DC=lab,DC=adsecurity,DC=org
DNSHostName                : ADSAP01.lab.adsecurity.org
Enabled                    : True
LastLogonDate              : 1/24/2016 11:03:41 AM
Name                       : ADSAP01
ObjectClass                : computer
ObjectGUID                 : b79bb5e3-8f9e-4ee0-a30c-5f66b61da681
OperatingSystem            : Windows Server 2008 R2 Datacenter
OperatingSystemServicePack : Service Pack 1
OperatingSystemVersion     : 6.1 (7601)
PasswordLastSet            : 1/4/2016 6:38:16 AM
SamAccountName             : ADSAP01$
ServicePrincipalName       : {WSMAN/ADSAP01.lab.adsecurity.org, WSMAN/ADSAP01, TERMSRV/ADSAP01.lab.adsecurity.org, TERMSRV/ADSAP01…}
SID                        : S-1-5-21-1581655573-3923512380-696647894-1105
TrustedForDelegation       : False
TrustedToAuthForDelegation : False
UserPrincipalName          :
```
- The same data for Domain Controllers can be gathered by changing the PrimaryGroupID value to "516"
```bash
PS C:\> get-adcomputer -filter {PrimaryGroupID -eq “516”} -Properties OperatingSystem,OperatingSystemVersion,OperatingSystemServicePack,PasswordLastSe
t,LastLogonDate,ServicePrincipalName,TrustedForDelegation,TrustedtoAuthForDelegation

DistinguishedName          : CN=ADSDC02,OU=Domain Controllers,DC=lab,DC=adsecurity,DC=org
DNSHostName                : ADSDC02.lab.adsecurity.org
Enabled                    : True
LastLogonDate              : 1/20/2016 6:46:18 AM
Name                       : ADSDC02
ObjectClass                : computer
ObjectGUID                 : 1efe44af-d8d9-420b-a66a-8d771d295085
OperatingSystem            : Windows Server 2008 R2 Datacenter
OperatingSystemServicePack : Service Pack 1
OperatingSystemVersion     : 6.1 (7601)
PasswordLastSet            : 12/31/2015 6:34:15 AM
SamAccountName             : ADSDC02$
ServicePrincipalName       : {DNS/ADSDC02.lab.adsecurity.org, HOST/ADSDC02/ADSECLAB, HOST/ADSDC02.lab.adsecurity.org/ADSECLAB,
GC/ADSDC02.lab.adsecurity.org/lab.adsecurity.org…}
SID                        : S-1-5-21-1581655573-3923512380-696647894-1103
TrustedForDelegation       : True
TrustedToAuthForDelegation : False
UserPrincipalName          :

DistinguishedName          : CN=ADSDC01,OU=Domain Controllers,DC=lab,DC=adsecurity,DC=org
DNSHostName                : ADSDC01.lab.adsecurity.org
Enabled                    : True
LastLogonDate              : 1/20/2016 6:47:21 AM
Name                       : ADSDC01
ObjectClass                : computer
ObjectGUID                 : 31b2038d-e63d-4cfe-b7b6-77206c325af9
OperatingSystem            : Windows Server 2008 R2 Datacenter
OperatingSystemServicePack : Service Pack 1
OperatingSystemVersion     : 6.1 (7601)
PasswordLastSet            : 12/31/2015 6:34:14 AM
SamAccountName             : ADSDC01$
ServicePrincipalName       : {ldap/ADSDC01.lab.adsecurity.org/ForestDnsZones.lab.adsecurity.org,
ldap/ADSDC01.lab.adsecurity.org/DomainDnsZones.lab.adsecurity.org, TERMSRV/ADSDC01,
TERMSRV/ADSDC01.lab.adsecurity.org…}
SID                        : S-1-5-21-1581655573-3923512380-696647894-1000
TrustedForDelegation       : True
TrustedToAuthForDelegation : False
UserPrincipalName          :
```
## IV. Identify Admin Accounts
- There are two effective methods for discovering accounts with elevated rights in Active Directory. The first is the standard group enumeration method which identifies all members of the standard Active Directory admin groups: Domain Admins, Administrators, Enterprise Admins, etc. Typically getting recursive group membership for the domain "Adminsitrators" group will provide a list of all AD admins
- The second method involves identifying all accounts which have the attribute “AdminCount” set to 1
```bash
PS C:\> get-aduser -filter {AdminCount -eq 1} -Properties Name,AdminCount,ServicePrincipalName,PasswordLastSet,LastLogonDate,MemberOf

AdminCount        : 1
DistinguishedName : CN=ADSAdministrator,CN=Users,DC=lab,DC=adsecurity,DC=org
Enabled           : True
GivenName         :
LastLogonDate     : 1/27/2016 8:55:48 AM
MemberOf          : {CN=Administrators,CN=Builtin,DC=lab,DC=adsecurity,DC=org, CN=Schema Admins,CN=Users,DC=lab,DC=adsecurity,DC=org, CN=Group
Policy Creator Owners,CN=Users,DC=lab,DC=adsecurity,DC=org, CN=Enterprise Admins,CN=Users,DC=lab,DC=adsecurity,DC=org…}
Name              : ADSAdministrator
ObjectClass       : user
ObjectGUID        : 72ac7731-0a76-4e5a-8e5d-b4ded9a304b5
PasswordLastSet   : 12/31/2015 8:45:27 AM
SamAccountName    : ADSAdministrator
SID               : S-1-5-21-1581655573-3923512380-696647894-500
Surname           :
UserPrincipalName :

AdminCount           : 1
DistinguishedName    : CN=krbtgt,CN=Users,DC=lab,DC=adsecurity,DC=org
Enabled              : False
GivenName            :
LastLogonDate        :
MemberOf             : {CN=Denied RODC Password Replication Group,CN=Users,DC=lab,DC=adsecurity,DC=org}
Name                 : krbtgt
ObjectClass          : user
ObjectGUID           : 3d5be8dd-df7f-4f84-b2cf-4556310a7292
PasswordLastSet      : 8/27/2015 7:10:22 PM
SamAccountName       : krbtgt
ServicePrincipalName : {kadmin/changepw}
SID                  : S-1-5-21-1581655573-3923512380-696647894-502
Surname              :
UserPrincipalName    :
```
## V. Find Admin Groups
```bash
PS C:\> get-adgroup -filter {GroupCategory -eq 'Security' -AND Name -like "*admin*"}

DistinguishedName : CN=Domain Admins,CN=Users,DC=lab,DC=adsecurity,DC=org
GroupCategory : Security
GroupScope : Global
Name : Domain Admins
ObjectClass : group
ObjectGUID : 5621cc71-d318-4e2c-b1b1-c181f630e10e
SamAccountName : Domain Admins
SID : S-1-5-21-1581655573-3923512380-696647894-512

DistinguishedName : CN=Workstation Admins,OU=AD Management,DC=lab,DC=adsecurity,DC=org
GroupCategory : Security
GroupScope : Global
Name : Workstation Admins
ObjectClass : group
ObjectGUID : 88cd4d52-aedb-4f90-9ebd-02d4c0e322e4
SamAccountName : WorkstationAdmins
SID : S-1-5-21-1581655573-3923512380-696647894-2627
```
## VI. Identify Partner Organizations
- External email addresses are added to the organization’s Global Address List (GAL) in order to facilitate collaboration among partner organization. These email addresses are created as contact objects in Active Directory.
```bash
PS C:\> get-adobject -filter {ObjectClass -eq “Contact”} -Prop *

CanonicalName                   : lab.adsecurity.org/Contaxts/Admiral Ackbar
CN                              : Admiral Ackbar
Created                         : 1/27/2016 10:00:06 AM
createTimeStamp                 : 1/27/2016 10:00:06 AM
Deleted                         :
Description                     :
DisplayName                     :
DistinguishedName               : CN=Admiral Ackbar,OU=Contaxts,DC=lab,DC=adsecurity,DC=org
dSCorePropagationData           : {12/31/1600 4:00:00 PM}
givenName                       : Admiral
instanceType                    : 4
isDeleted                       :
LastKnownParent                 :
mail                            : admackbar@RebelFleet.org
Modified                        : 1/27/2016 10:00:24 AM
modifyTimeStamp                 : 1/27/2016 10:00:24 AM
Name                            : Admiral Ackbar
nTSecurityDescriptor            : System.DirectoryServices.ActiveDirectorySecurity
ObjectCategory                  : CN=Person,CN=Schema,CN=Configuration,DC=lab,DC=adsecurity,DC=org
ObjectClass                     : contact
ObjectGUID                      : 52c80a1d-a614-4889-92d4-1f588387d9f3
ProtectedFromAccidentalDeletion : False
sDRightsEffective               : 15
sn                              : Ackbar
uSNChanged                      : 275113
uSNCreated                      : 275112
whenChanged                     : 1/27/2016 10:00:24 AM
whenCreated                     : 1/27/2016 10:00:06 AM
```
## VII. Identify Domain Password Policy
- The domain password policy is easily enumerated using either "net accounts" or the AD PowerShell module "Get-ADDefaultDomainPasswordPolicy".
```bash
PS C:\> Get-ADDefaultDomainPasswordPolicy

ComplexityEnabled           : True
DistinguishedName           : DC=lab,DC=adsecurity,DC=org
LockoutDuration             : 00:30:00
LockoutObservationWindow    : 00:30:00
LockoutThreshold            : 0
MaxPasswordAge              : 42.00:00:00
MinPasswordAge              : 1.00:00:00
MinPasswordLength           : 7
objectClass                 : {domainDNS}
objectGuid                  : bbf0907c-3171-4448-b33a-76a48d859039
PasswordHistoryCount        : 24
ReversibleEncryptionEnabled : False
```

