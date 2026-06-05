program weighted_power_distortion_profile
  implicit none
  real :: merit(3), evidence(3), sponsorship(3), resource_fit(3), stakeholder(3)
  real :: dissent(3), classification(3), power_alignment(3), advancement(3)
  real :: merit_score(3), support_score(3)
  character(len=36) :: names(3)
  integer :: i

  names = (/"Participatory Governance Model     ", "Executive Dashboard Expansion    ", "Cost Consolidation Plan          "/)
  merit = (/0.78, 0.62, 0.58/)
  evidence = (/0.72, 0.60, 0.52/)
  sponsorship = (/0.54, 0.86, 0.82/)
  resource_fit = (/0.58, 0.82, 0.80/)
  stakeholder = (/0.78, 0.42, 0.34/)
  dissent = (/0.72, 0.46, 0.38/)
  classification = (/0.76, 0.58, 0.46/)
  power_alignment = (/0.46, 0.84, 0.86/)
  advancement = (/0.52, 0.82, 0.80/)

  do i = 1, 3
     merit_score(i) = 0.32*merit(i) + 0.24*evidence(i) + 0.18*stakeholder(i) + &
                      0.14*dissent(i) + 0.12*classification(i)
     support_score(i) = 0.30*sponsorship(i) + 0.25*resource_fit(i) + &
                        0.25*power_alignment(i) + 0.20*advancement(i)
  end do

  print *, "Institutional power distortion scores"
  do i = 1, 3
     print *, trim(names(i)), merit_score(i), support_score(i), support_score(i) - merit_score(i)
  end do
end program weighted_power_distortion_profile
