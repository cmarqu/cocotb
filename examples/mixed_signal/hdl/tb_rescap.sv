import nettypes_pkg::*;

module tb_rescap;

  voltage_net vdd, vss;
  real vdd_val, vss_val = 0.0;

  assign vdd = vdd_val;
  assign vss = vss_val;

  // the design
  rescap i_rescap (.vdd  (vdd),
                   .vout (vout),
                   .vss  (vss)
                   );

  // the "multimeter"
  analog_probe i_analog_probe ();

endmodule
