import matplotlib
matplotlib.use('Agg')

import ROOT as r
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import mplhep as hep
from root_numpy import hist2array
import ctypes
from pathlib import Path

matplotlib.use('Agg')
r.gROOT.SetBatch(True)
r.gStyle.SetOptFit(111)

def errListFromTH1(hist):
    errs = []
    for i in range(1,hist.GetNbinsX()+1):
        errs.append(hist.GetBinError(i))
    return errs

def plotVarStack(hData,hsMC,mcLabels,outFile):

    dataErrs     = errListFromTH1(hData)
    hData, edges = hist2array(hData,return_edges=True)
    hArraysMC    = []
    for i, hMC in enumerate(hsMC):
        # we are assuming QCD is added last
        hTemp, _ = hist2array(hMC,return_edges=True)
        if i == len(hsMC)-1: hTemp[hTemp < 0.0] = 0.0 # zero out all negative QCD bins
        hArraysMC.append(hTemp)

    plt.style.use([hep.style.CMS])
    fig, axs = plt.subplots(2,1,sharex=True,sharey=False,gridspec_kw={'height_ratios': [4, 1],'hspace': 0.07})
    axs = axs.flatten()
    plt.sca(axs[0])

    centresData = (edges[0][:-1] + edges[0][1:])/2.

    hep.histplot(hArraysMC,edges[0],stack=True,color=['red','green','blue','yellow'],label=mcLabels,linewidth=1,histtype="fill",edgecolor='black')
    plt.errorbar(centresData,hData, yerr=dataErrs, fmt='o',color="k")    
    axs[0].legend()
    axs[0].set_ylabel("Events/bin",horizontalalignment='right', y=1.0)
    axs[1].set_xlabel(r"$m_{\phi}$",horizontalalignment='right', x=1.0)
    axs[1].set_ylabel("Data/MC")

    axs[0].set_ylim([0,max(hData)*2.0])
    hep.cms.text("WiP",loc=0)
    plt.legend(loc="best")#loc = 'best'

    #Ratio
    ratioVals = []
    for i in range(len(hData)):
        data      = hData[i]
        mc        = 0.0
        for hIdx in range(len(hArraysMC)):
            if hArraysMC[hIdx][i] < 0.0: continue # this will be the case for QCD loose sometimes (since it is data-bkg)
            mc += hArraysMC[hIdx][i]

        ratioVal     = data/(mc+0.000001)#Protect division by zero
        ratioVals.append(ratioVal)

    # switch to lower pad
    plt.sca(axs[1])
    axs[1].set_ylim([0.,2.])
    plt.errorbar(centresData,ratioVals,yerr=None, xerr=None, fmt='o',color="black")
    axs[1].axhline(y=1.0, color="grey",linestyle="--")

    #plt.tight_layout()
    print("Saving {0}".format(outFile))
    plt.savefig(outFile)
    #plt.savefig(outFile.replace(".png",".pdf"))
    plt.cla()
    plt.clf()


f           = r.TFile.Open("PseudoDataToy.root")
region      ="pass"
h2Data      = f.Get("MthvMh_particleNet_SR_{0}__nominal".format(region)) # toy
if region=='loose':
    h2QCD       = f.Get("DataMinusMCBkg_SR_{0}".format(region))
    #h2QCD       = f.Get("MthvMh_particleNet_SR_{0}__nominal".format(region))
else:
    h2QCD       = f.Get("SR_loose_times_b_2x2_equals_SR_pass")

nBinsY      = h2Data.GetNbinsY()
years       = ["16","17","18"] 
processes   = ["ttbar","ZJets","WJets"]#,"DataMinusMCBkg"]
h2sMC       = []
for process in processes:
    hTemp   = f.Get(process+"_16APV_SR_{0}".format(region))
    print(process+"_16APV_SR_{0}".format(region))
    print(hTemp.Integral())
    for year in years:
        hTemp.Add(f.Get(process+"_{0}_SR_{1}".format(year,region)),1.0)
    hTemp.SetName("{}_run2".format(process))
    h2sMC.append(hTemp)


h2sMC.append(h2QCD)
processes.append("QCD")
print(h2QCD.Integral())
for i in range(1,nBinsY+1):
    hsMC = []
    for p,h2MC in enumerate(h2sMC):
        h2Temp = h2MC.ProjectionX("{0}_projection_x_{1}".format(processes[p],i),i,i)
        hsMC.append(h2Temp)
    hDataTemp = h2Data.ProjectionX("data_projection_x_{0}".format(i),i,i)

    oFile = "projx_{0}_{1}.png".format(i,region)
    plotVarStack(hDataTemp,hsMC,processes,oFile)

