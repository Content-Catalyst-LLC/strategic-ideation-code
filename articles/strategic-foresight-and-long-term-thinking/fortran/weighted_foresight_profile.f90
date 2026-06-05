! Weighted strategic foresight profile example.
! Compile: gfortran weighted_foresight_profile.f90 -o weighted_foresight_profile
! Run: ./weighted_foresight_profile

program weighted_foresight_profile
  implicit none

  real :: short_term_return(3), foresight_depth(3), resilience(3), flexibility(3)
  real :: path_dependence_risk(3), signal_capacity(3), scenario_capacity(3), option_value(3)
  real :: ethics_review(3), governance_capacity(3), future_viability(3), short_term_bias(3)
  character(len=40) :: names(3)
  integer :: i

  names = (/"Short-Term Efficiency Strategy          ", "Balanced Foresight Strategy             ", "Resilience-Biased Long-Horizon Strategy "/)

  short_term_return = (/0.86, 0.72, 0.61/)
  foresight_depth = (/0.24, 0.79, 0.84/)
  resilience = (/0.32, 0.76, 0.88/)
  flexibility = (/0.28, 0.74, 0.79/)
  path_dependence_risk = (/0.71, 0.39, 0.34/)
  signal_capacity = (/0.30, 0.76, 0.80/)
  scenario_capacity = (/0.26, 0.74, 0.82/)
  option_value = (/0.30, 0.72, 0.78/)
  ethics_review = (/0.34, 0.68, 0.76/)
  governance_capacity = (/0.42, 0.74, 0.80/)

  do i = 1, 3
     future_viability(i) = 0.18 * foresight_depth(i) + &
                           0.18 * resilience(i) + &
                           0.16 * flexibility(i) + &
                           0.14 * option_value(i) + &
                           0.12 * scenario_capacity(i) + &
                           0.10 * signal_capacity(i) + &
                           0.08 * governance_capacity(i) + &
                           0.08 * ethics_review(i) - &
                           0.14 * path_dependence_risk(i)

     short_term_bias(i) = short_term_return(i) - ((foresight_depth(i) + resilience(i) + flexibility(i) + option_value(i)) / 4.0)
  end do

  print *, "Strategic foresight profiles"
  do i = 1, 3
     print *, trim(names(i)), future_viability(i), short_term_bias(i)
  end do
end program weighted_foresight_profile
