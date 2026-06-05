program weighted_learning_loop_profile
  implicit none
  real :: feedback(3), assumptions(3), interpretation(3), authority(3), closure(3)
  real :: memory(3), safety(3), scaling(3), ethics(3), score(3)
  character(len=44) :: names(3)
  integer :: i

  names = (/"Reporting-Heavy Organization          ", "Adaptive Learning Organization         ", "Pilot-Rich Memory-Poor Organization    "/)
  feedback = (/0.62, 0.84, 0.72/)
  assumptions = (/0.42, 0.82, 0.60/)
  interpretation = (/0.46, 0.80, 0.62/)
  authority = (/0.38, 0.78, 0.56/)
  closure = (/0.34, 0.82, 0.48/)
  memory = (/0.36, 0.76, 0.30/)
  safety = (/0.44, 0.78, 0.58/)
  scaling = (/0.40, 0.74, 0.36/)
  ethics = (/0.50, 0.80, 0.56/)

  do i = 1, 3
     score(i) = 0.13*feedback(i) + 0.13*assumptions(i) + 0.12*interpretation(i) + &
                0.14*authority(i) + 0.14*closure(i) + 0.10*memory(i) + &
                0.09*safety(i) + 0.08*scaling(i) + 0.07*ethics(i)
  end do

  print *, "Weighted learning loop scores"
  do i = 1, 3
     print *, trim(names(i)), score(i), 1.0 - score(i)
  end do
end program weighted_learning_loop_profile
