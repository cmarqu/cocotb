##############
Running cocotb
##############

cocotb is run by makefiles which are provided for a variety of simulators in :file:`cocotb/makefiles/simulators`.
The common makefile :file:`cocotb/makefiles/Makefile.sim` includes the appropriate simulator makefile based on the contents of the ``SIM`` variable.

Makefiles define two targets, ``sim`` and ``regression``, the default target is ``sim``.

Both targets create a results file in the calling directory called :file:`results.xml`.
This file is a JUnit-compatible output file suitable for use with e.g. `Jenkins <https://jenkins.io/>`_.
The ``sim`` target unconditionally re-runs the simulator whereas the ``regression`` target only re-builds if any dependencies have changed.

Typically the makefiles provided with cocotb for various simulators use a separate ``compile`` and ``run`` target.
This allows for a rapid re-running of a simulator if none of the HDL source files have changed and therefore the simulator does not need to recompile the HDL.

See also :doc:`/reference_makevars` and :doc:`reference_envvars`.
