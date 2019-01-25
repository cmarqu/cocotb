import cds_rnm_pkg::*;
nettype wreal1driver voltage_net;

module mixed_signal_regulator;

  voltage_net vdd, vss, node1;
  real vdd_val, vss_val = 0.0;
  logic signed [3:0] trim_val = 0;
  
  assign vdd = vdd_val;
  assign vss = vss_val;

  regulator 
    #(.vout_abs  (3.3),
      .trim_step (0.2))
  i_regulator
    (
     .vdd  (vdd),
     .trim (trim_val),
     .vout (node1),
     .vss  (vss)
     );

  resistor 
    #(.resistance (100))
  i_resistor
    (
     .p (node1),
     .n (vss)
     );

  analog_probe_cadence i_analog_probe ();

endmodule
