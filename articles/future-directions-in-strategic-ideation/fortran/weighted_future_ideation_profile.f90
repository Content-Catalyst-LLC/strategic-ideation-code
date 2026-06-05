program weighted_future_ideation_profile
  implicit none
  real :: frame(3), evidence(3), adaptability(3), scenario(3), stakeholder(3)
  real :: implementation(3), ethics(3), learning(3), option_value(3), ai(3), score(3)
  character(len=34) :: names(3)
  integer :: i

  names = (/"Scenario-Linked Option Portfolio ", "Participatory Strategy Lab       ", "Rapid Automation Initiative      "/)
  frame = (/0.78, 0.80, 0.54/)
  evidence = (/0.72, 0.74, 0.52/)
  adaptability = (/0.84, 0.78, 0.48/)
  scenario = (/0.86, 0.72, 0.46/)
  stakeholder = (/0.70, 0.86, 0.42/)
  implementation = (/0.70, 0.64, 0.50/)
  ethics = (/0.76, 0.84, 0.44/)
  learning = (/0.86, 0.78, 0.42/)
  option_value = (/0.90, 0.72, 0.46/)
  ai = (/0.62, 0.56, 0.38/)

  do i = 1, 3
     score(i) = 0.11*frame(i) + 0.11*evidence(i) + 0.11*adaptability(i) + &
                0.12*scenario(i) + 0.11*stakeholder(i) + 0.10*implementation(i) + &
                0.11*ethics(i) + 0.12*learning(i) + 0.07*option_value(i) + 0.04*ai(i)
  end do

  print *, "Future-ready strategic ideation scores"
  do i = 1, 3
     print *, trim(names(i)), score(i), 1.0 - score(i)
  end do
end program weighted_future_ideation_profile
