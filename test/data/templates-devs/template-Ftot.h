#ifndef _{{tot_name_lower}}_H_
#define _{{tot_name_lower}}_H_

#include <random>

#include "atomic.h"
#include "VTime.h"

#define {{tot_name_upper}} "{{tot_name_lower}}"

class {{tot_name_lower}} : public Atomic {
  public:
    
    {{tot_name_lower}}(const string &name = {{tot_name_upper}} );
    virtual string className() const {  return {{tot_name_upper}} ;}
  
  protected:
    Model &initFunction();
    Model &externalFunction( const ExternalMessage & );
    Model &internalFunction( const InternalMessage & );
    Model &outputFunction( const CollectMessage & );

  private:
    {% for input_port_name in plus_input_ports -%}
    const Port &in_plus_port_{{input_port_name}};
    {% endfor -%}
    {% for input_port_name in minus_input_ports -%}
    const Port &in_minus_port_{{input_port_name}};
    {% endfor -%}

    {% for out_port in out_ports -%}
    Port &out_port_{{out_port}};
    {% endfor %}
    Port &out_port_{{tot_name}};

    {% for input_port_name in plus_input_ports -%}
    double {{input_port_name}};
    {% endfor -%}
    {% for input_port_name in minus_input_ports -%}
    double {{input_port_name}};
    {% endfor -%}

    {% for input_port_name in plus_input_ports -%}
    bool isSet_{{input_port_name}};
    {% endfor %}
    {% for input_port_name in minus_input_ports -%}
    bool isSet_{{input_port_name}};
    {% endfor %}
};

#endif
