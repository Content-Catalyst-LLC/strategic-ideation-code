! Weighted strategic portfolio profile example.
! Compile: gfortran weighted_portfolio_profile.f90 -o weighted_portfolio_profile
! Run: ./weighted_portfolio_profile

program weighted_portfolio_profile
  implicit none

  real :: impact(3), risk(3), learning(3), option_value(3), strategic_fit(3)
  real :: capacity_demand(3), ethical_resilience(3), contribution(3), overload(3)
  character(len=42) :: names(3)
  integer :: i

  names = (/"Core Process Improvement             ", "Exploratory Market Experiment        ", "Transformational Strategic Bet       "/)

  impact = (/0.68, 0.58, 0.88/)
  risk = (/0.32, 0.56, 0.78/)
  learning = (/0.38, 0.84, 0.70/)
  option_value = (/0.34, 0.76, 0.62/)
  strategic_fit = (/0.72, 0.62, 0.70/)
  capacity_demand = (/0.44, 0.38, 0.86/)
  ethical_resilience = (/0.58, 0.62, 0.48/)

  do i = 1, 3
     contribution(i) = 0.18 * impact(i) + &
                       0.18 * strategic_fit(i) + &
                       0.16 * learning(i) + &
                       0.16 * option_value(i) + &
                       0.14 * ethical_resilience(i) - &
                       0.10 * risk(i) - &
                       0.08 * capacity_demand(i)

     overload(i) = 0.34 * capacity_demand(i) + &
                   0.24 * risk(i) + &
                   0.16 * (1.0 - strategic_fit(i)) + &
                   0.14 * (1.0 - ethical_resilience(i)) + &
                   0.12 * (1.0 - option_value(i))
  end do

  print *, "Strategic portfolio profiles"
  do i = 1, 3
     print *, trim(names(i)), contribution(i), overload(i)
  end do
end program weighted_portfolio_profile
