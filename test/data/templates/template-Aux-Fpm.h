#ifndef _{{aux_name_lower}}_H_
#define _{{aux_name_lower}}_H_

#include <random>

#include "atomic.h"
#include "VTime.h"


#define {{aux_name_upper}} "{{aux_name_lower}}"


class {{aux_name_lower}} : public Atomic {
  public:
    
    {{aux_name_lower}}(const string &name = {{aux_name_upper}} );
    virtual string className() const {  return {{aux_name_upper}} ;}
  
  protected:
    Model &initFunction();
    Model &externalFunction( const ExternalMessage & );
    Model &internalFunction( const InternalMessage & );
    Model &outputFunction( const CollectMessage & );

  private:
    {% for input_port_name in input_ports %}
    const Port &in_port_{{input_port_name}};
    {%- endfor -%}
    {% for output_port_name in output_ports %}
    Port &out_port_{{output_port_name}};
    {% endfor -%}
    {%- for input_port_name in input_ports %}
    double {{input_port_name}};
    {%- endfor -%}
    {%- for input_port_name in input_ports %}
    bool isSet_{{input_port_name}};
    {%- endfor %}
    bool non_negative = (bool){{non_negative}};
};

#endif
