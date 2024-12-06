# [Sharphound](https://github.com/BloodHoundAD/SharpHound)
## sharphound.exe
```bash
.\sharphound.exe -d local.domain --CollectionMethods DCOnly --ldapusername "username" --ldappassword "password"
```
## sharphound.ps1
- this is a polymorphic loader for the compiled code of sharphound.exe
```bash
Import-Module sharphound.ps1
Invoke-BloodHound -CollectionMethod DCOnly -LdapUsername "username" -LdapPassword "password" -ZipFileName output.zip -d local.domain
```
# Additional ways: [ADfind.exe](https://www.joeware.net/freetools/tools/adfind/)
```bash
.\AdFind.exe -default -f "(|(|(samaccounttype=268435457)(samaccounttype=268435456)(samaccounttype=536870913)(samaccounttype=536870912)(primarygroupid=*))(&(sAMAccountType=805306369)(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))(|(samAccountType=805306368)(samAccountType=805306369)(samAccountType=268435456)(samAccountType=268435457)(samAccountType=536870913)(samAccountType=536870912)(objectClass=domain)(&(objectcategory=groupPolicyContainer)(flags=*))(objectcategory=organizationalUnit))(objectclass=domain)(|(samaccounttype=268435456)(samaccounttype=268435457)(samaccounttype=536870913)(samaccounttype=536870912)(samaccounttype=805306368)(samaccounttype=805306369)(objectclass=domain)(objectclass=organizationalUnit)(&(objectcategory=groupPolicyContainer)(flags=*)))(|(&(&(objectcategory=groupPolicyContainer)(flags=*))(name=*)(gpcfilesyspath=*))(objectClass=domain)(objectcategory=organizationalUnit))(&(serviceprincipalname=*)(samaccounttype=805306368)))"
```
