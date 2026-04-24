# TTtoSStt_Final
We are considering pair produced vector like tops where each decays to a top quark and a new scalar, with consequent diphoton decay of one of the two scalars while second is treated inclusively, $TT\to tt\phi\phi, \phi\to\gamma\gamma$.  This branch covers the necessary analysis steps, from generating snapshots based on initial selection to obtaining the final selection / regions.

# Overall Analysis Strategy
We use JHU's TIMBER, which takes advantage of RDataFrame to process data fast, and to implement other CMS-related functionality, in order to  obtain the final selection shapes across the various regions of a 2-d mass space.  The consequent steps of fitting a model, a variation on the ABCD method, are covered in a separate branch, and take advantage of 2DAlphabet, again edited for the specific needs of this analysis.

The code here originates from Amitav Mitra's code for single production $T\to t\phi$ code, with specific edits for pair production and final state.  The edits are covered both in the README documentation here. as well as in the actual code.

# Set up TIMBER/analysis area
To set up the environment, including TIMBER and the analysis area we follow the same steps as for Amitav's set up for TopHBoostedAllHad which was edited and supplemented for pair production (take a look at https://github.com/ammitra/TIMBER and https://github.com/ammitra/TopHBoostedAllHad).  However, to make sure you have the required TIMBER edits and the required code for pair production you must clone TIMBER and TTtoSStt_Final from my area:

```
cmssw-el7 -p --bind `readlink $HOME` --bind `readlink -f ${HOME}/nobackup/` --bind /uscms_data --bind /cvmfs
export SCRAM_ARCH=slc7_amd64_gcc820 
mkdir yourAnalysisDirName
cd yourAnalysisDirName/
cmsrel CMSSW_11_1_4
cd CMSSW_11_1_4/src
cmsenv

git clone https://github.com/dpilipov/TIMBER.git
python -m virtualenv timber-env
source timber-env/bin/activate
cd TIMBER
source setup.sh
cd ..
git clone https://github.com/dpilipov/TTtoSStt_Final.git
cd TTtoSStt_Final
```
IMPORTANT NOTE!  HEM_drop.cc (see TIMBER/Framework/include for HEM_drop.h and TIMBER/Framework/src for HEM_drop.cc) is NOT used for the pair production analysis!  Instead, HEM_dropData and HEM_dropMC code is now included in TTmodules.cc, and is used for correcting for HEM in 2018.  During TIMBER setup you will get an error regarding HEM_drop.cc which you can ignore.

# Work in a container
Whenever you work in this area you need to use the container and set up the environment.  For example, 
```
cmssw-el7 -p --bind `readlink $HOME` --bind `readlink -f ${HOME}/nobackup/` --bind /uscms_data --bind /cvmfs
cd /uscms/home/dpilipov/nobackup/TIMBER/CMSSW_11_1_4/src
cmsenv
source timber-env/bin/activate
cd TIMBER
source setup.sh
cd ..
cd TTtoSStt_Final
voms-proxy-init --rfc --voms cms -valid 192:00                          
```
(Note, actually my work area is in /uscms/home/dpilipov/nobackup/TIMBER/CMSSW_11_1_4/src/TopHBoostedAllHad, hence, technically I would cd to TopHBoostedAllHad instead of TTtoSStt_Final above.)

**NOTE:** All the steps follow the same process as what is shown for https://github.com/ammitra/TopHBoostedAllHad in README.  Please use this as a reference.  The variations across the steps are explained below.

## 0. Generic TTClassdR
The preselection is specific to the pair production and final state and thus differs from https://github.com/ammitra/TopHBoostedAllHad in some details.  Most of the edits to accomodate this difference are denoted as 'DP edit' in the code.

The TTClassdR* modules hold all of the basic, generic logic to perform the selection.
Any additions, modifications, splittings, or saving of the selection should be added here.
Subsequent steps should always interface with this so that if something is changed, it's propagated
to the full pipeline.

**NOTE:** For snapshot generation only TTClassdR is necessary.  For SR/CR and VR-SR/CR selection it is necessary to use the corresponding version of TTClassdR (these include TTClassdR18, TTClassdRVR, TTClassdR18VR, and TTClassdRData): for MC selection in SR/CR use TTClassdR for 2016-2017 and for 2018 use TTClassdR18, for VR use the VR versions, and for data use the Data version.

