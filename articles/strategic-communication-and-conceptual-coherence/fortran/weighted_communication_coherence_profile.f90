program weighted_communication_coherence_profile
  implicit none
  real :: concept(3), narrative(3), evidence(3), audience(3), decision(3)
  real :: implementation(3), feedback(3), governance(3), ethics(3), score(3)
  character(len=36) :: names(3)
  integer :: i

  names = (/"Executive Strategy Briefing      ", "Stakeholder Explanation        ", "AI-Assisted Message Set        "/)
  concept = (/0.74, 0.68, 0.52/)
  narrative = (/0.76, 0.74, 0.58/)
  evidence = (/0.72, 0.70, 0.46/)
  audience = (/0.70, 0.82, 0.60/)
  decision = (/0.82, 0.66, 0.48/)
  implementation = (/0.62, 0.60, 0.46/)
  feedback = (/0.58, 0.78, 0.44/)
  governance = (/0.70, 0.66, 0.42/)
  ethics = (/0.64, 0.84, 0.40/)

  do i = 1, 3
     score(i) = 0.12*concept(i) + 0.12*narrative(i) + 0.13*evidence(i) + &
                0.10*audience(i) + 0.14*decision(i) + 0.12*implementation(i) + &
                0.08*feedback(i) + 0.10*governance(i) + 0.09*ethics(i)
  end do

  print *, "Weighted communication coherence scores"
  do i = 1, 3
     print *, trim(names(i)), score(i), 1.0 - score(i)
  end do
end program weighted_communication_coherence_profile
