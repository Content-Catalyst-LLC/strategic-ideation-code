program weighted_institutional_memory_profile
  implicit none
  real :: capture(3), metadata(3), context(3), decisions(3), learning(3)
  real :: retrieval(3), reuse(3), stewardship(3), continuity(3), ethics(3), score(3)
  character(len=34) :: names(3)
  integer :: i

  names = (/"Strategic Idea Repository       ", "Decision Memory                 ", "Retired Ideas Archive           "/)
  capture = (/0.72, 0.70, 0.58/)
  metadata = (/0.80, 0.74, 0.54/)
  context = (/0.76, 0.82, 0.56/)
  decisions = (/0.66, 0.86, 0.58/)
  learning = (/0.68, 0.72, 0.48/)
  retrieval = (/0.78, 0.74, 0.52/)
  reuse = (/0.80, 0.76, 0.60/)
  stewardship = (/0.72, 0.70, 0.50/)
  continuity = (/0.70, 0.72, 0.48/)
  ethics = (/0.62, 0.70, 0.58/)

  do i = 1, 3
     score(i) = 0.10*capture(i) + 0.12*metadata(i) + 0.12*context(i) + &
                0.13*decisions(i) + 0.12*learning(i) + 0.12*retrieval(i) + &
                0.10*reuse(i) + 0.08*stewardship(i) + 0.06*continuity(i) + 0.05*ethics(i)
  end do

  print *, "Weighted institutional memory scores"
  do i = 1, 3
     print *, trim(names(i)), score(i), 1.0 - score(i)
  end do
end program weighted_institutional_memory_profile
