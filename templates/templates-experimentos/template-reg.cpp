#include "pmodeladm.h"
#include "register.h"

{% for shocker in shockers %}
#include "{{shocker.name}}.h"
{%- endfor %}

#include "qss1.h"
#include "Cte.h"

#include "wageFunction.h"
#include "employmentRateValue.h"
#include "Labor.h"
#include "Output.h"
#include "piR.h"
#include "InvestmentGross.h"
#include "InterestPayments.h"
#include "debtRate.h"
#include "ProfitNet.h"
#include "ProfitGrossReal.h"
#include "Wages.h"
#include "Omega.h"
#include "InvestmentFunctionReal.h"
#include "InvestmentNetReal.h"
#include "chgPopulationPlus.h"
#include "chgPopulationMinus.h"
#include "chgLaborProductivityPlus.h"
#include "chgLaborProductivityMinus.h"
#include "chgDebtPlus.h"
#include "chgDebtMinus.h"
#include "chgWageRatePlus.h"
#include "chgWageRateMinus.h"
#include "chgCapitalPlus.h"
#include "chgCapitalMinus.h"
#include "LaborProductivityTot.h"
#include "WageRateTot.h"
#include "DebtTot.h"
#include "PopulationTot.h"
#include "CapitalTot.h"

// Registro modelos atomicos
void register_atomics_on(ParallelModelAdmin &admin)
{
	// Atomicos base
	admin.registerAtomic(NewAtomicFunction<QSS1>(), QSS_MODEL_NAME);
	admin.registerAtomic(NewAtomicFunction<Cte>(), CTE);
	
	// Atomicos para fusionar modelo cell-devs con modelo de Goodwin-Minsky
	{% for shocker in shockers %}
	admin.registerAtomic(NewAtomicFunction<{{shocker.name}}>(), {{shocker.name.upper()}});
	{%- endfor %}
	// admin.registerAtomic(NewAtomicFunction<Shocker>(), SHOCKER);
	// admin.registerAtomic(NewAtomicFunction<Conector>(), CONECTOR);

	// Atomicos especificos del modelo
	admin.registerAtomic(NewAtomicFunction<wageFunction>(), WAGEFUNCTION);
	admin.registerAtomic(NewAtomicFunction<employmentRateValue>(), EMPLOYMENTRATEVALUE);
	admin.registerAtomic(NewAtomicFunction<Labor>(), LABOR);
	admin.registerAtomic(NewAtomicFunction<Output>(), OUTPUT);
	admin.registerAtomic(NewAtomicFunction<piR>(), PIR);
	admin.registerAtomic(NewAtomicFunction<InvestmentGross>(), INVESTMENTGROSS);
	admin.registerAtomic(NewAtomicFunction<InterestPayments>(), INTERESTPAYMENTS);
	admin.registerAtomic(NewAtomicFunction<debtRate>(), DEBTRATE);
	admin.registerAtomic(NewAtomicFunction<ProfitNet>(), PROFITNET);
	admin.registerAtomic(NewAtomicFunction<ProfitGrossReal>(), PROFITGROSSREAL);
	admin.registerAtomic(NewAtomicFunction<Wages>(), WAGES);
	admin.registerAtomic(NewAtomicFunction<Omega>(), OMEGA);
	admin.registerAtomic(NewAtomicFunction<InvestmentFunctionReal>(), INVESTMENTFUNCTIONREAL);
	admin.registerAtomic(NewAtomicFunction<InvestmentNetReal>(), INVESTMENTNETREAL);
	admin.registerAtomic(NewAtomicFunction<chgPopulationPlus>(), CHGPOPULATIONPLUS);
	admin.registerAtomic(NewAtomicFunction<chgPopulationMinus>(), CHGPOPULATIONMINUS);
	admin.registerAtomic(NewAtomicFunction<chgLaborProductivityPlus>(), CHGLABORPRODUCTIVITYPLUS);
	admin.registerAtomic(NewAtomicFunction<chgLaborProductivityMinus>(), CHGLABORPRODUCTIVITYMINUS);
	admin.registerAtomic(NewAtomicFunction<chgDebtPlus>(), CHGDEBTPLUS);
	admin.registerAtomic(NewAtomicFunction<chgDebtMinus>(), CHGDEBTMINUS);
	admin.registerAtomic(NewAtomicFunction<chgWageRatePlus>(), CHGWAGERATEPLUS);
	admin.registerAtomic(NewAtomicFunction<chgWageRateMinus>(), CHGWAGERATEMINUS);
	admin.registerAtomic(NewAtomicFunction<chgCapitalPlus>(), CHGCAPITALPLUS);
	admin.registerAtomic(NewAtomicFunction<chgCapitalMinus>(), CHGCAPITALMINUS);
	admin.registerAtomic(NewAtomicFunction<LaborProductivityTot>(), LABORPRODUCTIVITYTOT);
	admin.registerAtomic(NewAtomicFunction<WageRateTot>(), WAGERATETOT);
	admin.registerAtomic(NewAtomicFunction<DebtTot>(), DEBTTOT);
	admin.registerAtomic(NewAtomicFunction<PopulationTot>(), POPULATIONTOT);
	admin.registerAtomic(NewAtomicFunction<CapitalTot>(), CAPITALTOT);
	//
}