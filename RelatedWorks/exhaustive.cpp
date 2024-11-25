#include <iostream>
#include <math.h>
#include <map>
#include <list>
#include <sstream>
#include <cstdlib>

using namespace std;

typedef list<int> Sol_t;
typedef Sol_t * Sol;
typedef Sol_t::iterator SolIter;

typedef list<list<int>*> SolSet_t;
typedef SolSet_t * SolSet;
typedef SolSet_t::iterator SolSetIter;

typedef map<int, list<list<int>*>*> SizeSolSet_t;
typedef SizeSolSet_t * SizeSolSet;
typedef SizeSolSet_t::iterator SizeSolSetIter;


#define INDEX_WIDTH 7
#define LEVEL_WIDTH 5
#define LOWERBOUND_WIDTH 7
#define FANOUT_WIDTH 7

int indexParameter = int(pow(2.0, INDEX_WIDTH)) - 1;
int levelParameter = int(pow(2.0, LEVEL_WIDTH)) - 1;
int fanoutParameter = int(pow(2.0, FANOUT_WIDTH)) - 1;
int lowerBoundParameter = int(pow(2.0, LOWERBOUND_WIDTH)) - 1;

// Bit-slicing APIs
// An integer contains 4 bytes, each byte capturing different information as mentioned in the paper
int getIndex(int val) {
        return val & indexParameter;
}

int getLevel(int val) {
        return (val & (levelParameter<<INDEX_WIDTH))>>INDEX_WIDTH;
}

int getFanout(int val) {
        return (val & (fanoutParameter<<(INDEX_WIDTH + LEVEL_WIDTH)))>>(INDEX_WIDTH + LEVEL_WIDTH);
}

int getLowerBound(int val) {
        return (val & (lowerBoundParameter<<(INDEX_WIDTH+LEVEL_WIDTH+FANOUT_WIDTH)))>>(INDEX_WIDTH + LEVEL_WIDTH + FANOUT_WIDTH);
}


void setIndex(int& val, int index) {
        val = (val & ~indexParameter) | index;
}

void setLevel(int& val, int level) {
        val = (val & ~(levelParameter<<INDEX_WIDTH)) | (level << INDEX_WIDTH);
}

void setFanout(int& val, int fo) {
        val = (val & ~(fanoutParameter<<(INDEX_WIDTH + LEVEL_WIDTH))) | (fo <<(INDEX_WIDTH + LEVEL_WIDTH));
}

void setLowerBound(int& val, int lb) {
        val = (val & ~(lowerBoundParameter<<(INDEX_WIDTH + LEVEL_WIDTH+ FANOUT_WIDTH))) | (lb << (INDEX_WIDTH + LEVEL_WIDTH + FANOUT_WIDTH));
}

//int bitArrivalTime [] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

int bitRequiredTime [] = {0, 1, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7}; 

//int bitArrivalTime [] = {0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 6, 6, 6 ,6 ,6 ,6, 5, 5, 4, 4, 3, 3, 2, 2, 1, 1, 0, 0};  FIG 11 
//int bitRequiredTime [] = { 10, 10, 10, 10, 10, 10, 10, 10,10, 10, 10, 10,10, 10, 10, 10,10, 10, 10, 10,10, 10, 10, 10,10, 10, 10, 10,10, 10, 10, 10}; // 63 with gDelta = 3

//int bitArrivalTime [] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 12, 12, 12, 12, 12, 12, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0}; FIG10
//int bitRequiredTime [] = {16, 16, 16, 16,16, 16, 16, 16,16, 16, 16, 16,16, 16, 16, 16,16, 16, 16, 16,16, 16, 16, 16,16, 16, 16, 16,16, 16, 16, 16}; // 56 with gDelta = 2

//int bitArrivalTime [] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}; 
//int bitRequiredTime [] = {8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5};  // FIG7 57 with gDelta = 1 and flag on

//int bitArrivalTime [] = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8};  // 49 gDelta from 3 to 2 at 16
//int bitRequiredTime [] = { 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13}; // Fig 9a 53 with gDelta = 2