All the TTClassdR* take advantage of functions provided by TTmodules.cc.

## 1. Grab latest raw NanoAOD file locations
--------------
Same as in https://github.com/ammitra/TopHBoostedAllHad:

The list of file locations in `raw_nano/` can be easily populated with
```
python raw_nano/get_all_lpc.py
```
If one wishes to add to the sets considered, simply modify the dictionary
in `raw_nano/get_all_lpc.py` with the name of the set and the DAS path.

## 2. Create pileup distributions for pileup weights
------------------
Same as in https://github.com/ammitra/TopHBoostedAllHad:

This is handled by THpileup.py.
```
python THpileup.py -s <setname> -y <year>
```
This script simply draws into a histogram the
distribution of the number of primary vertices in the set. This is relatively quick
but not quick enough to include in every snapshot or to run interactively.
To run with condor, use...
```
python CondorHelper.py -r condor/run_pileup.sh -a condor/pileup_args.txt -i "THpileup.py raw_nano/"
```
To collect the outputs to one local file called `THpileup.root`, use `scripts/get_pileup_file.sh`.

**NOTE:** Please follow instructions in https://github.com/ammitra/TopHBoostedAllHad to setup condor correctly.

## 3. Perform snapshot on `raw_nano/` files
-------------
Snapshot generation is specific to the pair production and final state and thus differs from https://github.com/ammitra/TopHBoostedAllHad in some details.  Most of the edits to accomodate this difference are denoted as 'DP edit' in the code.

The command to perform one snapshot using `TTsnapshot.py` is 
```
python TTsnapshot.py -s <setname> -y <16,16APV, 17,18> -j <ijob> -n <njobs>
```
where `<ijob>` and `<njobs>` determine the job number and the number of jobs to split into and default
to 1 and 1, respectively.

### 4. Condor
-----------
Please follow the instructions from https://github.com/ammitra/TopHBoostedAllHad for 
* Preparing an archived environment
* setting up Arguments file
* running the Bash script on condor node
* Submission
* collection
* checking job success
  
Take a look at condor/run_snapshot_TT.sh and condor/snapshot_args*.txt in this repository.

## 5. Making the trigger efficiencies
----------------------------
The trigger efficiency is measured in the SingleMuon dataset separately across periods using the `HLT_Mu50` trigger as a reference. The problem of missing triggers (HLT_AK8PFHT750_TrimMass50, HLT_AK8PFHT800_TrimMass50, HLT_AK8PFJet400_TrimMass30) in 2017 Data for run 2017B discussed in https://github.com/ammitra/TopHBoostedAllHad is extremely important in obtaining reasonable trigger efficiency in pair production analysis.   Please follow the instructions in https://github.com/ammitra/TopHBoostedAllHad to obtain the appropriate 2017 efficiencies.  

You should in the end have two 2017 trigger root files - one excluding the problem data but including all the triggers and one just for the problem data but excluding the problem triggers.  To see how these are applied, do a search for 'Applying 2017B trigger efficiency' in TTselectionNewCRmvaIDdR.py. 

The triggers used in this analysis are as follows:

