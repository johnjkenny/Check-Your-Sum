# Check-Your-Sum
Check-Your-Sum is a tool that allows you to create md5, sha1, sha224, sha256, sha384, and sha512 hash sums for a file
or string. It also checks the integrity of a file or string by comparing hash sums.

## Installation

Check-Your-Sum is a python package which can be found on [Python Package Index (PyPi)](https://pypi.org/project/Check-Your-Sum/). Run the following command to install:<br>
``` bash
pip install check-your-sum
```

## Import Check-Your-Sum Into Your Projects
``` python
from CheckYourSum.check_your_sum import CheckSum
```

## Usage
The CheckSum class requires a file path or string to be passed to the constructor. This is known as the 'ingest'
argument. It is also required to specify what type of ingest is being supplied to the 'ingest_type' argument. The choices
are 'file' or 'string'. The default is 'file'. The class has a 'hash_type' argument which is the hash algorithm to be
used. The hash type can be one of the following: md5, sha1, sha224, sha256, sha384, sha512. The default hash type is
sha256. CheckSum config options:

    key: name = (str) Name of the log file to be created. Default is 'check_your_sum.log'.

    key: ingest = (str) [Required] File or string to be hashed.

    key: ingest_type = (str) Type of data to be hashed. Default is 'file'.

    key: hash_type = (str) Type of hash to be created. Default is 'sha256'.

    key: verify_sum = (str) Checksum to be verified. Default is None.

Setting the configuration options on CheckSum() can be made by passing the config as key=value to the class, using a dictionary to define the key values, or by using dot notation to define particular values.

The ingest (file or string) must be set before calling CheckSum().create_hash() or CheckSum().create_all_hashes(). Example:

``` python
check_sum = CheckSum(ingest='/path/to/file.txt', ingest_type='file').create_hash()
# or
check_sum = CheckSum()
check_sum.ingest = '/path/to/file.txt'
check_sum.ingest_type = 'file'
created_hash = check_sum.create_hash()
```

### Create Hash Sum

#### create_hash Method
create_hash() will print the hash to the console on a successful run. It will return a tuple containing the hash (index 0) and the verified state (index 1). Example:
    
``` python
check_sum = CheckSum(ingest='test_string', ingest_type='string', hash_type='sha256').create_hash()
print(check_sum)
```
Output as png:<br>
![message Sample](/assets/output_tuple_example.png)

#### create_all_hashes Method
create_all_hashes() will print the hash to the console on a successful run of each hash algorithm. It will return a
dictionary containing the hash algorithm (key) and the hash (value).
``` python
check_sum = CheckSum(ingest='test_string', ingest_type='string').create_all_hashes()
for key, value in check_sum.items():
    print('{}: {}'.format(key, value))
```
Output as png:
![message Sample](/assets/output_dictionary_key_value.png)

### Verify Checksum and Use Dictionary to Set Configuration Options:
ISO file and checksum provided by [Ubuntu](https://ubuntu.com/download/desktop/thank-you?version=20.04.4&architecture=amd64#)

#### Successful Check:
``` python
config = {
    'ingest': 'ubuntu-20.04.4-desktop-amd64.iso',
    'ingest_type': 'file',
    'hash_type': 'sha256',
    'verify_sum': 'f92f7dca5bb6690e1af0052687ead49376281c7b64fbe4179cc44025965b7d1c' # Correct sum
}
hash_created = CheckSum(**config).create_hash()
print(hash_created)
```
Output as png:
![message Sample](/assets/verify_sum_success_example.png)

#### Failed Check:
``` python
config = {
    'ingest': 'ubuntu-20.04.4-desktop-amd64.iso',
    'ingest_type': 'file',
    'hash_type': 'sha256',
    'verify_sum': '4b641e9a923d1ea57e18fe41dcb543e2c4005c41ff210864a710b0fbb2654c11' # Incorrect sum
}
hash_created = CheckSum(**config).create_hash()
print(hash_created)
```
Output as png:
![message Sample](/assets/verify_sum_fail_example.png)

### Using Check-Your-Sum as Command Line Tool:

Configuring Check-Your-Sum as a command line tool can be done in the following ways:

#### 1. Running Check-Your-Sum directly from pip install path:
``` bash
python lib/python3.8/site-packages/CheckYourSum/check_your_sum.py -i ubuntu-20.04.4-desktop-amd64.iso -it file -ht sha256 -vs f92f7dca5bb6690e1af0052687ead49376281c7b64fbe4179cc44025965b7d1c
```

#### 2. Creating a command alias in your shell config file to run Check-Your-Sum:
.zshrc is used in this example because I am using the zsh shell. You can change this to your shell config file.
``` bash
echo 'alias check-your-sum="python /home/user1/.local/lib/python3.8/site-packages/CheckYourSum/check_your_sum.py"' >> .zshrc
source .zshrc
check-your-sum -i test -it string
```

#### 3. Creating a Symbolic Link to Check-Your-Sum:
``` bash
chmod +x /home/user1/.local/lib/python3.8/site-packages/checkYourSum/check_your_sum.py
ln -s /home/user1/.local/lib/python3.8/site-packages/checkYourSum/check_your_sum.py /home/user1/.local/bin/check-your-sum
check-your-sum -i test -it string 
```

#### 4. Importing the ArgParser class into your script:
``` python
from CheckYourSum.check_your_sum import ArgParser, CheckSum


if __name__ == '__main__':
    PARSER = ArgParser()
    if PARSER.args:
        CHECK_SUM = CheckSum(**PARSER.args)
        if CHECK_SUM.hash_type == 'all':
            CHECK_SUM.create_all_hashes()
        else:
            CHECK_SUM.create_hash()
```
``` bash
./my_script.py -i test -it string
./my_script.py -i test -it string -ht all
```
Output as png:
![message Sample](/assets/cli_importing_argparser_into_project_example.png)
