##############
Make Variables
##############

.. glossary::

    ``GUI``
      Set this to 1 to enable the GUI mode in the simulator (if supported).

    ``SIM``
      Selects which simulator Makefile to use.  Attempts to include a simulator specific makefile from :file:`cocotb/makefiles/makefile.$(SIM)`

    ``VERILOG_SOURCES``
      A list of the Verilog source files to include.

    ``VHDL_SOURCES``
      A list of the VHDL source files to include.

    ``VHDL_SOURCES_lib``
      A list of the VHDL source files to include in the VHDL library *lib* (currently GHDL only).

    ``COMPILE_ARGS``
      Any arguments or flags to pass to the compile stage of the simulation.

    ``SIM_ARGS``
      Any arguments or flags to pass to the execution of the compiled simulation.

    ``EXTRA_ARGS``
      Passed to both the compile and execute phases of simulators with two rules, or passed to the single compile and run command for simulators which don't have a distinct compilation stage.

    ``CUSTOM_COMPILE_DEPS``
      Use to add additional dependencies to the compilation target; useful for defining additional rules to run pre-compilation or if the compilation phase depends on files other than the RTL sources listed in :term:`VERILOG_SOURCES` or :term:`VHDL_SOURCES`.

    ``CUSTOM_SIM_DEPS``
      Use to add additional dependencies to the simulation target.

    ``COCOTB_NVC_TRACE``
      Set this to 1 to enable display of VHPI traces when using the nvc VHDL simulator.

    ``SIM_BUILD``
      Use to define a scratch directory for use by the simulator. The path is relative to the Makefile location.
      If not provided, the default scratch directory is :file:`sim_build`.

