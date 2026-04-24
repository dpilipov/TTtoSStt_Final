#include<ROOT/RVec.hxx>
#include <TRandom.h>
#include <string>
#include <iostream>
#include <stdio.h>
#include <vector>

/*
 * Class for applying ParticleNet scale factors on a jet-by-jet basis. 
 * For use in the T' -> t\phi analysis, with scale factors located at:
 * https://coli.web.cern.ch/coli/.cms/btv/boohft-calib/20220623_bb_TprimeB_useExpr_2016/4_fit/
 * 
 * Method: https://twiki.cern.ch/twiki/bin/viewauth/CMS/BTagSFMethods#2a_Jet_by_jet_updating_of_the_b
 * There are a few things for consideration:
 *  1) You have to run this for each working point, so that jets that were reassigned for the first WP are used for the second.
 *     To do so, create a new column using TIMBER analyzer's Define() method and pass the new column to the updateTag() method.
 *  2) The efficiencies do not always obey e_hp < e_mp < 1, so this has to be accounted for in the equality check functions.
*/

using namespace ROOT::VecOps;

class PNetSaaSFHandler {
  private:
    int _wp;     // 0,1,2,3 for cutBased
    float _effsP;    // efficiencies will be calculated via TIMBER then fed to constructor
    float _effsF;
    float _effsFF;
    std::string _year;    // 2016APV, 2016, 2017, 2018
    int _var;             // 0: nominal, 1: up, 2: down, passed to constructor
    TRandom _rand;        // used for random number generation
    int _newTags[3]  = {0,0,0};      // number of photons in each new category [failfail][fail][pass]
    int _origTags[3] = {0,0,0};      // original num photons in each category [failfail][fail][pass]
    
