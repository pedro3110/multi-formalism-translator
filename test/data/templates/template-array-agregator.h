#ifndef _{{dag_name_lower}}_H_
#define _{{dag_name_lower}}_H_

#include <random>

#include "atomic.h"
#include "VTime.h"
#include "equation_calculator.h"


#define {{dag_name_upper}} "{{dag_name_lower}}"


class {{dag_name_lower}} : public Atomic {
  public:
    
    {{dag_name_lower}}(const string &name = {{dag_name_upper}} );
    virtual string className() const {  return {{dag_name_upper}} ;}
  
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

    double res;
    string equation = "{{equation}}";
    map<int,int> map_dimension_size;

    EquationCalculator calculator = EquationCalculator();

};

#endif