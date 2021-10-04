#include <random>
#include <string>

#include "message.h"
#include "parsimu.h"
#include "real.h"
#include "tuple_value.h"

#include "{{cte_name_lower}}.h"

using namespace std;

{{cte_name_lower}}::{{cte_name_lower}}(const string &name) :
	{%- for input_port_name in input_ports %}
   	in_port_{{input_port_name}}(addInputPort("in_port_{{input_port_name}}")),
    {%- endfor %}
    out_port_{{cte_name}}(addOutputPort("out_port_{{cte_name}}")),
	{%- for input_port_name in input_ports %}
    {{input_port_name}}(-1),
    {% endfor -%}
    Atomic(name)
{
}


Model &{{cte_name_lower}}::initFunction()
{
	holdIn(AtomicState::passive, VTime::Inf);
	return *this;
}


Model &{{cte_name_lower}}::externalFunction(const ExternalMessage &msg)
{
	double x = Tuple<Real>::from_value(msg.value())[0].	value();
	{%- for input_port_name in input_ports %}
    if(msg.port() == in_port_{{input_port_name}}) {
    	{{input_port_name}} = x;
    }
    {% endfor -%}
	holdIn(AtomicState::active, VTime::Zero);
	return *this;
}


Model &{{cte_name_lower}}::internalFunction(const InternalMessage &)
{
	passivate();
	return *this ;
}


Model &{{cte_name_lower}}::outputFunction(const CollectMessage &msg)
{
	{%- for input_port_name in input_ports %}
    Tuple<Real> out_value { {{input_port_name}} };
	sendOutput(msg.time(),  out_port_{{input_port_name}}, out_value);
    {% endfor -%}
	return *this ;
}
