#ifndef _tuple2real_H_
#define _tuple2real_H_

#include <random>

#include "atomic.h"
#include "VTime.h"


#define TUPLE2REAL "tuple2real"


class tuple2real : public Atomic {
  public:
    
    tuple2real(const string &name = TUPLE2REAL );
    virtual string className() const {  return TUPLE2REAL ;}
  
  protected:
    Model &initFunction();
    Model &externalFunction( const ExternalMessage & );
    Model &internalFunction( const InternalMessage & );
    Model &outputFunction( const CollectMessage & );

  private:
    
    const Port &in;
    
    Port &out;
    
    Real val;
    };

#endif