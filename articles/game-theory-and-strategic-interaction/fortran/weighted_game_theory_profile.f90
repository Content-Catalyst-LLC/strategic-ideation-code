! Weighted game-theory strategic interaction profile example.
! Compile: gfortran weighted_game_theory_profile.f90 -o weighted_game_theory_profile
! Run: ./weighted_game_theory_profile

program weighted_game_theory_profile
  implicit none

  real :: rivalry(3), coordination(3), information_asymmetry(3), retaliation(3)
  real :: institutional_support(3), behavioral_realism(3), mechanism_design(3), ethical_complexity(3)
  real :: mechanism_opportunity(3), cooperation_fragility(3)
  character(len=42) :: names(3)
  integer :: i

  names = (/"Price Competition Environment          ", "Standards Coordination Environment     ", "Platform Ecosystem Environment         "/)

  rivalry = (/0.84, 0.36, 0.71/)
  coordination = (/0.28, 0.86, 0.74/)
  information_asymmetry = (/0.44, 0.31, 0.69/)
  retaliation = (/0.76, 0.24, 0.58/)
  institutional_support = (/0.39, 0.73, 0.57/)
  behavioral_realism = (/0.52, 0.68, 0.74/)
  mechanism_design = (/0.42, 0.78, 0.82/)
  ethical_complexity = (/0.46, 0.54, 0.76/)

  do i = 1, 3
     mechanism_opportunity(i) = 0.30 * mechanism_design(i) + &
                                0.18 * coordination(i) + &
                                0.16 * information_asymmetry(i) + &
                                0.14 * ethical_complexity(i) + &
                                0.12 * institutional_support(i) + &
                                0.10 * behavioral_realism(i)

     cooperation_fragility(i) = 0.22 * rivalry(i) + &
                                0.20 * retaliation(i) + &
                                0.16 * information_asymmetry(i) + &
                                0.12 * ethical_complexity(i) - &
                                0.15 * institutional_support(i) - &
                                0.15 * coordination(i)
  end do

  print *, "Strategic interaction profiles"
  do i = 1, 3
     print *, trim(names(i)), mechanism_opportunity(i), cooperation_fragility(i)
  end do
end program weighted_game_theory_profile
