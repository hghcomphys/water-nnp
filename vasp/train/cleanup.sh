rm -f CHG* CONTCAR* DOSCAR* DYNMAT EIGENVAL IBZKPT OPTIC OSZICAR* PROCAR* \
      PCDAT W* XDATCAR* PARCHG* vasprun.xml SUMMARY.* REPORT \
      wannier90.win wannier90_band.gnu wannier90_band.kpt wannier90.chk wannier90.wout \
      *.dat plotfile p4vasp.log \
      *.e[0-9]* *.o[0-9]* *.pe[0-9]* *.po[0-9]* *.err *.out \
	  stdout stderr WAVECAR XDATCAR IBZKPT CONTCAR IBZKPT DOSCAR EIGENVAL PCDAT

rm -f cleanup.sh submit_vasp.sh INCAR KPOINTS POTCAR submit_vasp.sh vdw_kernel.bindat
