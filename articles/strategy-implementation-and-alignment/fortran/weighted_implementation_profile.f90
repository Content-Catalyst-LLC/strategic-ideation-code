program weighted_implementation_profile
  implicit none
  real :: goal(3), coordination(3), structure(3), culture(3), incentives(3)
  real :: resources(3), communication(3), accountability(3), adaptation(3), score(3)
  character(len=48) :: names(3)
  integer :: i

  names = (/"High-Intent Fragmented Organization       ", "Balanced Aligned Organization             ", "Adaptive Cross-Functional Organization    "/)
  goal = (/0.70, 0.82, 0.78/)
  coordination = (/0.38, 0.81, 0.84/)
  structure = (/0.44, 0.79, 0.73/)
  culture = (/0.31, 0.78, 0.76/)
  incentives = (/0.29, 0.77, 0.71/)
  resources = (/0.52, 0.82, 0.76/)
  communication = (/0.41, 0.80, 0.78/)
  accountability = (/0.46, 0.76, 0.74/)
  adaptation = (/0.36, 0.74, 0.83/)

  do i = 1, 3
     score(i) = 0.12*goal(i) + 0.15*coordination(i) + 0.12*structure(i) + 0.12*culture(i) + &
                0.13*incentives(i) + 0.12*resources(i) + 0.11*communication(i) + &
                0.10*accountability(i) + 0.10*adaptation(i)
  end do

  print *, "Weighted implementation profile scores"
  do i = 1, 3
     print *, trim(names(i)), score(i)
  end do
end program weighted_implementation_profile
