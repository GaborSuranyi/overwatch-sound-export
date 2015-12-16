import os, subprocess, shutil, hashlib, csv, pprint, sys, json

print "Overwatch wem extractor v0.2"
# get config
with open('config.json') as data_file:
	config = json.load(data_file)
counter = 1
unknown = 0
# get hash storage
hashStorage = dict([])
with open(config["paths"]["important"], 'r') as csvfile:
	hashreader = csv.reader(csvfile, delimiter=',')
	for row in hashreader:
		#print ', '.join(row)
		hashStorage[row[0]] = row[1]
with open(config["paths"]["noise"], 'r') as csvfile:
	hashreader = csv.reader(csvfile, delimiter=',')
	for row in hashreader:
		#print ', '.join(row)
		hashStorage[row[0]] = row[1]

open(config["paths"]["unknowns"], 'a').truncate()

folder = config["paths"]["casc"]
for dir in os.listdir(folder):
	for file in os.listdir(folder+'/'+dir):
		if file.endswith(".xxx"):
			path = folder+'/'+dir+'/'+file
			with open(path, 'r') as f:
				first_line = f.readline()
				if "WAVEfmt" in first_line[:20]:
					if counter % 100 == 0:
						print counter
					counter = counter + 1

					FNULL = open(os.devnull, 'w')
					subprocess.call(config["paths"]["tools"]+'ww2ogg.exe '+path+' --pcb '+config["paths"]["tools"]+'packed_codebooks_aoTuV_603.bin', stdout=FNULL, stderr=subprocess.STDOUT)
					if os.path.isfile(path.replace(".xxx", ".ogg")):
						shutil.move(path.replace(".xxx", ".ogg"), config["paths"]["exported"]+str(counter)+".ogg")
						temp_path = config["paths"]["exported"]+str(counter)+".ogg"
						subprocess.call(config["paths"]["tools"]+'revorb.exe '+temp_path, stdout=FNULL, stderr=subprocess.STDOUT)
						hash = hashlib.md5(temp_path).hexdigest()
						if hash in hashStorage:
							shutil.move(temp_path, config["paths"]["exported"]+hashStorage[hash])
						else:
							unknown = unknown + 1
							if(not config["full_extract"] and unknown == 1000):
								sys.exit("1k unknowns listed. Please proceed to categorize. Ty! <3")
							log = open(config["paths"]["unknowns"], 'a')
							log.write(hash + ',' + temp_path.replace(config["paths"]["exported"], "") + "\n")
							log.close()
