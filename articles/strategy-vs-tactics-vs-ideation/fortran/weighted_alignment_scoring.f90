! Weighted alignment scoring example.
! Compile: gfortran weighted_alignment_scoring.f90 -o weighted_alignment_scoring
! Run: ./weighted_alignment_scoring

program weighted_alignment_scoring
  implicit none

  real :: ideation(3), strategy(3), tactics(3), feedback(3), learning(3), score(3)
  character(len=4) :: ids(3)
  integer :: i

  ids = (/"C001", "C002", "C003"/)
  ideation = (/0.32, 0.74, 0.89/)
  strategy = (/0.28, 0.79, 0.41/)
  tactics = (/0.39, 0.77, 0.34/)
  feedback = (/0.31, 0.75, 0.42/)
  learning = (/0.27, 0.76, 0.46/)

  do i = 1, 3
     score(i) = 0.18 * ideation(i) + 0.24 * strategy(i) + &
                0.22 * tactics(i) + 0.18 * feedback(i) + &
                0.18 * learning(i)
  end do

  print *, "Layer alignment scores"
  do i = 1, 3
     print *, trim(ids(i)), score(i)
  end do
end program weighted_alignment_scoring
