program weighted_sequencing_profile
  implicit none
  real :: capability(3), evidence(3), governance(3), legitimacy(3), dependency(3)
  real :: reversibility(3), capacity(3), timing(3), ethics(3), score(3)
  character(len=40) :: names(3)
  integer :: i

  names = (/"Data Governance Foundation      ", "Full Platform Rollout          ", "Adaptive Rollout Sequence      "/)
  capability = (/0.72, 0.52, 0.70/)
  evidence = (/0.66, 0.46, 0.68/)
  governance = (/0.78, 0.48, 0.72/)
  legitimacy = (/0.62, 0.44, 0.74/)
  dependency = (/0.42, 0.82, 0.52/)
  reversibility = (/0.70, 0.38, 0.76/)
  capacity = (/0.46, 0.84, 0.60/)
  timing = (/0.52, 0.60, 0.66/)
  ethics = (/0.70, 0.42, 0.78/)

  do i = 1, 3
     score(i) = 0.16*capability(i) + 0.15*evidence(i) + 0.15*governance(i) + &
                0.14*legitimacy(i) - 0.12*dependency(i) + 0.10*reversibility(i) - &
                0.10*capacity(i) + 0.08*timing(i) + 0.12*ethics(i)
  end do

  print *, "Weighted sequencing readiness scores"
  do i = 1, 3
     print *, trim(names(i)), score(i)
  end do
end program weighted_sequencing_profile
