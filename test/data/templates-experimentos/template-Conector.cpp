#include <random>
#include <string>
#include <vector>

#include "math.h"

#include "message.h"
#include "parsimu.h"
#include "real.h"
#include "tuple_value.h"

#include "Conector.h"

using namespace std;


Conector::Conector(const string &name) :
    Atomic(name),
    inShockCriteria(addInputPort("inShockCriteria")),
    inShockTimeInterval(addInputPort("inShockTimeInterval")),
    inShockTimeWait(addInputPort("inShockTimeWait")),
    isSet_ShockCriteria(false),
    isSet_ShockTimeInterval(false),
    isSet_ShockTimeWait(false),
    inLaborProductivity(addInputPort("inLaborProductivity")),
    inWageRate(addInputPort("inWageRate")),
    inDebt(addInputPort("inDebt")),
    inPopulation(addInputPort("inPopulation")),
    inCapital(addInputPort("inCapital")),
    isSet_LaborProductivity(false),
    isSet_WageRate(false),
    isSet_Debt(false),
    isSet_Population(false),
    isSet_Capital(false),
    prev_LaborProductivity(0),
    prev_WageRate(0),
    prev_Debt(0),
    prev_Population(0),
    prev_Capital(0),
    out0(addOutputPort("out0")),
    out1(addOutputPort("out1")),
    out2(addOutputPort("out2")),
    out3(addOutputPort("out3")),
    out4(addOutputPort("out4")),
    lastChange(0)
{
}


Model &Conector::initFunction()
{
    holdIn(AtomicState::passive, VTime::Inf);
    return *this;
}


Model &Conector::externalFunction(const ExternalMessage &msg)
{
    double x = Tuple<Real>::from_value(msg.value())[0].value();
    
    if(msg.port() == inShockCriteria) {
        ShockCriteria = x;
        isSet_ShockCriteria = true;
    }
    if(msg.port() == inLaborProductivity) {
        prev_LaborProductivity.push_back(LaborProductivity);
        LaborProductivity = x;
        isSet_LaborProductivity = true;
    }
    if(msg.port() == inWageRate) {
        prev_WageRate.push_back(WageRate);
        WageRate = x;
        isSet_WageRate = true;
    }
    if(msg.port() == inDebt) {
        prev_Debt.push_back(Debt);
        Debt = x;
        isSet_Debt = true;
    }
    if(msg.port() == inPopulation) {
        prev_Population.push_back(Population);
        Population = x;
        isSet_Population = true;
    }
    if(msg.port() == inCapital) {
        prev_Capital.push_back(Capital);
        Capital = x;
        isSet_Capital = true;
    }
    
    // TODO : recibir inShockTimeWait y inShockTimeInterval para shocks a ritmo constante
    // TODO : ACA, ESPERAR EL TIEMPO NECESARIO PARA LLEGAR A UN MULTIPLO DEL 'TIME_INTERVAL'
    // TODO : Mandar los momentos de shock mediante el .ev file. De esta forma, podemos mandar shocks a un ritmo definido ad hoc
    // TODO : O, la otra opcion seria modificar el ritmo de shockeo de acuerdo a los valores que el Conector lee de sus puertos de entrada
    
    VTime waitingTime = VTime::Zero;

    holdIn(AtomicState::active, waitingTime);
    return *this;
}


Model &Conector::internalFunction(const InternalMessage &)
{
    passivate();
    return *this ;
}


Model &Conector::outputFunction(const CollectMessage &msg)
{
    if( isSet_ShockCriteria && isSet_LaborProductivity && isSet_WageRate && isSet_Debt && isSet_Population && isSet_Capital ) {

        // Funcion que determina si activar o no activar los shockers

        if(ShockCriteria == 1 && lastChange != LaborProductivity) {
            // Regla : envio shocks
            if ((LaborProductivity > 1.5 && prev_LaborProductivity.back() < 1.5) || 
                (LaborProductivity > 2 && prev_LaborProductivity.back() < 2) || 
                (LaborProductivity > 2.5 && prev_LaborProductivity.back() < 2.5) || 
                (LaborProductivity > 3 && prev_LaborProductivity.back() < 3) || 
                (LaborProductivity > 3.5 && prev_LaborProductivity.back() < 3.5) || 
                (LaborProductivity > 4 && prev_LaborProductivity.back() < 4) ) {

                // Para que no afecten cambios en otras variables cuando 'LaborProductivity' cruza el threshold
                lastChange = LaborProductivity;

                // Shocks
                double val0 = 5.0; std::vector<Real> tv0; tv0.push_back(Real(val0));
                Tuple<Real> outValue0 = Tuple<Real>(&tv0);
                double val1 = 6.0; std::vector<Real> tv1; tv1.push_back(Real(val1));
                Tuple<Real> outValue1 = Tuple<Real>(&tv1);
                double val2 = 6.0; std::vector<Real> tv2; tv2.push_back(Real(val2));
                Tuple<Real> outValue2 = Tuple<Real>(&tv2);
                double val3 = 7.0; std::vector<Real> tv3; tv3.push_back(Real(val3));
                Tuple<Real> outValue3 = Tuple<Real>(&tv3);
                double val4 = 7.0; std::vector<Real> tv4; tv4.push_back(Real(val4));
                Tuple<Real> outValue4 = Tuple<Real>(&tv4);

                sendOutput(msg.time(), out0, outValue0);
                sendOutput(msg.time(), out1, outValue1);
                sendOutput(msg.time(), out2, outValue2);
                sendOutput(msg.time(), out3, outValue3);
                sendOutput(msg.time(), out4, outValue4);
            }
        } else if(ShockCriteria == 2) {
            // Regla : envio shocks 2
            // TODO : aca no hago nada
        }
    }
    return *this ;
}