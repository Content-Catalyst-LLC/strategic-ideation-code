! Weighted creative constraint profile scoring example.
! Compile: gfortran weighted_constraint_scoring.f90 -o weighted_constraint_scoring
! Run: ./weighted_constraint_scoring

program weighted_constraint_scoring
  implicit none

  real :: resource(3), technical(3), institutional(3), ecological(3), ethics(3)
  real :: focus(3), opportunity(3), legitimacy(3), learning(3), readiness(3), score(3)
  character(len=5) :: ids(3)
  integer :: i

  ids = (/"CC001", "CC002", "CC007"/)
  resource = (/0.12, 0.54, 0.66/)
  technical = (/0.18, 0.47, 0.52/)
  institutional = (/0.16, 0.43, 0.57/)
  ecological = (/0.20, 0.52, 0.92/)
  ethics = (/0.38, 0.66, 0.88/)
  focus = (/0.24, 0.78, 0.74/)
  opportunity = (/0.38, 0.81, 0.70/)
  legitimacy = (/0.42, 0.72, 0.82/)
  learning = (/0.36, 0.78, 0.76/)
  readiness = (/0.34, 0.76, 0.60/)

  do i = 1, 3
     score(i) = -0.10 * resource(i) - 0.10 * technical(i) - &
                0.10 * institutional(i) + 0.12 * ecological(i) + &
                0.16 * ethics(i) + 0.16 * focus(i) + &
                0.16 * opportunity(i) + 0.14 * legitimacy(i) + &
                0.14 * learning(i) + 0.12 * readiness(i)
  end do

  print *, "Creative constraint profile scores"
  do i = 1, 3
     print *, trim(ids(i)), score(i)
  end do
end program weighted_constraint_scoring
