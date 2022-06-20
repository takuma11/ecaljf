from mp_api.matproj import MPRester
import pymatgen.core as mg
from pymatgen.ext.matproj import MPRester
import os,sys,subprocess
import datetime



args = sys.argv

if len(args) == 1:
    print("please put mpid.\nex: mp-124\n")
    sys.exit()

#PATH = "/home/ktn1/matminer_fujiwara/mpcif/" + args[1] + ".cif"
#PATH = "mpcif/" + args[1] + ".cif"

#if os.path.isfile(PATH) == False:
    #print("Oh! this mpid's cif is not exist")
    #sys.exit()

aa = args[1].split("-")
num = aa[0] + aa[1]
print(num)



API_KEY = 'FXOVZxCb9eGkIMrV5JwE'  

try:
    with MPRester(API_KEY) as mpr:
        material = mpr.get_data(args[1])

except:
    print("Oh! can't get date from mpAPI")
    sys.exit()



if len(material) == 0:
    print("APIdate is empty")
    sys.exit()

    

#print(material) #many date of material, dic type
#sys.exit()
    
for item in material:

    mate = item["pretty_formula"]
    os.makedirs(num,exist_ok=True)
    os.chdir(num)
    print(item['material_id'])    # result is 'mp-101'
    struc = mpr.get_structure_by_material_id(item['material_id'])
    struc.to(fmt='poscar', filename='POSCAR')

#sys.exit()

subprocess.run("pwd")

#sys.exit()

#subprocess.run(["cp","../mpcif/"+args[1]+".cif","./"])

#sys.exit()
#subprocess.run(["cif2cell",args[1]+".cif","-p","vasp","--vasp-cartesian","--vasp-format=5"])
#sys.exit()
subprocess.run(["vasp2ctrl","POSCAR"])
subprocess.run(["cp","ctrls.POSCAR.vasp2ctrl","ctrls." + num])
subprocess.run(["ctrlgenM1.py",num])
subprocess.run(["cp","ctrlgenM1.ctrl."+num,"ctrl."+num])
subprocess.run(["lmfa",num])
subprocess.run(["mpirun","-np","4","lmf-MPIK",num])
subprocess.run(["getsyml",num])
subprocess.run(["job_band",num,"-np","4"])
subprocess.run(["job_tdos",num,"-np","4"])

#os.chdir("../")
#subprocess.run("pwd")
subprocess.run(["editglt.py",mate,num])
#os.chdir(mate)

if os.path.isfile("new.glt") == True:
    subprocess.run(["gnuplot","new.glt"])

else:
    print("sorry can't find new.glt")

os.chdir("../")