| Dataset  | Triggers |
| -------- | -------- |
| 2016  | 'HLT_AK8PFJet60', 'HLT_AK8PFJet80','HLT_PFHT800','HLT_PFHT900','HLT_AK8DiPFJet280_200_TrimMass30_BTagCSV_p20','HLT_Diphoton30EB_18EB_R9Id_OR_IsoCaloId_AND_HE_R9Id_DoublePixelVeto_Mass55','HLT_Diphoton30PV_18PV_R9Id_AND_IsoCaloId_AND_HE_R9Id_DoublePixelVeto_Mass55','HLT_Diphoton30_18_R9Id_OR_IsoCaloId_AND_HE_R9Id_DoublePixelSeedMatch_Mass70','HLT_Diphoton30_18_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass90','HLT_Diphoton30_18_Solid_R9Id_AND_IsoCaloId_AND_HE_R9Id_Mass55','HLT_DoublePhoton60','HLT_DoublePhoton85'  |
| 2016APV  | 'HLT_AK8PFJet60', 'HLT_AK8PFJet80','HLT_PFHT800','HLT_PFHT900','HLT_AK8DiPFJet280_200_TrimMass30_BTagCSV_p20','HLT_Diphoton30EB_18EB_R9Id_OR_IsoCaloId_AND_HE_R9Id_DoublePixelVeto_Mass55','HLT_Diphoton30PV_18PV_R9Id_AND_IsoCaloId_AND_HE_R9Id_DoublePixelVeto_Mass55','HLT_Diphoton30_18_R9Id_OR_IsoCaloId_AND_HE_R9Id_DoublePixelSeedMatch_Mass70','HLT_Diphoton30_18_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass90','HLT_Diphoton30_18_Solid_R9Id_AND_IsoCaloId_AND_HE_R9Id_Mass55','HLT_DoublePhoton60','HLT_DoublePhoton85'  |
| 2017  | 'HLT_AK8PFJet60', 'HLT_AK8PFJet80',"HLT_PFHT1050","HLT_AK8PFJet500","HLT_AK8PFHT750_TrimMass50","HLT_AK8PFHT800_TrimMass50","HLT_AK8PFJet400_TrimMass30",'HLT_Diphoton30EB_18EB_R9Id_OR_IsoCaloId_AND_HE_R9Id_DoublePixelVeto_Mass55','HLT_PFHT500_PFMET100_PFMHT100_IDTight','HLT_Diphoton30PV_18PV_R9Id_AND_IsoCaloId_AND_HE_R9Id_DoublePixelVeto_Mass55','HLT_Diphoton30_18_R9Id_OR_IsoCaloId_AND_HE_R9Id_DoublePixelSeedMatch_Mass70','HLT_Diphoton30_18_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass90','HLT_Diphoton30_18_Solid_R9Id_AND_IsoCaloId_AND_HE_R9Id_Mass55','HLT_DoublePhoton60','HLT_DoublePhoton85' |
| 2018  | 'HLT_AK8PFJet60', 'HLT_AK8PFJet80',"HLT_PFHT1050","HLT_AK8PFHT800_TrimMass50","HLT_AK8PFJet500","HLT_AK8PFJet450","HLT_AK8PFJet320","HLT_AK8PFJet420_TrimMass30","HLT_AK8PFHT750_TrimMass50","HLT_AK8PFJet400_TrimMass30","HLT_PFHT500_PFMET100_PFMHT100_IDTight","HLT_DoublePhoton70","HLT_DoublePhoton85" |

To calculate the trigger efficiencies with Clopper-Pearson errors, one can simply run
```
python TTtrigger2D_18.py --HT900
```
for the case of 2018, where an HT cut of 900GeV is also applied.  Omitting --HT900 would assume a zero HT cut.  

From here on the process for trigger efficiency is the same as in https://github.com/ammitra/TopHBoostedAllHad:
The script outputs one ROOT file per year. Inside are the 2D histograms (which do NOT store the errors) and the 
TEfficiency loaded by TIMBER later on (which do have the errors). Plots are also made in the `plots/` directory.

Five variations are created per-year. 
1. Dijet-only selection ("Pretag")
2. DeepAK8 top tag
3. DeepAK8 top anti-tag (for validation region)
4. ParticleNet top tag
5. ParticleNet top anti-tag (for validation region)

We select the pretag version since it is the smoothest and all variations are in agreement with one another.
</details>

## 7. Running Selection
To run the selection you will need the pileup (THpileup.root) and the trigger root files as discussed above.  You can run a selection on a single snapshot, for example 
'''
python TTselectionNewCRmvaIDdR.py -s StoAA1800x100 -y 16 --HT 900
'''
where TTselectionNewCRmvaIDdR.py uses TTClassdR.py.  For 2016, 2016APV, and 2017 where you want the selection in the SR and the CR (post unblinding) you can use TTselectionNewCRmvaIDdR.py for all MC samples.  For 2018 you should use TTselectionNewCRmvaIDdR18.py which also uses TTClassdR18.py.  But for working on a validation regions, VR-SR/CR, you can use TTselectionNewCRmvaIDdRVR.py and TTselectionNewCRmvaIDdR18.py.

