import nettypes_pkg::*;

module rescap(input  voltage_net vdd, 
              output voltage_net vout,
              input  voltage_net vss);

  resistor 
    #(.resistance (1e5))
  i_resistor
    (
     .p (vdd),
     .n (vout)
     );

  capacitor 
    #(.capacitance (1e-12))
  i_capacitor
    (
     .p (vout),
     .n (vss)
     );
  
endmodule
