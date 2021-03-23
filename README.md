# ReportCrypto


![alt text](https://github.com/adel-saada/ReportCrypto/blob/main/logo_project.PNG?raw=true)

## How To Use ##

1. Clone the repository
```bash
git clone https://github.com/adel-saada/ReportCrypto.git
```
2. Access to the folder
```bash
cd ReportCrypto/
```

3. Install VirtualEnvironment

  ```[DEBIAN/UBUNTU] ``` 
  ```bash
  apt-get install python3-venv 
  ```

  ```[CENTOS/REDHAT]```
  ```bash
  yum install python3-venv 
  ```


4. Create your env
```bash
python3 -m venv myenv
```

5. Activate your env
```bash
source myenv/bin/activate
```

6. Install all requirement (package python for use script)
```bash
python -m pip install -r requirement.txt
```

7. Create your file '.env' which contains credential gmail
```bash
vim .env
```
```
GMAIL_PASSWORD='<your_gmail_password>'
GMAIL_ADRESS='<your_gmail_adress>'
```
8. Edit file possession.csv for put respectively the name of the crypto, the number of currency and the total invested

- Separator is '|'  (ALTGR + 6)
- The exact name of the crypto (you can complete with a number if you had invest for the same crypto but with different value, like bitcoin1 bitcoin2 bitcoin3000..)
- You can add others crypto than in the example below of course, but just write the exact name of crypto
- Structure is : "exact_name_crypto"(string)|total_currency_of_this_crypto(float)|total_invest(int)

```EXAMPLE : ```
```
"bitcoin"|0.0041631|12
"ethereum"|0.000532081|11
"ethereum2"|0.0012244117|10
"chainlink"|1.86015018|14
"chainlink2"|1.09068143|18
"hedera-hashgraph"|100.589|1
"theta-network"|5.4435|12
"vechain"|200|10
"oasis-network"|12.699|10
"pundi-x"|0.127|10
```

9. Run script with in parameter your file csv
```bash
./infos_crypto.py --file possession.csv
```

10. [OPTIONAL] Add Crontab

```bash
crontab -e 
```
```
#Script Crypto Informations
SHELL=/bin/bash
0 9,21 * * * cd /home/your/path/report_crypto/ && ./botenv/bin/python3 ./infos_crypto.py --file possession.csv
```
