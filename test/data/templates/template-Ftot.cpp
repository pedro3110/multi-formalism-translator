#include <random>
#include <string>

#include "message.h"
#include "parsimu.h"
#include "real.h"
#include "tuple_value.h"

#include "{{tot_name_lower}}.h"

using namespace std;

{{tot_name_lower}}::{{tot_name_lower}}(const string &name) :
	Atomic(name),
	{% for port_plus in plus_input_ports -%}
	in_plus_port_{{port_plus}}(addInputPort("in_plus_port_{{port_plus}}")),
	{% endfor -%}
	{% for port_minus in minus_input_ports -%}
	in_minus_port_{{port_minus}}(addInputPort("in_minus_port_{{port_minus}}")),
	{% endfor -%}
	{% for port_plus in plus_input_ports -%}
	isSet_{{port_plus}}(false),
	{% endfor -%}
	{% for port_minus in minus_input_ports -%}
	isSet_{{port_minus}}(false),
	{% endfor -%}
	{% for port_out in output_ports -%}
	out_port_{{port_out}}(addOutputPort("out_port_{{port_out}}"))
	{% endfor -%}
{
}


Model &{{tot_name_lower}}::initFunction()
{
	holdIn(AtomicState::passive, VTime::Inf);
	return *this;
}


Model &{{tot_name_lower}}::externalFunction(const ExternalMessage &msg)
{
	double x = Tuple<Real>::from_value(msg.value())[0].value();

	{% for port_plus in plus_input_ports -%}
	if(msg.port() == in_plus_port_{{port_plus}}) {
		{{port_plus}} = x;
		isSet_{{port_plus}} = true;
	}
	{% endfor -%}
	{% for port_minus in minus_input_ports -%}
	if(msg.port() == in_minus_port_{{port_minus}}) {
		{{port_minus}} = x;
		isSet_{{port_minus}} = true;
	}
	{% endfor -%}
	holdIn(AtomicState::active, VTime::Zero);
	return *this;
}


Model &{{tot_name_lower}}::internalFunction(const InternalMessage &)
{
	passivate();
	return *this ;
}


Model &{{tot_name_lower}}::outputFunction(const CollectMessage &msg)
{
	double plus = 0;
	double minus = 0;
	{%- for port_plus in plus_input_ports -%} 
	if(isSet_{{port_plus}}) { plus = plus + {{port_plus}}; } 
	{%- endfor -%}
	{%- for port_minus in minus_input_ports -%}
	if(isSet_{{port_minus}}) { minus = minus + {{port_minus}}; }
	{%- endfor -%}

	double val = plus - minus;
	Tuple<Real> out_value { val };
	{% for port_out in output_ports -%}
	sendOutput(msg.time(), out_port_{{port_out}}, out_value);
	{% endfor -%}

	return *this ;
}
