#ifndef _{{name_full}}_H_
#define _{{name_full}}_H_

#include <string> 

#include "atomic.h"

#define {{name_full_upper}} "{{name_full}}"


class {{name_full}} : public Atomic {
  public:
    
    {{name_full}}(const string &name = {{name_full_upper}} );
    virtual string className() const {  return {{name_full_upper}} ;}
  
  protected:
    Model &initFunction();
    Model &externalFunction( const ExternalMessage & );
    Model &internalFunction( const InternalMessage & );
    Model &outputFunction( const CollectMessage & );

  private:
    const Port &in_port_Tot{{name}};
    Port &out_port_{{name}};

    double dQ, dQMin, dQRel;
    double x[2], q;
    double gain;
    VTime sigma; // track last change

    bool log_output_{{name}};
    double get_param(const string &);
    VTime minposroot(double *coeff);
    double to_seconds(const VTime &);

    // Agregados
    bool non_negative;
    const Port &in_port_subtract;
    const Port &in_port_increment;

};

#endif
