! Weighted strategic creativity scoring example.
! Compile: gfortran weighted_creativity_scoring.f90 -o weighted_creativity_scoring
! Run: ./weighted_creativity_scoring

program weighted_creativity_scoring
  implicit none

  real :: novelty(3), relevance(3), coherence(3), mechanism(3), testability(3)
  real :: stakeholder(3), systems(3), development(3), risk(3), revision(3), score(3)
  character(len=4) :: ids(3)
  integer :: i

  ids = (/"I002", "I005", "I009"/)
  novelty = (/0.72, 0.76, 0.70/)
  relevance = (/0.86, 0.88, 0.50/)
  coherence = (/0.78, 0.82, 0.52/)
  mechanism = (/0.80, 0.84, 0.34/)
  testability = (/0.70, 0.66, 0.46/)
  stakeholder = (/0.92, 0.70, 0.30/)
  systems = (/0.78, 0.90, 0.32/)
  development = (/0.82, 0.86, 0.42/)
  risk = (/0.56, 0.66, 0.40/)
  revision = (/0.82, 0.86, 0.38/)

  do i = 1, 3
     score(i) = 0.14 * novelty(i) + 0.16 * relevance(i) + &
                0.13 * coherence(i) + 0.14 * mechanism(i) + &
                0.11 * testability(i) + 0.13 * stakeholder(i) + &
                0.13 * systems(i) + 0.12 * development(i) + &
                0.08 * revision(i) - 0.12 * risk(i)
  end do

  print *, "Strategic creativity scores"
  do i = 1, 3
     print *, trim(ids(i)), score(i)
  end do
end program weighted_creativity_scoring