To obtain the various files you will need for nuisance calculations, you would similarly run
'''
python TTselectionNewCRmvaIDdR.py -s StoAA1800x100 -y 16 --HT 900 -v PNetTop_up
python TTselectionNewCRmvaIDdR.py -s StoAA1800x100 -y 16 --HT 900 -v PNetTop_down
python TTselectionNewCRmvaIDdR.py -s StoAA1800x100 -y 16 --HT 900 -v JES_up
python TTselectionNewCRmvaIDdR.py -s StoAA1800x100 -y 16 --HT 900 -v JES_down
python TTselectionNewCRmvaIDdR.py -s StoAA1800x100 -y 16 --HT 900 -v JER_up
python TTselectionNewCRmvaIDdR.py -s StoAA1800x100 -y 16 --HT 900 -v JER_down
python TTselectionNewCRmvaIDdR.py -s StoAA1800x100 -y 16 --HT 900 -v JMS_up
python TTselectionNewCRmvaIDdR.py -s StoAA1800x100 -y 16 --HT 900 -v JMS_down
python TTselectionNewCRmvaIDdR.py -s StoAA1800x100 -y 16 --HT 900 -v JMR_up
python TTselectionNewCRmvaIDdR.py -s StoAA1800x100 -y 16 --HT 900 -v JMR_down
'''

Clearly this is quite time consuming to do locally, and it's best to run on condor. However prior to running on condor it is a very good idea to first do a test run localy for a small MC signal sample to ensure you have everything properly in place!

Take a look at the required condor steps in https://github.com/ammitra/TopHBoostedAllHad.  Follow the general instructions there, but the call you want to make for pair production is the following:
'''
python CondorHelper.py -r condor/run_selectiondRVR_TT18.sh -a condor/selection_args_MC_18.txt -i "TTClassdRVR18.py TTselectionNewCRmvaIDdRVR18.py helpers.py"
'''
You can take a look at the condor directory in this repo to see what condor/run_selectiondRVR_TT18.sh does and what you must pass to it in condor/selection_args_MC_18.txt, for example.  This should give you a good idea as to what you need to do.

## 8. Gathering Cutflow Information
To get information on yields after all important cuts, run `python TTcutflowSummarydR.py`. 

In addition to the cutflow variables for jets there are also cutflow variables for photons.  You can cator your cut choices based on what your final state entails.

## Kinematic distributions
Same as in https://github.com/ammitra/TopHBoostedAllHad:

After having run snapshots, run `python dijet_nano/get_all.py` to populate the directory with the snapshot locations. Then, run `python THdistributions.py -y <year>` to generate kinematic distribution histograms in the `rootfiles/` directory. To plot, just run `python kinDistPlotter.py -y <year>`. **NOTE:** the plotting script only works with python3 since it uses fancy matplotlib things instead of ROOT. 


# DEPRECATED 

##  Final selections and studies
Once you are sure the snapshots are finished and available and their locations have been accessed,
the basic selection can be performed with `python TTselectiondR*.py -s <setname> -y <year>`. This script
will take in the corresponding txt file in `dijet_nano/*.txt` and perform the basic signal region and "fail" region
selections and makes 2D histograms for 2D Alphabet. However, any other selection or study 
can follow a similar format to perform more complicated manipulation of the snapshots.

# Data and background
2016
| Setname | DAS location |
|---------|--------------|
| DataB1 | /JetHT/Run2016B-ver1_HIPM_UL2016_MiniAODv1_NanoAODv2-v1/NANOAOD |
| DataB2 | /JetHT/Run2016B-ver2_HIPM_UL2016_MiniAODv1_NanoAODv2-v1/NANOAOD |
| QCDHT700 | /QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL16NanoAODv2-106X_mcRun2_asymptotic_v15-v1/NANOAODSIM |
| QCDHT1000 | /QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL16NanoAODv2-106X_mcRun2_asymptotic_v15-v1/NANOAODSIM |
| QCDHT1500 | /QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL16NanoAODv2-106X_mcRun2_asymptotic_v15-v1/NANOAODSIM |
| QCDHT2000 | /QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL16NanoAODv2-106X_mcRun2_asymptotic_v15-v1/NANOAODSIM |
| DataH | /JetHT/Run2016H-UL2016_MiniAODv1_NanoAODv2-v1/NANOAOD |
| DataE | /JetHT/Run2016E-UL2016_MiniAODv1_NanoAODv2-v1/NANOAOD |
| DataD | /JetHT/Run2016D-UL2016_MiniAODv1_NanoAODv2-v1/NANOAOD |
| DataG | /JetHT/Run2016G-UL2016_MiniAODv1_NanoAODv2-v1/NANOAOD |
| DataF | /JetHT/Run2016F-UL2016_MiniAODv1_NanoAODv2-v2/NANOAOD |
| DataC | /JetHT/Run2016C-UL2016_MiniAODv1_NanoAODv2-v1/NANOAOD |
| ttbar | /TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIISummer19UL16NanoAODv2-106X_mcRun2_asymptotic_v15-v1/NANOAODSIM |
| ttbar-semilep | /TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer19UL16NanoAODv2-106X_mcRun2_asymptotic_v15-v1/NANOAODSIM |

