! Weighted boundary quality scoring example.
! Compile: gfortran weighted_boundary_scoring.f90 -o weighted_boundary_scoring
! Run: ./weighted_boundary_scoring

program weighted_boundary_scoring
  implicit none

  real :: problem(3), system_context(3), stakeholder(3), causal(3), temporal(3)
  real :: institutional(3), evidence(3), ethical(3), revision(3), actionability(3)
  real :: quality(3)
  character(len=4) :: ids(3)
  integer :: i

  ids = (/"B001", "B003", "B005"/)

  problem = (/0.62, 0.82, 0.84/)
  system_context = (/0.38, 0.90, 0.86/)
  stakeholder = (/0.34, 0.72, 0.82/)
  causal = (/0.42, 0.88, 0.82/)
  temporal = (/0.38, 0.76, 0.84/)
  institutional = (/0.50, 0.78, 0.80/)
  evidence = (/0.40, 0.74, 0.86/)
  ethical = (/0.32, 0.70, 0.84/)
  revision = (/0.38, 0.72, 0.90/)
  actionability = (/0.82, 0.58, 0.66/)

  do i = 1, 3
     quality(i) = 0.12 * problem(i) + 0.13 * system_context(i) + &
                  0.14 * stakeholder(i) + 0.14 * causal(i) + &
                  0.12 * temporal(i) + 0.11 * institutional(i) + &
                  0.11 * evidence(i) + 0.10 * ethical(i) + &
                  0.09 * revision(i) + 0.04 * actionability(i)
  end do

  print *, "Boundary quality scores"
  do i = 1, 3
     print *, trim(ids(i)), quality(i)
  end do
end program weighted_boundary_scoring