//int bitArrivalTime [] = { 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8 , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, };  
//int bitRequiredTime [] = { 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13}; // Fig 9b 59 with gDelta = 2

//int bitArrivalTime [] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}; 
//int bitRequiredTime [] = { 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5};  // FIG9c 73 with gDelta = 2 and flag on


//int bitArrivalTime [] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}; 
//int bitRequiredTime [] = { 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12};  // FIG9d 50 with gDelta = 2 to 1 at 16


//int bitArrivalTime [] = {0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
//int bitRequiredTime [] = {6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6};  // 8.a (78 with gDelta = 2)


//int bitArrivalTime [] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0};
//int bitRequiredTime [] = {6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6};  // 8.a (78 with gDelta = 2)

// Circuit A
//int bitArrivalTime [] = {1, 2, 1, 3, 4, 2, 1, 3 ,1, 2, 1, 0, 3, 2, 1, 4, 2, 2, 1, 0, 1, 3, 4, 1, 2, 2, 1, 3, 1, 2, 2, 3};
//int bitRequiredTime [] = { 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9}; // 55

//int bitArrivalTime [] = {1, 3, 4, 2, 2, 1, 2, 1, 2, 3, 4, 4, 2, 3, 1, 0, 0, 2, 3, 1, 2, 3, 2, 1, 2, 4, 1, 2, 1, 2, 1, 3};
//int bitRequiredTime [] = { 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9}; // 62

// Circuit C
//int bitArrivalTime [] = {2, 1, 3, 2, 1, 0, 4, 3, 2, 1, 3, 2, 2, 1, 4, 2, 1, 2, 3, 1, 4, 0, 2, 1, 2, 1, 3, 2, 1, 3, 1, 2};
//int bitRequiredTime [] = { 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9}; // 58 (55 with gDelta = 3)

// Circuit D
//int bitArrivalTime [] = {1, 3, 2, 3, 2, 1, 3, 2, 1, 3, 4, 2, 1, 2, 4, 1, 3, 1, 2, 1, 2, 1, 1, 2, 3, 2, 4, 1, 3, 2, 2, 1}; // 56

//Circuit E
//int bitArrivalTime [] = {2, 3, 1, 1, 2, 3, 2, 1, 4, 3, 2, 1, 3, 2, 1, 1, 2, 3, 2, 1, 3, 1, 4, 1, 2, 3, 2, 3, 1, 2, 1, 2}; // 54

//Circuit F
//int bitArrivalTime [] = {1, 2, 1, 1, 1, 3, 2, 3, 4, 2, 3, 1, 2, 3, 2, 1, 2, 2, 1, 2, 1, 1, 2, 2, 2, 2, 1, 3, 2, 4, 1, 2}; //53

// Circuit G
//int bitArrivalTime [] = {3, 1, 2, 1, 2, 3, 2, 1, 1, 1, 4, 2, 3, 1, 2, 3, 1, 2, 1, 1, 2, 1, 2, 1, 1, 3, 2, 1, 4, 2, 3, 1}; // 55 (gDelta = 3)

// Circuit H
//int bitArrivalTime [] = {1, 2, 3, 2, 1, 3, 1, 2, 2, 4, 1, 2, 1, 2, 3, 2, 4, 2, 1, 1, 1, 1, 2, 1, 2, 1, 3, 4, 2, 1, 2, 1}; // 55

//CIRCUIT I 
//int bitArrivalTime [] = {2, 3, 3, 1, 2, 1, 1, 1, 1, 2, 2, 2, 3, 2, 3, 2, 1, 1, 4, 1, 2, 1, 1, 2, 1, 2, 1, 2, 1, 1, 2, 1}; //55