    // SF[var][etaCat][ptCat]
    // LOOSE, MEDIUM, TIGHT
    // ETA: [-Infinity, -2.0, -1.566, -1.444, -0.8, 0.0, 0.8 1.444, 1.566, 2.0, Infinity]
    // PT: 20.0, 35.0, 50.0, 80.0, 120.0, Infinity
    // HP (tight) cutBased = 3
    float SF2016APV_T[10][5]    = {{0.9832776,1.00561,1.0,1.039735,1.056701},{0.9712918,0.9835616,0.9867021,1.029216,1.042234},{1.035225,1.03876,1.006221,1.050406,1.048611},{0.9551282,0.9902642,0.9862826,1.019048,0.9850948},{0.9621711,0.9647391,0.955862,1.002793,0.9986014},{0.9916805,0.9871612, 0.979021,1.009845,1.02276},{0.996769,0.9971949,0.9848276,1.012414,1.041958},{1.036,1.015576,1.019017,1.069257,1.125714},{0.963141, 0.9821674,0.9933422,1.02571,1.009485},{0.9915683,1.01264,1.021592,1.029062,1.08931}};
    float SF2016_T[10][5]    = {{1.045918345451355,1.0369843244552612,1.0328317880630493,1.022757649421692,1.0284552574157715},{0.9825396537780762,0.9904502034187317,0.9920424222946167,1.0052909851074219,1.0647886991500854},{1.041338562965393,1.015455961227417,1.0125983953475952,1.0856643915176392,1.0301003456115723},{1.0032051801681519,0.9972106218338013,0.9917582273483276,1.0233516693115234,1.0361111164093018},{0.9817578792572021,0.9759206771850586,0.9681440591812134,1.0055943727493286,1.0070126056671143},{0.9884488582611084,0.9816384315490723,0.969613254070282,0.9986013770103455,1.0166898965835571},{1.0097087621688843,0.9985975027084351,0.9944751262664795,1.025174856185913,1.026063084602356},{0.9778671860694885,1.007836937904358,0.9842767119407654,0.975944995880127,1.0263158082962036},{0.9760383367538452,0.9904109835624695,0.9826666712760925,1.0405954122543335,1.0272108316421509},{1.0439189672470093,1.0339462757110596,1.028493881225586,1.061662197113037,1.058432936668396}};
    float SF2017_T[10][5]    = {{1.05428,1.049919,1.046338,1.041018,0.9879194},{0.9947461,1.0,1.0,1.038298,1.078035},{1.052209,1.03328,1.036508, 1.164557,1.111314},{1.018303,0.9971347,0.9915374,1.042253,1.025035},{0.9639794,0.9665698,0.9656652,1.015827, 0.9776536},{0.9863714,0.9797102,0.9702128,1.007072,1.012605},{1.008306,0.9971306,0.9873061,1.012346,1.013736},{1.044625,1.030351,1.071895, 1.053422,1.179191},{0.9912587,1.005874,1.018362,1.023256,1.060993},{1.085954,1.066129,1.053254, 1.073314,1.068085}};
    float SF2018_T[10][5]    = {{1.030369,1.017656,1.014793,1.07659,1.065598},{0.9775475,0.9898108,0.9831461,1.053901,1.042194},{1.067729,1.045669,1.060065,1.73913,1.199255},{0.9699499, 0.9656652,0.9340814,1.011158,1.024759},{0.9683656,0.9617084,0.9585122,0.9942939,1.017143},{0.9842382,0.9735294, 0.9657143,1.011511,1.012802},{0.9781145,0.9725036,0.9632249,1.018336,1.006878},{1.018256,1.041667,1.04918,1.136207,1.152057},{0.9809688,0.9898256,0.9957806,1.04298,1.052857},{1.067538,1.017771,1.004438,1.063218,1.070605}};
    // HP (medium) cutBased = a
    float SF2016APV_M[10][5]    = {{0.980303,1.005135,1.001236,1.032807,1.048349},{0.9647391,0.9779412,0.9856459,1.016607,1.044958},{1.021959,1.023161,1.002759,0.9709302,1.026397},{0.9835391,0.9865854,0.9806296,1.021951,0.9769138},{0.9592696,0.9666666,0.962149,1.004963,1.018821},{0.980226,0.9813433,0.972973,1.001244,1.006266},{0.9848276,0.990196,0.981774,1.002454,1.029888},{0.9156626,1.008208,0.9888734,1.016975,1.001667},{0.9534556,0.9779412,0.9868578,1.021765,1.010883},{0.983308,1.002558,1.014815,1.021924,1.067734}};
    float SF2016_M[10][5]    = {{1.0384024381637573,1.0325098037719727,1.0225000381469727,1.0295202732086182,1.0183823108673096},{0.9677419066429138,0.9853300452232361,0.9892473220825195,0.9869513511657715,1.028678297996521},{1.052901029586792,1.0067843198776245,1.0013889074325562,0.9956011772155762,1.0119940042495728},{1.0,0.9914634227752686,0.9890776872634888,1.0245699882507324,1.0260869264602661},{0.9548022747039795,0.9740419983863831,0.9670329689979553,1.0037267208099365,1.0162907838821411},{0.9831223487854004,0.9802225232124329,0.9694749712944031,0.9975185990333557,1.009987473487854},{0.9986187815666199,0.9926560521125793,0.9878345727920532,1.018587350845337,1.0270936489105225},{1.0260416269302368,1.0027472972869873,0.9707520604133606,1.0252366065979004,1.0160771608352661},{0.9731638431549072,0.9852941036224365,0.9844311475753784,1.0365407466888428,1.0182703733444214},{1.0428789854049683,1.0284605026245117,1.0124223232269287,1.0602705478668213,1.0550122261047363}};
    float SF2017_M[10][5]    = {{1.034358,1.032532,1.034256,1.03522,1.004843},{0.9773071,0.9884021,0.9950249,1.022195,1.054707},{1.030981,1.016552,1.026536,1.12381,1.052713},{0.9858956,0.9887781,0.9875931,1.048101,1.011111},{0.9622642,0.9671717,0.9637046,1.01906,0.9912391},{0.9783237,0.9772727,0.9700375,1.00375,1.013837},{0.9985875,0.9925094,0.9801735,1.017199,1.009876},{1.033044,1.018056,1.048571,1.077042,1.050157},{0.9818182,0.9935567,1.0,1.012121,1.032704},{1.067395,1.046742,1.038208, 1.060334,1.028049}};
    float SF2018_M[10][5]    = {{1.0,1.004231,1.005229, 1.064267,1.033505},{0.9596413,0.9795918,0.9789082,1.031056,1.038847},{0.9316239,1.037088, 1.048159,1.141975,1.154213},{0.9687943,0.9688279,0.9617756,1.008631,1.021014},{0.9704579,0.9669632, 0.9600499,1.001263,1.012658},{0.9808542,0.974587,0.9638404, 1.008872,1.008838},{0.978602,0.9761606,0.9677819,1.020025,1.007407},{0.9463668,1.026462,1.045845,1.149691,1.083994},{0.9640719, 0.9808673,0.9789604,1.02236,1.042767},{ 0.9962193,1.005682,0.9960682,1.035398,1.055556}};
    // MP (loose) cutBased = 1
    float SF2016APV_L[10][5]    = {{0.9623588,0.9878988,0.9892819,1.013844,0.998944},{0.9517327,0.9724366,0.9773463, 1.006459,1.021763},{1.009223,0.9977375,0.9807256,1.034803,0.9795427},{0.987074,0.9880435,0.9825708,1.020045,0.9743875},{0.9784173,0.9791667,0.9725877,1.008959,1.013575},{0.9759616,0.9835165,0.9747252,1.004479,1.005669},{0.9858823, 0.9836779,0.9825327,0.9966778,0.9966406},{1.029216,0.9966025,0.9898305,0.9669031,1.008475},{0.9467162,0.9724669,0.9773463,1.0,1.003293},{0.9610063,0.9889868,0.9957128,1.005336,1.028139}};
    float SF2016_L[10][5]    = {{1.0037453174591064,1.0,0.9967776536941528,1.006355881690979,0.9851064085960388},{0.9605911374092102,0.969264566898346,0.9806034564971924,0.9892473220825195,1.0344061851501465},{1.035433053970337,0.9954954981803894, 0.9909604787826538, 1.0199296474456787,0.9351415038108826,},{0.9953106641769409,0.9913138151168823,0.9825897812843323,1.0178173780441284,0.9988725781440735},{0.989195704460144,0.9824753403663635,0.9769737124443054,1.0066889524459839,0.994356632232666},{0.9856114983558655,0.9835526347160339,0.9769483804702759,1.0033669471740723,1.0158730745315552},{0.9952940940856934,0.990217387676239,0.984749436378479,1.0066889524459839,1.0135135650634766},{0.9880319237709045,0.9966063499450684,0.9897843599319458,1.0023781061172485,1.0236612558364868},{0.9628252983093262,0.9790979027748108,0.982758641242981,1.0129870176315308,0.9967355728149414},{0.99622642993927,0.9934065937995911,0.9967880249023438,1.022459864616394,1.0201913118362427}};
    float SF2017_L[10][5]    = {{1.008646,1.003505,1.011111,0.9779412,1.042857},{0.9536679,0.9740699,0.9846491,0.9891892,1.016667},{0.9735099,0.993205,0.9786757,1.027155,1.111409},{0.9988095,0.9912088,0.988938, 1.023836,1.044674},{0.9805353,0.9822813,0.9744728,1.010181,1.02439},{0.9842041,0.9833703,0.9821628,1.001129,1.003421},{0.9917061,0.9901316,0.9834254,1.019209,0.9541387},{0.9491979,1.003425,1.02781,1.026528,0.8594657},{0.9663648,0.9808127,0.9813597,0.9978284,1.061485},{1.033382,1.009368,0.9977876,1.032715,0.9874608}};
    float SF2018_L[10][5]    = {{0.9802431,0.9904762,0.9910514,1.013144,1.006417},{0.9494818,0.9695259,0.9702643,1.034444,1.03456},{1.05992,1.012528,1.021864,1.110294,1.072704},{0.9880669,0.9879254,0.9790979,1.008959,1.014723},{0.9853121,0.9833703,0.9767184,1.010204,1.004608},{0.9902201,0.9833887,0.9756368,0.9988649,0.9864712},{0.9904875,0.9835526,0.9823982,1.018038,1.005618},{0.9732977,1.013699,1.023041,1.088058,1.157104},{ 0.9533679,0.9740699,0.9790749,1.004357,1.025499},{0.9908116,0.9952039,0.987682,1.007642,1.075949}};

