! Weighted lateral thinking profile scoring example.
! Compile: gfortran weighted_lateral_scoring.f90 -o weighted_lateral_scoring
! Run: ./weighted_lateral_scoring

program weighted_lateral_scoring
  implicit none

  real :: rigidity(3), provocation(3), analogy(3), random_entry(3), reversal(3)
  real :: challenge(3), convergence(3), systems(3), legitimacy(3), political(3)
  real :: transformation(3), score(3)
  character(len=5) :: ids(3)
  integer :: i

  ids = (/"LT001", "LT004", "LT008"/)
  rigidity = (/0.86, 0.36, 0.52/)
  provocation = (/0.18, 0.74, 0.78/)
  analogy = (/0.21, 0.76, 0.68/)
  random_entry = (/0.16, 0.70, 0.72/)
  reversal = (/0.20, 0.78, 0.70/)
  challenge = (/0.28, 0.80, 0.46/)
  convergence = (/0.72, 0.82, 0.28/)
  systems = (/0.44, 0.86, 0.34/)
  legitimacy = (/0.50, 0.78, 0.36/)
  political = (/0.48, 0.74, 0.40/)
  transformation = (/0.24, 0.88, 0.62/)

  do i = 1, 3
     score(i) = -0.14 * rigidity(i) + 0.14 * provocation(i) + &
                0.12 * analogy(i) + 0.09 * random_entry(i) + &
                0.10 * reversal(i) + 0.10 * challenge(i) + &
                0.14 * convergence(i) + 0.12 * systems(i) + &
                0.08 * legitimacy(i) + 0.07 * political(i) + &
                0.14 * transformation(i)
  end do

  print *, "Lateral thinking profile scores"
  do i = 1, 3
     print *, trim(ids(i)), score(i)
  end do
end program weighted_lateral_scoring
