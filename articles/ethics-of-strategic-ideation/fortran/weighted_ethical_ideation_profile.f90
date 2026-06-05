program weighted_ethical_ideation_profile
  implicit none
  real :: voice(3), evidence(3), burden(3), uncertainty(3), reversibility(3)
  real :: long_term(3), ai(3), accountability(3), redress(3), score(3)
  character(len=37) :: names(3)
  integer :: i

  names = (/"AI-Assisted Service Triage       ", "Participatory Governance Council ", "Workforce Restructuring Plan      "/)
  voice = (/0.42, 0.84, 0.38/)
  evidence = (/0.56, 0.72, 0.58/)
  burden = (/0.44, 0.78, 0.40/)
  uncertainty = (/0.46, 0.70, 0.44/)
  reversibility = (/0.50, 0.72, 0.36/)
  long_term = (/0.52, 0.74, 0.42/)
  ai = (/0.38, 0.62, 0.40/)
  accountability = (/0.48, 0.76, 0.46/)
  redress = (/0.36, 0.72, 0.34/)

  do i = 1, 3
     score(i) = 0.14*voice(i) + 0.14*evidence(i) + 0.12*burden(i) + &
                0.11*uncertainty(i) + 0.10*reversibility(i) + &
                0.13*long_term(i) + 0.08*ai(i) + 0.10*accountability(i) + 0.08*redress(i)
  end do

  print *, "Weighted ethical ideation scores"
  do i = 1, 3
     print *, trim(names(i)), score(i), 1.0 - score(i)
  end do
end program weighted_ethical_ideation_profile
