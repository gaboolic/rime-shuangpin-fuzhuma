import subprocess

result = subprocess.run(['./program/unittest/rime_api_console', 'gegegojxyzgegegojxdegoge'], capture_output=True, text=True)

print(result.stdout)
