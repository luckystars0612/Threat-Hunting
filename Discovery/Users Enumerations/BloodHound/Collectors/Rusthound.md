# [Rusthound](https://github.com/NH-RED-TEAM/RustHound)
- Enum all data in domain
```bash
./rusthound.exe -d domain.local
```
- If using vm that doesn't join domain, use username and password for ldap enum
```bash
./rusthound.exe -d domain.local -u username -p password
```
- Bloodhound can load .zip file, so we can specify output to zip type
```bash
./rusthound.exe -d domain.local -u username -p password -o output_dir -z
```
***Note: In my opinion, Rusthound is more quickly than Sharphound on data collecting aspect***