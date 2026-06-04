! Weighted mental-model scoring example.
! Compile: gfortran weighted_model_scoring.f90 -o weighted_model_scoring
! Run: ./weighted_model_scoring

program weighted_model_scoring
  implicit none

  real :: systems(3), probability(3), flexibility(3), plurality(3), revision(3)
  real :: embedding(3), ethics(3), stakeholder(3), evidence(3), score(3)
  character(len=4) :: ids(3)
  integer :: i

  ids = (/"M001", "M003", "M010"/)
  systems = (/0.24, 0.89, 0.82/)
  probability = (/0.21, 0.84, 0.67/)
  flexibility = (/0.19, 0.88, 0.78/)
  plurality = (/0.22, 0.86, 0.84/)
  revision = (/0.22, 0.87, 0.79/)
  embedding = (/0.58, 0.71, 0.52/)
  ethics = (/0.31, 0.82, 0.93/)
  stakeholder = (/0.28, 0.80, 0.94/)
  evidence = (/0.34, 0.86, 0.78/)

  do i = 1, 3
     score(i) = 0.17 * systems(i) + 0.13 * probability(i) + &
                0.16 * flexibility(i) + 0.14 * plurality(i) + &
                0.16 * revision(i) - 0.08 * embedding(i) + &
                0.12 * ethics(i) + 0.10 * stakeholder(i) + &
                0.10 * evidence(i)
  end do

  print *, "Strategic mental-model scores"
  do i = 1, 3
     print *, trim(ids(i)), score(i)
  end do
end program weighted_model_scoring
