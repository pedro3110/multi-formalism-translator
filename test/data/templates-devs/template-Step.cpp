#include <random>
#include <string>

#include "message.h"
#include "parsimu.h"
#include "real.h"
#include "tuple_value.h"

#include "{{step_name_lower}}.h"

using namespace std;


{{step_name_lower}}::{{step_name_lower}}(const string &name) :
	Atomic(name),
	in_port_{{time_input}}(addInputPort("in_port_{{time_input}}")),
	isSet_{{time_input}}(false),
	firstTime(true),
	initial_value_sent(false),
	initial_value(0),
    in_port_{{height_input}}(addInputPort("in_port_{{height_input}}")),
    isSet_{{height_input}}(false),
	out(addOutputPort("out")),
	out_port_{{step_name}}(addOutputPort("out_port_{{step_name}}"))
{
}


Model &{{step_name_lower}}::initFunction()
{
	holdIn(AtomicState::passive, VTime::Zero);
	return *this;
}


Model &{{step_name_lower}}::externalFunction(const ExternalMessage &msg)
{
	double x = Tuple<Real>::from_value(msg.value())[0].value();

	if(msg.port() == in_port_{{time_input}}) 
	{
		{{time_input}} = x;
		isSet_{{time_input}} = true;
	}
	else if(msg.port() == in_port_{{height_input}})
	{
		isSet_{{height_input}} = true;
		{{height_input}} = x;
	}
	if(isSet_{{time_input}} && isSet_{{height_input}} && firstTime)
	{
		firstTime = false;
		if ({{time_input}} >= 1) {
			holdIn(AtomicState::active, VTime(0,0, (int) {{time_input}}, (int)(({{time_input}} - (int){{time_input}}) * 1000) ) );
		} else {
			holdIn(AtomicState::active, VTime(0,0,0, (int){{time_input}} * 1000));
		}

	}

	return *this;
}


Model &{{step_name_lower}}::internalFunction(const InternalMessage &)
{
	passivate();
	return *this ;
}


Model &{{step_name_lower}}::outputFunction(const CollectMessage &msg)
{
	if(!initial_value_sent) {
		initial_value_sent = true;
		Tuple<Real> out_value{ initial_value };
		sendOutput(msg.time(), out_port_{{step_name}}, out_value);	
	} else {
		Tuple<Real> out_value{ {{height_input}} };
		sendOutput(msg.time(), out_port_{{step_name}}, out_value);
	}
	return *this ;
}