2017
| Setname | DAS location |
|---------|--------------|
| QCDHT700 | /QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM |
| QCDHT1000 | /QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM |
| QCDHT1500 | /QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM |
| QCDHT2000 | /QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM |
| DataE | /JetHT/Run2017E-UL2017_MiniAODv1_NanoAODv2-v1/NANOAOD |
| DataD | /JetHT/Run2017D-UL2017_MiniAODv1_NanoAODv2-v1/NANOAOD |
| DataF | /JetHT/Run2017F-UL2017_MiniAODv1_NanoAODv2-v2/NANOAOD |
| DataC | /JetHT/Run2017C-UL2017_MiniAODv1_NanoAODv2-v1/NANOAOD |
| DataB | /JetHT/Run2017B-UL2017_MiniAODv1_NanoAODv2-v1/NANOAOD |
| ttbar | /TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIISummer19UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM |
| ttbar-semilep | /TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer19UL17NanoAODv2-106X_mc2017_realistic_v8-v1/NANOAODSIM |

2018
| Setname | DAS location |
|---------|--------------|
| QCDHT700 | /QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM |
| QCDHT1000 | /QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM |
| QCDHT1500 | /QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM |
| QCDHT2000 | /QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM |
| DataD | /JetHT/Run2018D-UL2018_MiniAODv1_NanoAODv2-v1/NANOAOD |
| DataA | /JetHT/Run2018A-UL2018_MiniAODv1_NanoAODv2-v1/NANOAOD |
| DataC | /JetHT/Run2018C-UL2018_MiniAODv1_NanoAODv2-v1/NANOAOD |
| DataB | /JetHT/Run2018B-UL2018_MiniAODv1_NanoAODv2-v1/NANOAOD |
| ttbar | /TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM |
| ttbar-semilep | /TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM |

# Signal samples
We originally generated only local samples to play with and better understand how the model works.  Ultimately, we requested centrally produced samples.   These are readily available (as NanoAODs) for you to take a look.  For example, for M_T = 1000GeV and M_S = 100GeV you can look at the available samples on DAS:
'''
dataset=/TprimeTprimeToSSTTTo2ASTT_MTprime-1000_MS-100_TuneCP5_13TeV-madgraph-pythia8/*/*
'''
On DAS you will find samples for M_T = 800 to 1500GeV and M_S=50 to 350GeV.  We expanded our M_T mass range during ARC review to include additional M_T points, up to 1800GeV.  These are locally generated, and you can find them in /store/user/dpilipov/TTtoSStt/* organized by periods.

# Selections

## Signal Region
| Variable      | Selection                 |
|---------------|---------------------------|
| p_T           | Both jets, > 350 GeV      |
| abs(\eta)     | Both jets, < 2.4          |
| \Delta \phi   | > M_PI/2                  |
| 2 Tops tag    | TvsQCD WP0.5%             |
| 2Photon tag   | mvaID WP80                |

## Control region
| Variable      | Selection                 |
|---------------|---------------------------|
| p_T           | Both jets, > 350 GeV      |
| abs(\eta)     | Both jets, < 2.4          |
| \Delta \phi   | > M_PI/2                  |
| 2 Tops tag    | TvsQCD WP0.5%             |
| 2Photon tag   | FAIL mvaID WP80           |


