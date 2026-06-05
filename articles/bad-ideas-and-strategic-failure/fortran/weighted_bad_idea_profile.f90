program weighted_bad_idea_profile
  implicit none
  real :: frame(3), mechanism(3), evidence(3), implementation(3), incentive(3)
  real :: ethics(3), support(3), merit(3), learning(3), distortion(3), risk(3)
  character(len=34) :: names(3)
  integer :: i

  names = (/"AI-Assisted Workflow Redesign   ", "Cost Consolidation Plan          ", "Reversible Pilot Portfolio       "/)
  frame = (/0.54, 0.50, 0.74/)
  mechanism = (/0.56, 0.52, 0.72/)
  evidence = (/0.52, 0.48, 0.70/)
  implementation = (/0.48, 0.44, 0.72/)
  incentive = (/0.44, 0.36, 0.68/)
  ethics = (/0.46, 0.38, 0.70/)
  support = (/0.78, 0.82, 0.58/)
  merit = (/0.58, 0.54, 0.78/)
  learning = (/0.46, 0.40, 0.82/)

  do i = 1, 3
     distortion(i) = max(0.0, support(i) - merit(i))
     risk(i) = 0.14*(1.0-frame(i)) + 0.12*(1.0-mechanism(i)) + &
               0.15*(1.0-evidence(i)) + 0.14*(1.0-implementation(i)) + &
               0.12*(1.0-incentive(i)) + 0.12*(1.0-ethics(i)) + &
               0.11*(1.0-learning(i)) + 0.10*distortion(i)
  end do

  print *, "Bad-idea risk scores"
  do i = 1, 3
     print *, trim(names(i)), risk(i)
  end do
end program weighted_bad_idea_profile
