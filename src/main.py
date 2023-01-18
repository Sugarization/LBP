import util
import subprocess

from pathlib import Path
from os import chdir

def main():
    typeList = ['.fa', '.fsa', '.fasta']
    remove_unmasked_database = True

    support.setSystemPath()

    promptDic = support.getPrompt()
    prompt = lambda section : print(promptDic[section])
    platform = support.getPlatform()

    if platform == 'Windows':
        os.system('@echo off')
        
    cleanInput = lambda: input().strip().replace('\\', '')
        
    prompt('welcome')
        
    prompt('fasta')
    genePath = Path(cleanInput())
    print(genePath)

    print('Enter path to database FASTA file or masked database:')
    rawDBPath = Path(cleanInput())
    print(rawDBPath)

    print('Enter working dirctory: (Leave blank to use the directory of the gene pattern.)')
    workingPathStr = cleanInput()

    p = Path(workingPathStr) if workingPathStr else genePath.parent
    print(p)

    if not p.exists():
    	p.mkdir()

    dbType = rawDBPath.suffix
    maskedDBName = ''

    if dbType in typeList:
        dbPath = p / '_database'
        dbName = rawDBPath.stem
        maskName = dbName + '_mask.asnb'
        maskedDBName = 'masked_' + dbName
        if not dbPath.exists():
            dbPath.mkdir()
            chdir(dbPath)
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
    	    # unlink
    	    print('\n[Script Info] Unmasked database removed.')
        
    else:
    	if rawDBPath.exists():
    		(_, _, fileList) = next(os.walk(rawDBPath))
    		maskedDBName = Path(fileList[0]).stem
    		print('\n[Script Info] Treating database folder as masked database.')
    		print('\n[Script Info] Beginning blast...')
    		chdir(rawDBPath)
    	else:
    		print('\n[Error] Cannot find masked database.')
    		exit(1)


    subprocess.run(['blastn', '-query', str(genePath), '-db', maskedDBName, 
    '-outfmt', '7', '-out', 'blastResult.out', '-num_threads', '5'])
    subprocess.call(['move', 'blastResult.out', str(p)])

    print('\n[Script Info] Blast finished.')

    promptText.close()
    
if __name__ == '__main__':
    main()
    

