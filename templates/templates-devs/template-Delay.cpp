#include <random>
#include <string>

#include "message.h"
#include "parsimu.h"
#include "real.h"
#include "tuple_value.h"

#include "{{delay_name_lower}}.h"

using namespace std;


{{delay_name_lower}}::{{delay_name_lower}}(const string &name) :
	Atomic(name),
	firstTime(true),
	in_port_{{input_parameter}}(addInputPort("in_port_{{input_parameter}}")),
	isSet_{{input_parameter}}(false),
    in_port_{{delay_parameter}}(addInputPort("in_port_{{delay_parameter}}")),
    isSet_{{delay_parameter}}(false),

    // TODO: considerar hacer algo cuando me pasan el initial_delay_parameter
    {% if initial_delay_parameter != 'None' -%}
    in_port_{{initial_delay_parameter}}(addInputPort("in_port_{{initial_delay_parameter}}")),
    isSet_{{initial_delay_parameter}}(false),
    {% endif -%}
	out_port_{{delay_name}}(addOutputPort("out_port_{{delay_name}}"))
{
	last_time = VTime(0,0,0,0);
}


Model &{{delay_name_lower}}::initFunction()
{
	holdIn(AtomicState::passive, VTime::Inf);
	return *this;
}


Model &{{delay_name_lower}}::externalFunction(const ExternalMessage &msg)
{
	double x = Tuple<Real>::from_value(msg.value())[0].value();

	if(msg.port() == in_port_{{delay_parameter}}) {
    	{{delay_parameter}} = x;
    	isSet_{{delay_parameter}} = true;
    }

    // TODO: guardar el ELAPSED TIME tambien. Para que cuando se cumpla el tiempo de delay, poder replicar la llegada de inputs a este componente
	if(msg.port() == in_port_{{input_parameter}}) {
    	
    	input_values.push(x);

    	VTime elapsed_time = msg.time() - last_time; 
    	last_time = msg.time();

    	elapsed_time_values.push(elapsed_time);

    	isSet_{{input_parameter}} = true;
    }

    if(isSet_{{input_parameter}} && isSet_{{delay_parameter}} && firstTime) {
    	
    	firstTime = false;

    	// Es re cabeza manda output por aca. Pero sino se complica un poco...
    	Tuple<Real> out_value{Real(input_values.front())};
    	sendOutput(msg.time(), out_port_{{delay_name}}, out_value);

    	// Setear time advance.
    	if ({{delay_parameter}} >= 1) {
			holdIn(AtomicState::passive, VTime(0,0,{{delay_parameter}}, (int)(({{delay_parameter}} - (int){{delay_parameter}}) * 1000) ) );

		} else {
			holdIn(AtomicState::passive, VTime(0,0,0, (int)({{delay_parameter}} * 1000)));
		}
    }
	
	return *this;
}


Model &{{delay_name_lower}}::internalFunction(const InternalMessage &)
{
	VTime elapsed_time_now = elapsed_time_values.front();
	elapsed_time_values.pop();

	holdIn(AtomicState::passive, elapsed_time_now);
	
	return *this ;
}


Model &{{delay_name_lower}}::outputFunction(const CollectMessage &msg)
{
	if(input_values.size() > 1) {
		double val = input_values.front();
		input_values.pop();

		Tuple<Real> out_value{Real(val)};
		sendOutput(msg.time(), out_port_{{delay_name}}, out_value);
	}
	
	return *this ;
}
