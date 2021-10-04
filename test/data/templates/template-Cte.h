#ifndef _{{cte_name_lower}}_H_
#define _{{cte_name_lower}}_H_

#include <random>

#include "atomic.h"
#include "VTime.h"


#define {{cte_name_upper}} "{{cte_name_lower}}"


class {{cte_name_lower}} : public Atomic {
  public:
    
    {{cte_name_lower}}(const string &name = {{cte_name_upper}} );
    virtual string className() const {  return {{cte_name_upper}} ;}
  
  protected:
    Model &initFunction();
    Model &externalFunction( const ExternalMessage & );
    Model &internalFunction( const InternalMessage & );
    Model &outputFunction( const CollectMessage & );

  private:
    {% for input_port_name in input_ports %}
    const Port &in_port_{{input_port_name}};
    {% endfor -%}
    {% for output_port_name in output_ports %}
    Port &out_port_{{output_port_name}};
    {% endfor -%}

    {% for input_port_name in input_ports %}
    double {{input_port_name}};
    {% endfor -%}
};

#endif
