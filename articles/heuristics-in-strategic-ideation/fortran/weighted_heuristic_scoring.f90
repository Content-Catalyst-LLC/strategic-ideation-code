! Weighted heuristic profile scoring example.
! Compile: gfortran weighted_heuristic_scoring.f90 -o weighted_heuristic_scoring
! Run: ./weighted_heuristic_scoring

program weighted_heuristic_scoring
  implicit none

  real :: availability(3), anchoring(3), recognition(3), satisficing(3), affect(3)
  real :: default_g(3), social_proof(3), diversity(3), stakeholder(3), source_domain(3)
  real :: systems(3), political(3), memory(3), score(3)
  character(len=4) :: ids(3)
  integer :: i

  ids = (/"H001", "H004", "H005"/)
  availability = (/0.84, 0.31, 0.76/)
  anchoring = (/0.63, 0.27, 0.72/)
  recognition = (/0.79, 0.36, 0.82/)
  satisficing = (/0.82, 0.34, 0.78/)
  affect = (/0.66, 0.32, 0.62/)
  default_g = (/0.72, 0.30, 0.88/)
  social_proof = (/0.70, 0.28, 0.74/)
  diversity = (/0.29, 0.89, 0.30/)
  stakeholder = (/0.34, 0.82, 0.28/)
  source_domain = (/0.28, 0.88, 0.26/)
  systems = (/0.40, 0.78, 0.36/)
  political = (/0.48, 0.74, 0.30/)
  memory = (/0.34, 0.72, 0.36/)

  do i = 1, 3
     score(i) = -0.11 * availability(i) - 0.11 * anchoring(i) - &
                0.10 * recognition(i) - 0.11 * satisficing(i) - &
                0.07 * affect(i) - 0.08 * default_g(i) - &
                0.06 * social_proof(i) + 0.17 * diversity(i) + &
                0.13 * stakeholder(i) + 0.13 * source_domain(i) + &
                0.14 * systems(i) + 0.07 * political(i) + &
                0.08 * memory(i)
  end do

  print *, "Heuristic profile scores"
  do i = 1, 3
     print *, trim(ids(i)), score(i)
  end do
end program weighted_heuristic_scoring
