#include <random>
#include <string>

#include "message.h"
#include "parsimu.h"
#include "real.h"
#include "tuple_value.h"
#include "math.h"

#include "{{aux_name_lower}}.h"

using namespace std;

{{aux_name_lower}}::{{aux_name_lower}}(const string &name) :
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
}


Model &{{aux_name_lower}}::initFunction()
{
	holdIn(AtomicState::passive, VTime::Inf);
	return *this;
}


Model &{{aux_name_lower}}::externalFunction(const ExternalMessage &msg)
{
	double x = Tuple<Real>::from_value(msg.value())[0].value();

	{% for input_port_name in input_ports -%}
	if(msg.port() == in_port_{{input_port_name}}) {
		{{input_port_name}} = x;
		isSet_{{input_port_name}} = true;
	}
	{% endfor -%}
	holdIn(AtomicState::active, VTime::Zero);
	return *this;
}


Model &{{aux_name_lower}}::internalFunction(const InternalMessage &)
{
	passivate();
	return *this ;
}


Model &{{aux_name_lower}}::outputFunction(const CollectMessage &msg)
{

	//TODO: hay veces en las que hay que consdierar que la variable que todavia no llego vale cero. Por ejemplo, eqn = STEP(1,1) + STEP(2,2)
	{% if input_ports|length > 0 %}
	if({% for input_port_name in input_ports -%}
		{% if loop.index0 == 0 %} isSet_{{input_port_name}} {% endif -%}
		{% if loop.index0 > 0 %}& isSet_{{input_port_name}} {% endif -%}
	{% endfor -%}) {
	    Tuple<Real> out_value { {{equation}} };
		if({{equation}} < 0 && non_negative) {
			out_value = { 0 };
		}
		//sendOutput(msg.time(), out_port_{{aux_name}}, out_value);
		{%- for output_port_name in output_ports %}
	    sendOutput(msg.time(), out_port_{{output_port_name}}, out_value);
	    {%- endfor -%}
	} else {
		Tuple<Real> out_value { 0 };
		//sendOutput(msg.time(), out_port_{{aux_name}}, out_value);
		{%- for output_port_name in output_ports %}
	    sendOutput(msg.time(), out_port_{{output_port_name}}, out_value);
	    {%- endfor -%}
	}
	{% endif %}

	return *this ;
}
