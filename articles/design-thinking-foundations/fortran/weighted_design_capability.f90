! Weighted design thinking capability example.
! Compile: gfortran weighted_design_capability.f90 -o weighted_design_capability
! Run: ./weighted_design_capability

program weighted_design_capability
  implicit none

  real :: empathy(3), reframing(3), divergence(3), convergence(3), prototyping(3)
  real :: testing(3), systems(3), ethics(3), decision(3), adaptability(3), memory(3)
  real :: capability(3), superficiality(3)
  character(len=4) :: ids(3)
  integer :: i

  ids = (/"C001", "C003", "C004"/)

  empathy = (/0.28, 0.81, 0.39/)
  reframing = (/0.31, 0.84, 0.34/)
  divergence = (/0.36, 0.86, 0.68/)
  convergence = (/0.58, 0.74, 0.38/)
  prototyping = (/0.24, 0.88, 0.41/)
  testing = (/0.29, 0.86, 0.36/)
  systems = (/0.35, 0.72, 0.30/)
  ethics = (/0.42, 0.74, 0.34/)
  decision = (/0.36, 0.78, 0.28/)
  adaptability = (/0.33, 0.89, 0.42/)
  memory = (/0.40, 0.76, 0.24/)

  do i = 1, 3
     capability(i) = 0.12 * empathy(i) + &
                     0.13 * reframing(i) + &
                     0.10 * divergence(i) + &
                     0.10 * convergence(i) + &
                     0.12 * prototyping(i) + &
                     0.12 * testing(i) + &
                     0.11 * systems(i) + &
                     0.10 * ethics(i) + &
                     0.10 * decision(i) + &
                     0.06 * adaptability(i) + &
                     0.04 * memory(i)

     superficiality(i) = 0.18 * (1.0 - empathy(i)) + &
                         0.14 * (1.0 - reframing(i)) + &
                         0.12 * (1.0 - testing(i)) + &
                         0.12 * (1.0 - systems(i)) + &
                         0.12 * (1.0 - ethics(i)) + &
                         0.16 * (1.0 - decision(i)) + &
                         0.10 * (1.0 - memory(i)) + &
                         0.06 * (1.0 - adaptability(i))
  end do

  print *, "Design capability and superficiality risk"
  do i = 1, 3
     print *, trim(ids(i)), capability(i), superficiality(i)
  end do
end program weighted_design_capability
