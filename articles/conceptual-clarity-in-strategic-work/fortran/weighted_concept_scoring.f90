! Weighted conceptual clarity scoring example.
! Compile: gfortran weighted_concept_scoring.f90 -o weighted_concept_scoring
! Run: ./weighted_concept_scoring

program weighted_concept_scoring
  implicit none

  real :: definition(3), boundary(3), distinction(3), operational(3), measurement(3)
  real :: revision(3), stakeholder(3), ethics(3), governance(3), score(3)
  character(len=5) :: ids(3)
  integer :: i

  ids = (/"CC001", "CC003", "CC006"/)
  definition = (/0.42, 0.64, 0.58/)
  boundary = (/0.31, 0.55, 0.50/)
  distinction = (/0.44, 0.68, 0.61/)
  operational = (/0.52, 0.70, 0.63/)
  measurement = (/0.36, 0.60, 0.54/)
  revision = (/0.29, 0.52, 0.49/)
  stakeholder = (/0.46, 0.66, 0.68/)
  ethics = (/0.41, 0.71, 0.78/)
  governance = (/0.30, 0.50, 0.47/)

  do i = 1, 3
     score(i) = 0.17 * definition(i) + 0.14 * boundary(i) + &
                0.14 * distinction(i) + 0.13 * operational(i) + &
                0.15 * measurement(i) + 0.10 * revision(i) + &
                0.07 * stakeholder(i) + 0.06 * ethics(i) + &
                0.04 * governance(i)
  end do

  print *, "Conceptual clarity scores"
  do i = 1, 3
     print *, trim(ids(i)), score(i)
  end do
end program weighted_concept_scoring
