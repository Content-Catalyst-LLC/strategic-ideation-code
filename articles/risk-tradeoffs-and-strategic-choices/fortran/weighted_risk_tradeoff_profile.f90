! Weighted risk and tradeoff profile example.
! Compile: gfortran weighted_risk_tradeoff_profile.f90 -o weighted_risk_tradeoff_profile
! Run: ./weighted_risk_tradeoff_profile

program weighted_risk_tradeoff_profile
  implicit none

  real :: short_return(3), resilience(3), flexibility(3), legitimacy(3)
  real :: opportunity_value(3), exposure(3), reversibility(3), ethical_resilience(3), learning_value(3)
  real :: tradeoff_score(3), fragility_warning(3)
  character(len=42) :: names(3)
  integer :: i

  names = (/"Efficiency-Optimized Option          ", "Balanced Strategic Option             ", "Resilience-First Option               "/)

  short_return = (/0.86, 0.71, 0.58/)
  resilience = (/0.32, 0.74, 0.88/)
  flexibility = (/0.36, 0.76, 0.79/)
  legitimacy = (/0.48, 0.72, 0.81/)
  opportunity_value = (/0.34, 0.70, 0.76/)
  exposure = (/0.74, 0.46, 0.34/)
  reversibility = (/0.30, 0.68, 0.72/)
  ethical_resilience = (/0.42, 0.70, 0.82/)
  learning_value = (/0.34, 0.72, 0.70/)

  do i = 1, 3
     tradeoff_score(i) = 0.18 * short_return(i) + &
                         0.20 * resilience(i) + &
                         0.16 * flexibility(i) + &
                         0.14 * legitimacy(i) + &
                         0.14 * opportunity_value(i) - &
                         0.18 * exposure(i) + &
                         0.08 * reversibility(i) + &
                         0.08 * ethical_resilience(i) + &
                         0.08 * learning_value(i)

     fragility_warning(i) = 0.26 * exposure(i) + &
                            0.18 * (1.0 - resilience(i)) + &
                            0.14 * (1.0 - flexibility(i)) + &
                            0.12 * (1.0 - legitimacy(i)) + &
                            0.12 * (1.0 - opportunity_value(i)) + &
                            0.10 * (1.0 - reversibility(i)) + &
                            0.08 * (1.0 - ethical_resilience(i))
  end do

  print *, "Risk and tradeoff profiles"
  do i = 1, 3
     print *, trim(names(i)), tradeoff_score(i), fragility_warning(i)
  end do
end program weighted_risk_tradeoff_profile