  public:
    PNetSaaSFHandler(float wp, float effsP, float effsF, float effsFF, std::string year, int var);  // default: wps={-0.995,-0.9}, effs={effl,effT}, var=0/1/2
    ~PNetSaaSFHandler();
    int getWPcat(RVec<int> taggerVal);                                    // determine WP category: 0: fail, 1: loose, 2: tight
    float getSF(RVec<float> pt, RVec<float> eta, RVec<int> taggerVal);                           // gets the proper SF based on jet's pt and score as well as internal variables _year, _var
    int updateTag(int photonCat, RVec<float> pt, RVec<float> eta, RVec<int> taggerVal);	      // determines the jet's new tagger category
    int createTag(RVec<int> taggerVal);				      // create new tagger category based on jet's original tagger value
    void printVals();						      // print the number of jets in each category

    // These functions should *NOT* be used, but are included for posterity
    // Essentially, instead of generating a vector of integers, just generate an integer
    // The reason is that we call these via TIMBER's Define() function, which takes in a C++ function or string and applies it to *EVERY* value in the column 
    // This means that we don't have to pass in the vectors themselves, just the column names
//    int updateTag(int photonCat, RVec<float> pt, RVec<float> eta, RVec<float> taggerVal);   // determines the jet's new tagger category 
//    int createTag(RVec<float> taggerVal);                                      // create vector of tagger categories based on jets' original tagger value.
};

