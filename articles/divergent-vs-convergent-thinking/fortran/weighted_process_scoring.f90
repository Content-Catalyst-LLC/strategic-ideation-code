! Weighted divergence-convergence process scoring example.
! Compile: gfortran weighted_process_scoring.f90 -o weighted_process_scoring
! Run: ./weighted_process_scoring

program weighted_process_scoring
  implicit none

  real :: exploration(3), evaluation(3), iteration(3), constraints(3)
  real :: inclusion(3), evidence(3), readiness(3), memory(3), score(3)
  character(len=5) :: ids(3)
  integer :: i

  ids = (/"DC001", "DC002", "DC004"/)
  exploration = (/0.28, 0.74, 0.79/)
  evaluation = (/0.86, 0.77, 0.72/)
  iteration = (/0.31, 0.76, 0.88/)
  constraints = (/0.71, 0.73, 0.69/)
  inclusion = (/0.34, 0.70, 0.76/)
  evidence = (/0.42, 0.74, 0.82/)
  readiness = (/0.79, 0.81, 0.77/)
  memory = (/0.38, 0.72, 0.80/)

  do i = 1, 3
     score(i) = 0.16 * exploration(i) + 0.16 * evaluation(i) + &
                0.18 * iteration(i) + 0.14 * constraints(i) + &
                0.12 * inclusion(i) + 0.12 * evidence(i) + &
                0.08 * readiness(i) + 0.04 * memory(i)
  end do

  print *, "Divergence-convergence process scores"
  do i = 1, 3
     print *, trim(ids(i)), score(i)
  end do
end program weighted_process_scoring
