program weighted_knowledge_architecture_profile
  implicit none
  real :: taxonomy(3), metadata(3), semantics(3), evidence(3), assumptions(3)
  real :: relationships(3), retrieval(3), memory(3), stewardship(3), ethics(3), score(3)
  character(len=42) :: names(3)
  integer :: i

  names = (/"Community Data Stewardship          ", "AI-Assisted Scenario Library       ", "Strategic Learning Repository      "/)
  taxonomy = (/0.74, 0.62, 0.78/)
  metadata = (/0.70, 0.58, 0.80/)
  semantics = (/0.76, 0.54, 0.82/)
  evidence = (/0.66, 0.52, 0.74/)
  assumptions = (/0.68, 0.50, 0.72/)
  relationships = (/0.72, 0.58, 0.82/)
  retrieval = (/0.70, 0.54, 0.84/)
  memory = (/0.62, 0.46, 0.78/)
  stewardship = (/0.64, 0.48, 0.76/)
  ethics = (/0.78, 0.46, 0.66/)

  do i = 1, 3
     score(i) = 0.11*taxonomy(i) + 0.12*metadata(i) + 0.11*semantics(i) + &
                0.12*evidence(i) + 0.11*assumptions(i) + 0.11*relationships(i) + &
                0.12*retrieval(i) + 0.09*memory(i) + 0.07*stewardship(i) + 0.04*ethics(i)
  end do

  print *, "Weighted knowledge architecture scores"
  do i = 1, 3
     print *, trim(names(i)), score(i), 1.0 - score(i)
  end do
end program weighted_knowledge_architecture_profile
