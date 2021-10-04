#include <random>
#include <string>

#include "message.h"
#include "parsimu.h"
#include "real.h"
#include "tuple_value.h"

#include "{{graphical_name_lower}}.h"

using namespace std;


{{graphical_name_lower}}::{{graphical_name_lower}}(const string &name) :
	Atomic(name),
	{%- for input_port_name in input_ports %}
    in_port_{{input_port_name}}(addInputPort("in_port_{{input_port_name}}")),
    {%- endfor -%}
	{%- for input_port_name in input_ports %}
    isSet_{{input_port_name}}(false),
    {%- endfor %}
	out_port_{{graphical_name}}(addOutputPort("out_port_{{graphical_name}}"))
{
	std::istringstream tokenStream(ypts_str);
	string token;
	while(std::getline(tokenStream, token, ',')) {
		ypts.push_back(std::stof(token));
	}

	x_time_interval = (xscale_max - xscale_min) / (double) (ypts.size() - 1);

}


Model &{{graphical_name_lower}}::initFunction()
{
	{% if equation == 'TIME' %}
	holdIn(AtomicState::passive, VTime::Zero);
	{% else %}
	holdIn(AtomicState::passive, VTime::Inf);
	{% endif %}
	return *this;
}


Model &{{graphical_name_lower}}::externalFunction(const ExternalMessage &msg)
{
	double x = Tuple<Real>::from_value(msg.value())[0].value();

	{% if equation != 'TIME' %}
	{% for input_port_name in input_ports -%}
	if(msg.port() == in_port_{{input_port_name}}) {
		{{input_port_name}} = x;
		isSet_{{input_port_name}} = true;
	}
	{% endfor -%}
	holdIn(AtomicState::active, VTime::Zero);
	{% endif %}
	return *this;
}


Model &{{graphical_name_lower}}::internalFunction(const InternalMessage &)
{
	{% if equation == 'TIME' %}
	next_index += 1;
	if (next_index <= ypts.size()) {
		if (x_time_interval >= 1) {
			holdIn(AtomicState::active, VTime(0, 0, x_time_interval, (int)((x_time_interval - (int)x_time_interval)*1000) ) );
		} else {
			holdIn(AtomicState::active, VTime(0, 0, 0, x_time_interval * 1000));
		}
	} else {
		passivate();
	}
	{% else %}
	passivate();
	{% endif %}
	return *this ;
}


Model &{{graphical_name_lower}}::outputFunction(const CollectMessage &msg)
{
	{% if equation == 'TIME' %}
	double out_val;
	if (next_index < ypts.size()) {
		out_val = ypts[next_index];
	} else {
		out_val = 0;
	}
	Tuple<Real> out_value { Real(out_val) };
	sendOutput(msg.time(), out_port_{{graphical_name}}, out_value);
	{% else %}
	if({% for input_port_name in input_ports -%}
		{% if loop.index0 == 0 %} isSet_{{input_port_name}} {% endif -%}
		{% if loop.index0 > 0 %}& isSet_{{input_port_name}} {% endif -%}
	{% endfor -%}) {
		double out_val;
		double x_val = {{equation}};
		if (x_val < xscale_min) {
			out_val = ypts[0];
		} else if (xscale_max < x_val) {
			out_val = ypts[ypts.size()-1];
		} else {
			int index = 0;
			double x_val_now = xscale_min;
			while(!(x_val_now <= x_val && x_val <= x_val_now + x_time_interval)) {
				index++;
				x_val_now += x_time_interval;
			}
			if (index >= ypts.size()) {
				throw runtime_error(string("Index out of range"));
			}
			out_val = ypts[index];
		}
		
		Tuple<Real> out_value { Real(out_val) };
		sendOutput(msg.time(), out_port_{{graphical_name}}, out_value);
	}
	{% endif %}
	return *this ;
}