#ifndef _{{pulse_name_upper}}_H_
#define _{{pulse_name_upper}}_H_

#include <random>

#include "atomic.h"
#include "VTime.h"


#define {{pulse_name_upper}} "{{pulse_name_lower}}"


class {{pulse_name_lower}} : public Atomic {
  public:
    
    {{pulse_name_lower}}(const string &name = {{pulse_name_upper}} );
    virtual string className() const {  return {{pulse_name_upper}} ;}
  
  protected:
    Model &initFunction();
    Model &externalFunction( const ExternalMessage & );
    Model &internalFunction( const InternalMessage & );
    Model &outputFunction( const CollectMessage & );

  private:
    Port &out;

    VTime interval_time;

    double dt = 1. / {{dt}};
    VTime pulse_time;
    
    bool pulse_on, interval_pulse_on;

    std::uniform_int_distribution<int> dist;
    std::mt19937 rng;

    // Agregados (volume + iterval)
    // TODO : volume y interval tienen que venir con el nombre de la variable + a que variable corresponde (volume o interval)
    {% if volume_param != None -%}
    double volume = {{volume_param}};
    bool isSet_volume;
    {% endif -%}
    {% if interval_param != None -%}
    double interval;
    bool isSet_interval;
    {% endif -%}

    const Port &in_port_{{firstPulse_input}};
    double firstPulse;
    bool isSet_firstPulse;
    bool firstTime;
    
    {% if volume_input != None -%}
    const Port &in_port_{{volume_input}};
    double {{volume_input}};
    bool isSet_volume;
    {% endif -%}
    {% if interval_input != None -%}
    const Port &in_port_{{interval_input}};
    double {{interval_input}};
    bool isSet_interval;
    {% endif -%}

    {% for output_port_name in output_ports %}
    Port &out_port_{{output_port_name}};
    {% endfor %}
};

#endif
