! Weighted scoring example for strategic ideation.
! Compile: gfortran weighted_scoring.f90 -o weighted_scoring
! Run: ./weighted_scoring

program weighted_scoring
  implicit none

  real :: strategic_fit(3), feasibility(3), leverage(3), learning(3), uncertainty(3)
  real :: score(3)
  character(len=4) :: ids(3)
  integer :: i

  ids = (/"I001", "I004", "I008"/)
  strategic_fit = (/0.91, 0.78, 0.86/)
  feasibility = (/0.82, 0.76, 0.70/)
  leverage = (/0.74, 0.65, 0.89/)
  learning = (/0.88, 0.95, 0.88/)
  uncertainty = (/0.24, 0.28, 0.37/)

  do i = 1, 3
     score(i) = 0.28 * strategic_fit(i) + 0.18 * feasibility(i) + &
                0.24 * leverage(i) + 0.18 * learning(i) - &
                0.12 * uncertainty(i)
  end do

  print *, "Strategic ideation weighted scores"
  do i = 1, 3
     print *, trim(ids(i)), score(i)
  end do
end program weighted_scoring