// Circuit J
//int bitArrivalTime [] = {1, 1, 1, 2, 3, 1, 2, 3, 2, 1, 2, 1, 2, 1, 4, 4, 4, 3, 2, 3, 4, 2, 3, 1, 2, 3, 2, 1, 3, 2, 1, 3};
// cIRCUIT k
//int bitArrivalTime [] = {2, 1, 1, 2, 1, 2, 1, 2, 1, 3, 2, 2, 2, 2, 2, 1, 3, 1, 1, 2, 3, 4, 4, 4, 2, 1, 4, 2, 4, 1, 2, 3};

int bitArrivalTime [] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

//int bitRequiredTime [] = {6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6};

//int bitRequiredTime [] = {7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7};
//int bitRequiredTime [] = {5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,5, 5, 5, 5, 5, 5, 5, 5};

//int bitRequiredTime [] = {8, 8, 8, 8, 8,8, 8, 8, 8, 8, 8, 8, 8,8, 8, 8, 8, 8, 8, 8, 8,8, 8, 8, 8, 8, 8, 8, 8,8, 8, 8,8, 8, 8, 8, 8,8, 8, 8, 8, 8, 8, 8, 8,8, 8, 8, 8, 8, 8, 8, 8,8, 8, 8, 8, 8, 8, 8, 8,8, 8, 8,8, 8, 8, 8, 8,8, 8, 8, 8, 8, 8, 8, 8,8, 8, 8, 8, 8, 8, 8, 8,8, 8, 8, 8, 8, 8, 8, 8,8, 8, 8,8, 8, 8, 8, 8,8, 8, 8, 8, 8, 8, 8, 8,8, 8, 8, 8, 8, 8, 8, 8,8, 8, 8, 8, 8, 8, 8, 8,8, 8, 8};


void exhaustive(int, int, int);
void freeDS(int var);
void freeSolutionBeyondDelta(SizeSolSetIter sizeStart1, SizeSolSetIter sizeEnd1, SizeSolSet myMap);
void clearSolution(Sol soln);
void addSizeAndListOfPrefixNode(int bit, int size, Sol PrefixNodeList);
void makeCopyOfList(Sol newSoln, Sol soln);
void initialize(int var);
void printSolution(Sol soln, int bit);

bool buildRecursivePrefixGraph(Sol soln, SolIter pointer,int n, int size,int repeat, SolIter it);
void buildPrefixGraphN(int n, int level);
bool isSolutionValid(Sol soln, int n);


int countN[800];


// Not a very effective way, but should be ok as of now
// Assumption is we do not have prefix graphs with size more than 800
void initializeCountN () {
    for(int i =0; i < 800; i++) {
    	countN[i] = 0;
    }
}

int minSize;

// This is the tunable parameter
// For no fanput-restriction, usually, we are okay with low value such as 2 or 3
// For fanout restriction, we need more
int gDelta = 2;
int maxRepeat = 1;

int MAXLEVEL;
int MFO;  // maximum fan out

SizeSolSet * sizeToListOfPrefixNodeGlobalMap;

bool levelRestrictionFlag = false;

int noOfConstraints; // this is the number of such constraints for a bit. for example it is 3 for 7 , 1 for 5

int numberOfConstraints(int n) {
  int count = 0;
  while(n != 0) {
    if(n%2==0) return count;
    count +=1;
    n = n/2;
  }
  return count;
};


void freeDS(int bit) {
  for(int i=0; i<bit; ++i) {
    SizeSolSet sizeToListOfPrefixNodeMap = sizeToListOfPrefixNodeGlobalMap[i];
    if (sizeToListOfPrefixNodeMap == NULL) continue;
    SizeSolSetIter widthStart, widthEnd;
    for(widthStart = sizeToListOfPrefixNodeMap->begin(); widthStart != sizeToListOfPrefixNodeMap->end(); ++widthStart) {
      SolSet solnSet = widthStart->second;
      SolSetIter solnSetStart;
      for(solnSetStart = solnSet->begin(); solnSetStart != solnSet->end();++solnSetStart) {	
	Sol soln = *solnSetStart;
	clearSolution(soln);
      }
      delete solnSet;
      solnSet = NULL;
    }
    delete (sizeToListOfPrefixNodeMap);
    sizeToListOfPrefixNodeMap = NULL;
  }
}

