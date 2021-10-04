#ifndef _{{graphical_name_upper}}_H_
#define _{{graphical_name_upper}}_H_

#include <random>

#include "atomic.h"
#include "VTime.h"


#define {{graphical_name_upper}} "{{graphical_name_lower}}"


class {{graphical_name_lower}} : public Atomic {
  public:
    
    {{graphical_name_lower}}(const string &name = {{graphical_name_upper}} );
    virtual string className() const {  return {{graphical_name_upper}} ;}
  
  protected:
    Model &initFunction();
    Model &externalFunction( const ExternalMessage & );
    Model &internalFunction( const InternalMessage & );
    Model &outputFunction( const CollectMessage & );

  private:

    int next_index = 0;
    double x_time_interval;

    double yscale_min = {{yscale_min}};
    double yscale_max = {{yscale_max}};

    double xscale_min = {{xscale_min}};
    double xscale_max = {{xscale_max}};

    string equation = "{{equation}}";
    string ypts_str = "{{ypts}}";

    vector<double> ypts;

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
};

#endif