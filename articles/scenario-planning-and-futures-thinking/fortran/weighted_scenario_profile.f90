! Weighted scenario robustness profile example.
! Compile: gfortran weighted_scenario_profile.f90 -o weighted_scenario_profile
! Run: ./weighted_scenario_profile

program weighted_scenario_profile
  implicit none

  real :: values(3, 5)
  real :: flexibility(3), implementation_readiness(3), ethical_resilience(3), option_value(3)
  real :: mean_value(3), worst_case(3), robustness(3)
  character(len=32) :: names(3)
  integer :: i

  names = (/"Short-Term Optimization Strategy ", "Balanced Adaptive Strategy      ", "Resilience-Oriented Strategy   "/)

  values(1, :) = (/0.84, 0.41, 0.36, 0.48, 0.38/)
  values(2, :) = (/0.74, 0.71, 0.67, 0.70, 0.66/)
  values(3, :) = (/0.68, 0.75, 0.79, 0.73, 0.76/)

  flexibility = (/0.28, 0.73, 0.82/)
  implementation_readiness = (/0.86, 0.74, 0.66/)
  ethical_resilience = (/0.42, 0.68, 0.76/)
  option_value = (/0.30, 0.72, 0.78/)

  do i = 1, 3
     mean_value(i) = sum(values(i, :)) / 5.0
     worst_case(i) = minval(values(i, :))
     robustness(i) = 0.30 * worst_case(i) + &
                     0.24 * mean_value(i) + &
                     0.16 * flexibility(i) + &
                     0.12 * implementation_readiness(i) + &
                     0.10 * ethical_resilience(i) + &
                     0.10 * option_value(i)
  end do

  print *, "Scenario robustness profiles"
  do i = 1, 3
     print *, trim(names(i)), mean_value(i), worst_case(i), robustness(i)
  end do
end program weighted_scenario_profile
