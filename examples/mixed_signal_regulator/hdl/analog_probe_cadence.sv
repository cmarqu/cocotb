module analog_probe_cadence;

  var string hierarchy_to_probe = "";

  logic probe_voltage_toggle = 0;
  real voltage;
  
  logic probe_current_toggle = 0;
  real current;
  
  logic probe_power_toggle = 0;
  real power;
  
  always @(probe_voltage_toggle) begin: probe_voltage
    if ($cds_analog_is_valid(hierarchy_to_probe, "potential")) begin
      voltage = $cds_get_analog_value(hierarchy_to_probe, "potential");
    end else begin
      $display("%m: hierarchy_to_probe=%s is not valid, returning 0.0", hierarchy_to_probe);
      voltage = 0.0;
    end
  end

  always @(probe_current_toggle) begin: probe_current
    if ($cds_analog_is_valid(hierarchy_to_probe, "flow")) begin
      current = $cds_get_analog_value(hierarchy_to_probe, "flow");
    end else begin
      $display("%m: hierarchy_to_probe=%s is not valid, returning 0.0", hierarchy_to_probe);
      current = 0.0;
    end
  end

  always @(probe_power_toggle) begin: probe_power
    if ($cds_analog_is_valid(hierarchy_to_probe, "pwr")) begin
      power = $cds_get_analog_value(hierarchy_to_probe, "pwr");
    end else begin
      $display("%m: hierarchy_to_probe=%s is not valid, returning 0.0", hierarchy_to_probe);
      power = 0.0;
    end
  end

// The syntax of the cds_get_analog_value function is the following: 
//     real $cds_get_analog_value(hierarchical_name [, optional index[, optional quantity qualifier]])
// where: 
// The index can be variable, reg, or parameters so long as their value evaluates to an integer constant
// The quantity qualifier can be potential, flow, pwr, or param. If none is specified, potential is assumed
// 
// Note: It is possible to check whether the object referred to by hierarchical_name meets these conditions by using the
// helper functions cds_analog_is_valid, cds_analog_exists, and cds_analog_get_width. These helper functions enable the
// user to create reusable testbenches where the representation of the model containing the object that the value fetch
// routine points to can change from digital to analog or vice versa.
// 
// The value fetch routine can be called from within Verilog, SystemVerilog, or Verilog-AMS.  The fetch routine needs to
// reference an analog object. It can reference into any analog language including Verilog-AMS, VHDL-AMS, Spectre®, SPICE,
// or Verilog-A (compiled as Verilog-AMS or included by ahdl_include).

endmodule
