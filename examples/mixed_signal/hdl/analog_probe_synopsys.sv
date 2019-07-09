module analog_probe;

  var string node_to_probe = "";

  logic probe_voltage_toggle = 0;
  real voltage;

  always @(probe_voltage_toggle) begin: probe_voltage
    voltage = $snps_get_volt(node_to_probe);
  end

  logic probe_current_toggle = 0;
  real current;

  always @(probe_current_toggle) begin: probe_current
    current = $snps_get_port_current(node_to_probe);
  end

// also useful:
// $snps_force_volt(node, val) 
// $snps_release_volt(node)

endmodule
