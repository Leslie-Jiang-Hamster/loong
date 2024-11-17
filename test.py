import loong

assert set(loong.all_files()) == set(['sample/sample1/sample1.mgf', 'sample/sample2/sample2.mgf'])

all_ms = loong.split_ms(loong.read_file('sample/sample1/sample1.mgf'))
assert loong.ms_seq(all_ms[-1]) == 'VGAGAPVYLAAVLEYLTAEILELAGNAAR'
assert loong.ms_seq(all_ms[0]) == 'LVHVEEPHTETVR'

PTM_ms = all_ms[3]
assert loong.ms_seq(PTM_ms) == 'GLVASLDM[15.99]QLEQAQGTR'

assert loong.ms_len(PTM_ms) == 17