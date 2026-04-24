import ROOT, time
ROOT.gROOT.SetBatch(True)
# ROOT.ROOT.EnableImplicitMT(2)
from TIMBER.Tools.Common import CompileCpp
from argparse import ArgumentParser
from TTClass import TTClass
from array import array

parser = ArgumentParser()
parser.add_argument('-s', type=str, dest='setname',
                    action='store', required=True,
                    help='Setname to process.')
parser.add_argument('-y', type=str, dest='era',
                    action='store', required=True,
                    help='Year of set (16, 17, 18).')
parser.add_argument('-j', type=int, dest='ijob',
                    action='store', default=1,
                    help='Job number')
parser.add_argument('-n', type=int, dest='njobs',
                    action='store', default=1,
                    help='Number of jobs')
args = parser.parse_args()

start = time.time()

CompileCpp('TTmodules.cc')
print('Pre selection')
selection = TTClass('raw_nano/%s_%s.txt'%(args.setname,args.era),args.era,args.ijob,args.njobs)
print('Post selection pre analysis1')
selection.ApplyKinematicsSnap()
print('After Kinematics Pre Lepton')
selection.LeptonVeto()
print('After Lepton Pre analysis')
selection.analysis1()
print('After analysis1 Pre Out')
out = selection.ApplyStandardCorrections(snapshot=True)
selection.Snapshot(out)
print ('%s sec'%(time.time()-start))