void PNetSaaSFHandler::printVals() {
    // prints the number of original and new tagger values
    printf("Number of Original\n\tFailFail: %d\n\tFail: %d\n\tPass: %d\n\tTotal: %d\n", _origTags[0], _origTags[1], _origTags[2], _origTags[0]+_origTags[1]+_origTags[2]);
    printf("Number of New\n\tFailFail: %d\n\tFail: %d\n\tPass: %d\n\tTotal: %d\n", _newTags[0], _newTags[1], _newTags[2], _newTags[0]+_newTags[1]+_newTags[2]);
};

PNetSaaSFHandler::PNetSaaSFHandler(float wp, float effsP, float effsF, float effsFF, std::string year, int var) {
  _wp = wp;
  _effsP = effsP;
  _effsF = effsF;
  _effsFF = effsFF;
  _year = year;
  _var = var;
  // unique but repeatable random numbers. For repeated calls in the same event, random #s from Rndm() will be identical
  _rand = TRandom(1234);
};

PNetSaaSFHandler::~PNetSaaSFHandler() {
    // print out number of original and new tagger vals upon destruction
    printVals();
};

int PNetSaaSFHandler::getWPcat(RVec<int> taggerVal) {
  // determine the WP category we're in, 0:fail, 1:loose, 2:tight
  int wpCat;
  if ((taggerVal[0] >= _wp) && (taggerVal[1] >= _wp)) { // pass
    wpCat = 2;
  }
  else if ((taggerVal[0] < _wp) && (taggerVal[1] < _wp)) { // failfail
    wpCat = 0;
  }
  else {  // fail
    wpCat = 1;
  }
  return wpCat;
}

//int PNetSaaSFHandler::getWPcat1(int taggerVal1) {
  // determine the WP category we're in, 0:fail 1: pass
//  int wpCat1=0;
//  if (taggerVal1>= _wp) wpCat1 = 1;
//  return wpCat1;
//}

