#ifndef EQUATIONCALCULATOR_H
#define EQUATIONCALCULATOR_H

#include <string>
#include <map>
#include <vector>
#include <algorithm>
#include <iostream>
#include <regex>

using namespace std;


class EquationCalculator
{
	string calculation_type;
	bool agregation_type;
	string equation;
	vector<int> dimension_size;
	vector<int> selected_indices;

public:

	EquationCalculator(){}

	EquationCalculator(string e, map<int,int> m){
		
		vector<pair<int,int>> dimension_size_pairs;
		for(map<int,int>::iterator it = m.begin(); it != m.end(); ++it) {
			dimension_size_pairs.push_back(*it);
		}
		// Ordeno por primer elemento (que es el id de la dimension; el segundo es el size)
		sort(dimension_size_pairs.begin(), dimension_size_pairs.end());
		for(int i=0; i<dimension_size_pairs.size(); i++) {
			dimension_size.push_back(dimension_size_pairs[i].second);
		}

		/* Parse equation and set local variables accordingly
		Casos: (siempre asumimos que solo vienen variables de un unico 'DEVSArrayCollector')
		1. SUM(converter[*,*,*]) 
		2. PROD(converter[*,1,*])
		3. MEAN(converter[1,*,2])
		4. converter[1,2,1]
		*/

		// =================================================================================== //
		equation = e;
		// 1. Parsear. Detectar si hay algun 'SUM', 'PROD', 'MEAN'
		// 2. obtener para cada dimension, si hay un '*' o un valor
		// 3. Recorrer el vector 'values', acumulando y haciendo la operacion 
		//    deseada sobre los valores que correspondan
		// TODO: setear 'calculation_type', segun el cual 'calculate' va a hacer cosas distintas

		int n_values = 1;
		for(int i=0; i<dimension_size.size(); i++) {
			n_values *= dimension_size[i];
		}

		// TODO: por ahora la unica funcion de agregacion es 'SUM'
		calculation_type = "SUM";
		if (equation.find("SUM") != std::string::npos) {
		    agregation_type = true;
		} else {
			agregation_type = false;
		}

		if(agregation_type) {
			// TODO: ahora, AGREGO TODOS LOS INDICES SI ES AGREGACION
			for(int i=0; i<n_values; i++) {
				selected_indices.push_back(i);
			}
		} else {

			smatch matches;
			std::regex rgx("\\[[\\*\\d+][,\\*\\d+]*\\]");
			 if (std::regex_search(equation, matches, rgx)) {
			 	// Recorro dimensiones de la ultima hasta la primera
		        for (size_t i = 0; i < matches.size(); i++) {
		        	// Get i'th dimension position
		        	std::string s = matches[i];
		        	s.erase(0, 1);
					s.erase(s.size() - 1);

					vector<int> positions;
					stringstream ss(s);
					string temp;
					while (std::getline(ss, temp, ',')) {
					    positions.push_back(std::stoi(temp) - 1);
					}

					int tot = 0, acum = 1;
					for(int j = positions.size() - 1; j >= 0; j--) {
						tot += positions[j] * acum;
						acum *= dimension_size[j];	
					}
		        	selected_indices.push_back(tot);
		        }
		    }
		}

	};

	double calculate(vector<double> c);
};


#endif