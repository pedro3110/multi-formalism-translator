#include <random>
#include <string>

#include "message.h"
#include "parsimu.h"
#include "real.h"
#include "tuple_value.h"

#include "tuple_to_real.h"

using namespace std;

tuple2real::tuple2real(const string &name) :
   	in(addInputPort("in")),
    out(addOutputPort("out")),
    Atomic(name)
{
}


Model &tuple2real::initFunction()
{
	holdIn(AtomicState::passive, VTime::Inf);
	return *this;
}


Model &tuple2real::externalFunction(const ExternalMessage &msg)
{
	double x = Tuple<Real>::from_value(msg.value())[0].	value();
    if(msg.port() == in) {
    	val = x;
    }
    holdIn(AtomicState::active, VTime::Zero);
	return *this;
}


Model &tuple2real::internalFunction(const InternalMessage &)
{
	passivate();
	return *this ;
}


Model &tuple2real::outputFunction(const CollectMessage &msg)
{
	sendOutput(msg.time(),  out, val);
    return *this ;
}