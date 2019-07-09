module rescap(input  vdd, 
              output vout,
              input  vss);

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
