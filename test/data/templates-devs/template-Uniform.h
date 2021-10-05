#ifndef _{{uniform_name_upper}}_H_
#define _{{uniform_name_upper}}_H_

#include <random>

#include "atomic.h"
#include "VTime.h"


#define {{uniform_name_upper}} "{{uniform_name_lower}}"


class {{uniform_name_lower}} : public Atomic {
  public:
    
    {{uniform_name_lower}}(const string &name = {{uniform_name_upper}} );
    virtual string className() const {  return {{uniform_name_upper}} ;}
  
  protected:
    Model &initFunction();
    Model &externalFunction( const ExternalMessage & );
    Model &internalFunction( const InternalMessage & );
    Model &outputFunction( const CollectMessage & );

  private:

    {% for input_port_name in input_ports %}
    const Port &in_port_{{input_port_name}};
    double {{input_port_name}};
    {% endfor -%}
    
    {% for output_port_name in output_ports %}
    Port &out_port_{{output_port_name}};
    {% endfor -%}

    VTime uniform_time;
    double dt = 1. / {{dt}};

};

#endif
