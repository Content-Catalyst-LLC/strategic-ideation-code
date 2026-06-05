! Weighted co-design profile example.
! Compile: gfortran weighted_codesign_profile.f90 -o weighted_codesign_profile
! Run: ./weighted_codesign_profile

program weighted_codesign_profile
  implicit none

  real :: representation(3), influence(3), accessibility(3), reciprocity(3)
  real :: power_awareness(3), knowledge_integration(3), decision_linkage(3), accountability(3), learning_memory(3)
  real :: quality(3), tokenism(3)
  character(len=4) :: ids(3)
  integer :: i

  ids = (/"P001", "P004", "P008"/)

  representation = (/0.34, 0.86, 0.58/)
  influence = (/0.22, 0.84, 0.24/)
  accessibility = (/0.40, 0.82, 0.52/)
  reciprocity = (/0.24, 0.80, 0.18/)
  power_awareness = (/0.28, 0.86, 0.30/)
  knowledge_integration = (/0.42, 0.84, 0.54/)
  decision_linkage = (/0.20, 0.82, 0.22/)
  accountability = (/0.18, 0.86, 0.16/)
  learning_memory = (/0.24, 0.84, 0.20/)

  do i = 1, 3
     quality(i) = 0.13 * representation(i) + &
                  0.15 * influence(i) + &
                  0.11 * accessibility(i) + &
                  0.11 * reciprocity(i) + &
                  0.13 * power_awareness(i) + &
                  0.12 * knowledge_integration(i) + &
                  0.11 * decision_linkage(i) + &
                  0.10 * accountability(i) + &
                  0.04 * learning_memory(i)

     tokenism(i) = 0.16 * (1.0 - influence(i)) + &
                   0.14 * (1.0 - decision_linkage(i)) + &
                   0.14 * (1.0 - accountability(i)) + &
                   0.13 * (1.0 - reciprocity(i)) + &
                   0.13 * (1.0 - power_awareness(i)) + &
                   0.11 * (1.0 - representation(i)) + &
                   0.10 * (1.0 - accessibility(i)) + &
                   0.09 * (1.0 - learning_memory(i))
  end do

  print *, "Participation quality and tokenism risk"
  do i = 1, 3
     print *, trim(ids(i)), quality(i), tokenism(i)
  end do
end program weighted_codesign_profile
