#include <random>
#include <string>

#include "message.h"
#include "parsimu.h"
#include "real.h"
#include "tuple_value.h"

#include "{{dag_name_lower}}.h"

using namespace std;

{{dag_name_lower}}::{{dag_name_lower}}(const string &name):
    {%- for input_port_name in input_ports %}
    in_port_{{input_port_name}}(addInputPort("in_port_{{input_port_name}}")),
    {%- endfor -%}
    {%- for input_port_name in input_ports %}
    isSet_{{input_port_name}}(false),
    {%- endfor %}
    {%- for output_port_name in output_ports %}
    out_port_{{output_port_name}}(addOutputPort("out_port_{{output_port_name}}")),
    {%- endfor -%}
    Atomic(name)
{
    {% for d in dimensions -%}
    map_dimension_size.insert(pair<int,int>({{d['position']}}, {{d['size']}}));
    {% endfor %}

    calculator = EquationCalculator(equation,map_dimension_size);
}


Model &{{dag_name_lower}}::initFunction()
{
    holdIn(AtomicState::passive, VTime::Inf);
    return *this;
}


Model &{{dag_name_lower}}::externalFunction(const ExternalMessage &msg)
{
    Tuple<Real> tuple = Tuple<Real>::from_value(msg.value());

    vector<double> values;
    for(int i=0; i < tuple.size(); i++) {
        double x = tuple[i].value();
        values.push_back(x);
    }
    
    res = calculator.calculate(values);
    
    holdIn(AtomicState::active, VTime::Zero);
    return *this;
}


Model &{{dag_name_lower}}::internalFunction(const InternalMessage &)
{
    passivate();
    return *this ;
}


Model &{{dag_name_lower}}::outputFunction(const CollectMessage &msg)
{
    Tuple<Real> out_value { Real(res) };
    {%- for output_port_name in output_ports %}
    sendOutput(msg.time(), out_port_{{output_port_name}}, out_value);
    {% endfor %}
    return *this ;
}