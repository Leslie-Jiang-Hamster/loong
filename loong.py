import config
import os
import re

def all_files():
  files = []
  for root, dirs, files_in_dir in os.walk(config.data_dir):
    for file in files_in_dir:
      file_path = os.path.join(root, file)
      if os.path.isfile(file_path):
        files.append(file_path)
  return files

def read_file(file_name):
  with open(file_name, 'r') as f:
    return f.read().strip()

def split_ms(mgf_content):
  all_ms = mgf_content.split('\n\n')
  for ms in all_ms:
    assert ms.startswith('BEGIN IONS')
    assert ms.endswith('END IONS')
  return all_ms

def ms_seq(ms):
  assert ms.startswith('BEGIN IONS')
  assert ms.endswith('END IONS')
  seq = ''
  for line in ms.split('\n'):
    if line.startswith('SEQ='):
      seq = line[4:]
  assert seq
  return seq

def ms_len(ms):
  simple_seq = re.sub(r'\[.*\]', '', ms_seq(ms))
  return len(simple_seq)

def write_ms(ms):
  with open(config.dist_file, 'a') as f:
    f.write(ms + '\n\n')

def clean():
  try:
    os.remove(config.dist_file)
  except FileNotFoundError:
    pass

def main():
  clean()
  long_ms_count = 0
  for file in all_files():
    mgf_content = read_file(file)
    long_ms = [ms for ms in split_ms(mgf_content) if ms_len(ms) > config.threshold]
    long_ms_count += len(long_ms)
    print(f'Reading {file}... Now there are {long_ms_count} long MSs.')
    for ms in long_ms:
      write_ms(ms)
  print('All done!')
  dist_size = os.path.getsize(config.dist_file)
  print(f'Output file size: {round(dist_size / 1024 / 1024, 2)} MB')

main()