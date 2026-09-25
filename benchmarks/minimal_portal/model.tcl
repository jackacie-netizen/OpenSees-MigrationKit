# Synthetic one-bay, one-storey elastic 2D portal frame.
# Reference artifact only: OpenSees-MigrationKit v0.1.0 does not execute Tcl.
model BasicBuilder -ndm 2 -ndf 3

node 1 0.0 0.0
node 2 4.0 0.0
node 3 0.0 3.0
node 4 4.0 3.0

fix 1 1 1 1
fix 2 1 1 1

geomTransf Linear 1
set A 0.02
set E 2.0e11
set Iz 8.0e-5

element elasticBeamColumn 1 1 3 $A $E $Iz 1
element elasticBeamColumn 2 2 4 $A $E $Iz 1
element elasticBeamColumn 3 3 4 $A $E $Iz 1
