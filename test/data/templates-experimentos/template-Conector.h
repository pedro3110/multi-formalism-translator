#ifndef _Conector_H_
#define _Conector_H_

#include <random>

#include "atomic.h"
#include "VTime.h"

#define CONECTOR "Conector"

class Conector : public Atomic {
  public:
    
    Conector(const string &name = CONECTOR );
    virtual string className() const {  return CONECTOR ;}
  
  protected:
    Model &initFunction();
    Model &externalFunction( const ExternalMessage & );
    Model &internalFunction( const InternalMessage & );
    Model &outputFunction( const CollectMessage & );

  private:

    // Input ports
    const Port &inLaborProductivity;
    const Port &inWageRate;
    const Port &inDebt;
    const Port &inPopulation;
    const Port &inCapital;

    const Port &inShockCriteria;
    const Port &inShockTimeInterval;
    const Port &inShockTimeWait;

    // Output ports
    Port &out0, &out1, &out2, &out3, &out4;

    // State variables
    double lastChange;

    double LaborProductivity; 
    std::vector<double> prev_LaborProductivity;
    
    double WageRate;
    std::vector<double> prev_WageRate;
    
    double Debt;
    std::vector<double> prev_Debt;
    
    double Population;
    std::vector<double> prev_Population;
    
    double Capital;
    std::vector<double> prev_Capital;

    double ShockCriteria;
    VTime ShockTimeWait;
    VTime ShockTimeInterval;

    // Variables set
    bool isSet_LaborProductivity;
    bool isSet_WageRate;
    bool isSet_Debt;
    bool isSet_Population;
    bool isSet_Capital;

    bool isSet_ShockCriteria;
    bool isSet_ShockTimeInterval;
    bool isSet_ShockTimeWait;

};

#endif