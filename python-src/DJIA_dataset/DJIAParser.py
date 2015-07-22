f=open("DJIA.csv")
chaosf=open("ChaosAttractorInputSequence_DJIA.txt","w")
line_toks=[]
indices=[]
line=f.readline()
while True:
	line=f.readline()
	if not line:
		break
	line_toks=line.split(",")
	indices.append(line_toks[1])
print "DJIA historical data:",indices
print "DJIA historical data size:",len(indices)
for i in indices:
	chaosf.write(i)
	chaosf.write(",")	
