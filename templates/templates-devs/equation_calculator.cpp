#include <string>
#include <map>
#include <vector>
#include "equation_calculator.h"
#include <assert.h>


double EquationCalculator::calculate(std::vector<double> values) {
	double res = 0;

	if (agregation_type and calculation_type == "SUM") {
		// Recorro los indices seleccionados, y los uso en la agregacion
		for(int i=0; i<selected_indices.size(); i++) {
			res += values[i];
		}
	}
	else {
		// No hay agregacion. Es de la forma var[1,2]
		return values[selected_indices[0]];
	}


	return res;
}