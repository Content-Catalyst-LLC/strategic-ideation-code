program weighted_taxonomy_profile
  implicit none
  real :: category(3), level(3), maturity(3), evidence(3), function_score(3)
  real :: relationships(3), retrieval(3), governance(3), ethics(3), score(3)
  character(len=39) :: names(3)
  integer :: i

  names = (/"Strategic Learning Repository        ", "Participatory Governance Prototype   ", "Advisory Panel Without Authority      "/)
  category = (/0.78, 0.76, 0.66/)
  level = (/0.76, 0.74, 0.62/)
  maturity = (/0.72, 0.76, 0.72/)
  evidence = (/0.72, 0.70, 0.62/)
  function_score = (/0.80, 0.74, 0.60/)
  relationships = (/0.76, 0.72, 0.66/)
  retrieval = (/0.82, 0.76, 0.62/)
  governance = (/0.74, 0.70, 0.56/)
  ethics = (/0.66, 0.82, 0.76/)

  do i = 1, 3
     score(i) = 0.13*category(i) + 0.11*level(i) + 0.11*maturity(i) + &
                0.12*evidence(i) + 0.13*function_score(i) + &
                0.11*relationships(i) + 0.13*retrieval(i) + &
                0.09*governance(i) + 0.07*ethics(i)
  end do

  print *, "Weighted taxonomy scores"
  do i = 1, 3
     print *, trim(names(i)), score(i), 1.0 - score(i)
  end do
end program weighted_taxonomy_profile
