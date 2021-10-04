#ifndef _{{step_name_upper}}_H_
#define _{{step_name_upper}}_H_

#include <random>

#include "atomic.h"
#include "VTime.h"


#define {{step_name_upper}} "{{step_name_lower}}"


class {{step_name_lower}} : public Atomic {
  public:
    
    {{step_name_lower}}(const string &name = {{step_name_upper}} );
    virtual string className() const {  return {{step_name_upper}} ;}
  
  protected:
    Model &initFunction();
    Model &externalFunction( const ExternalMessage & );
    Model &internalFunction( const InternalMessage & );
    Model &outputFunction( const CollectMessage & );

  private:
    Port &out;

    bool firstTime;

    bool initial_value_sent;
    double initial_value;

    const Port &in_port_{{time_input}};
    double {{time_input}};
    bool isSet_{{time_input}};
    
    const Port &in_port_{{height_input}};
    double {{height_input}};
    bool isSet_{{height_input}};

    {% for output_port_name in output_ports %}
    Port &out_port_{{output_port_name}};
    {% endfor %}
};

#endif