float PNetSaaSFHandler::getSF(RVec<float> pt, RVec<float> eta, RVec<int> taggerVal) {
  /* getthe scale factor from the jet's year, score, and pt */
  float SF;
  float SF1;
  float SF2;
  int ptCat1=0;
  int ptCat2=0;
  int etaCat1=0;
  int etaCat2=0;
  int wpCat = getWPcat(taggerVal);
  int wpCat1 = taggerVal[0];
  int wpCat2 = taggerVal[1];
// ETA: [-Infinity, -2.0, -1.566, -1.444, -0.8, 0.0, 0.8 1.444, 1.566, 2.0, Infinity]
  if (eta[0] >= 2.0) {
    etaCat1 = 9;
  } else if ((eta[0] >= 1.566) && (eta[0] < 2.0)) {
    etaCat1 = 8;
  } else if ((eta[0] >= 1.444) && (eta[0] < 1.566)) {
    etaCat1 = 7;
  } else if ((eta[0] >= 0.8) && (eta[0] < 1.444)) {
    etaCat1 = 6;
  } else if ((eta[0] >= 0.0) && (eta[0] < 0.8)) {
    etaCat1 = 5;
  } else if ((eta[0] >= -0.8) && (eta[0] < 0.0)) {
    etaCat1 = 4; 
  } else if ((eta[0] >= -1.444) && (eta[0] < -0.8)) {
    etaCat1 = 3; 
  } else if ((eta[0] >= -1.566) && (eta[0] < -1.444)) {
    etaCat1 = 2; 
  } else if ((eta[0] >= -2.0) && (eta[0] < -1.566)) {
    etaCat1 = 1;
  } else { 
    etaCat1 = 0;
  }
  if (eta[1] >= 2.0) {
    etaCat2 = 9;
  } else if ((eta[1] >= 1.566) && (eta[1] < 2.0)) {
    etaCat2 = 8;
  } else if ((eta[1] >= 1.444) && (eta[1] < 1.566)) {
    etaCat2 = 7;
  } else if ((eta[1] >= 0.8) && (eta[1] < 1.444)) {
    etaCat2 = 6;
  } else if ((eta[1] >= 0.0) && (eta[1] < 0.8)) {
    etaCat2 = 5;
  } else if ((eta[1] >= -0.8) && (eta[1] < 0.0)) {
    etaCat2 = 4;
  } else if ((eta[1] >= -1.444) && (eta[1] < -0.8)) {
    etaCat2 = 3;
  } else if ((eta[1] >= -1.566) && (eta[1] < -1.444)) {
    etaCat2 = 2;
  } else if ((eta[1] >= -2.0) && (eta[1] < -1.566)) {
    etaCat2 = 1;
  } else {
    etaCat2 = 0;
  }
//     // PT: 20.0, 35.0, 50.0, 80.0, 120.0, Infinity
  // get the pT category
  if (pt[0] >= 120.0) {
    ptCat1 = 4;
  } else if ((pt[0] >= 80.0) && (pt[0] < 120.0)) {
    ptCat1 = 3;
  } else if ((pt[0] >= 50.0) && (pt[0] < 80.0)) {
    ptCat1 = 2;
  } else if ((pt[0] >= 35.0) && (pt[0] < 50.0)) {
    ptCat1 = 1;
  } else {
    ptCat1 = 0;
  }
  if (pt[1] >= 120.0) {
    ptCat2 = 4; 
  } else if ((pt[1] >= 80.0) && (pt[1] < 120.0)) {
    ptCat2 = 3; 
  } else if ((pt[1] >= 50.0) && (pt[1] < 80.0)) {
    ptCat2 = 2; 
  } else if ((pt[1] >= 35.0) && (pt[1] < 50.0)) {
    ptCat2 = 1;
  } else { 
    ptCat2 = 0;
  }

  // get the SF
  switch (wpCat1) {
    case 0:   // if photon is originally in fail, pass SF of 1.0 (no change)
      SF1 = 1.0;
    case 1:   // photon is in MP (loose)
      if (_year=="2016APV") { SF1 = SF2016APV_L[etaCat1][ptCat1]; }
      else if (_year=="2016") { SF1 = SF2016_L[etaCat1][ptCat1]; }
      else if (_year=="2017") { SF1 = SF2017_L[etaCat1][ptCat1]; }
      else { SF1 = SF2018_L[etaCat1][ptCat1]; }
    case 2:   // photon is in HP (medium)
      if (_year=="2016APV") { SF1 = SF2016APV_M[etaCat1][ptCat1]; }
      else if (_year=="2016") { SF1 = SF2016_M[etaCat1][ptCat1]; }
      else if (_year=="2017") { SF1 = SF2017_M[etaCat1][ptCat1]; }
      else { SF1 = SF2018_M[etaCat1][ptCat1]; }
    case 3:   // photon is in HP (tight)
      if (_year=="2016APV") { SF1 = SF2016APV_T[etaCat1][ptCat1]; }
      else if (_year=="2016") { SF1 = SF2016_T[etaCat1][ptCat1]; }
      else if (_year=="2017") { SF1 = SF2017_T[etaCat1][ptCat1]; }
      else { SF1 = SF2018_T[etaCat1][ptCat1]; }
  }
  switch (wpCat2) {
    case 0:   // if photon is originally in fail, pass SF of 1.0 (no change)
      SF2 = 1.0;
    case 1:   // photon is in MP (loose)
      if (_year=="2016APV") { SF2 = SF2016APV_L[etaCat2][ptCat2]; }
      else if (_year=="2016") { SF2 = SF2016_L[etaCat2][ptCat2]; }
      else if (_year=="2017") { SF2 = SF2017_L[etaCat2][ptCat2]; }
      else { SF2 = SF2018_L[etaCat2][ptCat2]; }
    case 2:   // photon is in HP (medium)
      if (_year=="2016APV") { SF2 = SF2016APV_M[etaCat2][ptCat2]; }
      else if (_year=="2016") { SF2 = SF2016_M[etaCat2][ptCat2]; }
      else if (_year=="2017") { SF2 = SF2017_M[etaCat2][ptCat2]; }
      else { SF2 = SF2018_M[etaCat2][ptCat2]; }
    case 3:   // photon is in HP (tight)
      if (_year=="2016APV") { SF2 = SF2016APV_T[etaCat2][ptCat2]; }
      else if (_year=="2016") { SF2 = SF2016_T[etaCat2][ptCat2]; }
      else if (_year=="2017") { SF2 = SF2017_T[etaCat2][ptCat2]; }
      else { SF2 = SF2018_T[etaCat2][ptCat2]; }
  }
  SF = SF1 * SF2;
std::cout << "Calculating SF " << SF << std::endl;
  return SF;
};


