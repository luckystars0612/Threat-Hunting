# Data Hunting Overview
## 1. Network shares and fileservers
* Native net windows
```bash
# List shares on the local host
net share

# List network computers
net view

# List shares on a remote PC
net view COMPUTER_NAME /all
```
- List all computers that are a part of the "Domain Computers" group and filter all computers that have "FILE" in their name
```bash
net group "Domain Computers" /domain | findstr "FILE"
```
* Powerview (pywerview)
```bash
# Find network shares and fileservers using Powerview
Find-DomainShare
Get-DomainFileServer
```
```bash
# Find where a specific user is logged in using Powerview:
Find-DomainUserLocation -UserIdentity USER_NAME

# Find where a group of users are logged in using Powerview:
Find-DomainUserLocation -UserGroupIdentity GROUP_NAME

# Powerview modules in Empire:
situational_awareness/network/powerview/user_hunter

```