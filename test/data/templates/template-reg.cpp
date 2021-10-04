#include "pmodeladm.h"
#include "register.h"
#include "tuple_to_real.h"
{% for atomic_name in atomics_names -%}
#include "{{atomic_name}}.h"
{% endfor -%}

// Registro modelos atomicos
void register_atomics_on(ParallelModelAdmin &admin)
{
	// Atomicos base
	//admin.registerAtomic(NewAtomicFunction<QSS1>(), QSS_MODEL_NAME);
	admin.registerAtomic(NewAtomicFunction<tuple2real>(), TUPLE2REAL);
	// Atomicos especificos del modelo
	{% for atomic_name in atomics_names -%}
	admin.registerAtomic(NewAtomicFunction<{{atomic_name}}>(), {{atomic_name.upper()}});
	{% endfor %}
}
