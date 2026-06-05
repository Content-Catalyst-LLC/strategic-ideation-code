! Weighted experimentation profile example.
! Compile: gfortran weighted_experimentation_profile.f90 -o weighted_experimentation_profile
! Run: ./weighted_experimentation_profile

program weighted_experimentation_profile
  implicit none

  real :: speed(3), cost_efficiency(3), insight_depth(3), user_validation(3)
  real :: assumption_criticality(3), evidence_quality(3), systems_awareness(3)
  real :: ethical_review(3), decision_linkage(3), learning_memory(3)
  real :: profile(3), superficial(3)
  character(len=4) :: ids(3)
  integer :: i

  ids = (/"E001", "E004", "E006"/)

  speed = (/0.24, 0.61, 0.70/)
  cost_efficiency = (/0.31, 0.67, 0.50/)
  insight_depth = (/0.42, 0.89, 0.36/)
  user_validation = (/0.36, 0.84, 0.42/)
  assumption_criticality = (/0.44, 0.86, 0.38/)
  evidence_quality = (/0.38, 0.88, 0.34/)
  systems_awareness = (/0.34, 0.82, 0.28/)
  ethical_review = (/0.42, 0.70, 0.30/)
  decision_linkage = (/0.30, 0.82, 0.24/)
  learning_memory = (/0.32, 0.80, 0.22/)

  do i = 1, 3
     profile(i) = 0.10 * speed(i) + &
                  0.09 * cost_efficiency(i) + &
                  0.15 * insight_depth(i) + &
                  0.12 * user_validation(i) + &
                  0.12 * assumption_criticality(i) + &
                  0.14 * evidence_quality(i) + &
                  0.10 * systems_awareness(i) + &
                  0.08 * ethical_review(i) + &
                  0.10 * decision_linkage(i) + &
                  0.10 * learning_memory(i)

     superficial(i) = 0.14 * speed(i) + &
                      0.16 * (1.0 - insight_depth(i)) + &
                      0.15 * (1.0 - evidence_quality(i)) + &
                      0.13 * (1.0 - systems_awareness(i)) + &
                      0.13 * (1.0 - ethical_review(i)) + &
                      0.13 * (1.0 - decision_linkage(i)) + &
                      0.09 * (1.0 - assumption_criticality(i)) + &
                      0.07 * (1.0 - learning_memory(i))
  end do

  print *, "Experimentation profile and superficial testing risk"
  do i = 1, 3
     print *, trim(ids(i)), profile(i), superficial(i)
  end do
end program weighted_experimentation_profile
