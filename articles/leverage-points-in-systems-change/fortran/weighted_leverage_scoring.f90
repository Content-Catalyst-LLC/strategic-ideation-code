! Weighted leverage-point scoring example.
! Compile: gfortran weighted_leverage_scoring.f90 -o weighted_leverage_scoring
! Run: ./weighted_leverage_scoring

program weighted_leverage_scoring
  implicit none

  real :: implementation_ease(3), structural_depth(3), system_sensitivity(3)
  real :: feedback_influence(3), information_effect(3), rule_power(3), goal_alignment(3)
  real :: paradigm_relevance(3), transformative_potential(3), legitimacy_requirement(3)
  real :: unintended_risk(3), learning_capacity(3), leverage_score(3), governance_need(3)
  character(len=4) :: ids(3)
  integer :: i

  ids = (/"L001", "L006", "L008"/)

  implementation_ease = (/0.86, 0.44, 0.21/)
  structural_depth = (/0.22, 0.82, 0.96/)
  system_sensitivity = (/0.28, 0.82, 0.88/)
  feedback_influence = (/0.28, 0.76, 0.82/)
  information_effect = (/0.31, 0.66, 0.60/)
  rule_power = (/0.20, 0.90, 0.78/)
  goal_alignment = (/0.28, 0.78, 0.96/)
  paradigm_relevance = (/0.16, 0.58, 0.98/)
  transformative_potential = (/0.24, 0.82, 0.96/)
  legitimacy_requirement = (/0.24, 0.72, 0.90/)
  unintended_risk = (/0.26, 0.70, 0.82/)
  learning_capacity = (/0.34, 0.70, 0.78/)

  do i = 1, 3
     leverage_score(i) = 0.06 * implementation_ease(i) + 0.16 * structural_depth(i) + &
                         0.14 * system_sensitivity(i) + 0.13 * feedback_influence(i) + &
                         0.11 * information_effect(i) + 0.13 * rule_power(i) + &
                         0.13 * goal_alignment(i) + 0.08 * paradigm_relevance(i) + &
                         0.14 * transformative_potential(i) + 0.08 * learning_capacity(i) - &
                         0.06 * unintended_risk(i)

     governance_need(i) = 0.26 * legitimacy_requirement(i) + 0.24 * unintended_risk(i) + &
                          0.22 * transformative_potential(i) + 0.14 * (1.0 - implementation_ease(i)) + &
                          0.14 * paradigm_relevance(i)
  end do

  print *, "Leverage scores and governance needs"
  do i = 1, 3
     print *, trim(ids(i)), leverage_score(i), governance_need(i)
  end do
end program weighted_leverage_scoring
