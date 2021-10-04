#include <random>
#include <string>

#include "message.h"
#include "parsimu.h"
#include "real.h"
#include "tuple_value.h"

#include "{{dac_name_lower}}.h"

using namespace std;

{{dac_name_lower}}::{{dac_name_lower}}(const string &name):
    {%- for input_port_name in input_ports %}
    in_port_{{input_port_name}}(addInputPort("in_port_{{input_port_name}}")),
    {%- endfor -%}
    {%- for input_port_name in input_ports %}
    isSet_{{input_port_name}}(false),
    {%- endfor %}
    {%- for output_port_name in output_ports %}
    out_port_{{output_port_name}}(addOutputPort("out_port_{{output_port_name}}")),
    {%- endfor %}
    Atomic(name)
{
}


Model &{{dac_name_lower}}::initFunction()
{
	holdIn(AtomicState::passive, VTime::Inf);
	return *this;
}


Model &{{dac_name_lower}}::externalFunction(const ExternalMessage &msg)
{
	double x = Tuple<Real>::from_value(msg.value())[0].value();

    {% for k,v in array_position_name_map_list -%}
    if(msg.port() == in_port_{{v}}) {
        array{%-for i in k-%}[{{i}}]{%-endfor-%} = x;
        isSet_{{v}} = true;
    }
    {% endfor -%}

    holdIn(AtomicState::active, VTime::Zero);
	return *this;
}


Model &{{dac_name_lower}}::internalFunction(const InternalMessage &)
{
	passivate();
	return *this ;
}


Model &{{dac_name_lower}}::outputFunction(const CollectMessage &msg)
{
    if({% for input_port_name in input_ports -%}
        {% if loop.index0 == 0 %} isSet_{{input_port_name}} {% endif -%}
        {% if loop.index0 > 0 %}& isSet_{{input_port_name}} {% endif -%}
    {% endfor -%}) {
        Tuple<Real> out_value { 
            {% for k,v in array_position_name_map_list -%}
            Real(array{%-for i in k-%}[{{i}}]{%-endfor-%}){%if loop.index < array_position_name_map_list|length %},{%endif%}
            {% endfor %}
        };
    	{%- for output_port_name in output_ports %}
        sendOutput(msg.time(), out_port_{{output_port_name}}, out_value);
        {%- endfor %}
    }
    return *this ;
}