! Weighted scoring example for strategic ideation.
! Compile: gfortran weighted_scoring.f90 -o weighted_scoring
! Run: ./weighted_scoring

program weighted_scoring
  implicit none

  real :: fit(3), feasibility(3), leverage(3), learning(3), ethics(3), reusability(3)
  real :: uncertainty(3), assumption_risk(3), score(3)
  character(len=4) :: ids(3)
  integer :: i

  ids = (/"I001", "I010", "I012"/)
  fit = (/0.91, 0.90, 0.85/)
  feasibility = (/0.82, 0.73, 0.64/)
  leverage = (/0.74, 0.80, 0.84/)
  learning = (/0.88, 0.87, 0.94/)
  ethics = (/0.86, 0.84, 0.88/)
  reusability = (/0.94, 0.88, 0.85/)
  uncertainty = (/0.24, 0.29, 0.39/)
  assumption_risk = (/0.29, 0.33, 0.44/)

  do i = 1, 3
     score(i) = 0.20 * fit(i) + 0.12 * feasibility(i) + &
                0.18 * leverage(i) + 0.13 * learning(i) + &
                0.16 * ethics(i) + 0.09 * reusability(i) - &
                0.07 * uncertainty(i) - 0.05 * assumption_risk(i)
  end do

  print *, "Strategic ideation weighted scores"
  do i = 1, 3
     print *, trim(ids(i)), score(i)
  end do
end program weighted_scoring
