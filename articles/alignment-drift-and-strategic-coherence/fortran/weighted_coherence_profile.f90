program weighted_coherence_profile
  implicit none
  real :: purpose(3), priority(3), tradeoff(3), resources(3), incentives(3)
  real :: interpretation(3), governance(3), feedback(3), memory(3), ethics(3), score(3)
  character(len=44) :: names(3)
  integer :: i

  names = (/"Symbolically Aligned Organization      ", "Coherent Adaptive Organization         ", "Metric-Substituted Organization        "/)
  purpose = (/0.64, 0.84, 0.68/)
  priority = (/0.50, 0.80, 0.60/)
  tradeoff = (/0.46, 0.78, 0.54/)
  resources = (/0.46, 0.78, 0.62/)
  incentives = (/0.42, 0.80, 0.36/)
  interpretation = (/0.50, 0.82, 0.58/)
  governance = (/0.44, 0.78, 0.52/)
  feedback = (/0.48, 0.84, 0.44/)
  memory = (/0.40, 0.76, 0.50/)
  ethics = (/0.54, 0.80, 0.46/)

  do i = 1, 3
     score(i) = 0.15*purpose(i) + 0.12*priority(i) + 0.11*tradeoff(i) + &
                0.13*resources(i) + 0.13*incentives(i) + 0.11*interpretation(i) + &
                0.12*governance(i) + 0.08*feedback(i) + 0.07*memory(i) + 0.08*ethics(i)
  end do

  print *, "Weighted strategic coherence scores"
  do i = 1, 3
     print *, trim(names(i)), score(i), 1.0 - score(i)
  end do
end program weighted_coherence_profile
