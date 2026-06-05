! Weighted idea-to-strategy conversion profile example.
! Compile: gfortran weighted_strategy_conversion.f90 -o weighted_strategy_conversion
! Run: ./weighted_strategy_conversion

program weighted_strategy_conversion
  implicit none

  real :: feasibility(3), viability(3), desirability(3), integration_difficulty(3)
  real :: execution_readiness(3), strategic_fit(3), evidence_confidence(3), ethical_resilience(3), score(3)
  character(len=48) :: names(3)
  integer :: i

  names = (/"High-Idea Low-Execution Concept           ", "Balanced Strategic Initiative              ", "Integration-Challenged Initiative          "/)

  feasibility = (/0.78, 0.74, 0.69/)
  viability = (/0.38, 0.79, 0.71/)
  desirability = (/0.82, 0.77, 0.84/)
  integration_difficulty = (/0.72, 0.44, 0.83/)
  execution_readiness = (/0.29, 0.81, 0.52/)
  strategic_fit = (/0.62, 0.84, 0.76/)
  evidence_confidence = (/0.42, 0.76, 0.58/)
  ethical_resilience = (/0.54, 0.72, 0.60/)

  do i = 1, 3
     score(i) = 0.16 * feasibility(i) + &
                0.18 * viability(i) + &
                0.16 * desirability(i) - &
                0.12 * integration_difficulty(i) + &
                0.16 * execution_readiness(i) + &
                0.12 * strategic_fit(i) + &
                0.08 * evidence_confidence(i) + &
                0.06 * ethical_resilience(i)
  end do

  print *, "Weighted idea-to-strategy conversion scores"
  do i = 1, 3
     print *, trim(names(i)), score(i), score(i) * evidence_confidence(i)
  end do
end program weighted_strategy_conversion
