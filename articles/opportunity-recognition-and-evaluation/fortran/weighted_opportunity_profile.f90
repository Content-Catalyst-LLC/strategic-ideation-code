! Weighted opportunity profile example.
! Compile: gfortran weighted_opportunity_profile.f90 -o weighted_opportunity_profile
! Run: ./weighted_opportunity_profile

program weighted_opportunity_profile
  implicit none

  real :: signal(3), capability(3), desirability(3), viability(3), timing(3)
  real :: learning(3), option_value(3), strategic_fit(3), ethics(3), risk(3), confidence(3), score(3)
  character(len=45) :: names(3)
  integer :: i

  names = (/"Emerging Technology Adjacency          ", "High-Hype Weak-Fit Opportunity        ", "Slow-Build Sustainability Opportunity "/)

  signal = (/0.74, 0.86, 0.62/)
  capability = (/0.78, 0.31, 0.73/)
  desirability = (/0.72, 0.77, 0.81/)
  viability = (/0.71, 0.39, 0.74/)
  timing = (/0.76, 0.48, 0.67/)
  learning = (/0.70, 0.62, 0.64/)
  option_value = (/0.66, 0.44, 0.72/)
  strategic_fit = (/0.78, 0.40, 0.76/)
  ethics = (/0.62, 0.42, 0.82/)
  risk = (/0.46, 0.78, 0.41/)
  confidence = (/0.68, 0.38, 0.66/)

  do i = 1, 3
     score(i) = 0.13 * signal(i) + &
                0.14 * capability(i) + &
                0.12 * desirability(i) + &
                0.12 * viability(i) + &
                0.10 * timing(i) + &
                0.12 * learning(i) + &
                0.11 * option_value(i) + &
                0.10 * strategic_fit(i) + &
                0.10 * ethics(i) - &
                0.14 * risk(i)
  end do

  print *, "Weighted opportunity profile scores"
  do i = 1, 3
     print *, trim(names(i)), score(i), score(i) * confidence(i)
  end do
end program weighted_opportunity_profile
