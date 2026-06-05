! Weighted adaptive strategy profile example.
! Compile: gfortran weighted_adaptive_strategy_profile.f90 -o weighted_adaptive_strategy_profile
! Run: ./weighted_adaptive_strategy_profile

program weighted_adaptive_strategy_profile
  implicit none

  real :: flexibility(3), learning_capacity(3), exploration(3), exploitation_balance(3)
  real :: coherence(3), feedback_intelligence(3), governance(3), systems_awareness(3), learning_memory(3)
  real :: score(3), risk(3)
  character(len=5) :: ids(3)
  integer :: i

  ids = (/"AS001", "AS002", "AS004"/)

  flexibility = (/0.24, 0.82, 0.86/)
  learning_capacity = (/0.31, 0.84, 0.49/)
  exploration = (/0.18, 0.68, 0.57/)
  exploitation_balance = (/0.74, 0.79, 0.32/)
  coherence = (/0.81, 0.76, 0.28/)
  feedback_intelligence = (/0.34, 0.82, 0.42/)
  governance = (/0.62, 0.78, 0.24/)
  systems_awareness = (/0.38, 0.74, 0.36/)
  learning_memory = (/0.36, 0.76, 0.30/)

  do i = 1, 3
     score(i) = 0.13 * flexibility(i) + &
                0.15 * learning_capacity(i) + &
                0.09 * exploration(i) + &
                0.11 * exploitation_balance(i) + &
                0.15 * coherence(i) + &
                0.13 * feedback_intelligence(i) + &
                0.10 * governance(i) + &
                0.08 * systems_awareness(i) + &
                0.06 * learning_memory(i)

     risk(i) = 0.20 * flexibility(i) * (1.0 - coherence(i)) + &
               0.18 * (1.0 - governance(i)) + &
               0.16 * (1.0 - feedback_intelligence(i)) + &
               0.14 * (1.0 - learning_capacity(i)) + &
               0.12 * (1.0 - exploitation_balance(i)) + &
               0.10 * (1.0 - learning_memory(i)) + &
               0.10 * (1.0 - systems_awareness(i))
  end do

  print *, "Adaptive strategy score and over-adaptation risk"
  do i = 1, 3
     print *, trim(ids(i)), score(i), risk(i)
  end do
end program weighted_adaptive_strategy_profile
