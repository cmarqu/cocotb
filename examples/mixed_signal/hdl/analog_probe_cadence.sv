module analog_probe;

  var string node_to_probe = "<unassigned>";

  logic probe_voltage_toggle = 0;
  real voltage;

  always @(probe_voltage_toggle) begin: probe_voltage
    if ($cds_analog_is_valid(node_to_probe, "potential")) begin
      voltage = $cds_get_analog_value(node_to_probe, "potential");
    end else begin
      voltage = 0.123456;
      $display("%m: node_to_probe=%s is not valid, returning %f V", node_to_probe, voltage);
    end
  end

  logic probe_current_toggle = 0;
  real current;

  always @(probe_current_toggle) begin: probe_current
    if ($cds_analog_is_valid(node_to_probe, "flow")) begin
      current = $cds_get_analog_value(node_to_probe, "flow");
    end else begin
      current = 0.123456;
      $display("%m: node_to_probe=%s is not valid, returning %f A", node_to_probe, current);
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
