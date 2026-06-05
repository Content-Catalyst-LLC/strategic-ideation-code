! Weighted assumption risk scoring example.
! Compile: gfortran weighted_assumption_scoring.f90 -o weighted_assumption_scoring
! Run: ./weighted_assumption_scoring

program weighted_assumption_scoring
  implicit none

  real :: criticality(3), uncertainty(3), evidence_strength(3), evidence_relevance(3)
  real :: evidence_transferability(3), testability(3), stakeholder_sensitivity(3), system_sensitivity(3)
  real :: evidence_composite(3), risk_score(3), learning_value(3)
  character(len=4) :: ids(3)
  integer :: i

  ids = (/"A001", "A004", "A015"/)

  criticality = (/0.86, 0.90, 0.86/)
  uncertainty = (/0.70, 0.72, 0.66/)
  evidence_strength = (/0.38, 0.34, 0.38/)
  evidence_relevance = (/0.62, 0.72, 0.62/)
  evidence_transferability = (/0.54, 0.60, 0.52/)
  testability = (/0.78, 0.74, 0.62/)
  stakeholder_sensitivity = (/0.72, 0.94, 0.70/)
  system_sensitivity = (/0.70, 0.76, 0.74/)

  do i = 1, 3
     evidence_composite(i) = 0.40 * evidence_strength(i) + &
                             0.30 * evidence_relevance(i) + &
                             0.30 * evidence_transferability(i)

     risk_score(i) = criticality(i) * uncertainty(i) * (1.0 - evidence_composite(i))

     learning_value(i) = 0.34 * risk_score(i) + &
                         0.24 * testability(i) + &
                         0.18 * stakeholder_sensitivity(i) + &
                         0.14 * system_sensitivity(i) + &
                         0.10 * criticality(i)
  end do

  print *, "Assumption risk and learning value"
  do i = 1, 3
     print *, trim(ids(i)), risk_score(i), learning_value(i)
  end do
end program weighted_assumption_scoring
