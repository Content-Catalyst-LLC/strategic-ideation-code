! Weighted strategic hypothesis scoring example.
! Compile: gfortran weighted_hypothesis_scoring.f90 -o weighted_hypothesis_scoring
! Run: ./weighted_hypothesis_scoring

program weighted_hypothesis_scoring
  implicit none

  real :: explanatory(3), testability(3), evidence(3), relevance(3), stakeholder(3)
  real :: systems(3), actionability(3), risk(3), reversibility(3), score(3)
  character(len=4) :: ids(3)
  integer :: i

  ids = (/"H001", "H004", "H010"/)
  explanatory = (/0.82, 0.84, 0.88/)
  testability = (/0.74, 0.70, 0.68/)
  evidence = (/0.68, 0.66, 0.72/)
  relevance = (/0.86, 0.86, 0.90/)
  stakeholder = (/0.72, 0.92, 0.66/)
  systems = (/0.76, 0.78, 0.86/)
  actionability = (/0.72, 0.64, 0.62/)
  risk = (/0.52, 0.58, 0.66/)
  reversibility = (/0.74, 0.66, 0.58/)

  do i = 1, 3
     score(i) = 0.16 * explanatory(i) + 0.14 * testability(i) + &
                0.14 * evidence(i) + 0.16 * relevance(i) + &
                0.12 * stakeholder(i) + 0.12 * systems(i) + &
                0.10 * actionability(i) + 0.06 * reversibility(i) - &
                0.10 * risk(i)
  end do

  print *, "Strategic hypothesis scores"
  do i = 1, 3
     print *, trim(ids(i)), score(i)
  end do
end program weighted_hypothesis_scoring
