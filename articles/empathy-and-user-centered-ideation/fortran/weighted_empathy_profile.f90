! Weighted empathy and user-centered ideation profile example.
! Compile: gfortran weighted_empathy_profile.f90 -o weighted_empathy_profile
! Run: ./weighted_empathy_profile

program weighted_empathy_profile
  implicit none

  real :: observation(3), projection(3), unmet_need(3), stakeholder_breadth(3)
  real :: reframing(3), ethics(3), systems(3), decision(3), memory(3)
  real :: profile(3), superficiality(3)
  character(len=4) :: ids(3)
  integer :: i

  ids = (/"C001", "C004", "C005"/)

  observation = (/0.24, 0.76, 0.38/)
  projection = (/0.84, 0.48, 0.72/)
  unmet_need = (/0.31, 0.79, 0.42/)
  stakeholder_breadth = (/0.28, 0.90, 0.36/)
  reframing = (/0.34, 0.83, 0.40/)
  ethics = (/0.38, 0.86, 0.32/)
  systems = (/0.35, 0.88, 0.30/)
  decision = (/0.32, 0.78, 0.24/)
  memory = (/0.30, 0.76, 0.22/)

  do i = 1, 3
     profile(i) = 0.16 * observation(i) - &
                  0.14 * projection(i) + &
                  0.16 * unmet_need(i) + &
                  0.12 * stakeholder_breadth(i) + &
                  0.16 * reframing(i) + &
                  0.10 * ethics(i) + &
                  0.10 * systems(i) + &
                  0.14 * decision(i) + &
                  0.10 * memory(i)

     superficiality(i) = 0.20 * projection(i) + &
                         0.16 * (1.0 - decision(i)) + &
                         0.14 * (1.0 - observation(i)) + &
                         0.12 * (1.0 - unmet_need(i)) + &
                         0.12 * (1.0 - ethics(i)) + &
                         0.10 * (1.0 - systems(i)) + &
                         0.08 * (1.0 - stakeholder_breadth(i)) + &
                         0.08 * (1.0 - memory(i))
  end do

  print *, "Empathy profile and superficiality risk"
  do i = 1, 3
     print *, trim(ids(i)), profile(i), superficiality(i)
  end do
end program weighted_empathy_profile
