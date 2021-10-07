#include <random>
#include <string>

#include "message.h"
#include "parsimu.h"
#include "real.h"
#include "tuple_value.h"

#include "{{pulse_name_lower}}.h"

using namespace std;


{{pulse_name_lower}}::{{pulse_name_lower}}(const string &name) :
	Atomic(name),
	in_port_{{firstPulse_input}}(addInputPort("in_port_{{firstPulse_input}}")),
	isSet_firstPulse(false),
	firstTime(true),
	{% if volume_param != None -%}
    volume({{volume_param}}),
    isSet_volume(true),
    {% endif -%}
    {% if interval_param != None -%}
    interval({{interval_param}}),
    isSet_interval(true),
    {% endif -%}
    {% if volume_input != None -%}
    in_port_{{volume_input}}(addInputPort("in_port_{{volume_input}}")),
    isSet_volume(false),
    {% endif -%}
    {% if interval_input != None -%}
    in_port_{{interval_input}}(addInputPort("in_port_{{interval_input}}")),
    isSet_interval(false),
    {% endif -%}
	out(addOutputPort("out")),
	pulse_on(false),
	interval_pulse_on(true),
	dist(0,100),
	rng(random_device()()),
	out_port_{{pulse_name}}(addOutputPort("out_port_{{pulse_name}}"))
{
	if (dt < 1) {
        pulse_time = VTime(0, 0, 0, (int) (dt * 1000));
    } else {
        pulse_time = VTime(0, 0, dt, (int)( (dt - (int)dt) * 1000) );
    }
}


Model &{{pulse_name_lower}}::initFunction()
{
	//holdIn(AtomicState::active, this->interval_time);
	// TODO : get interval_time parameters from get_params in .ma file
	holdIn(AtomicState::passive, VTime::Inf);
	return *this;
}


Model &{{pulse_name_lower}}::externalFunction(const ExternalMessage &msg)
{
	double x = Tuple<Real>::from_value(msg.value())[0].value();

	// Requiere que cuando llega el 'firstpulse', ya esten seteados el 'interval' y el 'volume'
	if(msg.port() == in_port_{{firstPulse_input}}) 
	{
		this->firstPulse = x;
		isSet_firstPulse = true;
	}
	{% if volume_input != None -%}
	else if(msg.port() == in_port_{{volume_input}})
	{
		isSet_volume = true;
		this->{{volume_input}} = x / dt;
	}
	{% endif -%}
	{% if interval_input != None -%}
	else if(msg.port() == in_port_{{interval_input}})
	{
		{{interval_input}} = x - dt;

		if({{interval_input}} >= 1) {
			interval_time = VTime(0, 0, {{interval_input}}, (int)( ({{interval_input}} - (int){{interval_input}}) * 1000) );
		} else {
			interval_time = VTime(0, 0, 0, (int)({{interval_input}}*1000) );
		}
		interval_pulse_on = true;
		pulse_on = false;
		isSet_interval = true;
	}
	{% endif %}
	if(isSet_firstPulse && isSet_volume && isSet_interval && firstTime)
	{
		firstTime = false;
		if (firstPulse >= 1) {
			holdIn(AtomicState::active, VTime(0,0,firstPulse, (int)((firstPulse - (int)firstPulse) * 1000) ) );
		} else {
			holdIn(AtomicState::active, VTime(0,0,0, (int)(firstPulse * 1000)));
		}
	}

	return *this;
}


Model &{{pulse_name_lower}}::internalFunction(const InternalMessage &)
{
	// estaba en un intervalo entre pulsos. esperar lo que dura un pulso
	if(this->interval_pulse_on && !this->pulse_on) {

		this->interval_pulse_on = false;
		this->pulse_on = true;
		holdIn(AtomicState::active, this->pulse_time);
	}
	// estaba en un pulso. esperar lo que dura un intervalo entre pulso y pulso
	else if (!this->interval_pulse_on && this->pulse_on) {

		this->interval_pulse_on = true;
		this->pulse_on = false;
		holdIn(AtomicState::active, this->interval_time);
	} else {
		passivate();
	}

	return *this ;
}


Model &{{pulse_name_lower}}::outputFunction(const CollectMessage &msg)
{
	{% if volume_param != None -%}
	auto random_int = this->volume;//this->dist(this->rng);
	{% endif -%}
	{% if volume_input != None -%}
	auto random_int = this->{{volume_input}};//this->dist(this->rng);
	{% endif -%}
	Tuple<Real> out_value{Real(random_int)};
	Tuple<Real> out_value_2{Real(0)};
	if (this->interval_pulse_on) {
		// estaba en estado interval y paso a estado pulse
		sendOutput(msg.time(), out_port_{{pulse_name}}, out_value);
	}
	else if (this->pulse_on) {
		// estaba en estado pulse y paso a estado interval
		sendOutput(msg.time(), out_port_{{pulse_name}}, out_value_2);
	}
	return *this ;
}