// Function to clean up soltions when prefix graph sizes reach beyong delta a.k.a. size pruning
void freeSolutionBeyondDelta(SizeSolSetIter sizeStart, SizeSolSetIter sizeEnd, SizeSolSet solnSetForNBit) { 
  for(;sizeStart != sizeEnd; ++sizeStart) {
    SolSet solnSet = sizeStart->second;
    SolSetIter solnSetStart;
    for(solnSetStart = solnSet->begin(); solnSetStart != solnSet->end(); ++solnSetStart ) {
      Sol soln = (*solnSetStart);
      clearSolution(soln);
      solnSetStart = solnSet->erase(solnSetStart);
    }
    delete solnSet;
    solnSet = NULL;
    solnSetForNBit->erase(sizeStart);
  }
}

void clearSolution(Sol soln) {
  delete soln;
  soln = NULL;
}

// Store the solution
void addSizeAndListOfPrefixNode(int bit, int size, Sol soln) {
  countN[size] = countN[size] + 1;
  SizeSolSetIter sizeStart = (sizeToListOfPrefixNodeGlobalMap)[bit]->find(size);
  SolSet solnSet = NULL;
  if(sizeStart == (sizeToListOfPrefixNodeGlobalMap)[bit]->end()) {
    solnSet = new SolSet_t;
    (*(sizeToListOfPrefixNodeGlobalMap)[bit])[size] = solnSet;
  }
  else {
    solnSet = sizeStart->second;
  }
  solnSet->push_back(soln);
}


void initialize(int bit) {
  for(int i =0; i <= bit-1; ++i) {
    SizeSolSet newMap = new SizeSolSet_t;
    sizeToListOfPrefixNodeGlobalMap[i] = newMap;
  }
  
  Sol soln = new Sol_t;
  int val = 0;
  setIndex(val,1);
  setFanout(val, 0);
  setLowerBound(val,0);
  setLevel(val,1);
  soln->push_back(val);
  addSizeAndListOfPrefixNode(1,1,soln);
}

void makeCopyOfList(Sol newSoln, Sol soln) {
  SolIter solnStart;
  for(solnStart = soln->begin(); solnStart != soln->end(); ++solnStart) {
    newSoln->push_back((*solnStart));
  }
} 



void printSolution(Sol soln, int bit) {
  SizeSolSetIter sizeStart = ((sizeToListOfPrefixNodeGlobalMap)[bit-1])->begin();
  SizeSolSetIter sizeEnd = ((sizeToListOfPrefixNodeGlobalMap)[bit-1])->end();
  int size = sizeStart->first;
  
  SolSet solnSet = sizeStart->second;
  if(solnSet == NULL) {
    return;
  }

  int count = solnSet->size();

  SolSetIter solnSetStart, solnSetEnd; 
  for(solnSetStart = solnSet->begin(); solnSetStart != solnSet->end(); ++solnSetStart) {
    Sol firstSoln = (*solnSetStart);
    SolIter solnStart;
    for(solnStart = firstSoln->begin(); solnStart != firstSoln->end(); ++solnStart) {
      int value = (*solnStart);
      soln->push_back(value);
      cout<<" index = "<<getIndex(value);
    }
    break;
  }
  cout<<endl;
  {
    for(;sizeStart != sizeEnd; ++sizeStart) {
      int size = sizeStart->first;
      int count = sizeStart->second->size();
      cout<<" count with prefix graph size = "<<size<<" is "<<count<<endl;
    }
  }
  
  cout<<" min size = "<<size<<endl;
  cout<<" count = "<<count<<endl; 

}


