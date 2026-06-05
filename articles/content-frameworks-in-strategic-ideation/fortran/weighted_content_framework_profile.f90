program weighted_content_framework_profile
  implicit none
  real :: structure(3), clarity(3), evidence(3), assumptions(3), narrative(3)
  real :: decision(3), modularity(3), reuse(3), governance(3), ethics(3), score(3)
  character(len=38) :: names(3)
  integer :: i

  names = (/"Idea Record Framework             ", "Decision Memo Framework         ", "AI-Assisted Ideation Framework  "/)
  structure = (/0.76, 0.82, 0.62/)
  clarity = (/0.72, 0.76, 0.56/)
  evidence = (/0.66, 0.80, 0.50/)
  assumptions = (/0.68, 0.78, 0.48/)
  narrative = (/0.62, 0.74, 0.58/)
  decision = (/0.64, 0.86, 0.54/)
  modularity = (/0.74, 0.66, 0.60/)
  reuse = (/0.72, 0.68, 0.58/)
  governance = (/0.66, 0.72, 0.46/)
  ethics = (/0.60, 0.72, 0.42/)

  do i = 1, 3
     score(i) = 0.11*structure(i) + 0.11*clarity(i) + 0.12*evidence(i) + &
                0.10*assumptions(i) + 0.10*narrative(i) + 0.13*decision(i) + &
                0.10*modularity(i) + 0.10*reuse(i) + 0.08*governance(i) + 0.05*ethics(i)
  end do

  print *, "Weighted content framework scores"
  do i = 1, 3
     print *, trim(names(i)), score(i), 1.0 - score(i)
  end do
end program weighted_content_framework_profile
