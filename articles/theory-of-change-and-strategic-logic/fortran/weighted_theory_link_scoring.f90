! Weighted theory-of-change link risk scoring example.
! Compile: gfortran weighted_theory_link_scoring.f90 -o weighted_theory_link_scoring
! Run: ./weighted_theory_link_scoring

program weighted_theory_link_scoring
  implicit none

  real :: mechanism(3), evidence(3), actor(3), capacity(3), system_dep(3)
  real :: ethical(3), consequence(3), testability(3), risk(3), priority(3)
  character(len=4) :: ids(3)
  integer :: i

  ids = (/"L002", "L004", "L009"/)

  mechanism = (/0.66, 0.72, 0.48/)
  evidence = (/0.38, 0.44, 0.32/)
  actor = (/0.86, 0.82, 0.62/)
  capacity = (/0.62, 0.58, 0.48/)
  system_dep = (/0.58, 0.68, 0.64/)
  ethical = (/0.52, 0.90, 0.60/)
  consequence = (/0.80, 0.86, 0.78/)
  testability = (/0.78, 0.74, 0.58/)

  do i = 1, 3
     risk(i) = 0.16 * (1.0 - mechanism(i)) + &
               0.18 * (1.0 - evidence(i)) + &
               0.13 * actor(i) + &
               0.11 * capacity(i) + &
               0.14 * system_dep(i) + &
               0.12 * ethical(i) + &
               0.16 * consequence(i)

     priority(i) = risk(i) * testability(i)
  end do

  print *, "Theory-of-change link risk and test priority"
  do i = 1, 3
     print *, trim(ids(i)), risk(i), priority(i)
  end do
end program weighted_theory_link_scoring
