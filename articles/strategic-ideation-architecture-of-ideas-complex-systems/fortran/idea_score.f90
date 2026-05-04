program idea_score
  implicit none

  real, dimension(7) :: values
  real, dimension(7) :: weights
  real :: score

  values = (/0.62, 0.86, 0.68, 0.88, 0.74, 0.35, 0.63/)
  weights = (/0.16, 0.20, 0.16, 0.20, 0.14, -0.08, 0.14/)

  score = sum(values * weights)

  print *, "Synthetic strategic idea score:", score

end program idea_score
