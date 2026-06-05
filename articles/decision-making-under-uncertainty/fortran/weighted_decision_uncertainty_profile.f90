! Weighted decision profile under uncertainty example.
! Compile: gfortran weighted_decision_uncertainty_profile.f90 -o weighted_decision_uncertainty_profile
! Run: ./weighted_decision_uncertainty_profile

program weighted_decision_uncertainty_profile
  implicit none

  real :: expected_return(3), robustness(3), flexibility(3), information_quality(3)
  real :: exposure(3), option_value(3), reversibility(3), ethical_resilience(3), learning_value(3)
  real :: profile(3), fragility(3)
  character(len=40) :: names(3)
  integer :: i

  names = (/"High-Return Brittle Option       ", "Balanced Robust Option           ", "Exploratory Optionality Option   "/)

  expected_return = (/0.86, 0.72, 0.61/)
  robustness = (/0.28, 0.79, 0.71/)
  flexibility = (/0.31, 0.74, 0.88/)
  information_quality = (/0.63, 0.72, 0.49/)
  exposure = (/0.82, 0.44, 0.53/)
  option_value = (/0.26, 0.72, 0.86/)
  reversibility = (/0.22, 0.68, 0.82/)
  ethical_resilience = (/0.38, 0.68, 0.62/)
  learning_value = (/0.30, 0.70, 0.88/)

  do i = 1, 3
     profile(i) = 0.14 * expected_return(i) + &
                  0.18 * robustness(i) + &
                  0.16 * flexibility(i) + &
                  0.12 * information_quality(i) - &
                  0.16 * exposure(i) + &
                  0.14 * option_value(i) + &
                  0.10 * reversibility(i) + &
                  0.10 * ethical_resilience(i) + &
                  0.10 * learning_value(i)

     fragility(i) = 0.24 * exposure(i) + &
                    0.18 * (1.0 - robustness(i)) + &
                    0.14 * (1.0 - flexibility(i)) + &
                    0.13 * (1.0 - option_value(i)) + &
                    0.12 * (1.0 - reversibility(i)) + &
                    0.10 * (1.0 - ethical_resilience(i)) + &
                    0.09 * (1.0 - information_quality(i))
  end do

  print *, "Decision profiles under uncertainty"
  do i = 1, 3
     print *, trim(names(i)), profile(i), fragility(i)
  end do
end program weighted_decision_uncertainty_profile
