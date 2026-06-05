! Weighted journey profile example.
! Compile: gfortran weighted_journey_profile.f90 -o weighted_journey_profile
! Run: ./weighted_journey_profile

program weighted_journey_profile
  implicit none

  real :: clarity(3), emotional_confidence(3), friction(3), transition_quality(3)
  real :: accessibility(3), trust(3), completion_support(3), backstage_alignment(3), measurement_quality(3)
  real :: profile(3), redesign_need(3)
  character(len=4) :: ids(3)
  integer :: i

  ids = (/"J001", "J005", "J007"/)

  clarity = (/0.36, 0.81, 0.54/)
  emotional_confidence = (/0.31, 0.79, 0.45/)
  friction = (/0.82, 0.28, 0.72/)
  transition_quality = (/0.28, 0.82, 0.36/)
  accessibility = (/0.34, 0.88, 0.50/)
  trust = (/0.30, 0.84, 0.44/)
  completion_support = (/0.34, 0.86, 0.52/)
  backstage_alignment = (/0.30, 0.78, 0.34/)
  measurement_quality = (/0.38, 0.76, 0.46/)

  do i = 1, 3
     profile(i) = 0.15 * clarity(i) + &
                  0.12 * emotional_confidence(i) - &
                  0.18 * friction(i) + &
                  0.14 * transition_quality(i) + &
                  0.12 * accessibility(i) + &
                  0.12 * trust(i) + &
                  0.10 * completion_support(i) + &
                  0.10 * backstage_alignment(i) + &
                  0.07 * measurement_quality(i)

     redesign_need(i) = 0.22 * friction(i) + &
                        0.16 * (1.0 - transition_quality(i)) + &
                        0.14 * (1.0 - accessibility(i)) + &
                        0.13 * (1.0 - trust(i)) + &
                        0.12 * (1.0 - clarity(i)) + &
                        0.11 * (1.0 - backstage_alignment(i)) + &
                        0.07 * (1.0 - completion_support(i)) + &
                        0.05 * (1.0 - measurement_quality(i))
  end do

  print *, "Journey profile and redesign need"
  do i = 1, 3
     print *, trim(ids(i)), profile(i), redesign_need(i)
  end do
end program weighted_journey_profile
