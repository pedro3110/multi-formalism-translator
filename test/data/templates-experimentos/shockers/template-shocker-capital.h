#ifndef _{{atomicClass}}_H_
#define _{{atomicClass}}_H_

#include <random>

#include "atomic.h"
#include "VTime.h"

#define {{atomicClassConstant}} "{{atomicClass}}"

class {{atomicClass}} : public Atomic {
  public:
    
    {{atomicClass}}(const string &name = {{atomicClassConstant}} );
    virtual string className() const {  return {{atomicClassConstant}} ;}
  
  protected:
    Model &initFunction();
    Model &externalFunction( const ExternalMessage & );
    Model &internalFunction( const InternalMessage & );
    Model &outputFunction( const CollectMessage & );

  private:
    // Input ports
    const Port &in;
    const Port &inCapital;

    // Output ports
    Port {% for outPort in outPorts -%}
    {% if loop.index0 < outPorts|length - 1 -%}&{{outPort}}, {% else -%}&{{outPort}};{% endif -%}
    {% endfor %}

    bool shock_only_once = {{shock_only_once}};
    int n_shocks = 0;

    // State variables
    double numberOfOutputPorts;
    double numberOfChosenOutputPorts;
    Real shockValue = {{shockValue}};

    // Variables de decision
    bool isSet_Capital;
    double Capital;
    std::vector<double> prev_Capital;
};

#endif
