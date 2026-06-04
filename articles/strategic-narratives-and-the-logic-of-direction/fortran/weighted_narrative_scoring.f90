! Weighted strategic narrative coherence scoring example.
! Compile: gfortran weighted_narrative_scoring.f90 -o weighted_narrative_scoring
! Run: ./weighted_narrative_scoring

program weighted_narrative_scoring
  implicit none

  real :: diagnosis(3), purpose(3), choice(3), sequence(3), role(3)
  real :: future(3), accountability(3), evidence(3), stakeholder(3), ethics(3), score(3)
  character(len=5) :: ids(3)
  integer :: i

  ids = (/"SN001", "SN003", "SN006"/)
  diagnosis = (/0.32, 0.86, 0.72/)
  purpose = (/0.44, 0.82, 0.80/)
  choice = (/0.28, 0.76, 0.69/)
  sequence = (/0.30, 0.84, 0.67/)
  role = (/0.36, 0.78, 0.76/)
  future = (/0.42, 0.80, 0.78/)
  accountability = (/0.25, 0.82, 0.73/)
  evidence = (/0.34, 0.84, 0.76/)
  stakeholder = (/0.38, 0.78, 0.91/)
  ethics = (/0.35, 0.81, 0.89/)

  do i = 1, 3
     score(i) = 0.14 * diagnosis(i) + 0.12 * purpose(i) + &
                0.14 * choice(i) + 0.12 * sequence(i) + &
                0.11 * role(i) + 0.10 * future(i) + &
                0.11 * accountability(i) + 0.08 * evidence(i) + &
                0.05 * stakeholder(i) + 0.03 * ethics(i)
  end do

  print *, "Strategic narrative coherence scores"
  do i = 1, 3
     print *, trim(ids(i)), score(i)
  end do
end program weighted_narrative_scoring