int bucketSize = 50000;
// This is the key function
bool buildRecursivePrefixGraph(Sol soln, SolIter solnIter,int n, int size, int repeat, int& lastValue, int inserted) {
  if(lastValue != 0 && getLowerBound(lastValue) == 0) {
    if(countN[size] > bucketSize) return true;  // bucket is full
    Sol newSoln = NULL;
    newSoln = new Sol_t;
    makeCopyOfList(newSoln, soln);
    addSizeAndListOfPrefixNode(n, size, newSoln); // store the solution
    
    if(size < minSize) {
      minSize = size;
      SizeSolSetIter sizeStart = ((sizeToListOfPrefixNodeGlobalMap)[n])->begin();
      SizeSolSetIter sizeEnd = ((sizeToListOfPrefixNodeGlobalMap)[n])->end();
      for(int i=0; i <=gDelta; ++i) {
	if(sizeStart != sizeEnd) sizeStart++;	
      }
      freeSolutionBeyondDelta(sizeStart, sizeEnd, sizeToListOfPrefixNodeGlobalMap[n]);   // removing all irrelevant solutions dynamically
    }
    return true;  // valid prefix graph constructed
  }


   
  if(size >= minSize + gDelta) return false;  // checking size constraints
  // insert
  SolIter soln_copy = solnIter;
  int qPreVal = 0;
  if(soln_copy != soln->begin()) {
    soln_copy--;
    qPreVal = (*soln_copy);
  }
  
  int nFanout = 0; int qFanout = 0;
  int nBound  = n;
  int q = n -1;
  //int nLevel = 0; int qLevel = 0;
  int nLevel = bitArrivalTime[n];
  int qLevel = bitArrivalTime[q];
  if(lastValue != 0) {
    nLevel = getLevel(lastValue);	
    nFanout = getFanout(lastValue);
    nBound = getLowerBound(lastValue);
  }
  if(qPreVal  != 0) {
    q = getLowerBound(qPreVal);
    qLevel = getLevel(qPreVal);
    qFanout = getFanout(qPreVal);
    
  }
  int level = max(nLevel, qLevel);
  if(level >= MAXLEVEL) {  // Checking level constraints
    return false;
  }
  
  int searchFor = nBound - 1;

  // Fanout check + level restriction in non-trivial fanin + repeatibility pruning
  if(max(nFanout,qFanout) < MFO && (nLevel <= qLevel || q == 0) && repeat <  maxRepeat) {  
    int val = 0;
    setIndex(val, n);
    setLevel(val, level + 1);
    setLowerBound(val, q);
    
    if(lastValue != 0) {
      setFanout(lastValue, nFanout + 1);
    }
    if(qPreVal != 0) {
      setFanout(qPreVal, qFanout+ 1);
      (*soln_copy) = qPreVal;
    }
    
    soln->insert(solnIter, val);
    
    SolIter x = solnIter;
    x--;
    bool checkFlag = buildRecursivePrefixGraph(soln,solnIter,n, size + 1, repeat +1, (*x), inserted + 1);
    solnIter--;
    solnIter = soln->erase(solnIter);
    
    if(lastValue  != 0) {
      setFanout(lastValue, nFanout);
    }
    if(qPreVal  != 0) {
      setFanout(qPreVal, qFanout);
      (*soln_copy)  = qPreVal;
    }
    if(checkFlag == true) return false;	
  }  
  
  if(levelRestrictionFlag == true) { 
    if(inserted < noOfConstraints  && repeat == 0 && inserted == qLevel ) return false; // This is for logn level restriction
  }
  if(solnIter == soln->end()) return false;



  int nodeIndex = -1;
  do {
    nodeIndex = getIndex((*solnIter));
    solnIter++;
  } while(nodeIndex != searchFor && solnIter != soln->end());
  if(nodeIndex == searchFor) {
    buildRecursivePrefixGraph(soln, solnIter,n,size, 0, lastValue, inserted);
  }
  return false;
}

