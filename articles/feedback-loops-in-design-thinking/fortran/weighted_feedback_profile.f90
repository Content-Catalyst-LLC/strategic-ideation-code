! Weighted feedback profile example.
! Compile: gfortran weighted_feedback_profile.f90 -o weighted_feedback_profile
! Run: ./weighted_feedback_profile

program weighted_feedback_profile
  implicit none

  real :: signal_quality(3), interpretation_capacity(3), adjustment_speed(3), user_insight_depth(3)
  real :: stability(3), ethical_integrity(3), systems_awareness(3), decision_linkage(3), learning_memory(3)
  real :: profile(3), churn(3)
  character(len=4) :: ids(3)
  integer :: i

  ids = (/"F001", "F004", "F006"/)

  signal_quality = (/0.34, 0.82, 0.62/)
  interpretation_capacity = (/0.31, 0.84, 0.42/)
  adjustment_speed = (/0.29, 0.63, 0.34/)
  user_insight_depth = (/0.36, 0.88, 0.46/)
  stability = (/0.41, 0.72, 0.50/)
  ethical_integrity = (/0.38, 0.72, 0.40/)
  systems_awareness = (/0.32, 0.84, 0.38/)
  decision_linkage = (/0.28, 0.80, 0.24/)
  learning_memory = (/0.26, 0.82, 0.28/)

  do i = 1, 3
     profile(i) = 0.13 * signal_quality(i) + &
                  0.13 * interpretation_capacity(i) + &
                  0.10 * adjustment_speed(i) + &
                  0.13 * user_insight_depth(i) + &
                  0.10 * stability(i) + &
                  0.11 * ethical_integrity(i) + &
                  0.10 * systems_awareness(i) + &
                  0.10 * decision_linkage(i) + &
                  0.10 * learning_memory(i)

     churn(i) = 0.16 * adjustment_speed(i) + &
                0.15 * (1.0 - signal_quality(i)) + &
                0.15 * (1.0 - interpretation_capacity(i)) + &
                0.13 * (1.0 - stability(i)) + &
                0.12 * (1.0 - systems_awareness(i)) + &
                0.12 * (1.0 - ethical_integrity(i)) + &
                0.10 * (1.0 - decision_linkage(i)) + &
                0.07 * (1.0 - learning_memory(i))
  end do

  print *, "Feedback profile and noisy churn risk"
  do i = 1, 3
     print *, trim(ids(i)), profile(i), churn(i)
  end do
end program weighted_feedback_profile
