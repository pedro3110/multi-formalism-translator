#ifndef _{{delay_name_upper}}_H_
#define _{{delay_name_upper}}_H_

#include <random>
#include <queue>
#include <stack>

#include "atomic.h"
#include "VTime.h"


#define {{delay_name_upper}} "{{delay_name_lower}}"


class {{delay_name_lower}} : public Atomic {
  public:
    
    {{delay_name_lower}}(const string &name = {{delay_name_upper}} );
    virtual string className() const {  return {{delay_name_upper}} ;}
  
  protected:
    Model &initFunction();
    Model &externalFunction( const ExternalMessage & );
    Model &internalFunction( const InternalMessage & );
    Model &outputFunction( const CollectMessage & );

  private:

    bool firstTime;
    std::queue<double> input_values;
    std::queue<VTime> elapsed_time_values;
    VTime last_time;

    const Port &in_port_{{input_parameter}};
    double {{input_parameter}};
    bool isSet_{{input_parameter}};

    const Port &in_port_{{delay_parameter}};
    double {{delay_parameter}};
    bool isSet_{{delay_parameter}};
    
    {% if initial_delay_parameter != 'None' -%}
    const Port &in_port_{{initial_delay_parameter}};
    double {{initial_delay_parameter}};
    bool isSet_{{initial_delay_parameter}};
    {% endif -%}

    {% for output_port_name in output_ports %}
    Port &out_port_{{output_port_name}};
    {% endfor %}
};

#endif
