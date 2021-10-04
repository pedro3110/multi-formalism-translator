#ifndef _{{dac_name_lower}}_H_
#define _{{dac_name_lower}}_H_

#include <random>

#include "atomic.h"
#include "VTime.h"


#define {{dac_name_upper}} "{{dac_name_lower}}"


class {{dac_name_lower}} : public Atomic {
  public:
    
    {{dac_name_lower}}(const string &name = {{dac_name_upper}} );
    virtual string className() const {  return {{dac_name_upper}} ;}
  
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

    double array{%-for d in dimensions-%}[{{d['size']}}]{%-endfor-%};

};

#endif