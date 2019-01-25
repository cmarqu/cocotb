import cds_rnm_pkg::*;
nettype wreal1driver voltage_net;

module mixed_signal;

  voltage_net vdd, gnd;
  real vdd_val, gnd_val = 0.0;
  
  assign vdd = vdd_val;
  assign gnd = gnd_val;

  wire node1;

  resistor 
    #(.resistance (1e5))
  i_resistor
    (
     .p (vdd),
     .n (node1)
     );

  capacitor 
    #(.capacitance (1e-12))
  i_capacitor
    (
     .p (node1),
     .n (gnd)
     );

  analog_probe_cadence i_analog_probe ();

endmodule
