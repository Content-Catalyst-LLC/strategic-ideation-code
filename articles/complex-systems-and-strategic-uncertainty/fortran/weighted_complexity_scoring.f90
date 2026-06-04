! Weighted complexity profile scoring example.
! Compile: gfortran weighted_complexity_scoring.f90 -o weighted_complexity_scoring
! Run: ./weighted_complexity_scoring

program weighted_complexity_scoring
  implicit none

  real :: interdependence(3), nonlinearity(3), feedback(3), adaptation(3), path(3)
  real :: boundary(3), emergence(3), deep_uncertainty(3), scenario_need(3), learning_need(3), score(3)
  character(len=6) :: ids(3)
  integer :: i

  ids = (/"ENV001", "ENV003", "ENV004"/)
  interdependence = (/0.32, 0.81, 0.88/)
  nonlinearity = (/0.24, 0.74, 0.86/)
  feedback = (/0.31, 0.79, 0.87/)
  adaptation = (/0.28, 0.71, 0.82/)
  path = (/0.36, 0.78, 0.84/)
  boundary = (/0.30, 0.76, 0.82/)
  emergence = (/0.26, 0.74, 0.86/)
  deep_uncertainty = (/0.28, 0.82, 0.90/)
  scenario_need = (/0.30, 0.82, 0.90/)
  learning_need = (/0.34, 0.80, 0.88/)

  do i = 1, 3
     score(i) = 0.13 * interdependence(i) + 0.13 * nonlinearity(i) + &
                0.14 * feedback(i) + 0.12 * adaptation(i) + &
                0.11 * path(i) + 0.10 * boundary(i) + &
                0.10 * emergence(i) + 0.09 * deep_uncertainty(i) + &
                0.09 * scenario_need(i) + 0.09 * learning_need(i)
  end do

  print *, "Complexity profile scores"
  do i = 1, 3
     print *, trim(ids(i)), score(i)
  end do
end program weighted_complexity_scoring
