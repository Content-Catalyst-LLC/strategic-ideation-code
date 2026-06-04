! Weighted systems-ideation scoring example.
! Compile: gfortran weighted_systems_scoring.f90 -o weighted_systems_scoring
! Run: ./weighted_systems_scoring

program weighted_systems_scoring
  implicit none

  real :: feedback(3), leverage(3), root_cause(3), stakeholder(3), boundary(3)
  real :: stock_flow(3), delay(3), learning(3), consequence_risk(3), local_risk(3), score(3)
  character(len=6) :: ids(3)
  integer :: i

  ids = (/"SYS001", "SYS003", "SYS005"/)
  feedback = (/0.24, 0.86, 0.78/)
  leverage = (/0.21, 0.91, 0.76/)
  root_cause = (/0.31, 0.88, 0.80/)
  stakeholder = (/0.28, 0.70, 0.90/)
  boundary = (/0.34, 0.78, 0.86/)
  stock_flow = (/0.30, 0.82, 0.74/)
  delay = (/0.26, 0.76, 0.72/)
  learning = (/0.29, 0.83, 0.82/)
  consequence_risk = (/0.79, 0.36, 0.34/)
  local_risk = (/0.76, 0.32, 0.30/)

  do i = 1, 3
     score(i) = 0.14 * feedback(i) + 0.14 * leverage(i) + &
                0.13 * root_cause(i) + 0.12 * stakeholder(i) + &
                0.12 * boundary(i) + 0.10 * stock_flow(i) + &
                0.10 * delay(i) + 0.13 * learning(i) - &
                0.10 * consequence_risk(i) - 0.08 * local_risk(i)
  end do

  print *, "Systems-ideation scores"
  do i = 1, 3
     print *, trim(ids(i)), score(i)
  end do
end program weighted_systems_scoring
