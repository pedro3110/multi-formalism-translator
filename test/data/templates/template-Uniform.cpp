#include <random>
#include <string>

#include "message.h"
#include "parsimu.h"
#include "real.h"
#include "tuple_value.h"

#include "{{uniform_name_lower}}.h"

using namespace std;


{{uniform_name_lower}}::{{uniform_name_lower}}(const string &name) :
    {%- for input_port_name in input_ports %}
    in_port_{{input_port_name}}(addInputPort("in_port_{{input_port_name}}")),
    {%- endfor %}
    {%- for output_port_name in output_ports %}
    out_port_{{output_port_name}}(addOutputPort("out_port_{{output_port_name}}")),
    {%- endfor -%}
    Atomic(name)
{
}


Model &{{uniform_name_lower}}::initFunction()
{
    holdIn(AtomicState::passive, VTime::Inf);
    return *this;
}


Model &{{uniform_name_lower}}::externalFunction(const ExternalMessage &msg)
{
    double x = Tuple<Real>::from_value(msg.value())[0].value();

    {%- for input_port_name in input_ports %}
    if(msg.port() == in_port_{{input_port_name}}) {
        {{input_port_name}} = x;
    }
    {% endfor -%}

    holdIn(AtomicState::passive, VTime::Zero);
    return *this;
}


Model &{{uniform_name_lower}}::internalFunction(const InternalMessage &)
{
    if (dt < 1) {
        uniform_time = VTime(0, 0, 0, (int) (dt * 1000));
    } else {
        uniform_time = VTime(0, 0, dt, (int)( (dt - (int)dt) * 1000) );
    }
    holdIn(AtomicState::passive, uniform_time);
    return *this ;
}


Model &{{uniform_name_lower}}::outputFunction(const CollectMessage &msg)
{
    std::random_device rd;  //Will be used to obtain a seed for the random number engine
    std::mt19937 gen(rd()); //Standard mersenne_twister_engine seeded with rd()
    std::uniform_real_distribution<> dis({{min_val}}, {{max_val}});
    double val = dis(gen);

    Tuple<Real> out_value{Real(val)};
    sendOutput(msg.time(), out_port_{{uniform_name}}, out_value);
    return *this ;
}
