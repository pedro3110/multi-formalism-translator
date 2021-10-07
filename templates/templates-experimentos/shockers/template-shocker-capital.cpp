#include <random>
#include <string>
#include <vector>

#include "math.h"

#include "message.h"
#include "parsimu.h"
#include "real.h"
#include "tuple_value.h"

#include "{{atomicClass}}.h"

using namespace std;

{{atomicClass}}::{{atomicClass}}(const string &name) :
	Atomic(name),
	{% for outPort in outPorts -%}
	{{outPort}}(addOutputPort("{{outPort}}")),
	{% endfor -%}
	in(addInputPort("in")),
	inCapital(addInputPort("inCapital")),
	prev_Capital(0),
	isSet_Capital(false),
	numberOfOutputPorts({{numberOfOutputPorts}}),
	numberOfChosenOutputPorts({{numberOfChosenOutputPorts}})
{
}


Model &{{atomicClass}}::initFunction()
{
	holdIn(AtomicState::passive, VTime::Inf);
	return *this;
}


Model &{{atomicClass}}::externalFunction(const ExternalMessage &msg)
{
	double x = Tuple<Real>::from_value(msg.value())[0].value();
	if(msg.port() == inCapital) {
        prev_Capital.push_back(Capital);
        Capital = x;
        isSet_Capital = true;
    }
    VTime waitingTime = VTime::Zero;
    holdIn(AtomicState::active, waitingTime);
	return *this;
}


Model &{{atomicClass}}::internalFunction(const InternalMessage &)
{
	passivate();
	return *this ;
}


Model &{{atomicClass}}::outputFunction(const CollectMessage &msg)
{
	float limit = {{limit}};
	if(isSet_Capital) {
		// Condiciona solo en variable 'Capital'. 
		// TODO: condicionar en mas variabels. TODO: que solamente shoquee una vez? o cada vez que se supere el threshold?

		if (Capital > limit && prev_Capital.back() < limit && !(shock_only_once && n_shocks > 0)) {
			srand(time(0));
			vector<int> selected_ports;
			// Generate vector with indices of output ports used
			for(int i = 0; i < {{numberOfOutputPorts}}; i++) {
				if(i < {{numberOfChosenOutputPorts}}) {
					selected_ports.push_back(1);
				} else {
					selected_ports.push_back(0);
				}
		  	}
		  	// Shuffle selected ports
		  	std::random_shuffle ( selected_ports.begin(), selected_ports.end() );
			
			// Send output
			Real outValue = shockValue;

			{% for outPort in outPorts -%} 
			if(selected_ports[{{loop.index - 1}}] == 1) { sendOutput(msg.time(), {{outPort}}, outValue); }
			{% endfor -%}

			n_shocks++;
		}
	}
	return *this ;
}