int PNetSaaSFHandler::createTag(RVec<int> taggerVal) {
    /* Creates tagger categories for phi candidate jets
     * this MUST be called in TIMBER before running the rest of the script, as it places all jets into their respective categories for later use in updateTag()
     * This function is meant to be called after selecting the top and higgs in CR and SR (see THselection.py - getEfficiencies)
    */
    if ((taggerVal[0] >= _wp) && (taggerVal[1] >= _wp)) {
	_origTags[2] = _origTags[2] + 1;
std::cout << "PASS wp " << _origTags[2] << " " << _wp << std::endl;
        printVals();
	return 2;
    }
    else if ((taggerVal[0] < _wp) && (taggerVal[1] < _wp)){
        _origTags[0] = _origTags[0] + 1;
std::cout << "FAILFAIL " << _origTags[0]  << " " << _wp<< std::endl;
        printVals();
        return 0;
    }
    else {
	_origTags[1] = _origTags[1] + 1;
std::cout << "FAIL " << _origTags[1] << " " << _wp << std::endl;
        printVals();
	return 1;
    }
};

int PNetSaaSFHandler::updateTag(int photonCat, RVec<float> pt, RVec<float> eta, RVec<int> taggerVal) {
    /* updates the tagger category for phi jets
     * https://twiki.cern.ch/twiki/bin/view/CMS/BTagSFMethods#2a_Jet_by_jet_updating_of_the_b
     * Params:
     * 	 photonCat    = original photon category (0: failfail, 1: fail, 2: pass)
     * 	 pt        = jet pt
     * 	 taggerVal = particleNet tagger value
    */ 
    float SF = getSF(pt, eta, taggerVal);
    float SF_P = SF;
    float SF_F = SF;
    float SF_FF = SF;
    float eff_P = _effsP;
    float eff_FF = _effsFF;
    float eff_F = _effsF;
    double rn = _rand.Rndm();
    int newCat = photonCat;	// grab the original tag category, will be updated
    // begin logica
    if ((SF_F < 1) && (SF_P < 1)) {
	if ( (newCat==2) && (rn < (1.-SF_P)) ) newCat=0;	// tight (2) -> untag (0)
	if ( (newCat==1) && (rn < (1.-SF_F)) ) newCat=0;	// loose (1) -> untag (0)
    }
    if ((SF_F > 1) && (SF_P > 1)) {
	float fF, fP;
	if (newCat==0) {
	    float num = eff_P*(SF_P-1.);
	    float den = 1.-(eff_F+eff_P);
	    fP = num/den;
	    if (rn < fP) newCat=2;	// untag (0) -> tight (2)
	    else {
		rn = _rand.Rndm();
		num = eff_F*(SF_F-1.);
		den = (1.-eff_F-eff_P)*(1.-fP);
		fF = num/den;
		if (rn < fF) newCat=1; 	// loose (1) -> tight (2)
	    }
	}
    }
    if ((SF_F < 1) && (SF_P > 1)) {
	if (newCat==0) {
	    float num = eff_P*(SF_P-1.);
	    float den = 1.-(eff_F+eff_P);
	    float f = num/den;
	    if (rn < f) newCat=2;	    // untag (0) -> tight (2)
	}
	if (newCat==1) {
	    if (rn < (1.-SF_F)) newCat=0;   // loose (1) -> untag (0)
	}
    }
    if ((SF_F > 1) && (SF_P < 1)) { 
	if ((newCat==2) && (rn < (1.-SF_P))) newCat=0;	// tight (2) -> untag (0)
	if (newCat==0) {
	    float num = eff_F*(SF_F-1.);
	    float den = 1.-(eff_F+eff_P);
	    float f = num/den;
	    if (rn < f) newCat=1;	// untag (0) -> loose (1)
	}
    }
    // update the new tag category array
    _newTags[newCat]++;
    // return the new tagger category value
    return newCat;
};

/* ----------------------------------------------------------------------------------
 *
 *    Do not use these functions, use the above versions 
 *
 * ----------------------------------------------------------------------------------
 */