// Building prefix graphs of bitwidth n
void buildPrefixGraphN(int n, int level) {
  if(n<1) return;
  initializeCountN();
  MAXLEVEL = level;
  noOfConstraints = numberOfConstraints(n);
  minSize = 10000;
  SizeSolSetIter sizeStart = ((sizeToListOfPrefixNodeGlobalMap)[n-1])->begin();
  SizeSolSetIter sizeEnd = ((sizeToListOfPrefixNodeGlobalMap)[n-1])->end();
  if(sizeStart == sizeEnd) {
     cout<<" no solution at "<<n;
  }
  for(; sizeStart != sizeEnd; ++sizeStart) {
    int size = sizeStart->first;
    SolSet solnSet = sizeStart->second;
    SolSetIter solnSetStart;
    for(solnSetStart = solnSet->begin(); solnSetStart != solnSet->end(); ++solnSetStart) {
      Sol soln = (*solnSetStart);
      if(soln == NULL) continue;
      SolIter solnStart = soln->begin();
      int lastValue = 0;
      buildRecursivePrefixGraph(soln, solnStart,n,  size,0, lastValue,0);
      clearSolution(soln);
    }
    delete solnSet;
    solnSet = NULL;
    (sizeToListOfPrefixNodeGlobalMap)[n-1]->erase(sizeStart);
  }
  
  SizeSolSetIter sizeStart1 = ((sizeToListOfPrefixNodeGlobalMap)[n])->begin();
  SizeSolSetIter sizeEnd1 = ((sizeToListOfPrefixNodeGlobalMap)[n])->end();
  {
   if(sizeStart1 != sizeEnd1) {
        int size = sizeStart1->first;
        cout<<" min size for "<<n<<" = "<<size<<endl;
   }

  } 
  for(int i = 0; i <= gDelta; ++i)  {
    if(sizeStart1 != sizeEnd1)
      sizeStart1++;
  }
  freeSolutionBeyondDelta(sizeStart1, sizeEnd1, sizeToListOfPrefixNodeGlobalMap[n]);
  
  SizeSolSet delMap =  sizeToListOfPrefixNodeGlobalMap[n-1];
  delete delMap;
  sizeToListOfPrefixNodeGlobalMap[n-1]  = NULL;
}

// Checking the validity of the solution
bool isSolutionValid(Sol soln, int n) {
  SolIter solnStart = soln->begin();
  SolIter solnEnd = soln->end();
  if(solnStart == solnEnd) return false;
  int localIndexArray[n]; 
  for(int i = 0; i < n; ++i) localIndexArray[i] = i;
  for(; solnStart != solnEnd; ++solnStart) {
    int value = (*solnStart);
    int index = getIndex(value);
    localIndexArray[index] = localIndexArray[localIndexArray[index] - 1];
  }
  
  bool retValue = true;	
  for(int i =0; i <n; ++i) {
    if(localIndexArray[i] != 0) {
      retValue = false;
      break;
    }
  }
  
  return retValue;
}


void exhaustive(int bit_width, int level, int mfo) {
  MFO = mfo; 
  
  if(double(level) == log2(bit_width)) {
	levelRestrictionFlag = true;
	cout<<"level restriction flag set"<<endl;
  }

  sizeToListOfPrefixNodeGlobalMap = (SizeSolSet *)malloc(bit_width* sizeof(SizeSolSet));
  // cout<<"Test"<<endl;
  initialize(bit_width);
  // Bottom up prefix graph building
  for(int p = 2; p<bit_width; p++) {
    cout<<" p = "<<p<<endl;
    // level = bitRequiredTime[p];
    // cout<<"Test required time"<<endl;
    buildPrefixGraphN(p, level);
  }

  Sol soln = NULL;
  soln = new Sol_t;
  printSolution(soln, bit_width);


  bool consistencyFlag = isSolutionValid(soln, bit_width);
  if(consistencyFlag == true) {
  }
  clearSolution(soln);

  freeDS(bit_width);
  delete sizeToListOfPrefixNodeGlobalMap;
   sizeToListOfPrefixNodeGlobalMap = NULL;
}


	
int main(int argc, char** argv) {
  
  if(argc != 4) {
    return 0;
  }
 
  int bit_width = atoi(argv[1]);
  int level = atoi(argv[2]);
  int maxFanout = atoi(argv[3]);
   
  exhaustive(bit_width, level, maxFanout);
  
  return 0; 
}	
