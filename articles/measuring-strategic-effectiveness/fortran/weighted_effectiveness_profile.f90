program weighted_effectiveness_profile
  implicit none
  real :: performance(3), alignment(3), resilience(3), adaptability(3), impact(3), learning(3), confidence(3), ethics(3), score(3)
  character(len=40) :: names(3)
  integer :: i

  names = (/"Efficiency-Led Strategy        ", "Balanced Capability Strategy   ", "Adaptive Learning Strategy     "/)
  performance = (/0.84, 0.72, 0.70/)
  alignment = (/0.58, 0.79, 0.76/)
  resilience = (/0.42, 0.76, 0.78/)
  adaptability = (/0.46, 0.78, 0.88/)
  impact = (/0.51, 0.73, 0.74/)
  learning = (/0.42, 0.76, 0.90/)
  confidence = (/0.66, 0.74, 0.70/)
  ethics = (/0.48, 0.72, 0.76/)

  do i = 1, 3
     score(i) = 0.20*performance(i) + 0.15*alignment(i) + 0.16*resilience(i) + &
                0.15*adaptability(i) + 0.14*impact(i) + 0.10*learning(i) + &
                0.05*confidence(i) + 0.05*ethics(i)
  end do

  print *, "Weighted strategic effectiveness scores"
  do i = 1, 3
     print *, trim(names(i)), score(i), score(i) * confidence(i)
  end do
end program weighted_effectiveness_profile
