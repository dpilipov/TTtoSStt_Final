from TIMBER.Tools.Common import ExecuteCmd
import sys
das = {
    "18": {
        "DataD": "/JetHT/Run2018D-UL2018_MiniAODv2_NanoAODv9-v2/NANOAOD",
    }
}

def GetFiles(das_name,setname,year):
    ExecuteCmd('dasgoclient -query "file dataset=%s" > %s_%s_temp.txt'%(das_name,setname,year),'dryrun' in sys.argv)
    f = open('%s_%s_temp.txt'%(setname,year),'r')
    fout = open('%s_%s.txt'%(setname,year),'w')
    for l in f.readlines():
        fout.write('root://cmsxrootd.fnal.gov/'+l)
        print(l)
    f.close()
    fout.close()
#    if 'dryrun' not in sys.argv:
#        ExecuteCmd('rm %s_%s_temp.txt'%(setname,year),'dryrun' in sys.argv)

latex_lines = {k:[] for k in das.keys()}
for year in das.keys():
    print(year)
    for setname in das[year].keys():
        if 'Tprime' in setname:
            for T_mass in range(800,1900,100):
                for phi_mass in [75,100,125,175,200,250,350,450,500]:
                    das_name = das[year][setname].replace('MTMASS','MT'+str(T_mass)).replace('MHMASS','MH'+str(phi_mass))
                    setname_mod = '%s-%s-%s'%(setname, T_mass, phi_mass)
                    GetFiles(das_name,setname_mod,year)
                    latex_lines[year].append('| %s | %s |'%(setname_mod.replace('-', ' ')+' GeV',das_name))
        else:
            GetFiles(das[year][setname],setname,year)
            latex_lines[year].append('| %s | %s |'%(setname,das[year][setname]))
            
for y in sorted(latex_lines.keys()):
    print ('\n20%s'%y)
    print ('| Setname | DAS location |')
    print ('|---------|--------------|')
    for l in latex_lines[y]: print (l)
