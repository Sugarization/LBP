import support
import subprocess

typeList = ['.fa', '.fsa', '.fasta']
remove_unmasked_database = True

support.setSystemPath()

prompts = support.getPrompt()
platform = support.getPlatform()

os.system('@echo off')
print('Enter path to gene pattern FASTA file:')
genePath = Path(input())

print('Enter path to database FASTA file or masked database:')
rawDBPath = Path(input())

print('Enter working dirctory: (Leave blank to use the directory of the gene pattern.)')
workingPathStr = input()

p = Path(workingPathStr) if workingPathStr != '' else genePath.parent

if not p.exists():
	os.system('mkdir ' + str(p))

dbType = rawDBPath.suffix
maskedDBName = ''

if dbType in typeList:
    dbPath = p / '_database'
    dbName = rawDBPath.stem
    maskName = dbName + '_mask.asnb'
    maskedDBName = 'masked_' + dbName
    if not dbPath.exists():
        os.system('mkdir ' + str(dbPath))
        os.chdir(dbPath)
    subprocess.run(['makeblastdb', '-in', str(rawDBPath), '-parse_seqids',  
    '-title', dbName, '-dbtype', 'nucl', '-out', dbName])
    print('\n[Script Info] Plain database generated.\n')
    subprocess.run(['dustmasker', '-in', dbName, '-infmt', 'blastdb',
    '-parse_seqids', '-outfmt', 'maskinfo_asn1_bin', '-out', maskName])
    print('\n[Script Info] Database mask generated (with dustmasker).\n')
    subprocess.run(['makeblastdb', '-in', dbName, '-input_type', 'blastdb', 
    '-dbtype', 'nucl', '-parse_seqids', 
    '-mask_data', maskName, '-out', maskedDBName, '-title', dbName])
    print('\n[Script Info] Masked database generated. beginning blast...\n')
    if remove_unmasked_database:
	    os.system('del ' + dbName + '*')
	    print('\n[Script Info] Unmasked database removed.')
    
else:
	if rawDBPath.exists():
		(_, _, fileList) = next(os.walk(rawDBPath))
		maskedDBName = Path(fileList[0]).stem
		print('\n[Script Info] Treating database folder as masked database.')
		print('\n[Script Info] Beginning blast...')
		os.chdir(rawDBPath)
	else:
		print('\n[Error] Cannot find masked database.')
		exit(1)


subprocess.run(['blastn', '-query', str(genePath), '-db', maskedDBName, 
'-outfmt', '7', '-out', 'blastResult.out', '-num_threads', '5'])
os.system('move blastResult.out ' + str(p))

print('\n[Script Info] Blast finished.')

promptText.close()
