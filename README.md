# Terrafile Update Script

Script to update Terrafile to the latest tagged versions.

```bash
🕙[ 10:42:07 ] ➜ ./terrupdate.py --help
usage: terrupdate.py [-h] [-i INPUT] [-o OUTPUT] [-m] [-v] [-c]

Upgrade Terrafile module versions

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input Terrafile YAML, default=Terrafile
  -o OUTPUT, --output OUTPUT
                        Input Terrafile YAML, default=Terrafile.new
  -m, --major           Update major versions of modules
  -v, --verbose         Verbose output
  -c, --check           Just check no output
  ```

  *Note* Currently only works with HTTPS formatted Git references.
