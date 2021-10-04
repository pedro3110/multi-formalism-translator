#include <random>
#include <string>
#include <vector>

#include "math.h"

#include "message.h"
#include "parsimu.h"
#include "real.h"
#include "tuple_value.h"

#include <iostream>
#include <fstream>

#include "{{atomicClass}}.h"

using namespace std;

{{atomicClass}}::{{atomicClass}}(const string &name) :
	Atomic(name),
	{% for outPort in outPorts -%}
	{{outPort}}(addOutputPort("{{outPort}}")),
	{% endfor -%}
	in(addInputPort("in")),
	inWageRate(addInputPort("inWageRate")),
	inEmploymentRateValue(addInputPort("inEmploymentRateValue")),
	prev_WageRate(0), prev_EmploymentRateValue(0),
	isSet_WageRate(false), isSet_EmploymentRateValue(false),
	inThresholdWR(addInputPort("inThresholdWR")),
	inThresholdER(addInputPort("inThresholdER")),
	isSet_ThresholdWR(false),isSet_ThresholdER(false),
	numberOfOutputPorts({{numberOfOutputPorts}})
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
	if(msg.port() == inWageRate) {
        prev_WageRate.push_back(WageRate);
        WageRate = x;
        isSet_WageRate = true;
    }
    if(msg.port() == inEmploymentRateValue) {
    	prev_EmploymentRateValue.push_back(EmploymentRateValue);
    	EmploymentRateValue = x;
    	isSet_EmploymentRateValue = true;
    }
    if(msg.port() == inThresholdWR) {
    	thresholdWR = x;
    	isSet_ThresholdWR = true;
    }
    if(msg.port() == inThresholdER) {
    	thresholdER = x;
    	isSet_ThresholdER = true;
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
	// TODO: NO HARCODEAR LOS n_positive / n_negative !!!
	int n_positive = 0;
	int n_negative = 0;
	int option = 0;

	// std::cerr << "###" << endl;
	// std::cerr << isSet_WageRate << "  " << isSet_EmploymentRateValue << "  " << isSet_ThresholdWR << "  " << isSet_ThresholdER << endl;

	if(isSet_WageRate && isSet_EmploymentRateValue && isSet_ThresholdWR && isSet_ThresholdER) {

		// TODO: VER
		// std::cerr << "##########" << endl;
		// std::cerr << prev_WageRate[prev_WageRate.size() - 1] << "  |  " << prev_WageRate[prev_WageRate.size() - 1] << "  |  " << WageRate << endl;
		// std::cerr << prev_EmploymentRateValue[prev_EmploymentRateValue.size() - 1] << "   |   " << prev_EmploymentRateValue[prev_EmploymentRateValue.size() - 1] << "   |   "<< EmploymentRateValue << endl;

		if(prev_WageRate.size() <= 1 || prev_EmploymentRateValue.size() <= 1) {
			return *this;
		}
		
		// WR cambio para arriba
		if (prev_WageRate[prev_WageRate.size() - 1] <= thresholdWR && WageRate > thresholdWR) {
			if (EmploymentRateValue < thresholdER) // arriba izq
			{ option = 1; n_positive = 5; n_negative = 10; }
			else if(EmploymentRateValue > thresholdER) // arriba der
			{ option = 2; n_positive = 15; n_negative = 0; }
		}

		// WR cambio para abajo
		else if (prev_WageRate[prev_WageRate.size() - 1] >= thresholdWR && WageRate < thresholdWR) {
			if(EmploymentRateValue < thresholdER) // abajo izq
			{ option = 3; n_positive = 0; n_negative = 15; }
			else if(EmploymentRateValue > thresholdER) // abajo der
			{ option = 4; n_positive = 10; n_negative = 15; }
		}

		// ER cambio para derecha
		else if (prev_EmploymentRateValue[prev_EmploymentRateValue.size() - 1] <= thresholdER && EmploymentRateValue > thresholdER) {
			if(WageRate < thresholdWR) // arriba der
			{ option = 2; n_positive = 15; n_negative = 0; }
			else if(WageRate > thresholdWR) // abajo der
			{ option = 4; n_positive = 10; n_negative = 15; }
		}

		// ER cambio para izquierda
		else if (prev_EmploymentRateValue[prev_EmploymentRateValue.size() - 1] >= thresholdER && EmploymentRateValue < thresholdER) {
			if(WageRate < thresholdWR) // abajo izq
			{ option = 3; n_positive = 0; n_negative = 15; }
			else if(WageRate > thresholdWR) // arriba izq
			{ option = 1; n_positive = 5; n_negative = 10; }
		}

		// if(option > 0) {
		// 	std::cerr << "################################################3" << option << endl;
		// 	std::cerr << "HAY CAMBIO " << option << endl;
		// }

		/* TODO */
		if (n_positive + n_negative > 0) {
			srand(time(0));
			vector<int> selected_ports;
			// Generate vector with indices of output ports used
			for(int i = 0; i < {{numberOfOutputPorts}}; i++) {
				// Coloco shocks positivos
				if (i < n_positive) {
					selected_ports.push_back(1);
				// Coloco shocks negativos
				} else if (i >= n_positive && i < n_positive + n_negative) {
					selected_ports.push_back(0);
				// Celdas SIN SHOCK
				} else {
					selected_ports.push_back(-1);
				}
		  	}
		  	// Shuffle selected ports
		  	std::random_shuffle ( selected_ports.begin(), selected_ports.end() );
			
			// Send output
			Real out_positive = {{positive_shock}};
			Real out_negative = {{negative_shock}};

			{% for outPort in outPorts -%} 
			if(selected_ports[{{loop.index - 1}}] == 0) { sendOutput(msg.time(), {{outPort}}, out_negative); }
			if(selected_ports[{{loop.index - 1}}] == 1) { sendOutput(msg.time(), {{outPort}}, out_positive); }
			{% endfor -%}

			n_shocks++;
		}
	}
	return *this ;
}
