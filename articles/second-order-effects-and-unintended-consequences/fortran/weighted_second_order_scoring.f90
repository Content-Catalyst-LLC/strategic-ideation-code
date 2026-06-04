! Weighted second-order effects scoring example.
! Compile: gfortran weighted_second_order_scoring.f90 -o weighted_second_order_scoring
! Run: ./weighted_second_order_scoring

program weighted_second_order_scoring
  implicit none

  real :: first_gain(3), adaptation(3), feedback(3), delay(3), burden(3)
  real :: gaming(3), fragility(3), learning(3), legitimacy(3), reversibility(3)
  real :: risk_score(3), false_success(3)
  character(len=4) :: ids(3)
  integer :: i

  ids = (/"I001", "I002", "I003"/)

  first_gain = (/0.88, 0.71, 0.63/)
  adaptation = (/0.76, 0.44, 0.81/)
  feedback = (/0.58, 0.51, 0.73/)
  delay = (/0.69, 0.42, 0.57/)
  burden = (/0.66, 0.34, 0.78/)
  gaming = (/0.52, 0.28, 0.74/)
  fragility = (/0.82, 0.39, 0.74/)
  learning = (/0.38, 0.76, 0.42/)
  legitimacy = (/0.44, 0.72, 0.46/)
  reversibility = (/0.42, 0.70, 0.38/)

  do i = 1, 3
     risk_score(i) = 0.16 * adaptation(i) + 0.15 * feedback(i) + &
                     0.14 * delay(i) + 0.15 * burden(i) + &
                     0.14 * gaming(i) + 0.16 * fragility(i) - &
                     0.10 * learning(i) - 0.06 * legitimacy(i) - &
                     0.06 * reversibility(i)

     false_success(i) = 0.26 * first_gain(i) + 0.20 * fragility(i) + &
                        0.16 * delay(i) + 0.14 * gaming(i) + &
                        0.12 * burden(i) - 0.16 * learning(i)
  end do

  print *, "Second-order risk scores"
  do i = 1, 3
     print *, trim(ids(i)), risk_score(i), false_success(i)
  end do
end program weighted_second_order_scoring
